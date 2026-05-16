#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Editais do PNCP (Portal Nacional de Contratações Públicas)
Objetivo: Extrair editais de TI, Inovação e Tecnologia para o Copiloto Algorítmico

Autor: Renato de Oliveira Rosa
Data: Maio 2026
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# ============================================
# CONFIGURAÇÕES
# ============================================

# Palavras-chave para busca (TI, Inovação, Tecnologia)
PALAVRAS_CHAVE = [
    "inteligência artificial",
    "software",
    "inovação",
    "tecnologia da informação",
    "nuvem",
    "computação em nuvem",
    "machine learning",
    "desenvolvimento de sistemas",
    "soluções tecnológicas",
    "transformação digital",
]

# Data inicial: 01/01/2021 (vigência Nova Lei 14.133)
DATA_INICIAL = "2021-01-01"

# Pagination
TAMANHO_PAGINA = 20
MAX_PAGINAS = 50  # Limite de segurança por palavra-chave
MAX_RESULTADOS_POR_TERMO = 200

# Rate limit (PNCP permite ~100 req/min, usaremos 30 req/min para segurança)
TEMPO_ESPERA = 2  # segundos entre requisições

# Timeout
TIMEOUT = 30

# Pasta de destino
PASTA_DESTINO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Raw_Data",
    "Artefato_Copiloto",
    "amostra_pncp_ti.json",
)

# ============================================
# FUNÇÕES
# ============================================


def buscar_contratacoes_por_orgao(api_base, orgão_cnpj, palavra_chave, pagina=1):
    """
    Busca contratações de um órgão específico por palavra-chave.
    """
    url = f"{api_base}orgaos/{orgão_cnpj}/contratacoes"

    params = {
        "pagina": pagina,
        "tamanhoPagina": TAMANHO_PAGINA,
        "palavraChave": palavra_chave,
        "dataInicial": DATA_INICIAL,
        "status": "vigente",  # Apenas contratações vigentes/encerradas
    }

    response = None
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response and response.status_code == 404:
            return []
        if response:
            print(f"  ❌ Erro HTTP {response.status_code}: {e}")
        else:
            print(f"  ❌ Erro HTTP: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro na requisição: {e}")
        return None


def buscar_contratacoes_por_todos_orgaos(api_base, palavra_chave):
    """
    Busca contratações usando o endpoint de busca por órgãos.
    O PNCP não tem endpoint direto de busca global, então precisamos
    primeiro buscar órgãos e depois suas contratações.
    """
    resultados = []

    # Primeiro, buscar lista de órgãos (primeiros 20 para teste)
    url_orgaos = f"{api_base}orgaos"

    try:
        response = requests.get(url_orgaos, timeout=TIMEOUT)
        response.raise_for_status()
        orgaos_data = response.json()

        orgaos = orgaos_data.get("items", [])[:20]  # Primeiros 20 órgãos

        print(f"  📡 Encontrados {len(orgaos)} órgãos para buscar")

    except Exception as e:
        print(f"  ❌ Erro ao buscar órgãos: {e}")
        return resultados

    # Para cada órgão, buscar contratações
    for orgao in orgaos:
        cnpj = orgao.get("cpfCnpj", "")
        nome_orgao = orgao.get("nome", "")

        url = f"{api_base}orgaos/{cnpj}/contratacoes"

        params = {
            "pagina": 1,
            "tamanhoPagina": TAMANHO_PAGINA,
            "palavraChave": palavra_chave,
        }

        try:
            response = requests.get(url, params=params, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])
            if items:
                print(f"    ✅ {nome_orgao[:30]}: {len(items)} contratações")
                resultados.extend(items)

                # Verificar limite
                if len(resultados) >= MAX_RESULTADOS_POR_TERMO:
                    print(f"  ⚠️ Limite de {MAX_RESULTADOS_POR_TERMO} atingido")
                    break

            time.sleep(TEMPO_ESPERA)

        except requests.exceptions.HTTPError as e:
            if response.status_code != 404:
                print(f"    ⚠️ Erro em {nome_orgao[:30]}: {response.status_code}")
            continue
        except Exception as e:
            continue

    return resultados


def extrair_dados_importantes(contratacao):
    """
    Extrai campos relevantes de uma contratação.
    """
    resultado = {
        "id": contratacao.get("id", ""),
        "numero_processo": contratacao.get("numeroProcesso", ""),
        "objeto": contratacao.get("objeto", ""),
        "orgao": None,
        "unidade_compradora": None,
        "modalidade": None,
        "situacao": None,
        "valor_estimado": None,
        "valor_total": None,
        "data_publicacao": None,
        "data_inicio_vigencia": None,
        "data_fim_vigencia": None,
        "link_edital": None,
        "links_anexos": [],
    }

    # Informações do órgão
    orgao = contratacao.get("orgao", {})
    if orgao:
        resultado["orgao"] = orgao.get("nome", "")

    # Unidade compradora
    unidade = contratacao.get("unidadeCompradora", {})
    if unidade:
        resultado["unidade_compradora"] = unidade.get("nome", "")

    # Modalidade
    modalidade = contratacao.get("modalidade", {})
    if modalidade:
        resultado["modalidade"] = modalidade.get("nome", "")

    # Situação
    situacao = contratacao.get("situacao", {})
    if situacao:
        resultado["situacao"] = situacao.get("descricao", "")

    # Valores
    valor_estimado = contratacao.get("valorEstimado")
    if valor_estimado:
        resultado["valor_estimado"] = valor_estimado

    valor_total = contratacao.get("valorTotal")
    if valor_total:
        resultado["valor_total"] = valor_total

    # Datas
    resultado["data_publicacao"] = contratacao.get("dataPublicacao", "")
    resultado["data_inicio_vigencia"] = contratacao.get("dataInicioVigencia", "")
    resultado["data_fim_vigencia"] = contratacao.get("dataFimVigencia", "")

    # Links
    resultado["link_edital"] = contratacao.get("linkEdital", "")

    # Anexos
    anexos = contratacao.get("anexos", [])
    for anexo in anexos:
        resultado["links_anexos"].append(
            {
                "nome": anexo.get("nome", ""),
                "tipo": anexo.get("tipo", ""),
                "url": anexo.get("url", ""),
            }
        )

    return resultado


