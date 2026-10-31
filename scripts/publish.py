#!/usr/bin/env python3
"""Outils des routines UpdateMe : lire l'état publié, publier un flux.

  pull                 Déchiffre feeds/ et config/ dans plain/ (ignoré par git).
  push <feedId> [--check-links]
                       Publie plain/feeds/<feedId>.json : garde au plus MAX_ITEMS items,
                       met à jour l'index, valide tout plain/feeds (liens du seul flux publié
                       avec --check-links), puis chiffre le flux et l'index dans feeds/.
  config-push          Valide plain/config/criteres.json et le chiffre dans config/.

La clé est lue dans UPDATEME_KEY (voir crypto.py). Code de sortie 1 si rien n'est publié.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import crypto
import validate

ROOT = Path(__file__).resolve().parent.parent
PLAIN = ROOT / "plain"
MAX_ITEMS = 30


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def seal(key: bytes, src: Path, dst: Path):
    envelope = crypto.encrypt_bytes(key, src.name, src.read_bytes())
    dst.write_text(json.dumps(envelope) + "\n", encoding="utf-8")


def pull():
    for folder in ("feeds", "config"):
        if (ROOT / folder).is_dir() and any((ROOT / folder).glob("*.json")):
            crypto.transform(ROOT / folder, PLAIN / folder, encrypt=False)
    return 0


def push(feed_id: str, check_links: bool):
    key = crypto.load_key()
    feeds = PLAIN / "feeds"
    feed_path = feeds / f"{feed_id}.json"
    index = read_json(feeds / "index.json")
    entry = next((e for e in index["feeds"] if e["id"] == feed_id), None)
    if entry is None:
        print(f"ERREUR {feed_id} absent de l'index")
        return 1

    feed = read_json(feed_path)
    stamp = now_iso()
    feed["items"] = sorted(feed["items"], key=lambda i: i.get("publishedAt", ""), reverse=True)[:MAX_ITEMS]
    feed["updatedAt"] = stamp
    feed.pop("demo", None)
    write_json(feed_path, feed)
    entry["updatedAt"] = stamp
    index["generatedAt"] = stamp
    write_json(feeds / "index.json", index)

    errors = validate.validate(feeds, check_links=False)
    if check_links:
        errors += [f"{feed_id}.json : {i['id']} : lien mort {u}"
                   for i in feed["items"] for u in validate.item_links(i) if not validate.link_ok(u)]
    for e in errors:
        print(f"ERREUR {e}")
    if errors:
        print("Rien n'est publié.")
        return 1

    seal(key, feed_path, ROOT / "feeds" / feed_path.name)
    seal(key, feeds / "index.json", ROOT / "feeds" / "index.json")
    print(f"Publié : {feed_id} ({len(feed['items'])} items) et index.json")
    return 0


def config_push():
    key = crypto.load_key()
    path = PLAIN / "config" / "criteres.json"
    config = read_json(path)
    if config.get("schemaVersion") != 1 or not isinstance(config.get("tabs"), dict):
        print("ERREUR criteres.json : schemaVersion 1 et objet tabs attendus")
        return 1
    config["updatedAt"] = now_iso()
    write_json(path, config)
    (ROOT / "config").mkdir(exist_ok=True)
    seal(key, path, ROOT / "config" / path.name)
    print("Publié : config/criteres.json")
    return 0


def main(argv):
    if argv[:1] == ["pull"]:
        return pull()
    if argv[:1] == ["push"] and len(argv) >= 2:
        return push(argv[1], "--check-links" in argv)
    if argv[:1] == ["config-push"]:
        return config_push()
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
