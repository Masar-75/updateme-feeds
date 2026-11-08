# Routine Jeux de société (jalon M4)

Onglet `jeux-societe`, kind `boardgame`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.jeux-societe` de `criteres.json`)

`joueurs` (nombre habituel), `dureeMaxMin`, `complexite` (légère, moyenne, experte), `style` (coopératif,
compétitif, en équipes), `themesAEviter`, et `notes` d'Arthur (sur 5, ou sur 10 si `echelle` vaut 10) : les mécaniques et thèmes aimés
se déduisent des jeux bien notés.

## Sélection à partir des notes (`scripts/reco_jeux.py`)

Dès que `tabs.jeux-societe.notes` contient des notes, lancer d'abord, sur `criteres.json` déchiffré (le script écarte de lui-même les jeux BGG de la wish list) :

```
python3 scripts/reco_jeux.py --criteres plain/config/criteres.json --max 10 > /tmp/selection.json
python3 scripts/reco_jeux.py --criteres plain/config/criteres.json --nouveautes --max 10 > /tmp/nouveautes.json
```

Le script (bibliothèque standard, 3 à 6 minutes, l'API est lente) :
1. retrouve chaque jeu noté dans Recommend.Games (données BoardGameGeek, API publique sans jeton) :
   par `id` BGG si `source` vaut `bgg` ou `ref-jeu`, sinon par le titre (jeu le plus voté) ;
2. calcule un profil par personne : mécaniques, catégories et types pondérés par la note centrée
   (note − 3), et complexité moyenne des jeux aimés ;
3. demande à Recommend.Games les jeux « aussi aimés » par les fans des jeux aimés de chaque personne
   (filtrage collaboratif sur les notes BGG, calculé par Recommend.Games : on n'entraîne aucun modèle) ;
4. applique les critères en filtres durs (joueurs, durée, complexité, style, thèmes à éviter) ;
5. score = 0,6 × rang « aussi aimé » + 0,4 × accord avec le profil ; à deux, un jeu sous le seuil
   pour l'une des deux personnes est écarté (moyenne sans misère) ; diversité : une seule famille
   de jeu (par exemple un seul Azul) et des mécaniques variées ;
6. ajoute 1 découverte sur 5, ancrée sur une mécanique très aimée, sans trait rejeté.

Chaque jeu du résultat a `pourquoi` (explication par personne), `lien` BGG et les champs de l'item.
Publier environ 6 jeux de `nouveautes.json` (sorties récentes) et 4 de `selection.json` (classiques à
découvrir, tag `Sélection`), sans doublon avec les items déjà publiés. Écrire `pourquoi` en français
dans le `summary` après la phrase sur le principe (traduire les mécaniques : Open Drafting → draft ouvert,
Tile Placement → pose de tuiles, etc.). Sans notes, faire comme avant (section suivante).
Recommend.Games est un projet indépendant : si l'API ne répond pas, faire comme avant et le signaler.

## Quoi chercher (sans notes, ou en complément)

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
- `sourceUrl` : la fiche BGG (`https://boardgamegeek.com/boardgame/<id>`). Mentionner « Données : BoardGameGeek » (attribution).
