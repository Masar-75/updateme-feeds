# Routine Veille (jalon M2)

Onglet `veille`, kind `article`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.veille` de `criteres.json`)

`metier`, `technos` (liste), `niveau` (synthèse, détaillé, expert). L'app ne propose pas encore de sources
à privilégier ni à exclure : s'en tenir aux sources primaires.

## Quoi chercher

Les nouveautés parues depuis le passage précédent (`updatedAt` du flux ; 7 jours au plus) sur le métier et
chaque techno. La routine passe plusieurs fois par semaine (`tabs.veille.frequence.jours`) : un passage
sans vraie nouveauté publie peu, voire rien, plutôt que de répéter. Chercher :
versions publiées, annonces officielles, articles de fond, retours d'expérience. Priorité aux sources
primaires (blog officiel, notes de version, dépôt du projet). `niveau` règle la profondeur :
synthèse = l'essentiel en une phrase, expert = détails techniques et changements incompatibles.
Regrouper les doublons : une seule carte par nouveauté, avec la source la plus primaire.

Au plus 15 items par passage, souvent moins. Mieux vaut 3 items solides que 15 approximatifs.

## Remplir l'item

- `title` : la nouveauté en une ligne ; `subtitle` : la source (nom du site).
- `summary` : une phrase qui dit pourquoi c'est utile pour le métier d'Arthur.
- `tags` : la ou les technos concernées.
- `detail` : `{"kind": "article", "source": "<nom du site>", "keyPoints": ["…", "…", "…"]}`,
  trois points au plus, tirés de l'article lu.
- `aiGenerated: true` (le résumé et les points sont écrits par Claude).

## Terminé quand (M2)

Trois publications de suite sans intervention, aucun lien mort.
