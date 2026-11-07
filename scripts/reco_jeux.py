#!/usr/bin/env python3
"""Sélection de jeux de société à partir des notes d'Arthur et de Julie.

Méthode (routines/jeux-societe.md) :
  1. Les jeux notés sont retrouvés dans Recommend.Games (données BoardGameGeek, API publique sans jeton).
  2. Profil de goût par personne : mécaniques, catégories et types de jeu pondérés par les notes centrées
     (note - 3), plus la complexité moyenne des jeux aimés.
  3. Jeux voisins (« aussi aimés ») : recommandations de Recommend.Games à partir des jeux aimés
     (filtrage collaboratif calculé par Recommend.Games sur les notes BGG ; nous n'entraînons aucun modèle).
  4. Filtres durs des critères de l'onglet : joueurs, durée, complexité, thèmes à éviter.
  5. Score = 0,6 x rang collaboratif + 0,4 x accord avec le profil ; à deux, « moyenne sans misère ».
  6. Environ 1 sur 5 est une Découverte : partage une mécanique très aimée, mais loin du profil pour le reste.

Usage :
  python3 scripts/reco_jeux.py --criteres plain/config/criteres.json [--nouveautes] [--max 10] > candidats.json
  python3 scripts/reco_jeux.py --demo   # notes fictives, pour vérifier la méthode

Bibliothèque standard seulement. Sortie : JSON avec, pour chaque jeu, les champs utiles à l'item
`boardgame` et une explication en français.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

API = "https://recommend.games/api"
UA = "UpdateMe-routine/1.0 (usage personnel non commercial)"
COMPLEXITE = {"légère": (1.0, 2.2), "moyenne": (2.0, 3.3), "experte": (3.0, 5.0)}
POIDS_COLLAB, POIDS_PROFIL = 0.6, 0.4
SEUIL_MISERE = 0.25  # à deux : un jeu dont l'accord avec un profil est sous ce seuil est écarté
DOSE_DECOUVERTE = 5   # 1 découverte sur 5


def get(path: str, **params) -> dict:
    q = urllib.parse.urlencode([(k, v) for k, vs in params.items()
                                for v in (vs if isinstance(vs, list) else [vs])])
    url = f"{API}/{path}?format=json" + (f"&{q}" if q else "")
    for essai in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:  # réseau capricieux : on réessaie doucement
            if essai == 3:
                raise
            time.sleep(2 ** essai)
    raise RuntimeError(url)


def tous(path: str) -> list[dict]:
    out, page = [], 1
    while True:
        d = get(path, page=page)
        out += d.get("results", [])
        if not d.get("next"):
            return out
        page += 1


def retrouver(note: dict) -> dict | None:
    """Trouve la fiche d'un jeu noté : par id BGG si connu, sinon par titre (le plus voté)."""
    if note.get("source") == "bgg" or note.get("source") == "ref-jeu":
        try:
            return get(f"games/{int(note['id'])}/")
        except Exception:
            pass
    titre = note.get("titre") or ""
    if not titre:
        return None
    res = get("games/", search=titre, ordering="-num_votes").get("results", [])
    return res[0] if res else None


def traits(g: dict) -> set[str]:
    return ({f"m:{m}" for m in g.get("mechanic_name") or []}
            | {f"c:{c}" for c in g.get("category_name") or []}
            | {f"t:{t}" for t in g.get("game_type_name") or []}
            | ({"m:Cooperative Game"} if g.get("cooperative") else set()))


def profil(notes_jeux: list[tuple[dict, int]]) -> dict:
    """Poids de chaque trait = somme des notes centrées / (nombre + 2) : un trait vu une fois pèse peu."""
    somme, nb = defaultdict(float), defaultdict(int)
    for g, note in notes_jeux:
        for t in traits(g):
            somme[t] += note - 3
            nb[t] += 1
    poids = {t: somme[t] / (nb[t] + 2) for t in somme}
    aimes = [g for g, n in notes_jeux if n >= 4]
    cx = [g["complexity"] for g in aimes if g.get("complexity")]
    return {"poids": poids, "complexite": sum(cx) / len(cx) if cx else None,
            "aimes": aimes, "rejetes": [g for g, n in notes_jeux if n <= 2]}


def accord(g: dict, p: dict) -> float:
    """Accord entre un jeu et un profil, entre 0 et 1 (0,5 = neutre)."""
    ts = traits(g)
    if not ts or not p["poids"]:
        return 0.5
    s = sum(p["poids"].get(t, 0.0) for t in ts) / math.sqrt(len(ts))
    if p["complexite"] and g.get("complexity"):
        s -= 0.5 * abs(g["complexity"] - p["complexite"])
    return 1 / (1 + math.exp(-s))


def explication(g: dict, p: dict) -> tuple[list[str], str | None]:
    """Traits aimés partagés (les plus forts d'abord) et jeu aimé le plus proche."""
    ts = traits(g)
    forts = sorted((t for t in ts if p["poids"].get(t, 0) > 0), key=lambda t: -p["poids"][t])
    proche = max(p["aimes"], key=lambda a: len(traits(a) & ts), default=None)
    return list(dict.fromkeys(t[2:] for t in forts))[:3], (proche["name"] if proche and traits(proche) & ts else None)


