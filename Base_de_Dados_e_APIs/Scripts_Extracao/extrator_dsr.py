#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Artigos Acadêmicos - DSR em Contabilidade Pública
API: OpenAlex

Objetivo: Extrair metadados de artigos sobre Design Science Research em contabilidade/administração pública

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

# Queries específicas para DSR + Contabilidade Pública
QUERIES = [
    '"Design Science Research" "public accounting"',
    '"Design Science Research" "public administration"',
    '"DSR" "public sector" accounting',
    '"Design Science" "government" accounting',
]

# Campos a solicitar
CAMPOS_BASE = "id,doi,title,authors,publication_year,primary_location,open_access,cited_by_count,keywords,concepts"

# Pagination
PER_PAGE = 25
MAX_PAGINAS = 4

# Rate limit
TEMPO_ESPERA = 1

# Timeout
TIMEOUT = 30

# Email
EMAIL = "pesquisador@ufsc.br"

# Pasta de destino
PASTA_DESTINO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Raw_Data",
    "Revisao_Sistematica",
    "dsr_public_accounting.csv",
)

# Termos para filtrar relevância
TERMOS_RELEVANTES = [
    "design",
    "science",
    "research",
    "accounting",
    "public",
    "administration",
    "government",
    "audit",
    "financial",
    "management",
    "information",
    "systems",
]

TERMOS_EXCLUIR = ["disease", "health", "medical", "clinical", "biology", "genetic"]


# ============================================
# FUNÇÕES
# ============================================


def filtrar_artigo_relevante(work):
    """
    Filtra artigos para garantir relevância ao tema DSR + Contabilidade Pública.
    """
    titulo = work.get("title", "") or ""
    keywords = work.get("keywords", [])
    keywords_str = " ".join([k.get("display_name", "").lower() for k in keywords])
    concepts = work.get("concepts", [])
    concepts_str = " ".join([c.get("display_name", "").lower() for c in concepts])

    texto_completo = titulo.lower() + " " + keywords_str + " " + concepts_str

    # Excluir falsos positivos
    for termo in TERMOS_EXCLUIR:
        if termo in texto_completo:
            return False

    # Verificar se tem termos de DSR
    termos_dsr = ["design science", "dsr", "design research", "artifact", "construct"]
    tem_dsr = any(t in texto_completo for t in termos_dsr)

    # Verificar se tem referência a administração pública/contabilidade
    termos_area = [
        "accounting",
        "public",
        "administration",
        "government",
        "audit",
        "financial",
        "management",
        "governance",
    ]
    tem_area = any(t in texto_completo for t in termos_area)

    if tem_dsr and tem_area:
        return True
    elif "design" in texto_completo and tem_area:
        return True

    return False

    # Verificar se tem termos de DSR
    termos_dsr = ["design science", "dsr", "design research", "artifact", "construct"]
    tem_dsr = any(t in texto_completo for t in termos_dsr)

    # Verificar se tem referência a administração pública/contabilidade
    termos_area = [
        "accounting",
        "public",
        "administration",
        "government",
        "audit",
        "financial",
        "management",
        "governance",
    ]
    tem_area = any(t in texto_completo for t in termos_area)

    if tem_dsr and tem_area:
        return True
    elif "design" in texto_completo and tem_area:
        return True

    return False


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

    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        return None


def extrair_metadados(work):
    """
    Extrai metadados relevantes de um work.
    """
    autores_lista = work.get("authorships", [])
    autores = "; ".join(
        [a.get("author", {}).get("display_name", "") for a in autores_lista[:5]]
    )
    if len(autores_lista) > 5:
        autores += f" et al. ({len(autores_lista)} autores)"

    doi = work.get("doi", "")
    url = work.get("doi", "")

    primary_location = work.get("primary_location", {})
    source = primary_location.get("source") if primary_location else None
    periodico = source.get("display_name", "") if source else ""

    oa = work.get("open_access", {})
    is_oa = "Sim" if oa.get("is_oa", False) else "Não"

    keywords = work.get("keywords", [])
    keywords_str = "; ".join([k.get("display_name", "") for k in keywords[:5]])

    concepts = work.get("concepts", [])
    concepts_str = "; ".join([c.get("display_name", "") for c in concepts[:3]])

    citacoes = work.get("cited_by_count", 0)

    return {
        "titulo": work.get("title", ""),
        "autores": autores,
        "ano": str(work.get("publication_year", "")),
        "periodico": periodico,
        "citacoes": citacoes,
        "doi": doi,
        "url": url,
        "open_access": is_oa,
        "keywords": keywords_str,
        "areas_tematicas": concepts_str,
        "openalex_id": work.get("id", ""),
    }


def buscar_todos_works_por_query(query):
    """
    Busca todos os works com filtragem.
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
            if filtrar_artigo_relevante(work):
                metadados = extrair_metadados(work)
                metadados["query_busca"] = query
                todos_works.append(metadados)

        print(
            f"  📄 Página {pagina}: {len(results)} encontrados, {len(todos_works)} relevantes até agora"
        )

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
        "areas_tematicas",
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
    Função principal.
    """
    print("=" * 60)
    print("EXTRATOR DSR - CONTABILIDADE PÚBLICA")
    print("=" * 60)

    todos_resultados = []
    ids_unicos = set()

    print(f"\n📡 API: OpenAlex")
    print(f"🔍 Queries: {len(QUERIES)} combinações")

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
                f"  ✅ Papers relevantes: {len(works)} | Total único: {len(todos_resultados)}"
            )

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
        for ano, qtd in sorted(anos.items(), reverse=True)[:8]:
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

    print(f"\n💾 Salvando {len(todos_resultados)} registros...")
    salvar_csv(todos_resultados, PASTA_DESTINO)

    print("\n" + "=" * 60)
    print("✅ EXTRAÇÃO CONCLUÍDA!")
    print("=" * 60)

    return todos_resultados


if __name__ == "__main__":
    main()
