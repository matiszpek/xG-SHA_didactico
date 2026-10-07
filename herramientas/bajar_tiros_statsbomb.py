"""Baja los TIROS de StatsBomb Open Data y los guarda en un CSV — herramienta PROVISTA (U3).

    python herramientas/bajar_tiros_statsbomb.py                    # torneos de selecciones recientes (~260 partidos)
    python herramientas/bajar_tiros_statsbomb.py --preset ligas2015 # las 5 grandes ligas 2015/16 (~1800 partidos)
    python herramientas/bajar_tiros_statsbomb.py --competiciones 43:106 55:282

Salida: datos/statsbomb/tiros.csv, una fila por tiro, con:
    match_id, competicion, temporada, periodo, minuto, x, y  (coordenadas StatsBomb, en yardas: cancha 120 × 80,
                                                              el equipo que patea ataca hacia x = 120)
    parte_cuerpo   pie / cabeza / otro
    tipo           Open Play / Free Kick / Penalty / Corner / Kick Off
    patron         cómo empezó la jugada (Regular Play, From Corner, From Counter, ...)
    bajo_presion   0/1
    primer_toque   0/1
    xg_statsbomb   el xG del modelo (propietario) de StatsBomb, para comparar
    gol            0/1   ← lo que vamos a predecir
    n_rivales_triangulo  rivales (sin el arquero) dentro del triángulo tirador–palo–palo (del freeze frame)
    dist_arquero   distancia del arquero al CENTRO DEL ARCO, en yardas (vacío si no hay dato)

Se baja cada archivo de eventos (~3 MB), se extraen los tiros y se descarta el resto: en disco queda solo el CSV.
Las definiciones por penales (período 5) se excluyen: no son tiros "de juego".

Datos: StatsBomb Open Data (https://github.com/statsbomb/open-data). Uso NO comercial y con atribución.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "datos" / "statsbomb" / "tiros.csv"

PRESETS = {
    # (competition_id, season_id)
    "torneos": [(43, 106), (43, 3), (55, 43), (55, 282), (223, 282)],   # Mundial 2022 y 2018, Euro 2020 y 2024, Copa América 2024
    "ligas2015": [(2, 27), (11, 27), (12, 27), (9, 27), (7, 27)],         # Premier, La Liga, Serie A, Bundesliga, Ligue 1 — 2015/16
}

COLUMNAS = ["match_id", "competicion", "temporada", "periodo", "minuto", "x", "y", "parte_cuerpo", "tipo", "patron",
            "bajo_presion", "primer_toque", "xg_statsbomb", "gol", "n_rivales_triangulo", "dist_arquero"]

PALO_IZQ, PALO_DER, CENTRO_ARCO = (120.0, 36.0), (120.0, 44.0), (120.0, 40.0)


def _json(url: str, intentos: int = 4):
    for k in range(intentos):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception as e:  # cortes de conexión, timeouts: reintentar con espera creciente
            if k == intentos - 1:
                raise RuntimeError(f"No se pudo bajar {url}: {e}") from e
            time.sleep(2 ** k)


def _en_triangulo(p, a, b, c) -> bool:
    def lado(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    d1, d2, d3 = lado(p, a, b), lado(p, b, c), lado(p, c, a)
    neg = d1 < 0 or d2 < 0 or d3 < 0
    pos = d1 > 0 or d2 > 0 or d3 > 0
    return not (neg and pos)


def _parte(nombre: str) -> str:
    if "Foot" in nombre:
        return "pie"
    if nombre == "Head":
        return "cabeza"
    return "otro"


def tiros_de_partido(match_id: int, competicion: str, temporada: str) -> list[dict]:
    eventos = _json(f"{BASE}/events/{match_id}.json")
    filas = []
    for e in eventos:
        if e["type"]["name"] != "Shot" or e["period"] == 5:     # período 5 = definición por penales: no es juego
            continue
        s = e["shot"]
        x, y = e["location"][:2]
        rivales, dist_arq = 0, ""
        for jug in s.get("freeze_frame", []) or []:
            if jug.get("teammate"):
                continue
            loc = jug["location"]
            if jug.get("position", {}).get("name") == "Goalkeeper":
                dist_arq = round(math.hypot(loc[0] - CENTRO_ARCO[0], loc[1] - CENTRO_ARCO[1]), 2)
            elif _en_triangulo(loc, (x, y), PALO_IZQ, PALO_DER):
                rivales += 1
        filas.append({
            "match_id": match_id, "competicion": competicion, "temporada": temporada,
            "periodo": e["period"], "minuto": e["minute"], "x": x, "y": y,
            "parte_cuerpo": _parte(s["body_part"]["name"]),
            "tipo": s["type"]["name"], "patron": e["play_pattern"]["name"],
            "bajo_presion": int(bool(e.get("under_pressure"))), "primer_toque": int(bool(s.get("first_time"))),
            "xg_statsbomb": s.get("statsbomb_xg", ""), "gol": int(s["outcome"]["name"] == "Goal"),
            "n_rivales_triangulo": rivales if s.get("freeze_frame") else "", "dist_arquero": dist_arq,
        })
    return filas


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--preset", choices=sorted(PRESETS), default="torneos")
    p.add_argument("--competiciones", nargs="*", help="pares competition_id:season_id (pisan el preset)")
    p.add_argument("--salida", type=Path, default=SALIDA)
    p.add_argument("--hilos", type=int, default=4)
    a = p.parse_args()

    pares = [tuple(map(int, c.split(":"))) for c in a.competiciones] if a.competiciones else PRESETS[a.preset]
    comps = {(c["competition_id"], c["season_id"]): c for c in _json(f"{BASE}/competitions.json")}

    partidos = []
    for cid, sid in pares:
        info = comps.get((cid, sid))
        if info is None:
            print(f"⚠ no existe la competencia {cid}:{sid} en StatsBomb Open Data", file=sys.stderr)
            continue
        ms = _json(f"{BASE}/matches/{cid}/{sid}.json")
        partidos += [(m["match_id"], info["competition_name"], info["season_name"]) for m in ms]
        print(f"{info['competition_name']} {info['season_name']}: {len(ms)} partidos")

    filas, hechos = [], 0
    with ThreadPoolExecutor(max_workers=a.hilos) as ex:
        futuros = [ex.submit(tiros_de_partido, *pt) for pt in partidos]
        for fut in as_completed(futuros):
            filas += fut.result()
            hechos += 1
            if hechos % 25 == 0 or hechos == len(partidos):
                print(f"  {hechos}/{len(partidos)} partidos, {len(filas)} tiros", flush=True)

    filas.sort(key=lambda r: (r["match_id"], r["minuto"]))
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    with open(a.salida, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)
    goles = sum(r["gol"] for r in filas)
    print(f"✓ {len(filas)} tiros ({goles} goles, {goles / max(len(filas), 1):.1%}) de {len(partidos)} partidos → {a.salida}")


if __name__ == "__main__":
    main()