def filtres(crit: dict, nouveautes: bool) -> dict:
    f = {}
    if crit.get("joueurs"):
        f["max_players__gte"] = int(crit["joueurs"])
        f["min_players__lte"] = int(crit["joueurs"])
    if crit.get("dureeMaxMin"):
        f["max_time__lte"] = int(crit["dureeMaxMin"])
    niveaux = [COMPLEXITE[c] for c in crit.get("complexite") or [] if c in COMPLEXITE]
    if niveaux:
        f["complexity__gte"] = min(a for a, _ in niveaux)
        f["complexity__lte"] = max(b for _, b in niveaux)
    if nouveautes:
        f["year__gte"] = dt.date.today().year - 1
    return f


def a_eviter(g: dict, crit: dict) -> bool:
    mots = [m.lower() for m in crit.get("themesAEviter") or []]
    texte = " ".join((g.get("category_name") or []) + [g.get("description") or ""]).lower()
    if any(m and m in texte for m in mots):
        return True
    styles = set(crit.get("style") or [])
    if styles and styles == {"coopératif"} and not g.get("cooperative"):
        return True
    if styles and "coopératif" not in styles and g.get("cooperative"):
        return True
    return False


def nom_famille(g: dict) -> str:
    """« Codenames: Pictures » → « codenames » : sert à ne pas reproposer un jeu déjà noté sous une autre édition."""
    return (g.get("name") or "").split(":")[0].strip().casefold()


def deja_note(g: dict, deja: set[int], familles: set[str]) -> bool:
    """Jeu déjà noté, réédition (implements) ou déclinaison de même nom d'un jeu déjà noté."""
    return (g["bgg_id"] in deja or bool(set(g.get("implements") or []) & deja)
            or nom_famille(g) in familles)


def candidats(likes: list[int], f: dict, deja: set[int], n: int = 100,
              familles: set[str] = frozenset()) -> list[dict]:
    out, page = [], 1
    while len(out) < n and page <= 3:
        d = get("games/recommend/", like=likes, page=page, **f) if likes else \
            get("games/", ordering="-bayes_rating", page=page, **f)
        for g in d.get("results", []):
            if not deja_note(g, deja, familles) and not g.get("compilation"):
                out.append(g)
        if not d.get("next"):
            break
        page += 1
    return out[:n]


def selection(notes: list[dict], crit: dict, nouveautes: bool, maxi: int) -> dict:
    par_personne: dict[str, list[tuple[dict, int]]] = defaultdict(list)
    introuvables, deja, familles = [], set(), set()
    for nt in notes:
        g = retrouver(nt)
        if not g:
            introuvables.append(nt.get("titre"))
            continue
        deja.add(g["bgg_id"])
        familles.add(nom_famille(g))
        par_personne[nt.get("personne", "arthur")].append((g, int(nt["note"])))
    profils = {p: profil(v) for p, v in par_personne.items()}
    f = filtres(crit, nouveautes)
    # Un ensemble de voisins par personne (ses jeux aimés), pour que les goûts de chacun comptent.
    rangs: dict[int, dict[str, float]] = defaultdict(dict)
    fiches: dict[int, dict] = {}
    for p, pr in (profils.items() or [("arthur", None)]):
        likes = sorted({g["bgg_id"] for g in pr["aimes"]}) if pr else []
        pool = [g for g in candidats(likes, f, deja, familles=familles) if not a_eviter(g, crit)]
        for rang, g in enumerate(pool):
            rangs[g["bgg_id"]][p] = 1 - rang / max(len(pool), 1)
            fiches[g["bgg_id"]] = g
    personnes = list(profils) or ["arthur"]

    notes_finales = []
    for bid, g in fiches.items():
        collab = sum(rangs[bid].get(p, 0.0) for p in personnes) / len(personnes)
        acc = {p: accord(g, pr) for p, pr in profils.items()} or {"arthur": 0.5}
        if len(acc) > 1 and min(acc.values()) < SEUIL_MISERE:
            continue  # moyenne sans misère
        a = sum(acc.values()) / len(acc)
        notes_finales.append((POIDS_COLLAB * collab + POIDS_PROFIL * a, a, g))
    notes_finales.sort(key=lambda x: -x[0])

    # Diversité (MMR) : un jeu trop semblable à un jeu déjà retenu (même famille, mêmes mécaniques) recule.
    nb_decouvertes = maxi // DOSE_DECOUVERTE
    choisis, reste = [], notes_finales[:60]
    while reste and len(choisis) < maxi - nb_decouvertes:
        def mmr(x):
            ts = traits(x[2])
            sim = max((len(ts & traits(c[2])) / max(len(ts | traits(c[2])), 1) for c in choisis), default=0)
            meme_famille = any(x[2]["name"].split(":")[0] == c[2]["name"].split(":")[0] for c in choisis)
            return x[0] - 0.5 * sim - (0.5 if meme_famille else 0)
        meilleur = max(reste, key=mmr)
        choisis.append(meilleur)
        reste.remove(meilleur)
    pris = {g["bgg_id"] for _, _, g in choisis}
    decouvertes = decouvrir(profils, f, crit, deja | pris, nb_decouvertes)

    def sortie(g, score, decouverte=False, ancre=None):
        if decouverte:
            return fiche(g, score, True, f"Découverte, parce que vous aimez : {ancre}.")
        bouts = []
        for p, pr in profils.items():
            aimes, proche = explication(g, pr)
            raisons = ([f"comme {proche}"] if proche else []) + (["aime " + ", ".join(aimes[:2])] if aimes else [])
            if raisons:
                bouts.append(f"{p.capitalize()} : " + ", ".join(raisons))
        pourquoi = ("; ".join(bouts) + ".") if bouts else "Bien classé par les joueurs de BGG."
        return fiche(g, score, False, pourquoi)

    def fiche(g, score, decouverte, pourquoi):
        return {"bggId": g["bgg_id"], "titre": g["name"], "annee": g.get("year"),
                "minPlayers": g.get("min_players"), "maxPlayers": g.get("max_players"),
                "durationMinutes": g.get("max_time"), "minAge": g.get("min_age"),
                "complexite": round(g["complexity"], 2) if g.get("complexity") else None,
                "designers": g.get("designer_name") or [], "mecaniques": g.get("mechanic_name") or [],
                "categories": g.get("category_name") or [], "rangBgg": g.get("bgg_rank"),
                "lien": f"https://boardgamegeek.com/boardgame/{g['bgg_id']}",
                "score": round(score, 3), "decouverte": decouverte, "pourquoi": pourquoi}

    return {"genere": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": "Recommend.Games (données BoardGameGeek)",
            "personnes": {p: {"jeuxNotes": len(par_personne[p]),
                              "traitsAimes": [t[2:] for t, w in sorted(pr["poids"].items(), key=lambda x: -x[1])[:6] if w > 0],
                              "traitsRejetes": [t[2:] for t, w in sorted(pr["poids"].items(), key=lambda x: x[1])[:4] if w < 0],
                              "complexiteAimee": round(pr["complexite"], 2) if pr["complexite"] else None}
                          for p, pr in profils.items()},
            "introuvables": introuvables,
            "jeux": [sortie(g, s) for s, _, g in choisis] + [sortie(g, s, True, a) for s, a, g in decouvertes]}


