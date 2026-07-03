import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set1")

# 1. Simulação dos Discursos (Custo Brasil)
topicos_peso = {
    "Ineficiência Burocrática e Excesso de Regras": 45,
    "Insegurança Jurídica e Risco de Punição": 35,
    "Corrupção e Desvios Éticos": 20
}

# Gerando dados
dados = []
np.random.seed(42)
for i in range(120): # 120 discursos
    tema = np.random.choice(list(topicos_peso.keys()), p=[0.45, 0.35, 0.20])
    dados.append({
        "id_discurso": f"DISC-{2023}-{str(i).zfill(3)}",
        "tema_predominante": tema
    })

df = pd.DataFrame(dados)

print("=== Análise de Discurso (Custo Brasil) ===")
contagem = df['tema_predominante'].value_counts(normalize=True) * 100
print(contagem)

# 2. Gráficos
dir_base = os.path.dirname(__file__)

plt.figure(figsize=(10, 5))
ax = sns.countplot(y='tema_predominante', data=df, order=df['tema_predominante'].value_counts().index, palette='Blues_r')
plt.title("Eixos Narrativos do Custo Brasil nos Discursos Políticos")
plt.xlabel("Número de Ocorrências (Discursos)")
plt.ylabel("")

# Adiciona porcentagem
total = len(df)
for p in ax.patches:
    percentage = f'{100 * p.get_width() / total:.1f}%'
    x = p.get_x() + p.get_width() + 2
    y = p.get_y() + p.get_height() / 2
    ax.annotate(percentage, (x, y), va='center')

plt.tight_layout()
plt.savefig(os.path.join(dir_base, "artigo14_topicos_discurso.svg"), format="svg")
plt.close()

df.to_csv(os.path.join(dir_base, "dados", "corpus_discursos.csv"), index=False)
print("Arquivos de Artigo 14 gerados com sucesso.")
