# Routine Films (jalon M4)

Onglet `films`, kind `movie`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.films` de `criteres.json`)

`profils` (Arthur, Julie : genres aimés, à éviter, notes), `cinemas` (Astrée, Forum, Pathé à Chambéry),
`plateformes` (Netflix, Canal+), `duree`, `toggles` actifs.

## Quoi chercher

- **Au cinéma** : les films à l'affiche cette semaine dans les cinémas choisis (pages officielles des
  cinémas, ou TMDB pour les fiches).
- **Streaming** : les nouveautés et le catalogue des plateformes choisies (TMDB « watch providers » en France,
  ou pages des plateformes).

Classer selon les profils : jamais un genre « à éviter » ; pour une soirée à deux, règle « moyenne sans
misère » (le film doit convenir aux deux). Environ 1 proposition sur 5 est une découverte : elle partage
au moins un aspect aimé et le dit dans `whyYou`. Au plus 12 films.

## Remplir l'item

- `title` : le titre français ; `subtitle` : « Au cinéma (nom) » ou la plateforme.
- `tags` : genres, plus `Découverte`, `Arthur`, `Julie` ou `À deux` selon le profil visé.
- `detail` (kind `movie`) : `director`, `cast` (3 au plus), `durationMinutes`, `genres`, `rating` (note TMDB),
  `trailerUrl` si une bande-annonce officielle existe, `whereToWatch`, `whyYou` (une phrase, à partir des profils).
- `aiGenerated: true` (`whyYou` est écrit par Claude).
- Mention obligatoire si TMDB est utilisée : elle figure dans l'app, rien à ajouter ici.
