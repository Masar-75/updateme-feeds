# Routines UpdateMe

Chaque fichier de ce dossier est le prompt d'une routine Claude planifiée. Toutes suivent le
même socle (ci-dessous) ; le fichier de l'onglet dit seulement quoi chercher et comment remplir `detail`.

| Routine | Onglet | Fréquence par défaut (6 h, heure de Paris) | Jalon |
| --- | --- | --- | --- |
| `veille.md` | Veille | lundi | M2 |
| `emploi.md` | Emploi | lundi et jeudi | M4 |
| `films.md` | Films | mercredi | M4 |
| `jeux-societe.md` | Jeux de société | 1er et 15 du mois | M4 |
| `jeux-video.md` | Jeux vidéo | 1er et 15 du mois | M4 |
| `revue.md` | Revue thématique | lundi | M4 |
| `transmission.md` | (aucun) : applique un prompt « Transmettre à Claude » collé par Arthur | à la demande | M2 |

Les fréquences réelles sont celles de `config/criteres.json` (`tabs.<id>.frequence`), réglées depuis l'app.
Les clés des critères sont celles de l'app : la liste fait référence dans `transmission.md`.

## Prérequis de l'environnement

- Secret `UPDATEME_KEY` : la clé d'Arthur (32 octets en base64). Jamais dans un prompt, un commit ou un message.
- Accès en écriture au dépôt `Masar-75/updateme-feeds`.
- `pip install jsonschema cryptography` dans le script d'installation.
- Réseau : les sources de l'onglet, plus un accès large en lecture pour vérifier les liens (`--check-links`).

## Socle commun à toutes les routines

1. `python3 scripts/publish.py pull` : déchiffre les flux publiés et `config/criteres.json` dans `plain/`.
2. Lire `plain/config/criteres.json`, section `tabs.<id>` de l'onglet. Si elle est absente ou vide,
   **ne rien publier** et terminer en disant quel critère manque.
3. Lire `plain/feeds/<id>.json` : les items déjà publiés. Ne jamais republier un item déjà présent
   (même `id`, ou même `sourceUrl`). Garder les items encore pertinents.
4. Chercher les nouveautés (recherche web et sources de l'onglet). Chaque item :
   - porte un `sourceUrl` réel, ouvert et lu pendant la routine ; aucun lien deviné ou reconstruit ;
   - a un `id` stable : `<id-onglet>-<AAAA-MM-JJ>-<slug court>` ;
   - porte `"aiGenerated": true` dès que le résumé ou le texte est écrit par Claude ;
   - n'invente rien : un champ inconnu est omis, pas estimé.
5. Écrire `plain/feeds/<id>.json` (format : `schema/feed.schema.json`, exemples : `samples/`).
6. `python3 scripts/publish.py push <id> --check-links`. Un flux invalide ou un lien mort bloque la
   publication : retirer l'item fautif et relancer, sans forcer.
7. `git add feeds && git commit -m "<Onglet> : N nouveautés" && git push`.
8. Terminer par un compte rendu court : nombre d'items ajoutés, retirés, et ce qui a été écarté.

Si une étape échoue (clé absente, source indisponible), ne rien publier et le dire.
