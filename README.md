# updateme-feeds

Contenu de l'application Android **UpdateMe**, mis à jour par des routines Claude planifiées et publié par GitHub Pages.
**Tout ce qui est publié est chiffré** (AES-256-GCM) : sans la clé, les fichiers sont illisibles.

## Organisation

| Dossier | Contenu |
| --- | --- |
| `feeds/` | Fichiers publiés et chiffrés : `index.json` et un fichier par thème. C'est ce que lit l'app. |
| `config/` | Critères et goûts d'Arthur, chiffrés eux aussi (`criteres.json`, écrit à partir des transmissions de l'app). |
| `routines/` | Prompts des routines Claude, un par onglet, et le socle commun. |
| `samples/` | Flux de démonstration **en clair**, fictifs, pour les tests. Onglets : emploi, films, jeux-societe, jeux-video, veille, revue. |
| `samples/en-attente/` | Musique et recettes, mises de côté : hors index et jamais publiées (le chiffrement ne lit que `samples/*.json`). |
| `schema/` | Schémas JSON du format en clair (version 1). |
| `scripts/validate.py` | Valide des flux en clair avant chiffrement. |
| `scripts/crypto.py` | Génère la clé, chiffre et déchiffre. |
| `scripts/publish.py` | Outils des routines : `pull` (déchiffre dans `plain/`), `push <onglet>`, `config-push`. |
| `scripts/selftest.py` | Test de bout en bout de `publish.py` avec une clé de test (lancé par la CI). |

## Chiffrement

- La clé fait 32 octets, en base64. Elle est lue dans la variable d'environnement `UPDATEME_KEY` et n'est **jamais** écrite dans ce dépôt.
- Elle vit à deux endroits seulement : le secret de l'environnement cloud des routines, et le coffre-fort de clés Android du téléphone.
- Chaque fichier publié est une enveloppe `{"updateme":"enc","v":1,"alg":"A256GCM","iv":…,"ct":…}`. Le nom du fichier est authentifié : deux fichiers échangés ne se déchiffrent pas.
- Reste visible publiquement : l'existence du dépôt, les dates de commit, le nombre et la taille des fichiers.

## Travail d'une routine

Le détail est dans `routines/README.md`. En bref :

```bash
python3 scripts/publish.py pull                      # flux publiés et critères, en clair dans plain/
# … écrire plain/feeds/<onglet>.json …
python3 scripts/publish.py push <onglet> --check-links  # valide, chiffre ; rien n'est publié en cas d'erreur
git add feeds && git commit -m "…" && git push
```

## Règles du format (en clair)

- Chaque item a un `id` stable (minuscules et tirets) : l'app s'en sert pour savoir ce qui est nouveau ou déjà lu.
- `detail.kind` choisit la fiche affichée (`job`, `movie`, `music`, `boardgame`, `videogame`, `recipe`, `article`). Un type inconnu s'affiche comme un `article`.
- `sourceUrl` est obligatoire. Un texte écrit par Claude porte `"aiGenerated": true`.

## Publication

Settings > Pages > Source : « Deploy from a branch », `main`, `/ (root)`.
Les flux sont servis à `https://masar-75.github.io/updateme-feeds/feeds/`.
