# Routine Emploi (jalon M4)

Onglet `emploi`, kind `job`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.emploi` de `criteres.json`)

`recherches` : liste de recherches simultanées. Chacune a une `cle` et ses réponses à plat : `metier`
(le poste), `lieu`, `rayonKm`, `contrats` (liste), `teletravail` (aucun, partiel, total, indifférent),
`salaireMinK` (k€ par an), `motsCles` (à trouver dans la description de l'offre), `exclure` (mots-clés
ou entreprises). Toute réponse peut manquer : ne filtrer que sur ce qui est renseigné.

`contrats` peut contenir `Consultant` (app 0.11) : il désigne les offres publiées par un cabinet de conseil,
une ESN ou une société de portage, **quel que soit le contrat affiché** (un CDI chez un cabinet de conseil
compte comme `Consultant`). Si `contrats` est renseigné **sans** `Consultant`, écarter ces offres (entreprise
qui se présente comme cabinet de conseil, conseil en ingénierie, ESN, portage, ou annonce « pour l'un de nos
clients ») ; si `Consultant` y figure, les garder. En cas de doute, garder l'offre et le dire dans
`missingCriteria` (« cabinet de conseil à vérifier »).

## Quoi chercher

Pour chaque recherche, les offres publiées depuis la dernière publication. Sources : API ou site de
France Travail, puis recherche web (sites d'entreprises, Welcome to the Jungle, APEC, Indeed).
Une offre vue sur plusieurs sites : une seule carte, avec le lien de l'annonce d'origine.
Écarter une offre expirée, sans lieu ou sans entreprise identifiable.

Au plus 10 offres par recherche, triées par `score`.

## Remplir l'item

- `title` : l'intitulé du poste ; `subtitle` : « entreprise · lieu ».
- `summary` : une phrase factuelle sur le poste, tirée de l'annonce.
- `tags` : le `metier` de la recherche qui l'a trouvée, puis le contrat.
- `detail` (kind `job`) : `company`, `location` obligatoires ; `contract`, `remote`, `salary` seulement
  s'ils figurent dans l'annonce (`remote` `complet` correspond à `teletravail` `total`). `score` (0 à 100) = part des critères remplis ;
  `matchedCriteria` et `missingCriteria` les nomment (« salaire non indiqué » compte comme manquant).
- `aiGenerated: true` si le résumé est reformulé.
