# Routine Jeux de société (jalon M4)

Onglet `jeux-societe`, kind `boardgame`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.jeux-societe` de `criteres.json`)

`joueurs` (nombre habituel), `dureeMaxMin`, `complexite` (légère, moyenne, experte), `style` (coopératif,
compétitif, en équipes), `themesAEviter`, et `notes` d'Arthur (1 à 5) : les mécaniques et thèmes aimés
se déduisent des jeux bien notés.

## Quoi chercher

Les sorties et nouveautés en français des deux dernières semaines : sites d'éditeurs, presse ludique
française, BoardGameGeek pour les fiches (l'API demande un jeton : sans lui, lire les pages publiques).
Écarter un jeu hors du nombre de joueurs ou de la durée. Environ 1 sur 5 est une découverte, ancrée sur
une mécanique ou un thème aimé. Au plus 10 jeux.

## Remplir l'item

- `title` : le nom du jeu ; `subtitle` : l'éditeur et la date de sortie en France si elle est connue.
- `summary` : une phrase sur le principe du jeu.
- `tags` : mécaniques et thèmes (6 au plus), plus `Découverte` le cas échéant.
- `detail` (kind `boardgame`) : `minPlayers`, `maxPlayers`, `durationMinutes`, `minAge`, `designers`, `publisher`.
- `aiGenerated: true` si le résumé est écrit par Claude.
