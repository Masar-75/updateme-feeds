#!/usr/bin/env python3
"""Chiffre et déchiffre les flux UpdateMe (AES-256-GCM).

Chaque fichier publié est une enveloppe JSON :
  {"updateme": "enc", "v": 1, "alg": "A256GCM", "iv": <base64, 12 octets>, "ct": <base64, chiffré + tag de 16 octets>}
Le nom du fichier (ex. "musique.json") sert de données authentifiées : on ne peut pas
échanger deux fichiers sans que le déchiffrement échoue.

La clé (32 octets en base64) est lue dans la variable d'environnement UPDATEME_KEY.
Elle n'est jamais écrite dans le dépôt.

Usage :
  python3 scripts/crypto.py genkey
  python3 scripts/crypto.py encrypt <dossier_en_clair> <dossier_publié>
  python3 scripts/crypto.py decrypt <dossier_publié> <dossier_en_clair>
"""
import base64
import json
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ENVELOPE_VERSION = 1


def load_key() -> bytes:
    raw = os.environ.get("UPDATEME_KEY")
    if not raw:
        sys.exit("UPDATEME_KEY absente de l'environnement")
    key = base64.b64decode(raw)
    if len(key) != 32:
        sys.exit("UPDATEME_KEY doit faire 32 octets (base64)")
    return key


def encrypt_bytes(key: bytes, name: str, plain: bytes) -> dict:
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, plain, name.encode("utf-8"))
    return {"updateme": "enc", "v": ENVELOPE_VERSION, "alg": "A256GCM",
            "iv": base64.b64encode(iv).decode(), "ct": base64.b64encode(ct).decode()}


def decrypt_envelope(key: bytes, name: str, envelope: dict) -> bytes:
    if envelope.get("updateme") != "enc" or envelope.get("v") != ENVELOPE_VERSION or envelope.get("alg") != "A256GCM":
        raise ValueError(f"{name} : enveloppe inconnue")
    return AESGCM(key).decrypt(base64.b64decode(envelope["iv"]), base64.b64decode(envelope["ct"]), name.encode("utf-8"))


def transform(src: Path, dst: Path, encrypt: bool):
    key = load_key()
    dst.mkdir(parents=True, exist_ok=True)
    for path in sorted(src.glob("*.json")):
        if encrypt:
            out = json.dumps(encrypt_bytes(key, path.name, path.read_bytes())) + "\n"
            (dst / path.name).write_text(out, encoding="utf-8")
        else:
            (dst / path.name).write_bytes(decrypt_envelope(key, path.name, json.loads(path.read_text(encoding="utf-8"))))
        print(f"{'chiffré' if encrypt else 'déchiffré'} : {path.name}")


def main(argv):
    if argv[:1] == ["genkey"]:
        print(base64.b64encode(AESGCM.generate_key(bit_length=256)).decode())
    elif len(argv) == 3 and argv[0] in ("encrypt", "decrypt"):
        transform(Path(argv[1]), Path(argv[2]), argv[0] == "encrypt")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
