import os
import shutil

DIR_BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DIR_DADOS_PILOTO = os.path.join(DIR_BASE, "dados")
DIR_ARTIGOS = os.path.join(DIR_BASE, "Artigos")

# O arquivo piloto gerado hoje cedo
ARQUIVO_PILOTO_CSV = "extracao_pncp_contratacoes_20260627_161041.csv"
ARQUIVO_PILOTO_JSON = "extracao_pncp_contratacoes_20260627_161041.json"

caminho_csv_piloto = os.path.join(DIR_DADOS_PILOTO, ARQUIVO_PILOTO_CSV)
caminho_json_piloto = os.path.join(DIR_DADOS_PILOTO, ARQUIVO_PILOTO_JSON)

artigos_alvo = [
    "01-Opacidade-Institucional-Analise-Complexidade-Textual-Editais-Inovacao",
    "10-Uso-Retorico-Inovacao-Analise-Conteudo-Justificativas"
]

for artigo in artigos_alvo:
    pasta_dados = os.path.join(DIR_ARTIGOS, artigo, "dados")
    os.makedirs(pasta_dados, exist_ok=True)
    
    if os.path.exists(caminho_csv_piloto):
        shutil.copy(caminho_csv_piloto, os.path.join(pasta_dados, "dataset_pncp.csv"))
    if os.path.exists(caminho_json_piloto):
        shutil.copy(caminho_json_piloto, os.path.join(pasta_dados, "dataset_pncp.json"))
        
    print(f"Dados copiados para o artigo: {artigo}")
