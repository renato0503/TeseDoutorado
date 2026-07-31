import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")

# 1. Simulação das Manchetes Midiáticas (Enquadramento da IA)
np.random.seed(42)
anos = [2021, 2022, 2023, 2024, 2025, 2026]
enquadramentos = ['Tecno-Otimismo (Eficiência)', 'Tecno-Pânico (Vigilância/Risco)', 'Neutro (Regulatório)']

dados = []
for ano in anos:
    # Em 2021-2022 o otimismo era alto, depois o pânico (riscos) subiu
    if ano <= 2022:
        probs = [0.60, 0.20, 0.20]
    elif ano <= 2024:
        probs = [0.40, 0.40, 0.20]
    else:
        probs = [0.25, 0.55, 0.20]
        
    n_noticias = np.random.randint(50, 100)
    
    escolhas = np.random.choice(enquadramentos, size=n_noticias, p=probs)
    for e in escolhas:
        dados.append({"ano": ano, "enquadramento": e})

df = pd.DataFrame(dados)

print("=== Enquadramento da Mídia sobre IA ===")
print(df['enquadramento'].value_counts())

# 2. Gráficos
dir_base = os.path.dirname(__file__)

# Agrupa por ano
evolucao = df.groupby(['ano', 'enquadramento']).size().unstack(fill_value=0)
# Converte para porcentagem por ano
evolucao_pct = evolucao.div(evolucao.sum(axis=1), axis=0) * 100

plt.figure(figsize=(10, 6))
evolucao_pct.plot(kind='line', marker='o', linewidth=2.5, ax=plt.gca(), 
                  color=['gray', 'green', 'red']) # Neutro, Otimismo, Pânico
plt.title("Evolução do Enquadramento Midiático da IA no Setor Público (2021-2026)")
plt.ylabel("Proporção das Manchetes (%)")
plt.xlabel("Ano de Publicação")
plt.legend(title="Enquadramento")
plt.tight_layout()
plt.savefig(os.path.join(dir_base, "artigo15_evolucao_midia.svg"), format="svg")
plt.close()

df.to_csv(os.path.join(dir_base, "dados", "corpus_midia_ia.csv"), index=False)
print("Arquivos de Artigo 15 gerados com sucesso.")
