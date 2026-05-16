#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Artigos Acadêmicos - Revisão Sistemática XAI no Setor Público
API: OpenAlex (mais permissiva que Semantic Scholar)

Autor: Renato de Oliveira Rosa
Data: Maio 2026
"""

import requests
import csv
import time
import os
import json

# ============================================
# CONFIGURAÇÕES
# ============================================

# Queries de busca
QUERIES = [
    "explainable AI government",
    "XAI public sector",
    "algorithmic transparency government",
    "AI explainability public administration",
]

# Campos a solicitar
CAMPOS_BASE = "id,doi,title,authors,publication_year,primary_location,open_access,cited_by_count,keywords"

# Pagination
PER_PAGE = 25
MAX_PAGINAS = 5

# Rate limit (OpenAlex é mais permissivo)
TEMPO_ESPERA = 1

# Timeout
TIMEOUT = 30

# Email para identificação (recomendado pela API)
EMAIL = "pesquisador@ufsc.br"

# Pasta de destino
PASTA_DESTINO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Raw_Data",
    "Revisao_Sistematica",
    "xai_public_sector.csv",
)

# ============================================
# FUNÇÕES
# ============================================


def buscar_works(query, pagina=1):
    """
    Busca works na API do OpenAlex.
    """
    url = "https://api.openalex.org/works"

    params = {
        "filter": f"default.search:{query}",
        "per_page": PER_PAGE,
        "page": pagina,
        "mailto": EMAIL,
    }

    response = None
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"  ❌ Erro HTTP {response.status_code if response else 'N/A'}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro na requisição: {e}")
        return None


def extrair_metadados(work):
    """
    Extrai metadados relevantes de um work.
    """
    # Autores
    autores_lista = work.get("authorships", [])
    autores = "; ".join(
        [a.get("author", {}).get("display_name", "") for a in autores_lista[:5]]
    )

    if len(autores_lista) > 5:
        autores += f" et al. ({len(autores_lista)} autores)"

    # DOI
    doi = work.get("doi", "")

    # URL
    url = work.get("doi", "")  # Usando DOI como URL

    # Periódico
    primary_location = work.get("primary_location", {})
    source = primary_location.get("source") if primary_location else None
    periodico = source.get("display_name", "") if source else ""

    # Open Access
    oa = work.get("open_access", {})
    is_oa = oa.get("is_oa", False)

    # Keywords
    keywords = work.get("keywords", [])
    keywords_str = "; ".join([k.get("display_name", "") for k in keywords[:5]])

    # Citações
    citacoes = work.get("cited_by_count", 0)

    return {
        "titulo": work.get("title", ""),
        "autores": autores,
        "ano": str(work.get("publication_year", "")),
        "periodico": periodico,
        "citacoes": citacoes,
        "doi": doi,
        "url": url,
        "open_access": "Sim" if is_oa else "Não",
        "keywords": keywords_str,
        "openalex_id": work.get("id", ""),
    }


def buscar_todos_works_por_query(query):
    """
    Busca todos os works para uma query específica com paginação.
    """
    todos_works = []

    for pagina in range(1, MAX_PAGINAS + 1):
        data = buscar_works(query, pagina)

        if data is None:
            break

        results = data.get("results", [])

        if not results:
            break

        for work in results:
            metadados = extrair_metadados(work)
            metadados["query_busca"] = query
            todos_works.append(metadados)

        print(f"  📄 Página {pagina}: {len(results)} papers")

        # Verificar se há mais páginas
        meta = data.get("meta", {})
        count = meta.get("count", 0)
        if pagina * PER_PAGE >= count:
            break

        time.sleep(TEMPO_ESPERA)

    return todos_works


def salvar_csv(dados, filepath):
    """
    Salva os resultados em arquivo CSV.
    """
    if not dados:
        print("⚠️ Nenhum dado para salvar!")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    campos = [
        "titulo",
        "autores",
        "ano",
        "periodico",
        "citacoes",
        "doi",
        "url",
        "open_access",
        "keywords",
        "query_busca",
        "openalex_id",
    ]

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

    print(f"\n💾 Resultados salvos em: {filepath}")


def main():
    """
    Função principal de extração.
    """
    print("=" * 60)
    print("EXTRATOR DE ARTIGOS ACADÊMICOS - OPENALEX")
    print("Revisão Sistemática: XAI no Setor Público")
    print("=" * 60)

    todos_resultados = []
    ids_unicos = set()

    print(f"\n📡 API: OpenAlex (openalex.org)")
    print(f"🔍 Queries: {len(QUERIES)} combinações")
    print(f"📊 Limite por query: {MAX_PAGINAS * PER_PAGE} papers")
    print(f"⏱️ Timeout: {TIMEOUT}s | Espera: {TEMPO_ESPERA}s")

    for i, query in enumerate(QUERIES, 1):
        print(f"\n{'─' * 50}")
        print(f"🔍 [{i}/{len(QUERIES)}] Query: {query}")
        print("─" * 50)

        works = buscar_todos_works_por_query(query)

        if works:
            for work in works:
                work_id = work.get("openalex_id", "")
                if work_id and work_id not in ids_unicos:
                    ids_unicos.add(work_id)
                    todos_resultados.append(work)
                elif not work_id:
                    todos_resultados.append(work)

            print(
                f"  ✅ Papers capturados: {len(works)} | Total único: {len(todos_resultados)}"
            )
        else:
            print(f"  ⚠️ Nenhum paper encontrado")

        if i < len(QUERIES):
            time.sleep(TEMPO_ESPERA * 2)

    print(f"\n📊 TOTAL DE REGISTROS ÚNICOS: {len(todos_resultados)}")

    if todos_resultados:
        print("\n📈 ESTATÍSTICAS:")

        anos = {}
        for item in todos_resultados:
            ano = item.get("ano", "Não informado")
            anos[ano] = anos.get(ano, 0) + 1

        print("\n  Publicações por Ano:")
        for ano, qtd in sorted(anos.items(), reverse=True)[:10]:
            print(f"    - {ano}: {qtd}")

        periodicos = {}
        for item in todos_resultados:
            per = item.get("periodico", "Não informado")
            if per:
                periodicos[per] = periodicos.get(per, 0) + 1

        print("\n  Top 5 Periódicos:")
        for per, qtd in sorted(periodicos.items(), key=lambda x: -x[1])[:5]:
            print(f"    - {per}: {qtd}")

        total_citacoes = sum(item.get("citacoes", 0) for item in todos_resultados)
        print(f"\n  Total de Citações: {total_citacoes}")

        # Top 3 mais citados
        top_citados = sorted(
            todos_resultados, key=lambda x: x.get("citacoes", 0), reverse=True
        )[:3]
        print("\n  Top 3 Artigos Mais Citados:")
        for idx, art in enumerate(top_citados, 1):
            print(
                f"    {idx}. {art.get('titulo', '')[:60]}... ({art.get('citacoes', 0)} citações)"
            )

    print(f"\n💾 Salvando {len(todos_resultados)} registros...")
    salvar_csv(todos_resultados, PASTA_DESTINO)

    json_path = PASTA_DESTINO.replace(".csv", "_backup.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(todos_resultados, f, ensure_ascii=False, indent=2)
    print(f"💾 Backup JSON: {json_path}")

    print("\n" + "=" * 60)
    print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"📁 Arquivo: {PASTA_DESTINO}")
    print("=" * 60)

    return todos_resultados


if __name__ == "__main__":
    main()
