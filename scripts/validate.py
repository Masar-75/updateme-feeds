#!/usr/bin/env python3
"""Valide les flux UpdateMe avant publication.

Vérifie : le schéma JSON de l'index et de chaque flux, que chaque flux de l'index
existe, que les identifiants d'items sont uniques, et (option --check-links)
que chaque lien répond. Code de sortie 0 si tout est valide, 1 sinon.

Le dossier validé contient les flux EN CLAIR (samples/ pour la démo, ou le dossier
de travail d'une routine avant chiffrement).

Usage : python3 scripts/validate.py [--check-links] [dossier_des_flux]
"""
import json
import sys
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

LINK_TIMEOUT_S = 10


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def schema_errors(validator, data, label):
    return [f"{label} : {'/'.join(map(str, e.absolute_path)) or '(racine)'} : {e.message}"
            for e in validator.iter_errors(data)]


def link_ok(url: str) -> bool:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "UpdateMe-validator"})
        try:
            with urllib.request.urlopen(req, timeout=LINK_TIMEOUT_S) as resp:
                if resp.status < 400:
                    return True
        except Exception:
            continue
    return False


def item_links(item):
    yield item["sourceUrl"]
    if "imageUrl" in item:
        yield item["imageUrl"]
    detail = item["detail"]
    for key in ("spotifyUrl", "trailerUrl"):
        if key in detail:
            yield detail[key]


def validate(feeds_dir: Path, check_links: bool) -> list[str]:
    root = Path(__file__).resolve().parent.parent
    fmt = FormatChecker()
    index_v = Draft202012Validator(load(root / "schema/index.schema.json"), format_checker=fmt)
    feed_v = Draft202012Validator(load(root / "schema/feed.schema.json"), format_checker=fmt)
    errors = []

    index = load(feeds_dir / "index.json")
    errors += schema_errors(index_v, index, "index.json")
    seen_ids = set()
    for entry in index.get("feeds", []):
        path = feeds_dir / entry["url"]
        if not path.exists():
            errors.append(f"index.json : le flux {entry['url']} n'existe pas")
            continue
        feed = load(path)
        errs = schema_errors(feed_v, feed, entry["url"])
        errors += errs
        if errs:
            continue
        if feed["feedId"] != entry["id"]:
            errors.append(f"{entry['url']} : feedId {feed['feedId']} différent de l'index ({entry['id']})")
        for item in feed["items"]:
            if item["id"] in seen_ids:
                errors.append(f"{entry['url']} : id en double {item['id']}")
            seen_ids.add(item["id"])
            if item["detail"]["kind"] != entry["kind"]:
                errors.append(f"{entry['url']} : {item['id']} est de type {item['detail']['kind']}, attendu {entry['kind']}")
            if check_links and not feed.get("demo", False):
                errors += [f"{entry['url']} : {item['id']} : lien mort {u}" for u in item_links(item) if not link_ok(u)]
    return errors


def main(argv):
    check_links = "--check-links" in argv
    args = [a for a in argv if not a.startswith("--")]
    feeds_dir = Path(args[0]) if args else Path(__file__).resolve().parent.parent / "samples"
    errors = validate(feeds_dir, check_links)
    for e in errors:
        print(f"ERREUR {e}")
    print("Flux valides." if not errors else f"{len(errors)} erreur(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
