#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder do Fichamento Curado dos Artigos de Congresso.

Metodologia (31/07/2026):
1. Lista-mestra curada de obras REAIS (classicos + recentes de alto impacto),
   organizada por tema/sprint (JSON em curadoria/bloco_*.json).
2. Validacao de cada DOI no Crossref:
   - lookup direto (api.crossref.org/works/{doi})
   - se 404, busca bibliografica (query.bibliographic) para recuperar DOI real
3. Correcao de metadados (titulo, autores, ano, periodico) pela fonte oficial.
4. Preenchimento dos campos analiticos (resumo, objetivos, metodologia,
   resultados, posicao academica, paradigma, achados, relacao_artigo) ja
   curados nos JSON (sintese fiel do conteudo real de cada obra).
5. Geracao do fichamento_congressos.csv final.

Autor: Renato de Oliveira Rosa
"""

import csv
import json
import os
import re
import sys
import time
import unicodedata

import requests

# ============================================
# CONFIGURACOES
# ============================================

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURADORIA_DIR = os.path.join(RAIZ, "curadoria")
OUT_CSV = os.path.join(RAIZ, "fichamento_congressos.csv")
EMAIL = "renatooliveirarosa@gmail.com"
TIMEOUT = 30
TEMPO_ESPERA = 1.2

SCHEMA = [
    "id", "tema", "autores", "ano", "titulo", "journal", "doi", "base_dados",
    "citacoes", "categoria", "palavras_chave", "resumo", "objetivos",
    "metodologia", "resultados", "posicao_academica", "paradigma",
    "principais_achados", "relacao_artigo", "status",
]


def normalizar_doi(doi):
    if not doi:
        return ""
    doi = doi.strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi.strip()


def crossref_por_doi(doi):
    """Valida DOI e retorna metadados oficiais do Crossref."""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        r = requests.get(url, params={"mailto": EMAIL}, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json().get("message", {})
        return None
    except requests.exceptions.RequestException:
        return None


def crossref_por_busca(titulo, autores_hint=""):
    """Busca bibliografica no Crossref para recuperar o DOI real."""
    url = "https://api.crossref.org/works"
    params = {
        "query.bibliographic": f"{titulo} {autores_hint}",
        "rows": 3,
        "mailto": EMAIL,
        "select": "DOI,title,author,issued,container-title",
    }
    try:
        r = requests.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        items = r.json().get("message", {}).get("items", [])
        return items
    except requests.exceptions.RequestException:
        return []


def extrair_metadados_crossref(msg):
    """Converte message do Crossref em metadados padronizados."""
    titulo = (msg.get("title") or [""])[0] if msg.get("title") else ""
    autores = []
    for a in msg.get("author", [])[:12]:
        autores.append(f"{a.get('family','')}, {a.get('given','')}".strip(", "))
    if not autores:
        contrib = msg.get("contributor", [])
        for a in contrib[:12]:
            autores.append(f"{a.get('family','')}, {a.get('given','')}".strip(", "))
    ano = ""
    dp = (msg.get("issued") or {}).get("date-parts", [[None]])
    if dp and dp[0]:
        ano = str(dp[0][0] or "")
    periodico = (msg.get("container-title") or [""])[0] if msg.get("container-title") else ""
    if not periodico:
        periodico = "Livro"
    return {
        "titulo": titulo,
        "autores": autores,
        "ano": ano,
        "periodico": periodico,
        "doi": msg.get("DOI", ""),
    }


import difflib


def normalizar_titulo(t):
    """Normaliza titulo para comparacao (minusculas, sem pontuacao/acentos)."""
    if not t:
        return ""
    t = t.lower()
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def similaridade_titulo(t1, t2):
    """Ratio de similaridade entre dois titulos normalizados."""
    a = normalizar_titulo(t1)
    b = normalizar_titulo(t2)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def validar_obra(obra):
    """Valida uma obra curada contra o Crossref por CORRESPONDENCIA DE TITULO.

    Regra (metodologia do projeto Itau):
    - Só aceita o DOI se o titulo retornado pelo Crossref tiver alta similaridade
      com o titulo curado (>= 0.62).
    - Se o DOI fornecido nao bater, tenta busca bibliografica pelo titulo curado
      e adota o melhor candidato que tambem bata no titulo.
    - Se nada bater, preserva os metadados CURADOS (fonte confiavel) e marca
      base_dados como 'Referencia (sem DOI confirmado)'.

    Retorna dict com metadados finais.
    """
    from difflib import SequenceMatcher

    titulo_curado = obra.get("titulo", "")
    doi_fornecido = normalizar_doi(obra.get("doi", ""))
    base = "Referencia (sem DOI confirmado)"
    meta = None
    melhor_ratio = 0.0

    def aceitar_candidato(msg):
        """Adota msg se o titulo bater com o curado."""
        nonlocal meta, base, melhor_ratio
        meta_candidato = extrair_metadados_crossref(msg)
        ratio = similaridade_titulo(titulo_curado, meta_candidato.get("titulo", ""))
        if ratio >= 0.62 and ratio > melhor_ratio:
            melhor_ratio = ratio
            meta_candidato["_ratio"] = ratio
            meta = meta_candidato
            meta["doi"] = normalizar_doi(msg.get("DOI", ""))
            base = "Crossref (titulo confirmado)"

    # 1) Lookup direto do DOI fornecido
    if doi_fornecido:
        msg = crossref_por_doi(doi_fornecido)
        if msg:
            aceitar_candidato(msg)
            if melhor_ratio >= 0.62:
                pass  # ja confirmado
            else:
                # DOI fornecido errado: tenta busca bibliografica
                time.sleep(TEMPO_ESPERA)
                itens = crossref_por_busca(titulo_curado, obra.get("autores", ""))
                for it in itens:
                    aceitar_candidato(it)
        else:
            # DOI inexistente: busca bibliografica
            time.sleep(TEMPO_ESPERA)
            itens = crossref_por_busca(titulo_curado, obra.get("autores", ""))
            for it in itens:
                aceitar_candidato(it)

    # 2) Sem DOI fornecido: busca bibliografica
    else:
        time.sleep(TEMPO_ESPERA)
        itens = crossref_por_busca(titulo_curado, obra.get("autores", ""))
        for it in itens:
            aceitar_candidato(it)

    if meta:
        obra["doi"] = meta.get("doi", "")
        obra["base_dados"] = base
        obra["titulo"] = meta["titulo"]
        if meta.get("ano"):
            obra["ano"] = meta["ano"]
        if meta.get("periodico") and meta.get("periodico") != "Livro":
            obra["journal"] = meta["periodico"]
        if meta.get("autores"):
            obra["autores"] = meta["autores"]
    else:
        obra["doi"] = ""
        obra["base_dados"] = base

    # Categoria derivada do ANO real (meta: 70% recentes 2018+, 30% classicos)
    try:
        ano_int = int(obra.get("ano", 0))
        obra["categoria"] = "recente" if ano_int >= 2018 else "classico"
    except (TypeError, ValueError):
        obra["categoria"] = obra.get("categoria", "recente")

    return obra


def gravar_csv(obras):
    """Grava o CSV final."""
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True) if os.path.dirname(OUT_CSV) else None
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEMA, delimiter=";")
        writer.writeheader()
        for obra in obras:
            row = {campo: obra.get(campo, "") for campo in SCHEMA}
            if isinstance(row["autores"], list):
                row["autores"] = "; ".join(row["autores"])
            writer.writerow(row)
    print(f"CSV final: {OUT_CSV} ({len(obras)} obras)")


def carregar_curadoria():
    """Carrega todos os JSONs de curadoria em ordem de bloco."""
    blocos = ["bloco_a.json", "bloco_b.json", "bloco_c.json", "bloco_d.json"]
    obras = []
    for nome in blocos:
        path = os.path.join(CURADORIA_DIR, nome)
        if not os.path.exists(path):
            print(f"[!] Bloco ausente: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            obras.extend(json.load(f))
    return obras


def main():
    obras = carregar_curadoria()
    print(f"Obras curadas carregadas: {len(obras)}")

    validas = 0
    sem_doi = 0
    for i, obra in enumerate(obras, 1):
        antes = obra.get("doi", "")
        obra = validar_obra(obra)
        status_doi = "OK" if obra.get("doi") else "SEM DOI"
        if obra.get("doi"):
            validas += 1
        else:
            sem_doi += 1
        print(f"[{i}/{len(obras)}] {status_doi:7s} | {obra.get('ano','')} | "
              f"{obra.get('titulo','')[:55]}")
        if i % 5 == 0:
            time.sleep(TEMPO_ESPERA)

    gravar_csv(obras)
    print(f"\nDOIs validados: {validas} | Sem DOI: {sem_doi} | Total: {len(obras)}")


if __name__ == "__main__":
    main()
