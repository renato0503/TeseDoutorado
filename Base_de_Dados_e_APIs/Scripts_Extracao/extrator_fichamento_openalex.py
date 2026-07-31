#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Artigos Academicos - Banco de Fichamento dos Artigos de Congresso
API: OpenAlex (gratuita, sem chave; recomenda-se mailto para maior rate limit)

Autor: Renato de Oliveira Rosa
Data: 31/07/2026

Uso:
    python extrator_fichamento_openalex.py [--tema ID|ALL] [--max-por-tema N] [--out arquivo.csv]

As queries por tema vem de revisao_literatura.md (raiz do projeto).
O resultado e um CSV com o schema de fichamento_congressos.csv (metadados preenchidos,
campos qualitativos deixados em branco para fichamento manual).
"""

import argparse
import csv
import json
import os
import sys
import time

import requests

# ============================================
# CONFIGURACOES
# ============================================

EMAIL = "renato.pesquisa@exemplo.com"  # trocar por email real do pesquisador

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(RAIZ, "fichamento_congressos.csv")

CAMPOS_BASE = (
    "id,doi,title,authorships,publication_year,primary_location,"
    "cited_by_count,keywords,abstract_inverted_index,open_access,type"
)
PER_PAGE = 25
TIMEOUT = 30
TEMPO_ESPERA = 1

# Lista de (tema, [queries EN/PT]).
# Sincronizada com revisao_literatura.md (15 sprints).
TEMAS = [
    ("Sprint 1 - Compras Publicas Complexas", [
        '("complex public procurement" OR "procurement complexity" OR "complex contracting") AND (government OR "public sector")',
        '("public procurement" AND complexity) AND (typology OR framework OR definition)',
    ]),
    ("Sprint 2 - Public Procurement of Innovation (PPI)", [
        '"public procurement of innovation" AND (policy OR demand-side OR instruments)',
        '(procurement AND innovation) AND (mission-oriented OR pre-commercial OR PCP)',
    ]),
    ("Sprint 3 - Estado Empreendedor / Mission-Oriented", [
        '("entrepreneurial state" OR "mission-oriented innovation" OR "mission economy") AND (public OR state OR government)',
        '"public procurement" AND ("market creation" OR "demand-side innovation policy")',
    ]),
    ("Sprint 4 - Economia dos Custos de Transacao (TCE)", [
        '("transaction cost economics" OR "transaction cost") AND ("public procurement" OR "government contracting")',
        '(Williamson OR Coase) AND (contract OR governance OR "asset specificity")',
    ]),
    ("Sprint 5 - Teoria da Agencia em Compras Publicas", [
        '("agency theory" OR "principal-agent") AND ("public procurement" OR "public contracting" OR outsourcing)',
        '"agency costs" AND (government OR "public sector") AND (contract OR outsourcing)',
    ]),
    ("Sprint 6 - Isomorfismo Institucional", [
        '("institutional isomorphism" OR "mimetic isomorphism" OR "new institutionalism") AND (public OR government)',
        '"institutional theory" AND ("public procurement" OR "public administration")',
    ]),
    ("Sprint 7 - Paralisia Decisoria / Medo", [
        '("bureaucratic paralysis" OR "decision paralysis" OR "fear of accountability") AND (public OR government OR procurement)',
        '("chilling effect" OR "fear of blame" OR "risk aversion") AND ("public manager" OR "public procurement")',
    ]),
    ("Sprint 8 - Washing (Green/CSR/Impact/Innovation)", [
        '("greenwashing" OR "csr-washing" OR "impact washing" OR "innovation washing") AND (institutional OR legitimacy OR rhetoric)',
        '"washing" AND ("public procurement" OR government OR "public sector")',
    ]),
    ("Sprint 9 - Framing Analysis e Midia", [
        '("framing theory" OR "media framing") AND (technology OR algorithms OR "artificial intelligence")',
        '"agenda-setting" AND ("public sector" OR government OR policy)',
    ]),
    ("Sprint 10 - Legitimidade Organizacional e Sociotecnica", [
        '("organizational legitimacy" OR "legitimacy theory") AND ("artificial intelligence" OR algorithm OR automation)',
        '"legitimacy" AND ("public administration" OR government) AND (technology OR digital)',
    ]),
    ("Sprint 11 - Governanca Algoritmica", [
        '("algorithmic governance" OR "algorithmic accountability") AND (government OR "public sector" OR "public administration")',
        '("governance of algorithms" OR "AI governance") AND (public OR state)',
    ]),
    ("Sprint 12 - Aceitacao de Algoritmos", [
        '("algorithm aversion" OR "algorithm appreciation") AND (decision OR public OR government)',
        '("acceptance of AI" OR "trust in algorithms") AND ("public sector" OR government)',
    ]),
    ("Sprint 13 - XAI / Explicabilidade", [
        '("explainable AI" OR XAI) AND (government OR "public sector" OR "public administration")',
        '(SHAP OR LIME OR "counterfactual explanations") AND ("decision support" OR accountability)',
    ]),
    ("Sprint 14 - IA e NLP em Compras Publicas", [
        '("artificial intelligence" OR "machine learning" OR NLP) AND ("public procurement")',
        '("e-procurement" OR "procurement automation") AND (AI OR algorithm OR "text mining")',
    ]),
    ("Sprint 15 - Design Science Research (DSR)", [
        '("design science research" OR DSR) AND (methodology OR evaluation OR artifacts)',
        '"design science" AND ("public administration" OR "public accounting" OR "public sector")',
    ]),
]

SCHEMA = [
    "id", "tema", "autores", "ano", "titulo", "journal", "doi", "base_dados",
    "citacoes", "categoria", "palavras_chave", "resumo", "objetivos",
    "metodologia", "resultados", "posicao_academica", "paradigma",
    "principais_achados", "relacao_artigo", "status",
]


def reconstruir_abstract(inverted_index):
    """Reconstroi o texto do abstract a partir do inverted_index do OpenAlex."""
    if not inverted_index:
        return ""
    posicoes = []
    for palavra, indices in inverted_index.items():
        for idx in indices:
            posicoes.append((idx, palavra))
    posicoes.sort(key=lambda x: x[0])
    return " ".join(p for _, p in posicoes)


def buscar_works_crossref(query, rows=25, recentes=False, tentativas=3):
    """Busca works na API Crossref (gratuita, sem orcamento diario).

    Usado como fallback quando o OpenAlex retorna 429 (budget esgotado).
    Crossref nao fornece abstract/keywords: campos qualitativos ficam vazios.
    """
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": rows,
        "mailto": EMAIL,
        "select": "DOI,title,author,issued,container-title,is-referenced-by-count,type",
    }
    if recentes:
        params["filter"] = "from-pub-date:2018-01-01"
    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json().get("message", {}).get("items", [])
        except requests.exceptions.HTTPError as e:
            if r.status_code == 429:
                espera = min(30, 5 * 2 ** (tentativa - 1))
                print(f"  [!] Crossref 429. Aguardando {espera}s...")
                time.sleep(espera)
                continue
            print(f"  [!] Crossref erro HTTP {r.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  [!] Crossref erro de rede: {e}")
            return None
    return None


def extrair_metadados_crossref(work):
    """Extrai metadados de um work Crossref no schema do fichamento."""
    autores = []
    for a in work.get("author", [])[:8]:
        nome = f"{a.get('family','')}, {a.get('given','')}".strip(", ")
        autores.append(nome)
    autores_str = "; ".join(autores)

    year = ""
    dp = (work.get("issued") or {}).get("date-parts", [[None]])
    if dp and dp[0]:
        year = str(dp[0][0] or "")

    journal = (work.get("container-title") or [""])[0] if work.get("container-title") else ""
    if not journal and work.get("type") == "book-chapter":
        journal = "Capítulo de livro"

    return {
        "id": "",
        "tema": "",
        "autores": autores_str,
        "ano": year,
        "titulo": (work.get("title") or [""])[0] if work.get("title") else "",
        "journal": journal,
        "doi": work.get("DOI", ""),
        "base_dados": "Crossref",
        "citacoes": work.get("is-referenced-by-count", 0),
        "categoria": "",
        "palavras_chave": "",
        "resumo": "",
        "objetivos": "",
        "metodologia": "",
        "resultados": "",
        "posicao_academica": "",
        "paradigma": "",
        "principais_achados": "",
        "relacao_artigo": "",
        "status": "pendente",
    }


def buscar_works(query, pagina=1, recentes=False, tentativas=5):
    """Busca works no OpenAlex. Se recentes=True, filtra a partir de 2018.

    A API do OpenAlex agora opera com orcamento diario (gratuito resetando a
    meia-noite UTC). Em caso de 429 (budget esgotado), aplica backoff
    exponencial e tenta novamente ate 'tentativas'.
    """
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"default.search:{query}",
        "per_page": PER_PAGE,
        "page": pagina,
        "mailto": EMAIL,
        "sort": "cited_by_count:desc",
    }
    if recentes:
        params["filter"] += ",from_publication_date:2018-01-01"
    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.HTTPError as e:
            if r.status_code == 429:
                espera = min(60, 5 * 2 ** (tentativa - 1))
                print(f"  [!] 429 rate limit (budget diario). Aguardando {espera}s "
                      f"(tentativa {tentativa}/{tentativas})...")
                time.sleep(espera)
                continue
            print(f"  [!] Erro HTTP {r.status_code}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  [!] Erro de rede: {e}")
            return None
    print("  [!] Budget diario do OpenAlex esgotado. Tente novamente apos a "
          "meia-noite UTC ou use outra base (Scopus/WoS/Google Scholar).")
    return None


def extrair_metadados(work):
    """Extrai metadados de um work no schema do fichamento."""
    autores_lista = work.get("authorships", [])
    autores = "; ".join(
        [a.get("author", {}).get("display_name", "") for a in autores_lista[:8]]
    )
    if len(autores_lista) > 8:
        autores += f" et al. ({len(autores_lista)} autores)"

    primary_location = work.get("primary_location", {}) or {}
    source = primary_location.get("source") or {}
    journal = source.get("display_name", "")

    keywords = work.get("keywords", [])
    keywords_str = "; ".join(k.get("display_name", "") for k in keywords[:8])

    return {
        "id": "",
        "tema": "",
        "autores": autores,
        "ano": str(work.get("publication_year", "")),
        "titulo": work.get("title", ""),
        "journal": journal,
        "doi": (work.get("doi") or "").replace("https://doi.org/", ""),
        "base_dados": "OpenAlex",
        "citacoes": work.get("cited_by_count", 0),
        "categoria": "",
        "palavras_chave": keywords_str,
        "resumo": reconstruir_abstract(work.get("abstract_inverted_index")),
        "objetivos": "",
        "metodologia": "",
        "resultados": "",
        "posicao_academica": "",
        "paradigma": "",
        "principais_achados": "",
        "relacao_artigo": "",
        "status": "pendente",
    }


def carregar_existentes(out):
    """Carrega DOIs ja presentes no CSV para evitar duplicacao."""
    existentes = set()
    if os.path.exists(out):
        with open(out, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f, delimiter=";"):
                doi = (row.get("doi") or "").strip().lower()
                if doi:
                    existentes.add(doi)
    return existentes


def salvar(out, linhas):
    """Salva as linhas em CSV (append se o arquivo ja existe)."""
    nova = not os.path.exists(out)
    with open(out, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA, delimiter=";")
        if nova:
            writer.writeheader()
        for linha in linhas:
            writer.writerow({campo: linha.get(campo, "") for campo in SCHEMA})


def rodar_tema(nome, queries, out, max_por_tema, recentes=False, fonte="auto"):
    """Executa todas as queries de um tema e grava no CSV.

    fonte='auto' tenta OpenAlex; se retornar 429 persistente, cai para Crossref.
    """
    existentes = carregar_existentes(out)
    novas_linhas = []
    vistos_por_tema = set()
    usar_crossref = fonte == "crossref"

    print(f"\n=== {nome} ===")
    for query in queries:
        if usar_crossref:
            works = buscar_works_crossref(query, rows=min(PER_PAGE, max_por_tema), recentes=recentes)
            resultados = works or []
            for work in resultados:
                if len(vistos_por_tema) >= max_por_tema:
                    break
                doi = (work.get("DOI") or "").lower()
                if doi and (doi in existentes or doi in vistos_por_tema):
                    continue
                meta = extrair_metadados_crossref(work)
                meta["id"] = f"{nome.split(' - ')[0].lower().replace(' ', '_')}_{len(vistos_por_tema)+1}"
                meta["tema"] = nome
                meta["categoria"] = "recente" if recentes else "classico"
                if doi:
                    vistos_por_tema.add(doi)
                novas_linhas.append(meta)
            time.sleep(TEMPO_ESPERA * 2)
            continue

        for pagina in range(1, 4):  # max 3 paginas por query (75 registros)
            data = buscar_works(query, pagina, recentes=recentes)
            if data is None:
                usar_crossref = True
                break
            results = data.get("results", [])
            if not results:
                break
            for work in results:
                if len(vistos_por_tema) >= max_por_tema:
                    break
                doi = (work.get("doi") or "").replace("https://doi.org/", "").lower()
                if doi and (doi in existentes or doi in vistos_por_tema):
                    continue
                meta = extrair_metadados(work)
                meta["id"] = f"{nome.split(' - ')[0].lower().replace(' ', '_')}_{len(vistos_por_tema)+1}"
                meta["tema"] = nome
                if recentes:
                    meta["categoria"] = "recente"
                else:
                    meta["categoria"] = "classico"
                if doi:
                    vistos_por_tema.add(doi)
                novas_linhas.append(meta)
            if pagina * PER_PAGE >= data.get("meta", {}).get("count", 0):
                break
            time.sleep(TEMPO_ESPERA)
        time.sleep(TEMPO_ESPERA * 2)
        if usar_crossref:
            print("  [*] OpenAlex indisponivel (budget). Alternando para Crossref.")
            break

    salvar(out, novas_linhas)
    print(f"  -> {len(novas_linhas)} novos registros gravados.")
    return novas_linhas


def main():
    parser = argparse.ArgumentParser(description="Extrator OpenAlex - fichamento congressos")
    parser.add_argument("--tema", default="ALL", help="ID do sprint (ex.: 'Sprint 1') ou ALL")
    parser.add_argument("--max-por-tema", type=int, default=25,
                        help="Maximo de registros novos por tema")
    parser.add_argument("--fonte", default="auto",
                        help="auto (OpenAlex com fallback Crossref) | crossref | openalex")
    parser.add_argument("--out", default=DEFAULT_OUT, help="CSV de destino")
    args = parser.parse_args()

    temas_alvo = TEMAS
    if args.tema != "ALL":
        alvo = args.tema.lower()
        temas_alvo = [t for t in TEMAS if t[0].lower() == alvo or t[0].lower().startswith(alvo)]
        if not temas_alvo:
            print(f"[!] Tema '{args.tema}' nao encontrado.")
            sys.exit(1)

    for nome, queries in temas_alvo:
        rodar_tema(nome, queries, args.out, args.max_por_tema, recentes=True, fonte=args.fonte)
        # complementa com classicos (sem filtro de ano) se necessario
        rodar_tema(nome + " (classicos)", queries, args.out,
                   max(1, args.max_por_tema // 3), recentes=False, fonte=args.fonte)

    print("\nConcluido. Fichar manualmente os campos qualitativos no CSV.")


if __name__ == "__main__":
    main()
