import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg') # backend non-interactive

dir_base = os.path.dirname(__file__)
dir_dados = os.path.join(dir_base, "dados")
arquivo_csv = os.path.join(dir_dados, "pncp_amostra_real.csv")

if not os.path.exists(arquivo_csv):
    print("CSV real do PNCP não encontrado.")
    exit(1)

# Lendo base real do PNCP
df = pd.read_csv(arquivo_csv)

# 1. Pré-processamento
# Remover valores nulos e extremos absurdos (erros de digitação > 1B)
df = df.dropna(subset=['valorTotalEstimado'])
df = df[(df['valorTotalEstimado'] > 100) & (df['valorTotalEstimado'] < 1000000000)]
df['log_valor'] = np.log1p(df['valorTotalEstimado'])

# 2. Isolation Forest para detecção de anomalias no Valor Estimado
X = df[['log_valor']]
iso_forest = IsolationForest(contamination=0.015, random_state=42)
df['anomalia'] = iso_forest.fit_predict(X)
df['tipo_anomalia'] = df['anomalia'].map({1: 'Normal', -1: 'Anômalo (Outlier)'})

# 3. Gerando o Gráfico (SVG)
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#f8f9fa", "grid.color": "#e9ecef"})
plt.figure(figsize=(10, 6))

ax = sns.scatterplot(
    data=df, 
    x=df.index, 
    y='log_valor', 
    hue='tipo_anomalia', 
    palette={'Normal': '#4C72B0', 'Anômalo (Outlier)': '#C44E52'},
    alpha=0.6,
    s=40
)

plt.title('Detecção de Anomalias Reais em Contratações PNCP (Isolation Forest)', fontsize=14, pad=15, fontweight='bold', color='#333333')
plt.xlabel('Índice da Licitação (Tempo/Sequência)', fontsize=12, labelpad=10)
plt.ylabel('Valor Estimado (Log10)', fontsize=12, labelpad=10)
plt.legend(title='Classificação Algorítmica', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.figtext(0.5, 0.01, 'Fonte: Dados primários extraídos via Web Scraping do PNCP (2026).', ha='center', fontsize=10, style='italic', color='#555555')

plt.tight_layout()
out_dir = os.path.join(dir_base, "graficos")
os.makedirs(out_dir, exist_ok=True)
plt.savefig(os.path.join(out_dir, "figura1_scatter_anomalias.svg"), format='svg', bbox_inches='tight')
plt.close()

print("✅ Artigo 02: Isolation Forest processado com dados reais do PNCP.")
