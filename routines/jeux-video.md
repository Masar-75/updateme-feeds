# Routine Jeux vidéo (jalon M4)

Onglet `jeux-video`, kind `videogame`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.jeux-video` de `criteres.json`)

`plateformes` (par défaut : PC seulement), `genresPreferes` (par défaut : infiltration), `heuresParSemaine`,
`mode` (solo, multijoueur, coopération), `genresAEviter`, et `notes` d'Arthur (1 à 5).

## Quoi chercher

Les sorties des deux dernières semaines et celles annoncées pour le mois à venir, sur les plateformes
choisies : pages Steam, sites des studios, presse spécialisée. RAWG ou IGDB pourront servir de base
de fiches quand leurs conditions auront été vérifiées ; d'ici là, ne s'appuyer que sur des pages publiques.
Environ 1 sur 5 est une découverte, ancrée sur un genre ou une mécanique aimés
(par exemple un jeu d'infiltration dans un autre décor). Au plus 10 jeux.

## Remplir l'item

- `title` : le nom du jeu ; `subtitle` : « studio · plateformes ».
- `summary` : une phrase sur le jeu.
- `tags` : genres, plus `Découverte` le cas échéant.
- `detail` (kind `videogame`) : `platforms`, `genres`, `releaseDate` (AAAA-MM-JJ, seulement si elle est
  annoncée), `studio`, `rating` (sur 10, seulement si une note publique existe : dire laquelle dans `summary`).
- `aiGenerated: true` si le résumé est écrit par Claude.
