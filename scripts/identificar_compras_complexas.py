import pandas as pd
import json
import os

# Configurações de pastas
DATA_FILE = 'dados/processed/pncp_contratos_full.csv'
OUTPUT_FILE = 'dados/processed/pncp_compras_complexas.csv'
STATS_FILE = 'Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/stats_compras_complexas.json'

print("Carregando dataset de 572 mil contratos (isso pode levar um momento)...")
df = pd.read_csv(DATA_FILE)

print(f"Total de registros carregados: {len(df)}")

# Dicionários de palavras-chave (regex patterns para case insensitive)
kw_inovacao = ['tecnologia', 'software', 'nuvem', 'inteligência artificial', 'inovação', 'inovacao', 'p&d', 'pesquisa e desenvolvimento', 'startup']
kw_sustentabilidade = ['sustentável', 'sustentavel', 'energia limpa', 'eficiência energética', 'reciclagem', 'logística reversa', 'logistica reversa', 'esg']

# Combina as palavras e formata para regex (borda de palavra opcional, mas 'contains' já pega substrings, então usaremos boundaries onde necessário)
pattern = '|'.join([f"\\b{kw}\\b" for kw in kw_inovacao + kw_sustentabilidade])

print("Aplicando filtro NLP (Regex) na coluna 'objeto'...")
# Preenchendo NaNs na coluna objeto com string vazia antes de buscar
df['objeto'] = df['objeto'].fillna('')
df['is_complexa'] = df['objeto'].str.contains(pattern, case=False, regex=True)

complexas = df[df['is_complexa'] == True]
normais = df[df['is_complexa'] == False]

qtd_complexas = len(complexas)
qtd_normais = len(normais)
perc_complexas = (qtd_complexas / len(df)) * 100

print(f"--- RESULTADOS DA FILTRAGEM ---")
print(f"Compras Complexas (Inovação/Sustentabilidade): {qtd_complexas} ({perc_complexas:.2f}%)")
print(f"Compras Normais: {qtd_normais}")

print("Identificando universos únicos de CNPJs e Órgãos nas compras complexas...")
fornecedores_unicos = complexas['fornecedor_cnpj'].nunique()
orgaos_unicos = complexas['orgao'].nunique()

print(f"Fornecedores únicos em compras complexas: {fornecedores_unicos}")
print(f"Órgãos únicos em compras complexas: {orgaos_unicos}")

print("Salvando subset (somente compras complexas) para evitar onerar as APIs...")
complexas.to_csv(OUTPUT_FILE, index=False)
print(f"Subset salvo em: {OUTPUT_FILE}")

# Salva as estatísticas para o Artigo 1
os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
stats = {
    "total_contratos_populacao": len(df),
    "total_compras_complexas": qtd_complexas,
    "percentual_complexas": perc_complexas,
    "fornecedores_unicos_complexas": fornecedores_unicos,
    "orgaos_unicos_complexas": orgaos_unicos
}

with open(STATS_FILE, 'w', encoding='utf-8') as f:
    json.dump(stats, f, indent=4, ensure_ascii=False)

print(f"Estatísticas salvas em: {STATS_FILE}")
print("Processo concluído com sucesso!")
