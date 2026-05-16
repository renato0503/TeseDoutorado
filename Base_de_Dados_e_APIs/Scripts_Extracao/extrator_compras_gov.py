#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados de Compras - Portal de Dados Abertos do Governo
Tentativa via dados.gov.br

Autor: Renato de Oliveira Rosa
Data: Maio 2026
"""

import requests
import json
import time
import os
import csv

# ============================================
# CONFIGURAÇÕES
# ============================================

# Pasta de destino
PASTA_DESTINO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Raw_Data",
    "Artefato_Copiloto",
    "amostra_pncp_ti.json",
)

# Timeout
TIMEOUT = 30

# Rate limit
TEMPO_ESPERA = 2


def buscar_datasets_compras():
    """
    Busca datasets relacionados a compras públicas no dados.gov.br
    """
    url = "https://dados.gov.br/api/v3/datasets"

    params = {"q": "licitação", "sort": "relevance", "page_size": 10}

    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()

        datasets = data.get("datasets", [])

        print(f"📊 Encontrados {len(datasets)} datasets sobre licitações:")

        for ds in datasets:
            titulo = ds.get("title", "")
            url_ds = ds.get("url", "")
            print(f"  - {titulo}")
            print(f"    URL: {url_ds}")

        return datasets

    except Exception as e:
        print(f"❌ Erro ao buscar datasets: {e}")
        return []


def extrair_exemplo_dados():
    """
    Cria dados de exemplo para demonstrar a estrutura.
    Como as APIs não estão acessíveis diretamente, criamos uma estrutura
    de exemplo baseada na documentação do PNCP.
    """

    # Estrutura de exemplo baseada na API PNCP
    exemplo_contratacoes = [
        {
            "id": "2024-00001",
            "numero_processo": "00000.000000/2024-01",
            "objeto": "Contratação de serviços de desenvolvimento de software para sistema de gestão",
            "orgao": "Ministério da Gestão e da Inovação em Serviços Públicos",
            "unidade_compradora": "Secretária de Tecnologia da Informação",
            "modalidade": "Pregão Eletrônico",
            "situacao": "Encerrada",
            "valor_estimado": 1500000.00,
            "valor_total": 1450000.00,
            "data_publicacao": "2024-01-15",
            "data_inicio_vigencia": "2024-02-01",
            "data_fim_vigencia": "2025-02-01",
            "link_edital": "https://pncp.gov.br/edital/00000.000000/2024-01",
            "links_anexos": [
                {
                    "nome": "Edital",
                    "tipo": "PDF",
                    "url": "https://pncp.gov.br/anexos/edital.pdf",
                },
                {
                    "nome": "Termo de Referência",
                    "tipo": "PDF",
                    "url": "https://pncp.gov.br/anexos/tr.pdf",
                },
            ],
            "categoria": "TI - Desenvolvimento de Sistemas",
        },
        {
            "id": "2024-00002",
            "numero_processo": "00000.000000/2024-02",
            "objeto": "Contratação de serviços de computação em nuvem (Cloud Computing)",
            "orgao": "Controladoria-Geral da União",
            "unidade_compradora": "Secretaria de Tecnologia da Informação",
            "modalidade": "Pregão Eletrônico",
            "situacao": "Vigente",
            "valor_estimado": 2500000.00,
            "valor_total": None,
            "data_publicacao": "2024-02-10",
            "data_inicio_vigencia": "2024-03-01",
            "data_fim_vigencia": "2026-03-01",
            "link_edital": "https://pncp.gov.br/edital/00000.000000/2024-02",
            "links_anexos": [],
            "categoria": "TI - Cloud Computing",
        },
        {
            "id": "2024-00003",
            "numero_processo": "00000.000000/2024-03",
            "objeto": "Contratação de soluções de inteligência artificial para análise de dados",
            "orgao": "Ministério da Ciência, Tecnologia e Inovação",
            "unidade_compradora": "Instituto Nacional de Ciência e Tecnologia",
            "modalidade": "Concorrência",
            "situacao": "Encerrada",
            "valor_estimado": 800000.00,
            "valor_total": 750000.00,
            "data_publicacao": "2024-03-05",
            "data_inicio_vigencia": "2024-04-01",
            "data_fim_vigencia": "2025-04-01",
            "link_edital": "https://pncp.gov.br/edital/00000.000000/2024-03",
            "links_anexos": [],
            "categoria": "TI - Inteligência Artificial",
        },
    ]

    return exemplo_contratacoes


def main():
    """
    Função principal.
    """
    print("=" * 60)
    print("EXTRATOR DE DADOS DE COMPRAS PÚBLICAS")
    print("=" * 60)

    print("\n📡 Tentando acessar Portal de Dados Abertos (dados.gov.br)...")

    # Tentar buscar datasets
    datasets = buscar_datasets_compras()

    if datasets:
        print(f"\n✅ Encontrados {len(datasets)} datasets disponíveis")
        print("\n⚠️ Para extração completa, seria necessário:")
        print("  1. Registrar-se no PNCP para obter API Key")
        print("  2. Implementar autenticaçãoOAuth2")
        print("  3. Configurar rate limits específicos")
    else:
        print("\n⚠️ API de dados.gov.br requer análise adicional")

    print("\n📊 Gerando dados de exemplo com estrutura do PNCP...")

    # Gerar exemplo
    dados_exemplo = extrair_exemplo_dados()

    print(f"✅ Gerados {len(dados_exemplo)} registros de exemplo")

    # Estatísticas
    print("\n📈 ESTATÍSTICAS (DADOS DE EXEMPLO):")

    if dados_exemplo:
        # Por modalidade
        modalidades = {}
        for item in dados_exemplo:
            mod = item.get("modalidade", "Não informado")
            modalidades[mod] = modalidades.get(mod, 0) + 1

        print("\n  Modalidades:")
        for mod, qtd in modalidades.items():
            print(f"    - {mod}: {qtd}")

        # Por órgão
        orgaos = {}
        for item in dados_exemplo:
            org = item.get("orgao", "Não informado")
            orgaos[org] = orgaos.get(org, 0) + 1

        print("\  Orgãos:")
        for org, qtd in orgaos.items():
            print(f"    - {org[:40]}...: {qtd}")

    # Salvar
    os.makedirs(os.path.dirname(PASTA_DESTINO), exist_ok=True)
    with open(PASTA_DESTINO, "w", encoding="utf-8") as f:
        json.dump(dados_exemplo, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Dados de exemplo salvos em: {PASTA_DESTINO}")

    print("\n" + "=" * 60)
    print("⚠️ NOTA: Os dados acima são de EXEMPLO.")
    print("Para dados reais, é necessário:")
    print("  1. Obter API Key do PNCP (https://pncp.gov.br)")
    print("  2. Implementar autenticação")
    print("  3. Configurar extração via endpoint institucional")
    print("=" * 60)

    return dados_exemplo


if __name__ == "__main__":
    main()
