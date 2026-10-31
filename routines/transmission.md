# Appliquer une transmission d'Arthur

Arthur colle dans le chat le prompt produit par l'app (Réglages > « Transmettre à Claude »). Il ne
contient que les ajouts et modifications depuis le dernier envoi : critères par onglet, notes, réponses
aux questionnaires, fréquences.

1. `python3 scripts/publish.py pull`.
2. Partir de `plain/config/criteres.json` (s'il n'existe pas : `{"schemaVersion": 1, "tabs": {}}`).
3. Appliquer chaque changement à `tabs.<id-onglet>` : un ajout s'ajoute, une modification remplace,
   une suppression retire. Ne rien déduire au-delà de ce que dit le prompt.
4. Recopier les fréquences dans `tabs.<id>.frequence`, puis mettre à jour la planification de la routine
   de l'onglet si elle a changé.
5. `python3 scripts/publish.py config-push`, puis `git add config && git commit -m "Critères : …" && git push`.
6. Répondre à Arthur en une ou deux phrases : ce qui a changé, et les routines dont la planification a bougé.

Les notes et réponses sont des données personnelles : elles ne vont que dans `config/` chiffré,
jamais dans un message de commit, un flux publié ou un fichier en clair committé.
