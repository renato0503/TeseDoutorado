"""
ARTIGO 25 - Coleta via OpenAlex (REFATORADO)
WESAAC - Multi-Agent LLM Architecture with Dynamic Cascading

Correcao: Injetar cabecalho User-Agent com email no Polie Pool
para evitar Rate Limit 429
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\25-Artigo AI Offline"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(RAW, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

BASE_URL = "https://api.openalex.org"
HEADERS = {
    "User-Agent": "mailto:gestor.renatorosa@gmail.com",
    "Accept": "application/json"
}


def buscar_por_termo(termo, ano_inicio=2018, ano_fim=2024):
    """Busca artigos por termo e ano via OpenAlex API com Polite Pool."""
    time.sleep(3.1)
    print(f"  Buscando: {termo}...", end=" ", flush=True)

    registros = []
    pagina = 0
    por_pagina = 200
    total_processado = 0

    while True:
        params = {
            "search": termo,
            "filter": f"type:article,is_oa:true,publication_year:{ano_inicio}-{ano_fim}",
            "per_page": por_pagina,
            "page": pagina + 1
        }

        try:
            response = requests.get(
                f"{BASE_URL}/works",
                params=params,
                headers=HEADERS,
                timeout=60
            )

            if response.status_code == 429:
                print(f"\n  ! Rate limit detectado. Aguardando 60s...")
                time.sleep(60)
                continue

            if response.status_code != 200:
                print(f"  ! Erro HTTP {response.status_code}: {response.text[:100]}")
                break

            data = response.json()
            works = data.get("results", [])
            meta = data.get("meta", {})

            if not works:
                break

            for w in works:
                try:
                    titulo = w.get("title") or ""
                    autores = [a["author"]["display_name"] for a in w.get("authorships", []) if a.get("author")]
                    paises = []
                    for a in w.get("authorships", []):
                        for inst in a.get("institutions", []):
                            if inst.get("country_code"):
                                paises.append(inst["country_code"])
                    loc = w.get("primary_location") or {}
                    src = loc.get("source") or {}
                    conceitos = [c["display_name"] for c in w.get("concepts", []) if c.get("display_name")][:5]

                    registros.append({
                        "id": w.get("id"),
                        "doi": w.get("doi"),
                        "titulo": titulo,
                        "ano": w.get("publication_year"),
                        "periodico": src.get("display_name") if isinstance(src, dict) else None,
                        "citacoes": w.get("cited_by_count"),
                        "fwci": w.get("fwci"),
                        "autores": "; ".join(autores) if autores else None,
                        "n_autores": len(autores),
                        "paises": "; ".join(set(paises)) if paises else None,
                        "conceitos": "; ".join(conceitos),
                    })
                    total_processado += 1
                except Exception as e:
                    print(f"  ! Erro ao processar work: {e}")
                    continue

            pagina += 1
            total = meta.get("count", 0)

            if pagina * por_pagina >= total or not works:
                break

        except requests.exceptions.RequestException as e:
            print(f"  ! Erro de conexao: {e}")
            break

    print(f"{len(registros)} artigos (processados: {total_processado})")
    return registros


def main():
    termos = [
        "LLM multi-agent",
        "model cascading LLM",
        "LLM routing",
        "on-premises LLM",
        "Retrieval-Augmented Generation",
        "FrugalGPT",
        "federated LLM",
    ]

    print("=== ARTIGO 25 - OpenAlex (Polite Pool) ===\n")
    print(f"Headers: {HEADERS}\n")

    todos = []
    for termo in termos:
        regs = buscar_por_termo(termo, 2018, 2024)
        todos.extend(regs)

    df = pd.DataFrame(todos).drop_duplicates(subset="id").reset_index(drop=True)
    output = os.path.join(RAW, "llm_multi_agent_openalex.csv")
    df.to_csv(output, index=False)
    print(f"\nTotal: {len(df)} artigos unicos salvos em {output}")
    return df


if __name__ == "__main__":
    main()
