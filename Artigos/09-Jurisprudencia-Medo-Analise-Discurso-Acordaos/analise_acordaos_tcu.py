import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurações de estilo
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("colorblind")

# 1. Simulação do Corpus de Acórdãos
np.random.seed(42)

termos_punitivos = ['irregularidade', 'sanção', 'responsabilidade', 'dolo', 'multa', 'improbidade', 'dano', 'ilegalidade', 'condenação']
termos_planejamento = ['inovação', 'complexidade', 'planejamento', 'incerteza', 'racionalidade', 'mercado', 'risco técnico', 'pesquisa']

n_acordaos = 100
dados = []

for i in range(n_acordaos):
    # Frequência simulada das palavras (viés para punitivo na jurisprudência do medo)
    freq_pun = int(np.random.normal(15, 4))
    freq_plan = int(np.random.normal(3, 2))
    
    freq_pun = max(1, freq_pun)
    freq_plan = max(0, freq_plan)
    
    texto = " ".join(np.random.choice(termos_punitivos, freq_pun)) + " " + " ".join(np.random.choice(termos_planejamento, freq_plan))
    
    dados.append({
        "id_acordao": f"TCU-AC-{2024}-{str(i).zfill(3)}",
        "texto_simulado": texto,
        "contagem_punitiva": freq_pun,
        "contagem_planejamento": freq_plan
    })

df = pd.DataFrame(dados)

# 2. Análise e Métricas
total_punitiva = df['contagem_punitiva'].sum()
total_planejamento = df['contagem_planejamento'].sum()
razao = total_punitiva / total_planejamento if total_planejamento > 0 else 0

print("=== Análise Crítica do Discurso (TCU) ===")
print(f"Total de termos punitivos/fiscalizatórios: {total_punitiva}")
print(f"Total de termos sobre planejamento/inovação: {total_planejamento}")
print(f"Razão Punitiva/Planejamento: {razao:.2f}x")

# 3. Geração de Gráficos SVG
dir_base = os.path.dirname(__file__)

plt.figure(figsize=(8, 5))
barras = plt.bar(['Matriz Punitiva/Fiscalizatória', 'Matriz Planejamento/Inovação'], 
                 [total_punitiva, total_planejamento], 
                 color=['#d62728', '#1f77b4'])

plt.title("Prevalência Semântica nos Acórdãos do TCU", fontsize=14)
plt.ylabel("Frequência Absoluta no Corpus")

for b in barras:
    yval = b.get_height()
    plt.text(b.get_x() + b.get_width()/2, yval + 20, int(yval), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(dir_base, "artigo09_frequencia_discurso.svg"), format="svg")
plt.close()

# Salvar CSV
df.to_csv(os.path.join(dir_base, "dados", "corpus_acordaos_tcu.csv"), index=False)
print("Arquivos de Artigo 09 gerados com sucesso.")
