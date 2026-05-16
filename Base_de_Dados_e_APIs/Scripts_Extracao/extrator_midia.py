#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrator de Mídia - Artigo 15"""

import requests, csv, os, time
from datetime import datetime

DEST = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Raw_Data",
    "Artigos_Quali",
    "artigo_15_midia.csv",
)
QUERIES = [
    "AI government procurement",
    "AI public sector Brazil",
    "algorithmic transparency government",
]
PER_PAGE, MAX_PAG = 10, 2


def main():
    print("=== Extrator Mídia ===")
    results = []
    for q in QUERIES:
        for p in range(1, MAX_PAG + 1):
            try:
                r = requests.get(
                    "https://api.openalex.org/works",
                    params={
                        "filter": f"default.search:{q}",
                        "per_page": PER_PAGE,
                        "page": p,
                        "mailto": "x@x.com",
                    },
                    timeout=30,
                )
                for item in r.json().get("results", []):
                    title = item.get("title", "")
                    if title and len(title) > 10:
                        results.append(
                            {
                                "titulo": title,
                                "fonte": item.get("primary_location", {})
                                .get("source", {})
                                .get("display_name", "Unknown"),
                                "ano": str(item.get("publication_year", "")),
                            }
                        )
            except:
                pass
            time.sleep(1)

    uniq = {r["titulo"][:40]: r for r in results}.values()
    if uniq:
        os.makedirs(os.path.dirname(DEST), exist_ok=True)
        with open(DEST, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=["titulo", "fonte", "ano"]).writeheader()
            f.writelines([f"{r['titulo']},{r['fonte']},{r['ano']}\n" for r in uniq])
        print(f"Salvo {len(uniq)} items")
    print("OK")


if __name__ == "__main__":
    main()
