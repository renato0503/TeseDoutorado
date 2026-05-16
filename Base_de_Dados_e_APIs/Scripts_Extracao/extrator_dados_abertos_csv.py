#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de Dados Abertos do Governo - Downloads de Dumps
Objetivo: Baixar arquivos massivos de licitações do Portal de Dados Abertos

Autor: Renato de Oliveira Rosa
Data: Maio 2026
"""

import requests
import os
import zipfile
import io
from datetime import datetime, timedelta
import time

# ============================================
# CONFIGURAÇÕES
# ============================================

# URLs base do Portal de Dados Abertos
BASE_URL = "http://arquivos.portaldatransparencia.gov.br/downloads.asp"

# Pasta de destino
PASTA_DESTINO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "Raw_Data", "Dados_Abertos"
)

# Período para download (últimos 12 meses)
MESES_ANTERIORES = 12


# ============================================
# FUNÇÕES
# ============================================


def get_available_files():
    """
    Verifica quais arquivos estão disponíveis no Portal de Dados Abertos.
    """
    # Estrutura Known de arquivos do Portal da Transparência
    arquivos_disponiveis = [
        {"nome": "licitacoes", "codigo": "licitacoes", "descricao": "Licitações"},
        {"nome": "contratos", "codigo": "contratos", "descricao": "Contratos"},
        {"nome": "empenhos", "codigo": "empenhos", "descricao": "Empenhos"},
        {"nome": "fornecedores", "codigo": "fornecedores", "descricao": "Fornecedores"},
    ]

    return arquivos_disponponiveis


def gerar_urls_download(arquivo_codigo, ano_inicio=2023, ano_fim=2025):
    """
    Gera URLs de download para cada mês do período.
    """
    urls = []

    for ano in range(ano_inicio, ano_fim + 1):
        for mes in range(1, 13):
            # Formato: http://arquivos.portaldatransparencia.gov.br/downloads/2024-01/Licitacoes-2024-01.zip
            url = f"http://arquivos.portaldatransparencia.gov.br/downloads/{ano}-{mes:02d}/{arquivo_codigo}-{ano}-{mes:02d}.zip"
            urls.append(
                {
                    "url": url,
                    "ano": ano,
                    "mes": mes,
                    "nome_arquivo": f"{arquivo_codigo}-{ano}-{mes:02d}.zip",
                }
            )

    return urls


def download_file(url, pasta_destino, nome_arquivo, timeout=60):
    """
    Faz o download de um arquivo.
    """
    try:
        print(f"  📥 Baixando: {nome_arquivo}...")

        response = requests.get(url, timeout=timeout, stream=True)

        if response.status_code == 200:
            caminho_zip = os.path.join(pasta_destino, nome_arquivo)

            with open(caminho_zip, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(
                f"  ✅ Salvo: {nome_arquivo} ({response.headers.get('content-length', '?')} bytes)"
            )
            return caminho_zip

        elif response.status_code == 404:
            print(f"  ⚠️ Não encontrado: {nome_arquivo}")
            return None
        else:
            print(f"  ❌ Erro {response.status_code}: {nome_arquivo}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erro: {e}")
        return None


def extract_zip(caminho_zip, pasta_destino):
    """
    Extrai o conteúdo de um arquivo ZIP.
    """
    if not caminho_zip or not os.path.exists(caminho_zip):
        return []

    arquivos_extraidos = []

    try:
        with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
            for membro in zip_ref.namelist():
                if membro.endswith(".csv"):
                    extrair_para = os.path.join(pasta_destino, os.path.basename(membro))
                    zip_ref.extract(membro, pasta_destino)
                    arquivos_extraidos.append(extrair_para)
                    print(f"    📄 Extraído: {membro}")

    except zipfile.BadZipFile:
        print(f"  ⚠️ Arquivo não é um ZIP válido")
    except Exception as e:
        print(f"  ⚠️ Erro ao extrair: {e}")

    return arquivos_extraidos


def main():
    """
    Função principal - baixa dumps de licitações e contratos.
    """
    print("=" * 60)
    print("EXTRATOR DE DADOS ABERTOS - PORTAL DA TRANSPARÊNCIA")
    print("=" * 60)

    print(f"\n📁 Pasta destino: {PASTA_DESTINO}")

    # Criar diretório
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    # Listar tipos de dados que queremos baixar
    tipos_download = [
        {"codigo": "Licitacoes", "nome": "Licitações"},
        {"codigo": "Contratos", "nome": "Contratos"},
    ]

    for tipo in tipos_download:
        print(f"\n🔍 Processando: {tipo['nome']}")

        pasta_tipo = os.path.join(PASTA_DESTINO, tipo["nome"])
        os.makedirs(pasta_tipo, exist_ok=True)

        # Baixar últimos 6 meses para teste (evitar muitos arquivos)
        urls = gerar_urls_download(tipo["codigo"], 2024, 2025)

        # Pegar apenas os últimos 6 meses
        urls_teste = urls[-6:]

        print(f"  📊 URLs a testar: {len(urls_teste)}")

        arquivos_baixados = 0

        for item in urls_teste:
            caminho = download_file(item["url"], pasta_tipo, item["nome_arquivo"])
            if caminho:
                extract_zip(caminho, pasta_tipo)
                arquivos_baixados += 1

            time.sleep(1)  # Rate limit

        print(f"  ✅ {arquivos_baixados} arquivos baixados para {tipo['nome']}")

    print("\n" + "=" * 60)
    print("⚠️ NOTA: Este script baixa dados do Portal da Transparência.")
    print("Se os links estiverem desatualizados, verificar:")
    print("  https://dados.gov.br/dataset/contratos-abertos")
    print("  https://dados.gov.br/dataset/licitacoes")
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()
