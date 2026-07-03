import requests
import time
import os
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://pncp.gov.br/api/consulta"

def get_session():
    """Retorna uma sessão do requests configurada com retries automáticos."""
    session = requests.Session()
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def extrair_paginado(endpoint: str, base_params: dict):
    """Extrai todas as páginas de um endpoint."""
    session = get_session()
    resultados = []
    pagina_atual = 1
    tamanho_pagina = 50
    
    while True:
        params = base_params.copy()
        params['pagina'] = pagina_atual
        params['tamanhoPagina'] = tamanho_pagina
        
        try:
            resp = session.get(endpoint, params=params, timeout=30)
            resp.raise_for_status()
            dados = resp.json()
        except Exception as e:
            print(f"Erro na página {pagina_atual} do endpoint {endpoint}: {e}")
            break
            
        itens = dados.get("data", [])
        if not itens or dados.get("empty", True):
            break
            
        resultados.extend(itens)
        
        paginas_restantes = dados.get("paginasRestantes", 0)
        if paginas_restantes == 0:
            break
            
        pagina_atual += 1
        time.sleep(0.5) # Proteção adicional contra rate limit
        
    return resultados

def salvar_dados(dados: list, pasta_destino: str, nome_arquivo: str):
    """Salva os dados no formato JSON e Parquet."""
    if not dados:
        return False
        
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_base = os.path.join(pasta_destino, nome_arquivo)
    
    df = pd.json_normalize(dados)
    
    # Substituir colunas que são objetos complexos por strings (para o parquet não quebrar)
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
            df[col] = df[col].astype(str)
            
    df.to_csv(f"{caminho_base}.csv", index=False, sep=";", encoding="utf-8-sig")
    
    # Salvar JSON raw sem flatten para ter a hierarquia original
    pd.Series(dados).to_json(f"{caminho_base}.json", orient="values", force_ascii=False)
    return True
