"""
ARTIGO 21 - Upgrade: Coletar Acordaos Reais do TCU (REFATORADO)

Repositorio Oficial de Dados Abertos: https://dados.tcu.gov.br/
Indexador de Dados Abertos: https://pesquisa.apps.tcu.gov.br/dados-abertos

Este script implementa download direto dos datasets de acordaos
via repositorio oficial de dados abertos do TCU.
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\21-Reacao-Mercado-Fiscalizacao-TCU-Estudo-Evento"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

HEADERS = {
    "User-Agent": "gestor.renatorosa@gmail.com",
    "Accept": "application/json, text/csv"
}


def listar_datasets_tcu():
    """
    Lista datasets disponiveis no repositorio de dados abertos do TCU.

    Returns:
        Lista de datasets ou DataFrame vazio
    """
    print("  Listando datasets do TCU...")

    url = "https://dados.tcu.gov.br/api/3/action/package_list"

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return data.get("result", [])
            else:
                print(f"  ! Erro na API: {data}")
                return []
        else:
            print(f"  ! HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"  ! Erro: {e}")
        return []


def baixar_dataset_csv(dataset_name, retry=3):
    """
    Baixa dataset em formato CSV do repositorio de dados abertos do TCU.

    Args:
        dataset_name: Nome do dataset (ex: 'acordaos', 'prestacao_contas')
        retry: Numero de tentativas

    Returns:
        DataFrame com os dados ou DataFrame vazio
    """
    url = f"https://dados.tcu.gov.br/api/3/action/package_show?id={dataset_name}"

    print(f"  Buscando dataset: {dataset_name}")

    for attempt in range(retry):
        try:
            response = requests.get(url, headers=HEADERS, timeout=60)

            if response.status_code == 404:
                print(f"  ! Dataset nao encontrado: {dataset_name}")
                return pd.DataFrame()

            if response.status_code == 429:
                wait_time = (attempt + 1) * 30
                print(f"  ! Rate limit. Aguardando {wait_time}s...")
                time.sleep(wait_time)
                continue

            if response.status_code != 200:
                print(f"  ! HTTP {response.status_code}")
                return pd.DataFrame()

            data = response.json()

            if not data.get("success"):
                print(f"  ! API error: {data}")
                return pd.DataFrame()

            resources = data.get("result", {}).get("resources", [])

            if not resources:
                print(f"  ! Sem recursos no dataset")
                return pd.DataFrame()

            csv_resource = None
            for r in resources:
                if r.get("format", "").upper() in ["CSV", "XLS", "XLSX"]:
                    csv_resource = r
                    break

            if not csv_resource:
                csv_resource = resources[0]

            download_url = csv_resource.get("url")

            if not download_url:
                print(f"  ! Sem URL de download")
                return pd.DataFrame()

            print(f"  Baixando: {download_url[:80]}...")

            time.sleep(2)
            download_response = requests.get(download_url, headers=HEADERS, timeout=120)

            if download_response.status_code != 200:
                print(f"  ! Erro no download: {download_response.status_code}")
                continue

            from io import StringIO

            content_type = download_response.headers.get("Content-Type", "")

            if "csv" in content_type.lower() or download_url.endswith(".csv"):
                df = pd.read_csv(StringIO(download_response.text), sep=";", encoding="utf-8")
            elif "xlsx" in content_type.lower() or download_url.endswith(".xlsx"):
                df = pd.read_excel(download_response.content)
            else:
                df = pd.read_csv(StringIO(download_response.text), sep=";", encoding="utf-8")

            print(f"  => {len(df)} registros")
            return df

        except requests.exceptions.Timeout:
            print(f"  ! Timeout na tentativa {attempt + 1}")
            time.sleep(5)
        except Exception as e:
            print(f"  ! Erro: {e}")
            time.sleep(2)

    return pd.DataFrame()


def coletar_acordaos_fiscalizacao(ano_inicio=2018, ano_fim=2024):
    """
    Coleta acordaos de fiscalizacao do TCU via dados abertos.

    Args:
        ano_inicio: Ano inicial para filtragem
        ano_fim: Ano final para filtragem

    Returns:
        DataFrame com acordaos
    """
    print("\n=== Coleta de Acordaos do TCU - Dados Abertos ===\n")

    datasets = [
        "acordaos",
        "acordaos_relator",
        "acordaos_gabinetes",
        "prestacao_contas",
    ]

    todos_dfs = []

    for dataset in datasets:
        print(f"\nProcessando dataset: {dataset}")
        df = baixar_dataset_csv(dataset)

        if not df.empty:
            print(f"  Colunas disponiveis: {df.columns.tolist()[:10]}")

            date_cols = [c for c in df.columns if "data" in c.lower()]
            for col in date_cols:
                try:
                    if df[col].dtype == object:
                        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
                    df[f"{col}_ano"] = df[col].dt.year
                    if "data" in col.lower():
                        df = df[(df[f"{col}_ano"] >= ano_inicio) & (df[f"{col}_ano"] <= ano_fim)]
                    df = df.drop(columns=[f"{col}_ano"])
                except Exception as e:
                    print(f"  ! Erro ao processar coluna {col}: {e}")

            df["dataset_origem"] = dataset
            todos_dfs.append(df)
            print(f"  => {len(df)} registros apos filtro")
        else:
            print(f"  ! Nenhum dado")

        time.sleep(2)

    if todos_dfs:
        df_final = pd.concat(todos_dfs, ignore_index=True)
        print(f"\nTotal consolidado: {len(df_final)} registros")
        return df_final
    else:
        print("\nNenhum dataset disponivel via dadosabertos.tcu.gov.br")
        return pd.DataFrame()


def criar_template_acordaos():
    """
    Cria template de acordaos para preenchimento manual.
    """
    print("\nCriando template para preenchimento manual...")

    df = pd.DataFrame({
        "numero": ["AC-0001/2018-2", "AC-0002/2019-3", "AC-0003/2020-5"],
        "processo": ["001.XXX/2018-5", "002.XXX/2019-7", "003.XXX/2020-9"],
        "relator": ["Ministro A", "Ministro B", "Ministro C"],
        "data": ["2018-01-15", "2019-02-20", "2020-03-10"],
        "unidade": ["CGU", "CGU", "TCU"],
        "tipo": ["Representacao", "Auditoria", "Fiscalizacao"],
        "ementa": [
            "EMENTA: Representacao sobre irregularidades em licitacoes...",
            "EMENTA: Auditoria em contratos de tecnologia da informacao...",
            "EMENTA: Fiscalizacao de despesas publicas em compras...",
        ],
        "dataset_origem": ["template"] * 3,
    })

    return df


def main():
    print("=== ARTIGO 21 - TCU (Dados Abertos) ===\n")
    print("Repositorio: https://dados.tcu.gov.br/\n")

    print("1. Listando datasets disponiveis...")
    datasets = listar_datasets_tcu()
    if datasets:
        print(f"   {len(datasets)} datasets encontrados")
        print(f"   Primeiros 5: {datasets[:5]}")

    print("\n2. Coletando acordaos de fiscalizacao (2018-2024)...")
    df = coletar_acordaos_fiscalizacao(2018, 2024)

    if df.empty:
        print("\n3. Tentando datasets alternativos...")
        datasets_alternativos = [
            "acordaos_comercial",
            "acordaos_monitoramento",
            "acordaos_tributario",
        ]
        for ds in datasets_alternativos:
            print(f"\n   Tentando: {ds}")
            df_alt = baixar_dataset_csv(ds)
            if not df_alt.empty:
                df = df_alt
                break

    if df.empty:
        print("\n4. Criando template para preenchimento manual...")
        df = criar_template_acordaos()

    output = os.path.join(RAW, "artigo21_acordaos_tcu.csv")
    df.to_csv(output, index=False, encoding="utf-8-sig")
    print(f"\n{len(df)} acordaos salvos em {output}")

    if "numero" in df.columns:
        print(f"   Amostra: {df['numero'].head(3).tolist()}")

    return df


if __name__ == "__main__":
    main()