def filtrar_por_tema(dados):
    """
    Filtra registros que contenham termos relacionados a TI/Inovação.
    """
    termos_ti = [
        "software",
        "sistema",
        "informação",
        "tecnologia",
        "digital",
        "inteligência",
        "artificial",
        "dados",
        "nuvem",
        "cloud",
        "ti",
        "desenvolvimento",
        "manutenção",
        "infraestrutura",
        "segurança",
        "machine learning",
        "ia",
        "bi",
        "erp",
        "crm",
        "api",
    ]

    filtrados = []
    for item in dados:
        objeto = item.get("objeto", "").lower()

        # Verificar se o objeto contém termos de TI/Inovação
        if any(termo in objeto for termo in termos_ti):
            filtrados.append(item)

    return filtrados


def salvar_resultados(dados, filepath):
    """
    Salva os resultados em arquivo JSON.
    """
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Resultados salvos em: {filepath}")


def main():
    """
    Função principal de extração.
    """
    print("=" * 60)
    print("EXTRATOR DE EDITAIS DO PNCP")
    print("Objetivo: Compilar editais de TI, Inovação e Tecnologia")
    print("=" * 60)

    # API Base do PNCP
    API_BASE = "https://pncp.gov.br/api/v1/"

    # Lista para armazenar todos os resultados
    todos_resultados = []
    resultados_unicos = {}  # Dicionário para evitar duplicatas por ID

    print(f"\n📡 API Base: {API_BASE}")
    print(f"📅 Período: {DATA_INICIAL} até hoje")
    print(f"🔑 Palavras-chave: {len(PALAVRAS_CHAVE)} termos")
    print(f"⏱️ Timeout: {TIMEOUT}s | Espera: {TEMPO_ESPERA}s")

    # Iterar sobre cada palavra-chave
    for i, palavra in enumerate(PALAVRAS_CHAVE, 1):
        print(f"\n{'─' * 50}")
        print(f"🔍 [{i}/{len(PALAVRAS_CHAVE)}] Buscando: '{palavra}'")
        print("─" * 50)

        resultados = buscar_contratacoes_por_todos_orgaos(API_BASE, palavra)

        if resultados:
            # Processar cada resultado
            for r in resultados:
                item = extrair_dados_importantes(r)

                # Usar ID como chave única
                item_id = item["id"]
                if item_id and item_id not in resultados_unicos:
                    resultados_unicos[item_id] = item

            print(
                f"  ✅ Total capturado: {len(resultados)} | Total único: {len(resultados_unicos)}"
            )
        else:
            print(f"  ⚠️ Nenhum resultado encontrado")

        # Pausa entre palavras-chave (maior para evitar rate limit)
        if i < len(PALAVRAS_CHAVE):
            time.sleep(TEMPO_ESPERA * 2)

    # Converter para lista
    todos_resultados = list(resultados_unicos.values())

    # Filtrar por tema (TI/Inovação)
    print(f"\n📊 Processando {len(todos_resultados)} registros únicos...")
    resultados_filtrados = filtrar_por_tema(todos_resultados)

    print(f"✅ Registros filtrados (TI/Inovação): {len(resultados_filtrados)}")

    # Estatísticas
    if resultados_filtrados:
        print("\n📈 ESTATÍSTICAS:")

        # Por modalidade
        modalidades = {}
        for item in resultados_filtrados:
            mod = item.get("modalidade", "Não informado")
            modalidades[mod] = modalidades.get(mod, 0) + 1

        print("\n  Modalidades:")
        for mod, qtd in sorted(modalidades.items(), key=lambda x: -x[1]):
            print(f"    - {mod}: {qtd}")

        # Por situação
        situacoes = {}
        for item in resultados_filtrados:
            sit = item.get("situacao", "Não informado")
            situacoes[sit] = situacoes.get(sit, 0) + 1

        print("\n  Situações:")
        for sit, qtd in sorted(situacoes.items(), key=lambda x: -x[1]):
            print(f"    - {sit}: {qtd}")

    # Salvar resultados
    print(f"\n💾 Salvando {len(resultados_filtrados)} registros...")
    salvar_resultados(resultados_filtrados, PASTA_DESTINO)

    print("\n" + "=" * 60)
    print("✅ EXTRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"📁 Arquivo: {PASTA_DESTINO}")
    print("=" * 60)

    return resultados_filtrados


if __name__ == "__main__":
    main()
