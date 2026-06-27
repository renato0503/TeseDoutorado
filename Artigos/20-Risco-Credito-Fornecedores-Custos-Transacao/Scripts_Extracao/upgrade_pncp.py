"""
ARTIGO 20 - Upgrade: Cruzar CNPJ/RIQ com PNCP (REFATORADO)
Portal Nacional de Compras Publicas - Nova API MGI

Correcao: Endpoint atualizado com parametro obligatorio codigoModalidadeContratacao
Modalidades: 1=Pregao, 6=Dispensa de Licitacao, etc.
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\20-Risco-Credito-Fornecedores-Custos-Transacao"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

BASE_URL = "https://pncp.gov.br/api/consulta/v1"
HEADERS = {
    "User-Agent": "gestor.renatorosa@gmail.com",
    "Accept": "application/json"
}

MODALIDADES = {
    "pregao": 1,
    "dispensa": 6,
    "inexigibilidade": 7,
    "concorrencia": 2,
    "tomada_precos": 3,
}


def buscar_contratacoes_publicacao(data_inicial, data_final, codigo_modalidade=6, tamanho=100, pagina=1):
    """
    Busca contratacoes publicadas no PNCP via novo endpoint.

    Args:
        data_inicial: Data inicio (YYYY-MM-DD)
        data_final: Data fim (YYYY-MM-DD)
        codigo_modalidade: Codigo da modalidade (6=Dispensa, 1=Pregao, etc.)
        tamanho: Tamanho da pagina (default 100)
        pagina: Numero da pagina (default 1, pois API exige >= 1)

    Returns:
        Lista de contratacoes ou lista vazia em caso de erro
    """
    time.sleep(2)
    url = f"{BASE_URL}/contratacoes/publicacao"
    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "codigoModalidadeContratacao": codigo_modalidade,
        "pagina": pagina,
        "tamanhoPagina": tamanho
    }

    print(f"    GET {url}")
    print(f"    Params: {params}")

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)

        if response.status_code == 400:
            print(f"    ! Erro 400: {response.text[:200]}")
            return []
        if response.status_code == 404:
            print(f"    ! Endpoint nao encontrado (404)")
            return []
        if response.status_code == 429:
            print(f"    ! Rate limit (429). Aguardando 60s...")
            time.sleep(60)
            return []

        if response.status_code != 200:
            print(f"    ! Erro HTTP {response.status_code}: {response.text[:100]}")
            return []

        data = response.json()

        if isinstance(data, dict):
            return data.get("content", [])
        elif isinstance(data, list):
            return data
        else:
            print(f"    ! Formato inesperado: {type(data)}")
            return []

    except requests.exceptions.Timeout:
        print(f"    ! Timeout na requisicao")
        return []
    except requests.exceptions.RequestException as e:
        print(f"    ! Erro de conexao: {e}")
        return []


def coletar_contratacoes_por_modalidade(modalidade_nome, codigo_modalidade, ano_inicio=2023, ano_fim=2024):
    """
    Coleta contratacoes por modalidade e periodo.

    Args:
        modalidade_nome: Nome da modalidade para exibicao
        codigo_modalidade: Codigo numerico da modalidade
        ano_inicio: Ano inicial
        ano_fim: Ano final

    Returns:
        DataFrame com contratacoes
    """
    todos = []

    for ano in range(ano_inicio, ano_fim + 1):
        for mes in range(1, 13):
            data_inicial = f"{ano}-{mes:02d}-01"
            if mes == 12:
                data_final = f"{ano}-12-31"
            else:
                data_final = f"{ano}-{mes+1:02d}-01"

            print(f"\n  {modalidade_nome} | {data_inicial} a {data_final}", end=" ")

            items = buscar_contratacoes_publicacao(
                data_inicial, data_final,
                codigo_modalidade=codigo_modalidade,
                tamanho=50
            )

            if items:
                for item in items:
                    if isinstance(item, dict):
                        orgao = item.get("orgaoEntidade", {})
                        unidade = item.get("unidadeOrgao", {})
                        todos.append({
                            "modalidade": modalidade_nome,
                            "ano": ano,
                            "mes": mes,
                            "numero_controle": item.get("numeroControlePNCP"),
                            "numero_compra": item.get("numeroCompra"),
                            "objeto": item.get("objetoCompra"),
                            "modalidade_nome": item.get("modalidadeNome"),
                            "modo_disputa": item.get("modoDisputaNome"),
                            "valor_estimado": item.get("valorTotalEstimado"),
                            "valor_homologado": item.get("valorTotalHomologado"),
                            "data_publicacao": item.get("dataPublicacaoPncp"),
                            "orgao_cnpj": orgao.get("cnpj"),
                            "orgao_razao_social": orgao.get("razaoSocial"),
                            "unidade_codigo": unidade.get("codigoUnidade"),
                            "unidade_nome": unidade.get("nomeUnidade"),
                            "uf": unidade.get("ufSigla"),
                            "municipio": unidade.get("municipioNome"),
                        })
                print(f"=> {len(items)} contratacoes")
            else:
                print("=> 0")

            time.sleep(1)

    return pd.DataFrame(todos)


def coletar_orgaos(ufs=None):
    """
    Coleta lista de orgaos por UF via PNCP.
    """
    ufs = ufs or ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "DF"]
    dados = []

    for uf in ufs:
        print(f"Buscando orgaos {uf}...", end=" ", flush=True)
        time.sleep(2)

        url = f"{BASE_URL}/orgaos?uf={uf}"

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)

            if response.status_code == 200:
                orgs = response.json()
                if isinstance(orgs, dict):
                    orgs = orgs.get("content", [])
                elif not isinstance(orgs, list):
                    orgs = []

                for org in orgs[:20]:
                    if isinstance(org, dict):
                        dados.append({
                            "uf": uf,
                            "codigo": org.get("codigo"),
                            "nome": org.get("nome"),
                            "tipo": org.get("tipo"),
                        })
                print(f"{len(orgs)} orgaos")
            else:
                print(f"Status {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")

        time.sleep(1)

    return pd.DataFrame(dados)


def main():
    print("=== ARTIGO 20 - PNCP (com codigoModalidadeContratacao) ===\n")
    print(f"Base URL: {BASE_URL}")
    print(f"Modalidades: {MODALIDADES}\n")

    print("=" * 60)
    print("COLETANDO CONTRATACOES POR MODALIDADE")
    print("=" * 60)

    todas_contratacoes = []

    print("\n1. Dispensa de Licitacao (codigo=6)...")
    df_dispensa = coletar_contratacoes_por_modalidade("Dispensa", 6, 2024, 2024)
    if not df_dispensa.empty:
        todas_contratacoes.append(df_dispensa)

    print("\n2. Pregao (codigo=1)...")
    df_pregao = coletar_contratacoes_por_modalidade("Pregao", 1, 2024, 2024)
    if not df_pregao.empty:
        todas_contratacoes.append(df_pregao)

    if todas_contratacoes:
        df_contratacoes = pd.concat(todas_contratacoes, ignore_index=True)
        output_contratacoes = os.path.join(RAW, "artigo20_pncp_contratacoes.csv")
        df_contratacoes.to_csv(output_contratacoes, index=False, encoding="utf-8-sig")
        print(f"\nTotal: {len(df_contratacoes)} contratacoes salvas em {output_contratacoes}")
    else:
        print("\nNenhuma contratacao coletada.")
        df_contratacoes = pd.DataFrame()

    print("\n" + "=" * 60)
    print("COLETANDO ORGAOS")
    print("=" * 60)

    df_orgaos = coletar_orgaos(["SP", "RJ", "MG"])
    output_orgaos = os.path.join(RAW, "artigo20_pncp_orgaos.csv")
    df_orgaos.to_csv(output_orgaos, index=False, encoding="utf-8-sig")
    print(f"\n{len(df_orgaos)} orgaos salvos em {output_orgaos}")

    return df_contratacoes, df_orgaos


if __name__ == "__main__":
    main()
