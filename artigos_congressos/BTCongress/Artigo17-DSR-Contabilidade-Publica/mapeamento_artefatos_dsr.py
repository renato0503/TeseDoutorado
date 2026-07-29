import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("pastel")

# 1. Simulação da Revisão Sistemática DSR
tipos_artefato = ['Construto', 'Modelo', 'Método', 'Instanciação']

np.random.seed(42)
dados = []

# Distribuição simulada: muita instanciação (sistemas), poucos construtos teóricos
for _ in range(10): dados.append('Construto')
for _ in range(25): dados.append('Modelo')
for _ in range(15): dados.append('Método')
for _ in range(30): dados.append('Instanciação')

df = pd.DataFrame({"tipo_artefato": dados})

print("=== Mapeamento de Artefatos DSR ===")
print(df['tipo_artefato'].value_counts())

# 2. Gráficos
dir_base = os.path.dirname(__file__)

contagem = df['tipo_artefato'].value_counts().reset_index()
contagem.columns = ['Tipo', 'Quantidade']

plt.figure(figsize=(8, 8))
plt.pie(contagem['Quantidade'], labels=contagem['Tipo'], autopct='%1.1f%%', startangle=140, 
        colors=['#3498db', '#e74c3c', '#f1c40f', '#2ecc71'])
plt.title("Distribuição dos Artefatos DSR na Literatura de Contabilidade Pública")
plt.tight_layout()
plt.savefig(os.path.join(dir_base, "artigo17_distribuicao_artefatos.svg"), format="svg")
plt.close()

df.to_csv(os.path.join(dir_base, "dados", "mapeamento_dsr.csv"), index=False)
print("Arquivos de Artigo 17 gerados com sucesso.")
