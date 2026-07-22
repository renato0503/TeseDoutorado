"""
A1-S6: Busca academica sistematica para o Referencial Teorico do Artigo 01.

Busca 200+ artigos em OpenAlex e Semantic Scholar cobrindo 4 temas
na hierarquia macro -> micro:

T1: Definicao de compras complexas (macro)
T2: Inovacao tecnologica em compras publicas
T3: ESG e sustentabilidade em compras publicas  
T4: Reducao de assimetria informacional (micro)

Uso: python scripts/buscar_artigos_referencial.py
"""

import requests
import time
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

OUT_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Art01")
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEMAS = {
    "T1_definicao_complexas": {
        "descricao": "Definicao e categorizacao de compras publicas complexas",
        "queries": [
            "complex public procurement",
            "public procurement complexity",
            "innovation procurement definition",
            "technology procurement public sector",
            "strategic public procurement",
            "complex purchasing government",
        ],
    },
    "T2_inovacao_tecnologica": {
        "descricao": "Inovacao tecnologica e P&D em compras publicas",
        "queries": [
            "public procurement innovation",
            "government procurement technology",
            "innovation-oriented public procurement",
            "pre-commercial procurement",
            "public procurement R&D",
            "transformative public procurement",
            "mission-oriented innovation procurement",
            "demand-side innovation policy",
        ],
    },
    "T3_esg_sustentabilidade": {
        "descricao": "ESG, sustentabilidade e compras verdes",
        "queries": [
            "green public procurement",
            "sustainable public procurement",
            "circular procurement",
            "socially responsible public procurement",
            "GPP criteria public procurement",
            "environmental public purchasing",
            "sustainable procurement policy",
            "circular economy procurement",
        ],
    },
    "T4_assimetria_reducao": {
        "descricao": "Reducao de assimetria informacional e ferramentas de suporte",
        "queries": [
            "information asymmetry public procurement",
            "transaction cost economics procurement",
            "buyer capability public procurement",
            "procurement capacity building",
            "decision support public procurement",
            "AI public procurement",
            "algorithmic procurement government",
            "digital procurement transformation",
            "e-procurement impact",
            "procurement professionalization",
        ],
    },
}

print("=" * 60)
print("BUSCA ACADEMICA — REFERENCIAL ARTIGO 01")
print("=" * 60)

all_results = []
total_queries = sum(len(t["queries"]) for t in TEMAS.values())
query_count = 0

for tema_id, tema_data in TEMAS.items():
    print(f"\n{'='*60}")
    print(f"TEMA: {tema_id}")
    print(f"  {tema_data['descricao']}")
    print(f"  Queries: {len(tema_data['queries'])}")

    for query in tema_data["queries"]:
        query_count += 1
        per_page = 25

        for page in range(1, 3):
            try:
                url = "https://api.openalex.org/works"
                params = {
                    "search": query,
                    "per_page": per_page,
                    "page": page,
                    "sort": "cited_by_count:desc",
                    "filter": "type:article,language:en",
                }
                r = requests.get(url, params=params, timeout=15)
                if r.status_code != 200:
                    break

                data = r.json()
                works = data.get("results", [])

                for w in works:
                    authors = [
                        a.get("author", {}).get("display_name", "")
                        for a in w.get("authorships", [])
                    ]
                    concepts = [
                        c.get("display_name", "")
                        for c in w.get("concepts", [])[:5]
                    ]

                    all_results.append({
                        "tema": tema_id,
                        "query": query,
                        "titulo": w.get("title", ""),
                        "autores": "; ".join(authors[:5]),
                        "ano": w.get("publication_year"),
                        "doi": w.get("doi", ""),
                        "abstract": (w.get("abstract_inverted_index") or {}).get("abstract", ""),
                        "citacoes": w.get("cited_by_count", 0),
                        "journal": w.get("primary_location", {}).get("source", {}).get("display_name", ""),
                        "tipo": w.get("type", ""),
                        "open_access": w.get("open_access", {}).get("is_oa", False),
                        "concepts": "; ".join(concepts),
                        "url": w.get("id", ""),
                    })

                time.sleep(0.3)

            except Exception as e:
                pass

        if query_count % 5 == 0:
            print(f"  [{query_count}/{total_queries}] Total artigos: {len(all_results)}")

df = pd.DataFrame(all_results)
df = df.drop_duplicates(subset=["doi"]).drop_duplicates(subset=["titulo"])
df = df[df["titulo"].notna() & (df["titulo"] != "")]

print(f"\n{'='*60}")
print(f"RESULTADO FINAL")
print(f"{'='*60}")
print(f"Total bruto: {len(all_results)}")
print(f"Total apos dedup: {len(df)}")

for tema_id in TEMAS:
    count = len(df[df["tema"] == tema_id])
    print(f"  {tema_id}: {count} artigos")

out_path = OUT_DIR / "referencial_artigos.csv"
df.to_csv(out_path, index=False, encoding="utf-8")
print(f"\nDataset salvo: {out_path}")
print(f"Tamanho: {out_path.stat().st_size / 1024:.1f} KB")

# Save stats
stats = {
    "data_busca": datetime.now().isoformat(),
    "total_artigos": int(len(df)),
    "por_tema": {t: int(len(df[df["tema"] == t])) for t in TEMAS},
    "ano_medio": round(float(df["ano"].mean()), 1) if len(df) > 0 else 0,
    "ano_mediano": round(float(df["ano"].median()), 1) if len(df) > 0 else 0,
    "top_citados": [
        {"titulo": row["titulo"], "citacoes": int(row["citacoes"]), "ano": int(row["ano"])}
        for _, row in df.nlargest(10, "citacoes").iterrows()
    ],
}
with open(OUT_DIR / "stats_busca.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)

print(f"Stats salvas: {OUT_DIR / 'stats_busca.json'}")

# Print top papers per theme
print(f"\n{'='*60}")
print("TOP 5 POR TEMA (mais citados)")
print(f"{'='*60}")
for tema_id in TEMAS:
    top = df[df["tema"] == tema_id].nlargest(5, "citacoes")
    print(f"\n  {tema_id}:")
    for _, row in top.iterrows():
        print(f"    [{row['citacoes']} cit] {row['autores'][:60]} ({row['ano']})")
        print(f"      {row['titulo'][:100]}")

print("\nCONCLUIDO.")
