import requests
import pandas as pd
import time
import os
from datetime import datetime

# URL base da API do PNCP (Portal Nacional de Contratações Públicas)
BASE_URL = "https://pncp.gov.br/api/consulta"

def extrair_contratacoes(data_inicial: str, data_final: str, uf: str = None, modalidade_id: int = 6, limite_paginas: int = 5):
    """
    Extrai dados de contratações do PNCP filtrando por data de publicação.
    
    :param data_inicial: Formato yyyyMMdd (ex: 20240101)
    :param data_final: Formato yyyyMMdd (ex: 20240131)
    :param uf: Sigla da UF (opcional, ex: SP)
    :param modalidade_id: ID da modalidade de contratação (Obrigatório pela API, ex: 6 para Pregão)
    :param limite_paginas: Limite de páginas para não sobrecarregar a API em testes
    """
    endpoint = f"{BASE_URL}/v1/contratacoes/publicacao"
    
    resultados = []
    pagina_atual = 1
    tamanho_pagina = 50 # Conforme documentação, tamanho default ou recomendado
    
    print(f"Iniciando coleta de {data_inicial} a {data_final}...")
    
    while pagina_atual <= limite_paginas:
        params = {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
            "codigoModalidadeContratacao": modalidade_id,
            "pagina": pagina_atual,
            "tamanhoPagina": tamanho_pagina
        }
        
        # Adiciona UF se fornecido
        if uf:
            params["uf"] = uf
            
        print(f"Buscando página {pagina_atual}...")
        
        try:
            response = requests.get(endpoint, params=params, timeout=15)
            response.raise_for_status() # Verifica se houve erro HTTP (4xx ou 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            if response is not None:
                print(f"Detalhes do erro: {response.text}")
            break
            
        # Tenta extrair o JSON
        try:
            dados_pagina = response.json()
        except ValueError:
            print("Erro ao decodificar a resposta JSON.")
            break
            
        if not dados_pagina or "data" not in dados_pagina:
            print("Nenhum dado encontrado ou formato de resposta inesperado.")
            break
            
        itens = dados_pagina.get("data", [])
        if not itens or dados_pagina.get("empty", True):
            print("Chegou ao fim dos registros.")
            break
            
        resultados.extend(itens)
        
        paginas_restantes = dados_pagina.get("paginasRestantes", 0)
        print(f"Página {pagina_atual} coletada. Retornou {len(itens)} itens. Páginas restantes: {paginas_restantes}")
        
        if paginas_restantes == 0:
            print("Todas as páginas foram coletadas.")
            break
            
        pagina_atual += 1
        
        # Pausa para evitar rate limit (bloqueio por muitas requisições)
        time.sleep(1)
        
    return resultados

def salvar_dados(dados: list, nome_base: str):
    """
    Salva os dados coletados em arquivos CSV e JSON.
    """
    if not dados:
        print("Nenhum dado para salvar.")
        return
        
    # Verifica se o diretório 'dados' existe, se não, cria
    dir_dados = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados")
    os.makedirs(dir_dados, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_csv = os.path.join(dir_dados, f"{nome_base}_{timestamp}.csv")
    caminho_json = os.path.join(dir_dados, f"{nome_base}_{timestamp}.json")
    
    # Salva JSON puro (útil para analisar estruturas aninhadas depois)
    df = pd.json_normalize(dados)
    
    # Salva JSON e CSV
    df.to_json(caminho_json, orient="records", force_ascii=False, indent=4)
    df.to_csv(caminho_csv, index=False, sep=";", encoding="utf-8-sig")
    
    print(f"\nDados salvos com sucesso!")
    print(f"-> JSON salvo em: {caminho_json}")
    print(f"-> CSV salvo em:  {caminho_csv}")

if __name__ == "__main__":
    # Exemplo de Uso:
    # Vamos coletar os dados publicados no primeiro trimestre de 2024.
    # Por segurança, estamos limitando a 3 páginas. Altere 'limite_paginas' para extrair tudo.
    
    DATA_INICIO = "20240101"
    DATA_FIM = "20240131"
    
    dados_extraidos = extrair_contratacoes(
        data_inicial=DATA_INICIO, 
        data_final=DATA_FIM, 
        uf="ES", # Coletando apenas do Espírito Santo como teste
        limite_paginas=3 
    )
    
    salvar_dados(dados_extraidos, "extracao_pncp_contratacoes")
