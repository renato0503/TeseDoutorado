"""
A1-S6 v2: Busca refinada com filtro de conceitos OpenAlex.

Foca em artigos RELEVANTES usando concept filters e search em title+abstract.

Uso: python scripts/buscar_artigos_referencial_v2.py
"""

import requests
import time
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

OUT_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Art01")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Conceitos OpenAlex mapeados para compras publicas
# https://api.openalex.org/concepts
CONCEPT_FILTERS = {
    "T1_definicao_complexas": {
        "descricao": "Definicao de compras complexas",
        "concepts": "public.procurement|government.procurement|public.administration",
        "queries": [
            "complex procurement public sector",
            "public procurement complexity innovation",
            "strategic procurement government",
            "public purchasing complexity",
            "government contracting innovation",
        ],
    },
    "T2_inovacao_tecnologica": {
        "descricao": "Inovacao tecnologica em compras publicas",
        "concepts": "innovation.policy|technology.policy|public.procurement",
        "queries": [
            "public procurement innovation policy",
            "innovation-oriented procurement",
            "pre-commercial procurement innovation",
            "demand-side innovation procurement",
            "public technology procurement",
            "mission-oriented innovation procurement",
        ],
    },
    "T3_esg_sustentabilidade": {
        "descricao": "ESG e sustentabilidade em compras",
        "concepts": "sustainable.procurement|green.procurement|environmental.policy",
        "queries": [
            "green public procurement policy",
            "sustainable public procurement",
            "circular procurement public sector",
            "socially responsible procurement",
            "environmental public purchasing",
            "sustainable procurement criteria",
        ],
    },
    "T4_assimetria_reducao": {
        "descricao": "Assimetria informacional e ferramentas",
        "concepts": "transaction.cost|information.asymmetry|public.procurement",
        "queries": [
            "information asymmetry procurement",
            "transaction cost public procurement",
            "procurement capability government",
            "decision support procurement",
            "digital procurement e-procurement",
            "procurement professionalization capacity",
            "AI procurement public sector",
        ],
    },
}

print("=" * 60)
print("BUSCA ACADEMICA REFINADA (CONCEPT FILTER)")
print("=" * 60)

all_results = []
total_queries = sum(len(t["queries"]) for t in CONCEPT_FILTERS.values())
query_count = 0

for tema_id, tema_data in CONCEPT_FILTERS.items():
    print(f"\n--- {tema_id}: {tema_data['descricao']} ---")

    for query in tema_data["queries"]:
        query_count += 1

        for page in range(1, 4):
            try:
                url = "https://api.openalex.org/works"
                params = {
                    "search": query,
                    "per_page": 25,
                    "page": page,
                    "sort": "cited_by_count:desc",
                    "filter": f"type:article,concepts.id:{tema_data['concepts']}",
                }
                r = requests.get(url, params=params, timeout=15)
                if r.status_code != 200:
                    break

                data = r.json()
                works = data.get("results", [])
                if not works:
                    break

                for w in works:
                    authors = [
                        a.get("author", {}).get("display_name", "")
                        for a in w.get("authorships", [])
                    ]
                    concepts = [
                        c.get("display_name", "")
                        for c in w.get("concepts", [])[:5]
                    ]

                    # Get abstract
                    abstract = ""
                    if w.get("abstract_inverted_index"):
                        idx = w["abstract_inverted_index"]
                        words = [""] * (max(idx.values(), key=lambda x: max(x) if x else 0) + 1)
                        for word, positions in idx.items():
                            for pos in positions:
                                words[pos] = word
                        abstract = " ".join(words)

                    all_results.append({
                        "tema": tema_id,
                        "query": query,
                        "titulo": w.get("title", ""),
                        "autores": "; ".join(authors[:5]),
                        "ano": w.get("publication_year"),
                        "doi": w.get("doi", "").replace("https://doi.org/", ""),
                        "abstract": abstract[:2000],
                        "citacoes": w.get("cited_by_count", 0),
                        "journal": w.get("primary_location", {}).get("source", {}).get("display_name", ""),
                        "tipo": w.get("type", ""),
                        "open_access": w.get("open_access", {}).get("is_oa", False),
                        "concepts": "; ".join(concepts),
                        "url": w.get("id", ""),
                    })

                time.sleep(0.25)

            except Exception:
                pass

        if query_count % 4 == 0:
            print(f"  [{query_count}/{total_queries}] | Artigos: {len(all_results)}")

