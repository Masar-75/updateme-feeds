# Appliquer une transmission d'Arthur

Arthur colle dans le chat le prompt produit par l'app (Réglages › « Transmettre à Claude »). Le prompt
ne contient que ce qui a changé depuis le dernier envoi, calculé par l'app comme la différence entre
l'état transmis et l'état courant (`PrefsDiff` dans le code de l'app). Une modification annulée avant
l'envoi n'y figure donc pas.

## Format du prompt

Une consigne en français, puis un bloc JSON :

```
{"updatemeReglages": 1, "date": "AAAA-MM-JJ", "changements": [{"op": …, "chemin": …, "valeur": …}, …]}
```

- `op` vaut `ajout`, `modification` ou `suppression`. Une `suppression` d'objet n'a pas de `valeur`.
- `chemin` désigne l'élément dans l'état de l'app :

| Chemin | Contenu |
| --- | --- |
| `criteres.<onglet>` | Toutes les réponses d'un onglet (objet), au premier critère ou quand l'onglet est vidé |
| `criteres.<onglet>.<question>` | Une réponse : texte, nombre, ou liste de textes |
| `recherchesEmploi[<cle>]` | Une recherche d'emploi : `{"cle", "reponses": {…}}` |
| `notes[<cle>]` | Une note : `{"cle", "domaine", "personne", "source", "id", "titre", "annee", "note", "lien"}` |
| `frequences.<onglet>` | Le rythme d'un onglet : `{"rythme", "jours", "joursDuMois", "heure"}` |
| `frequences.<onglet>.<champ>` | Un champ de ce rythme |

- Sur une **liste de textes** (par exemple `criteres.veille.technos`), chaque élément ajouté ou retiré est
  un changement séparé : `ajout` ou `suppression`, avec l'élément dans `valeur`.
- Le premier envoi contient les fréquences par défaut et les préférences connues des jeux vidéo
  (`plateformes` : PC, `genresPreferes` : infiltration).

## Onglets et questions (clés réelles de l'app)

Les ids d'onglet sont ceux de l'index : `emploi`, `films`, `jeux-societe`, `jeux-video`, `veille`, `revue`.
Les valeurs de choix sont enregistrées telles quelles.

| Onglet | Questions (`criteres.<onglet>.…`, ou `reponses` d'une recherche pour l'emploi) |
| --- | --- |
| `emploi` | Par recherche : `metier` (le poste), `lieu`, `rayonKm`, `contrats` (CDI, CDD, Freelance, Alternance, Intérim), `teletravail` (aucun, partiel, total, indifférent), `salaireMinK` (k€ par an), `motsCles` (mots-clés à trouver dans la description de l'offre), `exclure` (mots-clés ou entreprises) |
| `films` | `pourQui` (arthur, julie, à deux), `cinemas` (Astrée, Forum, Pathé Chambéry), `plateformes` (Netflix, Canal+), `genresAEviter`, `dureeMaxMin`, `version` (VF, VOST, indifférent) |
| `jeux-societe` | `joueurs`, `dureeMaxMin`, `complexite` (légère, moyenne, experte), `style` (coopératif, compétitif, en équipes), `themesAEviter` |
| `jeux-video` | `plateformes` (PC, PlayStation, Xbox, Switch, mobile), `genresPreferes`, `heuresParSemaine`, `mode` (solo, multijoueur, coopération), `genresAEviter` |
| `veille` | `metier`, `technos`, `niveau` (synthèse, détaillé, expert) |
| `revue` | `sujets` (ajoutés petit à petit), `mediasInclus`, `mediasExclus` |

Notes : `domaine` vaut film, jeu-societe, jeu-video ou musique ; `personne` vaut arthur ou julie ;
`note` va de 1 (détesté) à 5 (adoré) ; `source` vaut `tmdb` (film trouvé par la recherche de l'app,
`id` = id TMDB) ou `flux` (note donnée depuis une carte, `id` = id de l'item du flux).

## Où ranger chaque changement dans `config/criteres.json`

`criteres.json` = `{"schemaVersion": 1, "tabs": {"<onglet>": {…}}}`. Pour chaque onglet, `tabs.<onglet>`
contient les réponses aux questions (mêmes clés que ci-dessus), plus trois clés réservées :
`recherches` (emploi), `notes` et `frequence`.

| Changement | Effet dans `tabs` |
| --- | --- |
| `criteres.<onglet>` (objet) | `ajout` ou `modification` : écrire chaque réponse dans `tabs.<onglet>` ; `suppression` : retirer toutes les réponses aux questions, en gardant `recherches`, `notes` et `frequence` |
| `criteres.<onglet>.<question>` | Texte ou nombre : écrire ou retirer `tabs.<onglet>.<question>`. Liste de textes : ajouter ou retirer l'élément `valeur` |
| `recherchesEmploi[<cle>]` | Dans `tabs.emploi.recherches`, ajouter, remplacer ou retirer l'élément de même `cle`, sous la forme `{"cle", …reponses}` (réponses à plat) |
| `notes[<cle>]` | Dans `tabs.<onglet du domaine>.notes` (film → `films`, jeu-societe → `jeux-societe`, jeu-video → `jeux-video`, musique → `musique`), ajouter, remplacer ou retirer l'élément de même `cle` |
| `frequences.<onglet>` et ses champs | Écrire dans `tabs.<onglet>.frequence` ; si le rythme change, mettre à jour la planification de la routine de l'onglet |

Correspondance avec le format des flux : `teletravail` `total` correspond à `remote` `complet` dans une
offre ; `salaireMinK` est en milliers d'euros par an.

## Étapes

1. `python3 scripts/publish.py pull`.
2. Partir de `plain/config/criteres.json` (s'il n'existe pas : `{"schemaVersion": 1, "tabs": {}}`).
3. Appliquer chaque changement dans l'ordre du prompt, selon le tableau ci-dessus. Ne rien déduire
   au-delà de ce que dit le prompt.
4. Si une fréquence a changé, mettre à jour la planification de la routine concernée.
5. `python3 scripts/publish.py config-push`, puis `git add config && git commit -m "Critères : mise à jour" && git push`.
6. Répondre à Arthur en une ou deux phrases : ce qui a changé, et les routines dont la planification a bougé.

Les notes et réponses sont des données personnelles : elles ne vont que dans `config/` chiffré,
jamais dans un message de commit, un flux publié ou un fichier en clair committé.

## Exemple

Prompt tel que l'app le génère, avec des valeurs **fictives** :

````
Mise à jour des réglages UpdateMe du 2026-11-02.
Intègre ces changements dans les bases de goûts et de critères chiffrées de updateme-feeds (config/), puis ajuste les routines concernées (critères de recherche et fréquences). Seuls les éléments listés ont changé depuis le dernier envoi ; le reste est inchangé. Les notes vont de 1 (détesté) à 5 (adoré).

```json
{
    "updatemeReglages": 1,
    "date": "2026-11-02",
    "changements": [
        {
            "op": "ajout",
            "chemin": "criteres.veille",
            "valeur": {
                "metier": "Métier exemple",
                "technos": [
                    "Techno A",
                    "Techno B"
                ],
                "niveau": "détaillé"
            }
        },
        {
            "op": "ajout",
            "chemin": "criteres.revue.sujets",
            "valeur": "Sujet exemple"
        },
        {
            "op": "suppression",
            "chemin": "criteres.jeux-video.genresAEviter",
            "valeur": "Genre exemple"
        },
        {
            "op": "ajout",
            "chemin": "recherchesEmploi[recherche-1767339000000]",
            "valeur": {
                "cle": "recherche-1767339000000",
                "reponses": {
                    "metier": "Poste exemple",
                    "lieu": "Ville exemple",
                    "rayonKm": 30,
                    "contrats": [
                        "CDI"
                    ],
                    "salaireMinK": 40,
                    "motsCles": [
                        "mot-clé A"
                    ]
                }
            }
        },
        {
            "op": "ajout",
            "chemin": "notes[film:julie:tmdb:12345]",
            "valeur": {
                "cle": "film:julie:tmdb:12345",
                "domaine": "film",
                "personne": "julie",
                "source": "tmdb",
                "id": "12345",
                "titre": "Film exemple",
                "annee": 2001,
                "note": 4,
                "lien": "https://www.themoviedb.org/movie/12345"
            }
        },
        {
            "op": "suppression",
            "chemin": "notes[film:arthur:flux:films-demo-1]"
        },
        {
            "op": "modification",
            "chemin": "frequences.veille.heure",
            "valeur": 7
        }
    ]
}
```
````

Effet dans `criteres.json` :
- `tabs.veille` reçoit `metier`, `technos` et `niveau` ; `tabs.revue.sujets` gagne « Sujet exemple » ;
- « Genre exemple » quitte `tabs.jeux-video.genresAEviter` ;
- `tabs.emploi.recherches` gagne `{"cle": "recherche-1767339000000", "metier": "Poste exemple", …}` ;
- `tabs.films.notes` gagne la note de Julie et perd celle d'Arthur sur `films-demo-1` ;
- `tabs.veille.frequence.heure` passe à 7 : replanifier la routine Veille à 7 h.
