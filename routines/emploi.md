# Routine Emploi (jalon M4)

Onglet `emploi`, kind `job`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.emploi` de `criteres.json`)

`recherches` : liste de recherches simultanées, chacune avec `poste`, `lieu`, `rayonKm`,
`salaireMin`, `motsClesDescription`, et éventuellement `contrat`, `teletravail`, `exclure`.

## Quoi chercher

Pour chaque recherche, les offres publiées depuis la dernière publication. Sources : API ou site de
France Travail, puis recherche web (sites d'entreprises, Welcome to the Jungle, APEC, Indeed).
Une offre vue sur plusieurs sites : une seule carte, avec le lien de l'annonce d'origine.
Écarter une offre expirée, sans lieu ou sans entreprise identifiable.

Au plus 10 offres par recherche, triées par `score`.

## Remplir l'item

- `title` : l'intitulé du poste ; `subtitle` : « entreprise · lieu ».
- `summary` : une phrase factuelle sur le poste, tirée de l'annonce.
- `tags` : le `poste` de la recherche qui l'a trouvée, puis le contrat.
- `detail` (kind `job`) : `company`, `location` obligatoires ; `contract`, `remote`, `salary` seulement
  s'ils figurent dans l'annonce. `score` (0 à 100) = part des critères remplis ;
  `matchedCriteria` et `missingCriteria` les nomment (« salaire non indiqué » compte comme manquant).
- `aiGenerated: true` si le résumé est reformulé.
