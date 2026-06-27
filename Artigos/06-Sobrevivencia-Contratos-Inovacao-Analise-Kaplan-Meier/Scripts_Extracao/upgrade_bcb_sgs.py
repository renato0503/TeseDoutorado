"""
ARTIGO 06 - Upgrade: Contexto Macroeconomico (REFATORADO)
Substituicao: HG Brasil API -> BCB SGS API (Sistema Gerenciador de Series Temporais)

Banco Central do Brasil - Dados abertos em:
https://dadosabertos.bcb.gov.br/

URL Base: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json

Principais codigos de series:
- 432: Taxa Selic
- 4391: Taxa CDI
- 433: IPCA
- 4188: IPCA-15
- 1900: PIB Mensal
- 27842: Divida Publica Federal
- 1362: Taxa de Cambio PTAX
- 21619: Reserva Internacional
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\06-Sobrevivencia-Contratos-Inovacao-Analise-Kaplan-Meier"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"
HEADERS = {
    "User-Agent": "gestor.renatorosa@gmail.com",
    "Accept": "application/json"
}


SERIES_BCB = {
    "ipca": {
        "codigo": 433,
        "nome": "IPCA - Indice Nacional de Precos ao Consumidor Amplo",
        "periodicidade": "mensal",
        "fonte": "BCB/SGS"
    },
    "ipca_15": {
        "codigo": 4188,
        "nome": "IPCA-15 - Indice Nacional de Precos ao Consumidor Amplo 15",
        "periodicidade": "mensal",
        "fonte": "BCB/SGS"
    },
    "selic": {
        "codigo": 432,
        "nome": "Taxa de Juros - Selic",
        "periodicidade": "diario",
        "fonte": "BCB/SGS"
    },
    "cdi": {
        "codigo": 4391,
        "nome": "Taxa de Juros - CDI",
        "periodicidade": "diario",
        "fonte": "BCB/SGS"
    },
    "pibt": {
        "codigo": 4389,
        "nome": "PIB Trimestral (Taxa de variacao)",
        "periodicidade": "trimestral",
        "fonte": "BCB/SGS"
    },
    "cambio": {
        "codigo": 1362,
        "nome": "Taxa de Cambio - PTAX",
        "periodicidade": "diario",
        "fonte": "BCB/SGS"
    },
    "reservas": {
        "codigo": 21619,
        "nome": "Reservas Internacionais",
        "periodicidade": "diario",
        "fonte": "BCB/SGS"
    },
    "divida_federal": {
        "codigo": 27842,
        "nome": "Divida Publica Federal",
        "periodicidade": "mensal",
        "fonte": "BCB/SGS"
    },
    "inpc": {
        "codigo": 188,
        "nome": "INPC - Indice Nacional de Precos ao Consumidor",
        "periodicidade": "mensal",
        "fonte": "BCB/SGS"
    },
    "igpm": {
        "codigo": 189,
        "nome": "IGP-M - Indice Geral de Precos do Mercado",
        "periodicidade": "mensal",
        "fonte": "BCB/FGV"
    },
}


def buscar_serie_bcb(codigo_serie, data_inicio=None, data_fim=None, ApenasUltimoValor=False):
    """
    Busca serie temporal do SGS/BACEN.

    Args:
        codigo_serie: Codigo da serie no SGS (ex: 433 para IPCA)
        data_inicio: Data inicio no formato 'DD/MM/AAAA' ou None para inicio padrao
        data_fim: Data fim no formato 'DD/MM/AAAA' ou None para hoje
        ApenasUltimoValor: Se True, retorna apenas ultimo valor (True/False em string)

    Returns:
        DataFrame com colunas: data, valor
    """
    time.sleep(1)

    url = f"{BASE_URL}.{codigo_serie}/dados"

    params = {}
    if data_inicio:
        params["dataInicio"] = data_inicio
    if data_fim:
        params["dataFim"] = data_fim
    if ApenasUltimoValor:
        params["formato"] = "json"

    print(f"  GET {url}")
    if params:
        print(f"     Params: {params}")

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=60)

        if response.status_code == 404:
            print(f"  ! Serie nao encontrada (404): codigo {codigo_serie}")
            return pd.DataFrame()

        if response.status_code == 429:
            print(f"  ! Rate limit (429). Aguardando 30s...")
            time.sleep(30)
            return buscar_serie_bcb(codigo_serie, data_inicio, data_fim, ApenasUltimoValor)

        if response.status_code != 200:
            print(f"  ! Erro HTTP {response.status_code}: {response.text[:200]}")
            return pd.DataFrame()

        data = response.json()

        if not data or len(data) == 0:
            print(f"  ! Serie vazia")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        if "data" in df.columns and "valor" in df.columns:
            df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y", errors="coerce")
            df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
            df = df.dropna()
            print(f"  => {len(df)} registros")
            return df
        else:
            print(f"  ! Colunas inesperadas: {df.columns.tolist()}")
            return pd.DataFrame()

    except requests.exceptions.Timeout:
        print(f"  ! Timeout na requisicao")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"  ! Erro de conexao: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"  ! Erro inesperado: {e}")
        return pd.DataFrame()


def coletar_serie_completa(codigo_serie, ano_inicio=2018, ano_fim=2024):
    """
    Coleta serie completa filtrando por periodo.

    Args:
        codigo_serie: Codigo da serie
        ano_inicio: Ano inicial
        ano_fim: Ano final

    Returns:
        DataFrame filtrado
    """
    data_inicio = f"01/01/{ano_inicio}"
    data_fim = f"31/12/{ano_fim}"

    print(f"\n  Serie {codigo_serie} ({ano_inicio}-{ano_fim})")
    df = buscar_serie_bcb(codigo_serie, data_inicio, data_fim)

    if not df.empty and "data" in df.columns:
        df["ano"] = df["data"].dt.year
        df["mes"] = df["data"].dt.month
        df = df[(df["ano"] >= ano_inicio) & (df["ano"] <= ano_fim)]

    return df


def coletar_macroeconomico(ano_inicio=2018, ano_fim=2024):
    """
    Coleta conjunto de series macroeconômicas do BCB.

    Returns:
        Dicionario com DataFrames por serie
    """
    resultados = {}

    print("=== Coleta Macroeconomica - BCB/SGS ===\n")

    for nome, info in SERIES_BCB.items():
        codigo = info["codigo"]
        nome_exibicao = info["nome"]
        print(f"\n[{nome}] {nome_exibicao}")
        print(f"  Codigo SGS: {codigo}")

        df = coletar_serie_completa(codigo, ano_inicio, ano_fim)

        if not df.empty:
            df["serie"] = nome
            df["codigo_serie"] = codigo
            df["fonte"] = info["fonte"]
            resultados[nome] = df
            print(f"  OK: {len(df)} registros")
        else:
            print(f"  FALHA: Nenhum dado coletado")

        time.sleep(1)

    return resultados


def gerar_csv_unificado(resultados, output_path):
    """
    Gera CSV unificado com todas as series em formato long.

    Args:
        resultados: Dicionario de DataFrames
        output_path: Caminho do arquivo de saida
    """
    if not resultados:
        print("Nenhum dado para salvar")
        return

    dfs = []
    for nome, df in resultados.items():
        if not df.empty:
            dfs.append(df)

    if dfs:
        df_final = pd.concat(dfs, ignore_index=True)
        df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"\nTotal: {len(df_final)} registros salvos em {output_path}")
    else:
        print("Nenhum dado para salvar")


def main():
    print("=== ARTIGO 06 - BCB SGS (Substituto HG Brasil) ===\n")
    print(f"Base URL: {BASE_URL}\n")
    print(f"Series disponiveis: {list(SERIES_BCB.keys())}\n")

    resultados = coletar_macroeconomico(2018, 2024)

    output_path = os.path.join(RAW, "artigo06_macroeconomico_bcb.csv")
    gerar_csv_unificado(resultados, output_path)

    for nome, df in resultados.items():
        print(f"  {nome}: {len(df)} registros")

    if not resultados:
        print("\nATENCAO: Nenhuma serie coletada.")
        print("Salvando template de series disponiveis para referencia...")

        df_series = pd.DataFrame([
            {"serie": k, "codigo": v["codigo"], "nome": v["nome"],
             "periodicidade": v["periodicidade"], "fonte": v["fonte"]}
            for k, v in SERIES_BCB.items()
        ])
        output_series = os.path.join(RAW, "artigo06_series_bcb_disponiveis.csv")
        df_series.to_csv(output_series, index=False, encoding="utf-8-sig")
        print(f"Series disponiveis salvas em: {output_series}")

    return resultados


if __name__ == "__main__":
    main()
