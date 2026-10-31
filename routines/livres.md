# Routine Livres (générique, une par rubrique Livres)

Kind `book`. Suis le socle commun de `routines/README.md`.

Il peut y avoir plusieurs rubriques Livres, créées dans l'app à partir d'un modèle : `livres` (tous les
livres) et `livres-<nom>` (par exemple `livres-bd` pour les BD récentes). Cette routine sert à chacune :
la planification passe l'id de la rubrique, et tout le reste vient de `tabs.<id>` de `criteres.json`.

## Critères (`tabs.<id>` de `criteres.json`)

Clés de l'app (référence : `transmission.md`) : `nom`, `formats` (roman, bd, manga, comics, essai, autre),
`genresPreferes`, `auteursAimes` (auteurs et dessinateurs), `genresAEviter`, `langues` (français, anglais,
autre), `parutionMaxMois`. Les `notes` d'Arthur et de Julie (domaine `livre`) sont dans `tabs.livres.notes`,
communes à toutes les rubriques Livres. Ne garder que les formats de `formats` et, si `parutionMaxMois` est
renseigné, que les parutions plus récentes.

## Quoi chercher

Les parutions des deux dernières semaines et celles du mois à venir, en français, dans les formats
choisis : sites des éditeurs, programmes de parution, presse et sites spécialisés (pour la BD : listes de
sorties des éditeurs et sites de BD). Les fiches (auteurs, ISBN, pages) peuvent venir d'Open Library ou
de la page de l'éditeur. Une suite de série déjà bien notée passe en priorité.

Classer selon les notes : jamais un genre « à éviter ». Environ 1 proposition sur 5 est une découverte,
ancrée sur un aspect aimé (un auteur, un genre, un dessinateur) et le dit dans `whyYou`. Au plus 12 livres.

## Remplir l'item

- `title` : le titre ; `subtitle` : « auteur · éditeur », plus le tome pour une série.
- `summary` : une phrase sur le livre, tirée de la présentation de l'éditeur.
- `tags` : le format (`BD`, `Roman`…), les genres, plus `Découverte` le cas échéant.
- `detail` (kind `book`) : `format` ; `authors`, `illustrators` (BD), `publisher`, `series`, `volume`,
  `pages`, `genres`, `releaseDate` (AAAA-MM-JJ, seulement si elle est annoncée), `isbn` s'il est publié,
  `rating` (sur 10, seulement si une note publique existe), `whyYou` (une phrase, à partir des notes).
- `aiGenerated: true` (`whyYou` et le résumé sont écrits par Claude).