# Process results
df = pd.DataFrame(all_results)
if len(df) > 0:
    df = df.drop_duplicates(subset=["doi"])
    df = df.drop_duplicates(subset=["titulo"])
    df = df[df["titulo"].notna() & (df["titulo"] != "")]

print(f"\n{'='*60}")
print(f"RESULTADO FINAL")
print(f"{'='*60}")
print(f"Total: {len(df)} artigos unicos")

for tema_id in CONCEPT_FILTERS:
    count = len(df[df["tema"] == tema_id])
    print(f"  {tema_id}: {count}")

# Also do a broader search without concept filter for T1-T4
print(f"\n[EXTRA] Busca ampla complementar (sem filtro)...")
extra_results = []
extra_queries = [
    ("T_geral", "public procurement innovation sustainability"),
    ("T_geral", "government purchasing complex contracts"),
    ("T_geral", "procurement information asymmetry transaction costs"),
    ("T_geral", "public procurement reform modernization"),
]

for tema, query in extra_queries:
    try:
        url = "https://api.openalex.org/works"
        params = {
            "search": query,
            "per_page": 25,
            "page": 1,
            "sort": "cited_by_count:desc",
            "filter": "type:article",
        }
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            for w in r.json().get("results", []):
                authors = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
                concepts = [c.get("display_name", "") for c in w.get("concepts", [])[:5]]
                abstract = ""
                if w.get("abstract_inverted_index"):
                    idx = w["abstract_inverted_index"]
                    try:
                        max_pos = max(max(v) if v else 0 for v in idx.values())
                        words = [""] * (max_pos + 1)
                        for word, positions in idx.items():
                            for pos in positions:
                                words[pos] = word
                        abstract = " ".join(words)
                    except: pass
                extra_results.append({
                    "tema": tema, "query": query,
                    "titulo": w.get("title", ""),
                    "autores": "; ".join(authors[:5]),
                    "ano": w.get("publication_year"),
                    "doi": w.get("doi", "").replace("https://doi.org/", ""),
                    "abstract": abstract[:2000],
                    "citacoes": w.get("cited_by_count", 0),
                    "journal": w.get("primary_location", {}).get("source", {}).get("display_name", ""),
                    "tipo": w.get("type", ""),
                    "open_access": w.get("open_access", {}).get("is_oa", False),
                    "concepts": "; ".join(concepts),
                    "url": w.get("id", ""),
                })
        time.sleep(0.3)
    except: pass

df_extra = pd.DataFrame(extra_results)
df = pd.concat([df, df_extra], ignore_index=True)
df = df.drop_duplicates(subset=["doi"]).drop_duplicates(subset=["titulo"])
df = df[df["titulo"].notna() & (df["titulo"] != "")]

print(f"Total final (incluindo extra): {len(df)}")
for tema_id in CONCEPT_FILTERS:
    count = len(df[df["tema"] == tema_id])
    print(f"  {tema_id}: {count}")

out_path = OUT_DIR / "referencial_artigos.csv"
df.to_csv(out_path, index=False, encoding="utf-8")
print(f"\nDataset: {out_path}")

# Top papers per theme (clean output)
print(f"\n{'='*60}")
print("TOP CITADOS POR TEMA")
print(f"{'='*60}")
for tema_id in CONCEPT_FILTERS:
    subset = df[df["tema"] == tema_id]
    top = subset.nlargest(8, "citacoes")
    print(f"\n  {tema_id}:")
    for _, row in top.iterrows():
        print(f"    [{row['citacoes']}c] {row['autores'][:80]} ({row['ano']})")
        print(f"      {row['titulo'][:120]}")

stats = {
    "data": datetime.now().isoformat(),
    "total": int(len(df)),
    "por_tema": {t: int(len(df[df["tema"] == t])) for t in CONCEPT_FILTERS},
}
with open(OUT_DIR / "stats_busca.json", "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2, ensure_ascii=False)

print(f"\nCONCLUIDO. Dataset: {len(df)} artigos.")
