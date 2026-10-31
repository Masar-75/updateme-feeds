#!/usr/bin/env python3
"""Vérifie publish.py de bout en bout dans un dossier temporaire, avec une clé de test publique.

Usage : python3 scripts/selftest.py   (code de sortie 0 si tout passe)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEST_KEY = "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="


def run(work: Path, *args) -> int:
    env = {**os.environ, "UPDATEME_KEY": TEST_KEY}
    return subprocess.run([sys.executable, "scripts/" + args[0], *args[1:]], cwd=work, env=env,
                          capture_output=True, text=True).returncode


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for folder in ("scripts", "schema", "samples"):
            shutil.copytree(ROOT / folder, work / folder)
        checks = []
        checks.append(("chiffrement des samples", run(work, "crypto.py", "encrypt", "samples", "feeds") == 0))
        checks.append(("pull", run(work, "publish.py", "pull") == 0))

        veille = work / "plain/feeds/veille.json"
        feed = json.loads(veille.read_text(encoding="utf-8"))
        feed["items"].append({**feed["items"][0], "id": "veille-2026-10-31-test", "publishedAt": "2026-10-31"})
        veille.write_text(json.dumps(feed), encoding="utf-8")
        checks.append(("push d'un flux valide", run(work, "publish.py", "push", "veille") == 0))
        run(work, "crypto.py", "decrypt", "feeds", "out")
        published = json.loads((work / "out/veille.json").read_text(encoding="utf-8"))
        checks.append(("flux publié à jour, sans marque demo", len(published["items"]) == 2 and "demo" not in published))

        before = (work / "feeds/veille.json").read_bytes()
        del feed["items"][0]["sourceUrl"]
        veille.write_text(json.dumps(feed), encoding="utf-8")
        checks.append(("push refusé si invalide", run(work, "publish.py", "push", "veille") == 1))
        checks.append(("rien publié après un refus", (work / "feeds/veille.json").read_bytes() == before))
        checks.append(("onglet inconnu refusé", run(work, "publish.py", "push", "inconnu") == 1))

        (work / "plain/config").mkdir(parents=True, exist_ok=True)
        (work / "plain/config/criteres.json").write_text('{"schemaVersion": 1, "tabs": {}}', encoding="utf-8")
        checks.append(("config-push", run(work, "publish.py", "config-push") == 0 and (work / "config/criteres.json").exists()))

    for name, ok in checks:
        print(("OK     " if ok else "ÉCHEC  ") + name)
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
