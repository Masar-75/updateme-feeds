# Routine Revue thématique (jalon M4)

Onglet `revue`, kind `article`. Suis le socle commun de `routines/README.md`.

## Critères (`tabs.revue` de `criteres.json`)

`sujets` : liste ajoutée petit à petit depuis l'app. `mediasInclus` et `mediasExclus` valent pour tous
les sujets. Sans sujet, ne rien publier.

## Quoi chercher

Pour chaque sujet, ce qui s'est passé depuis la dernière publication, vu par **plusieurs médias**
(au moins deux, de lignes éditoriales différentes quand c'est possible). Une carte par fait marquant,
qui croise les sources ; signaler franchement un désaccord entre médias plutôt que de le lisser.
Au plus 5 cartes par sujet.

## Remplir l'item

- `title` : le fait en une ligne ; `subtitle` : le sujet.
- `summary` : la synthèse en une ou deux phrases.
- `sourceUrl` : l'article le plus complet ; les autres médias sont nommés dans `keyPoints`.
- `tags` : le sujet.
- `detail` : `{"kind": "article", "source": "<médias, séparés par des virgules>", "keyPoints": [...]}`
  (5 au plus, chacun attribué à son média : « Le Monde : … »).
- `aiGenerated: true`.
