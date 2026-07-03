import pandas as pd
import numpy as np
import os

# Carregar dados PNCP
df = pd.read_csv(r'C:\Users\Renato\Documents\Doutorado\dados\processed\pncp_contratos_full.csv')
print('Total contratos:', len(df))

# Palavras-chave de tecnologia/inovação
tech_keywords = ['TECNOLOGIA', 'SOFTWARE', 'INFORMÁTICA', 'INFORMATICA', 'SISTEMA', 'COMPUTADOR', 
                'DIGITAL', 'CIBERSEGURANÇA', 'CIBERSEGURANCA', 'NUVEM', 'CLOUD', 'TI ', 'PROC. DADOS',
                'TRATAMENTO DADOS', 'BANCO DADOS', 'BANCO DE DADOS', 'DESENVOLVIMENTO SISTEMAS',
                'PROJETO TECNOLOGICO', 'INOVAÇÃO', 'INOVACAO']

# Criar coluna de justificativa (objeto do contrato)
df['justificativa'] = df['objeto'].fillna('')

# Filtrar contratos que parecem ter justificativas de inovação
mask_tech = df['justificativa'].str.upper().str.contains('|'.join(tech_keywords), na=False)
df_tech = df[mask_tech].copy()
print('Contratos de tecnologia/inovação:', len(df_tech))

# Amostra aleatória de 350 contratos
np.random.seed(2026)
if len(df_tech) >= 350:
    df_sample = df_tech.sample(n=350, random_state=2026)
else:
    df_sample = df_tech.copy()
    
print('Amostra selecionada:', len(df_sample))

# Criar dataset de justificativas
dataset_justificativas = df_sample[['justificativa', 'uf', 'orgao', 'valor_global', 'tipo_contrato']].copy()
dataset_justificativas.columns = ['justificativa', 'uf', 'orgao', 'valor', 'modalidade']
dataset_justificativas['id'] = range(1, len(dataset_justificativas) + 1)

# Reordenar colunas
dataset_justificativas = dataset_justificativas[['id', 'justificativa', 'uf', 'orgao', 'valor', 'modalidade']]

# Mostrar distribuição por modalidade
print()
print('Distribuição por modalidade:')
print(dataset_justificativas['modalidade'].value_counts())

# Criar diretório se não existir
output_dir = r'C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Artigos_Quanti\10_Retorica'
os.makedirs(output_dir, exist_ok=True)

# Salvar CSV
output_path = os.path.join(output_dir, 'justificativas_pncp.csv')
dataset_justificativas.to_csv(output_path, index=False, encoding='utf-8')
print(f'\nDataset salvo em: {output_path}')

# Mostrar exemplos
print()
print('Exemplos de justificativas:')
for i, row in dataset_justificativas.head(5).iterrows():
    texto = row['justificativa'][:120].replace('\n', ' ')
    print(f"[{row['id']:03d}] ({row['modalidade']}) {texto}...")

# Estatísticas de valor
print()
print('Estatísticas de valor:')
print(f"  Total: R$ {dataset_justificativas['valor'].sum():,.2f}")
print(f"  Média: R$ {dataset_justificativas['valor'].mean():,.2f}")
print(f"  Mediana: R$ {dataset_justificativas['valor'].median():,.2f}")

# Distribuição por UF
print()
print('Top 10 UFs:')
print(dataset_justificativas['uf'].value_counts().head(10))