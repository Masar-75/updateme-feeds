# Routine Films (jalon M4)

Onglet `films`, kind `movie`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.films` de `criteres.json`)

`pourQui` (arthur, julie, à deux), `cinemas` (Astrée, Forum, Pathé Chambéry), `plateformes` (Netflix,
Canal+), `genresAEviter`, `dureeMaxMin`, `version` (VF, VOST, indifférent), et `notes` : les notes
d'Arthur et de Julie (sur 5, ou sur 10 si `echelle` vaut 10 ; voir transmission.md), par `personne`), qui forment leurs profils de goût.

## Quoi chercher

- **Au cinéma** : les films à l'affiche cette semaine dans les cinémas choisis (pages officielles des
  cinémas, ou TMDB pour les fiches).
- **Streaming** : les nouveautés et le catalogue des plateformes choisies (TMDB « watch providers » en France,
  ou pages des plateformes).

Ne chercher que pour les personnes de `pourQui`, que dans les `cinemas` et `plateformes` cochés.
Classer selon les notes : jamais un genre « à éviter », jamais plus long que `dureeMaxMin` ; pour une soirée à deux, règle « moyenne sans
misère » (le film doit convenir aux deux). Environ 1 proposition sur 5 est une découverte : elle partage
au moins un aspect aimé et le dit dans `whyYou`. Au plus 12 films.

Lire les notes : `source` `tmdb` → `id` est l'id TMDB (récupérer genres, réalisateur, acteurs sur TMDB pour
construire le profil) ; `source` `flux` → `id` est l'id d'une carte déjà publiée, se servir du `titre`.
Une note de 4 ou 5 = aimé, 1 ou 2 = rejeté, 3 = neutre. Ne jamais reproposer un film déjà noté par la
personne visée (même id TMDB ou même titre), ni une suite d'un film qu'elle a noté 1 ou 2.

## Remplir l'item

- `title` : le titre français ; `subtitle` : « Au cinéma (nom) » ou la plateforme.
- `tags` : genres, plus `Découverte`, `Arthur`, `Julie` ou `À deux` selon le profil visé.
- `detail` (kind `movie`) : `director`, `cast` (3 au plus), `durationMinutes`, `genres`, `rating` (note TMDB),
  `trailerUrl` si une bande-annonce officielle existe, `whereToWatch`, `whyYou` (une phrase, à partir des profils).
- `aiGenerated: true` (`whyYou` est écrit par Claude).
- Mention obligatoire si TMDB est utilisée : elle figure dans l'app, rien à ajouter ici.

## Pour qui (app 0.13)

`pourQui` vaut `arthur`, `julie` ou `à deux` : composer les propositions pour cette personne (ses notes), ou pour les deux avec la règle « moyenne sans misère » (écarter ce qu'un des deux déteste). Même règle pour `jeux-societe`.
