from utils import BASE_URL, extrair_paginado, salvar_dados
import os

def extrair(data_inicial: str, data_final: str, dir_base: str):
    """Extrai contratos por período."""
    endpoint = f"{BASE_URL}/v1/contratos"
    
    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }
    
    dados = extrair_paginado(endpoint, params)
        
    print(f"[{data_inicial}-{data_final}] Contratos coletados: {len(dados)}")
    if dados:
        pasta = os.path.join(dir_base, "contratos")
        salvar_dados(dados, pasta, f"contratos_{data_inicial}_{data_final}")
        
    return len(dados)
