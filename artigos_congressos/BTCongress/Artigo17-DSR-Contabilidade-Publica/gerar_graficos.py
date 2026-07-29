import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import csv
import os
from collections import Counter

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\17-DSR-Contabilidade-Publica-Mapeamento-Artefatos"
csv_path = r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Sistematica\dsr_public_accounting.csv"

years = []
citations = []
journals = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            y = int(row["ano"])
            years.append(y)
        except:
            pass
        try:
            c = int(row["citacoes"])
            citations.append(c)
        except:
            citations.append(0)
        j = row.get("periodico", "").strip()
        if j:
            journals.append(j)

# ============================================================
# FIGURA 1: Artefatos por tipo (barras)
# Dados simulados baseados na Tabela 2 do artigo
# ============================================================
tipos = [
    "Sistemas de\nInformação",
    "Frameworks\nConceituais",
    "IA e\nAprendizado",
    "Ferramentas de\nAnálise",
    "Metodologias\ne Processos",
]
freq_tipos = [15, 12, 8, 5, 2]
cores_tipos = ["#1A365D", "#2b579a", "#4a8bc2", "#6b9fd4", "#a0c4e8"]

fig1, ax1 = plt.subplots(figsize=(7, 4.5))
bars = ax1.bar(
    range(len(tipos)),
    freq_tipos,
    width=0.6,
    color=cores_tipos,
    edgecolor="black",
    linewidth=0.4,
)
for i, (bar, v) in enumerate(zip(bars, freq_tipos)):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{v} ({v / 42 * 100:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax1.set_xticks(range(len(tipos)))
ax1.set_xticklabels(tipos, fontsize=8)
ax1.set_ylabel("Número de Artigos", fontsize=10)
ax1.set_title(
    "Tipologia dos Artefatos de DSR na Contabilidade\nPública (n = 42)",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f1 = os.path.join(out_dir, "figura1_tipos_artefatos.png")
fig1.savefig(f1, format="png", dpi=300, bbox_inches="tight")
plt.close(fig1)
print(f"Figura 1 salva: {f1}")

# ============================================================
# FIGURA 2: Metodos de avaliacao (barras horizontais)
# Dados da Tabela 3
# ============================================================
metodos = [
    "Estudo de Caso\n(Naturalista)",
    "Experimento/\nSimulação",
    "Especialistas\n(Qualitativa)",
    "Métodos Mistos\n(Híbrida)",
    "Survey\n(Quantitativa)",
]
freq_met = [14, 11, 9, 5, 3]
metodos.reverse()
freq_met.reverse()

fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.barh(
    range(len(metodos)),
    freq_met,
    height=0.6,
    color="#2b579a",
    edgecolor="black",
    linewidth=0.4,
)
for i, c in enumerate(freq_met):
    ax2.text(c + 0.3, i, str(c), ha="left", va="center", fontsize=9, fontweight="bold")
ax2.set_yticks(range(len(metodos)))
ax2.set_yticklabels(metodos, fontsize=8)
ax2.set_xlabel("Número de Artigos (n = 42)", fontsize=10)
ax2.set_title(
    "Métodos de Avaliação Empregados nos\nEstudos de DSR",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax2.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="x", alpha=0.3, linestyle="--")
plt.tight_layout()
f2 = os.path.join(out_dir, "figura2_metodos_avaliacao.png")
fig2.savefig(f2, format="png", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"Figura 2 salva: {f2}")

# ============================================================
# FIGURA 3: Evolucao temporal (linha)
# ============================================================
year_counts = Counter(years)
all_years = sorted(year_counts.keys())
counts = [year_counts[y] for y in all_years]

fig3, ax3 = plt.subplots(figsize=(6.5, 4.2))
ax3.plot(
    all_years,
    counts,
    marker="o",
    linestyle="-",
    linewidth=2,
    color="#1A365D",
    markersize=7,
    markerfacecolor="#1A365D",
    markeredgecolor="white",
    markeredgewidth=0.8,
)
ax3.fill_between(all_years, counts, alpha=0.10, color="#1A365D")
for y_val, c_val in zip(all_years, counts):
    ax3.text(
        y_val,
        c_val + 0.4,
        str(c_val),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax3.set_xlabel("Ano", fontsize=10)
ax3.set_ylabel("Número de Publicações", fontsize=10)
ax3.set_title(
    "Evolução Temporal das Publicações de DSR\nem Contabilidade Pública (2004-2026)",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax3.set_xticks(all_years)
ax3.set_xticklabels([str(y) if y % 2 == 0 else "" for y in all_years], fontsize=9)
ax3.set_xlim(min(all_years) - 0.5, max(all_years) + 0.5)
ax3.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f3 = os.path.join(out_dir, "figura3_evolucao_temporal.png")
fig3.savefig(f3, format="png", dpi=300, bbox_inches="tight")
plt.close(fig3)
print(f"Figura 3 salva: {f3}")

# ============================================================
# FIGURA 4: Distribuicao geografica (pizza)
# ============================================================
regioes = ["Europa", "América do\nNorte", "Ásia", "América\nLatina", "Oceania\nÁfrica"]
freq_reg = [16, 11, 7, 4, 4]
cores_reg = ["#1A365D", "#2b579a", "#4a8bc2", "#c0392b", "#6b9fd4"]

fig4, ax4 = plt.subplots(figsize=(5.5, 4.5))
wedges, texts, autotexts = ax4.pie(
    freq_reg,
    labels=regioes,
    colors=cores_reg,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.75,
    explode=[0.03] * 5,
    textprops={"fontsize": 9},
)
for w in wedges:
    w.set_edgecolor("white")
    w.set_linewidth(0.5)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
ax4.set_title(
    "Distribuição Geográfica dos Estudos\nde DSR em Contabilidade Pública",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
plt.tight_layout()
f4 = os.path.join(out_dir, "figura4_distribuicao_geografica.png")
fig4.savefig(f4, format="png", dpi=300, bbox_inches="tight")
plt.close(fig4)
print(f"Figura 4 salva: {f4}")

print(f"Done! Artigos: {len(years)}, Citações totais: {sum(citations)}")