def decouvrir(profils: dict, f: dict, crit: dict, exclus: set[int], n: int) -> list:
    """Ancre = une mécanique fortement aimée ; on cherche des jeux bien classés qui l'ont,
    mais qui partagent peu d'autres traits avec les jeux aimés, et aucun trait fortement rejeté."""
    if n <= 0 or not profils:
        return []
    poids = defaultdict(float)
    for pr in profils.values():
        for t, w in pr["poids"].items():
            poids[t] += w
    ancres = [t for t, w in sorted(poids.items(), key=lambda x: -x[1]) if t.startswith("m:") and w > 0.3][:3]
    rejetes = {t for t, w in poids.items() if w < -0.3}
    mech_ids = {m["name"]: m["bgg_id"] for m in tous("mechanics/")}
    out = []
    for i in range(n):
        if not ancres:
            break
        ancre = ancres[i % len(ancres)][2:]
        if ancre not in mech_ids:
            continue
        res = get("games/", mechanic=mech_ids[ancre], ordering="-bayes_rating", **f).get("results", [])
        res = [g for g in res if g["bgg_id"] not in exclus and not (traits(g) & rejetes) and not a_eviter(g, crit)]
        res.sort(key=lambda g: sum(1 for t in traits(g) if poids.get(t, 0) > 0))  # le plus éloigné d'abord
        if res:
            g = res[0]
            exclus.add(g["bgg_id"])
            out.append((0.0, ancre, g))
    return out


DEMO = [  # notes FICTIVES pour vérifier la méthode : ce ne sont pas les goûts d'Arthur
    {"personne": "arthur", "titre": "Azul", "note": 5},
    {"personne": "arthur", "titre": "Cascadia", "note": 4},
    {"personne": "arthur", "titre": "The Crew: The Quest for Planet Nine", "note": 5},
    {"personne": "arthur", "titre": "Monopoly", "note": 1},
    {"personne": "julie", "titre": "Dixit", "note": 5},
    {"personne": "julie", "titre": "Azul", "note": 4},
    {"personne": "julie", "titre": "Twilight Imperium: Fourth Edition", "note": 1},
]


def main(argv: list[str]) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--criteres", help="criteres.json en clair")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--nouveautes", action="store_true", help="seulement les jeux de l'an dernier et de cette année")
    ap.add_argument("--max", type=int, default=10)
    a = ap.parse_args(argv)
    if a.demo:
        crit = {"joueurs": 4, "dureeMaxMin": 45, "complexite": ["légère", "moyenne"], "themesAEviter": ["vulgaire"]}
        notes = DEMO
    else:
        tab = json.load(open(a.criteres, encoding="utf-8"))["tabs"].get("jeux-societe", {})
        crit, notes = tab, tab.get("notes", [])
    json.dump(selection(notes, crit, a.nouveautes, a.max), sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
