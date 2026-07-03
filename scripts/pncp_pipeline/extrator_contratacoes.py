from utils import BASE_URL, extrair_paginado, salvar_dados
import os

def extrair(data_inicial: str, data_final: str, dir_base: str):
    """Extrai contratações por período."""
    endpoint = f"{BASE_URL}/v1/contratacoes/publicacao"
    
    # Vamos extrair iterando por modalidade_id para ser seguro, ou sem se pudermos.
    # O swagger diz que codigoModalidadeContratacao é required.
    # Modalidades comuns: 1 a 15 (ex: 6=Pregão, 8=Dispensa)
    todas_contratacoes = []
    
    for modalidade in range(1, 15):
        params = {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
            "codigoModalidadeContratacao": modalidade
        }
        
        dados_mod = extrair_paginado(endpoint, params)
        todas_contratacoes.extend(dados_mod)
        
    print(f"[{data_inicial}-{data_final}] Contratações coletadas: {len(todas_contratacoes)}")
    if todas_contratacoes:
        pasta = os.path.join(dir_base, "contratacoes")
        salvar_dados(todas_contratacoes, pasta, f"contratacoes_{data_inicial}_{data_final}")
    
    return len(todas_contratacoes)
