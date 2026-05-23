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

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica"
csv_path = r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Sistematica\xai_public_sector.csv"

years = []
journals = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            y = int(row["ano"])
            years.append(y)
        except:
            pass
        j = row.get("periodico", "").strip()
        if j:
            journals.append(j)

# ============================================================
# FIGURA 1: Publicacoes por Ano
# ============================================================
year_counts = Counter(years)
all_years = sorted(year_counts.keys())
counts = [year_counts[y] for y in all_years]

fig1, ax1 = plt.subplots(figsize=(6, 4.2))
ax1.bar(all_years, counts, width=0.6, color="#1A365D", edgecolor="black", linewidth=0.4)
for y_val, c_val in zip(all_years, counts):
    ax1.text(
        y_val,
        c_val + 0.3,
        str(c_val),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax1.set_xlabel("Ano", fontsize=10)
ax1.set_ylabel("Número de Publicações", fontsize=10)
ax1.set_title(
    "Evolução Temporal das Publicações sobre XAI\nno Setor Público (2017-2026)",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax1.set_xticks(all_years)
ax1.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f1 = os.path.join(out_dir, "figura1_evolucao_publicacoes.png")
fig1.savefig(f1, format="png", dpi=300, bbox_inches="tight")
plt.close(fig1)
print(f"Figura 1 salva: {f1}")

# ============================================================
# FIGURA 2: Top 10 Periodicos
# ============================================================
journal_counts = Counter(journals)
top10 = journal_counts.most_common(10)
j_names = [j[0] if len(j[0]) < 50 else j[0][:47] + "..." for j in top10]
j_counts = [j[1] for j in top10]
j_names.reverse()
j_counts.reverse()

fig2, ax2 = plt.subplots(figsize=(7, 4.5))
ax2.barh(
    range(len(j_names)),
    j_counts,
    height=0.6,
    color="#2b579a",
    edgecolor="black",
    linewidth=0.4,
)
for i, c in enumerate(j_counts):
    ax2.text(c + 0.2, i, str(c), ha="left", va="center", fontsize=8, fontweight="bold")
ax2.set_yticks(range(len(j_names)))
ax2.set_yticklabels(j_names, fontsize=7)
ax2.set_xlabel("Número de Artigos", fontsize=10)
ax2.set_title(
    "Periódicos com Maior Número de Publicações\nsobre XAI no Setor Público",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax2.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="x", alpha=0.3, linestyle="--")
plt.tight_layout()
f2 = os.path.join(out_dir, "figura2_periodicos_top.png")
fig2.savefig(f2, format="png", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"Figura 2 salva: {f2}")

print("Done! Total records:", len(years))
