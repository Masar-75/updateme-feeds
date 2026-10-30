# updateme-feeds

Contenu de l'application Android **UpdateMe** : un fichier JSON par thème, mis à jour par des routines Claude planifiées et publié par GitHub Pages.

## Organisation

| Dossier | Contenu |
| --- | --- |
| `feeds/` | `index.json` (liste des thèmes) et un fichier par thème. C'est ce que lit l'app. |
| `schema/` | Schémas JSON du format (version 1). |
| `config/preferences.json` | Critères et goûts lus par les routines. Dépôt public : rien de personnel ou sensible ici. |
| `scripts/validate.py` | Validation lancée par chaque routine avant son commit, et par GitHub Actions à chaque push. |

## Règles du format

- Chaque item a un `id` stable (minuscules et tirets) : l'app s'en sert pour savoir ce qui est nouveau ou déjà lu.
- `detail.kind` choisit la fiche affichée dans l'app (`job`, `movie`, `music`, `boardgame`, `recipe`, `article`). Un type inconnu de l'app s'affiche comme un `article`.
- `sourceUrl` est obligatoire : chaque information renvoie à sa source. Une recette ou un texte écrit par Claude porte `"aiGenerated": true`.
- Les flux marqués `"demo": true` sont des exemples ; la validation ne teste pas leurs liens.

## Valider en local

```bash
pip install jsonschema
python scripts/validate.py --check-links .
```

## Publication

Settings > Pages > Source : branche `main`, dossier `/ (root)`. Les flux sont alors servis à
`https://masar-75.github.io/updateme-feeds/feeds/index.json`.
