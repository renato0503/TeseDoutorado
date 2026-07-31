#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consolida os blocos de curadoria, deduplicando por (tema, titulo)."""

import json
import os
import re

CURADORIA = r"C:\Users\Renato\Documents\Doutorado\curadoria"

BLOCO_POR_SPRINT = {}
for s in range(1, 8):
    BLOCO_POR_SPRINT[s] = "bloco_a.json"
for s in range(8, 11):
    BLOCO_POR_SPRINT[s] = "bloco_b.json"
for s in range(11, 16):
    BLOCO_POR_SPRINT[s] = "bloco_c.json"


def sprint_de_tema(tema):
    m = re.match(r"Sprint\s+(\d+)", tema)
    return int(m.group(1)) if m else None


def main():
    todos = []
    for b in ["bloco_a.json", "bloco_b.json", "bloco_c.json"]:
        path = os.path.join(CURADORIA, b)
        todos.extend(json.load(open(path, encoding="utf-8")))

    # dedup por (tema, titulo normalizado)
    vistos = {}
    for obra in todos:
        chave = (obra.get("tema", "").strip(), obra.get("titulo", "").strip().lower())
        vistos[chave] = obra
    unicos = list(vistos.values())
    print(f"Totais: brutos={len(todos)} | unicos={len(unicos)}")

    # reagrupa por bloco
    blocos = {"bloco_a.json": [], "bloco_b.json": [], "bloco_c.json": []}
    sem_sprint = []
    for obra in unicos:
        s = sprint_de_tema(obra.get("tema", ""))
        bloco = BLOCO_POR_SPRINT.get(s)
        if bloco:
            blocos[bloco].append(obra)
        else:
            sem_sprint.append(obra)

    for bloco, obras in blocos.items():
        path = os.path.join(CURADORIA, bloco)
        json.dump(obras, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"{bloco}: {len(obras)}")
    if sem_sprint:
        print("SEM SPRINT:", len(sem_sprint))
        for o in sem_sprint[:5]:
            print("  ", o.get("tema"))


if __name__ == "__main__":
    main()
