#!/usr/bin/env python3
"""Cherche (et télécharge) des sons libres sur Openverse, sans clé.
openverse.py "whoosh"                      liste les résultats (CC0 et domaine public)
openverse.py "whoosh" --prendre 1          télécharge le n° 1 dans assets/sfx/
openverse.py "piano calme" --musique --cc-by   musique, licences CC BY incluses (crédit obligatoire)
Chaque téléchargement est noté dans CREDITS.md. Une licence déclarée reste à vérifier sur la page source."""
import argparse, json, pathlib, re, sys, urllib.parse, urllib.request
UA = {"User-Agent": "openverse-cli/1.0"}
p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument("recherche"); p.add_argument("--prendre", type=int, metavar="N")
p.add_argument("--musique", action="store_true"); p.add_argument("--cc-by", action="store_true")
p.add_argument("--max", type=int, default=10, help="résultats (20 au plus)")
a = p.parse_args()
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40)
params = {"q": a.recherche, "license": "cc0,pdm" + (",by" if a.cc_by else ""), "page_size": min(a.max, 20)}
if a.musique: params["category"] = "music"
try:
    res = json.load(get("https://api.openverse.org/v1/audio/?" + urllib.parse.urlencode(params)))["results"]
except Exception as e:
    sys.exit(f"Openverse inaccessible : {e}")
if not res: sys.exit("Aucun résultat (essayer en anglais).")
for i, r in enumerate(res, 1):
    print(f"{i:2} {r['license']:5} {(r.get('duration') or 0)/1000:6.1f}s  {r['title']} - {r.get('creator')}  {r['foreign_landing_url']}")
if a.prendre is not None:
    if not 1 <= a.prendre <= len(res): sys.exit("Numéro hors liste.")
    r = res[a.prendre - 1]
    d = pathlib.Path(__file__).resolve().parent.parent / "assets" / ("musique" if a.musique else "sfx")
    ext = re.sub(r"\W", "", r.get("filetype") or "mp3")
    f = d / f"{re.sub(r'[^a-z0-9]+', '-', r['title'].lower()).strip('-')[:50]}-{r['id'][:8]}.{ext}"
    if not r["url"].startswith("https://"): sys.exit("URL non sécurisée, refusée.")
    f.write_bytes(get(r["url"]).read())
    with open(d.parent / "CREDITS.md", "a", encoding="utf-8") as c:
        c.write(f"- `{f.relative_to(d.parent)}` : {r['attribution']} {r['foreign_landing_url']}\n")
    print(f)
