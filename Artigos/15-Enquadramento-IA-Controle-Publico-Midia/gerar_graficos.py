import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\15-Enquadramento-IA-Controle-Publico-Midia"

# ============================================================
# FIGURA 1: Enquadramentos por Portal (dado principal - chi2)
# ============================================================
categorias = ["MET\nEficiência", "RVO\nOpacidade", "LCC\nLegalidade", "STM\nGovTech"]
conjur = [18, 54, 58, 12]
valor = [78, 10, 12, 18]
jota = [50, 38, 28, 12]

x = np.arange(len(categorias))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 4.8))
b1 = ax.bar(
    x - width,
    conjur,
    width,
    label="Conjur",
    color="#c0392b",
    edgecolor="black",
    linewidth=0.4,
)
b2 = ax.bar(
    x,
    valor,
    width,
    label="Valor Econômico",
    color="#1A365D",
    edgecolor="black",
    linewidth=0.4,
)
b3 = ax.bar(
    x + width,
    jota,
    width,
    label="Jota",
    color="#6b9fd4",
    edgecolor="black",
    linewidth=0.4,
)

for bar in b1:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
for bar in b2:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
for bar in b3:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.8,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )

ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=9)
ax.set_ylabel("Frequência Absoluta", fontsize=10)
ax.set_title(
    "Distribuição dos Enquadramentos sobre IA no Controle Público\npor Portal de Notícias",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
ax.set_ylim(0, 90)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f1 = os.path.join(out_dir, "figura1_enquadramentos_portal.svg")
fig.savefig(f1, format="svg", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Figura 1 salva: {f1}")

# ============================================================
# FIGURA 2: Distribuicao geral dos frames (torta)
# ============================================================
labels_f2 = ["MET\nEficiência", "RVO\nOpacidade", "LCC\nLegalidade", "STM\nGovTech"]
sizes_f2 = [146, 102, 98, 42]
colors_f2 = ["#1A365D", "#c0392b", "#2b579a", "#6b9fd4"]
explode_f2 = (0.05, 0.05, 0.05, 0.05)

fig2, ax2 = plt.subplots(figsize=(5.5, 4.5))
wedges, texts, autotexts = ax2.pie(
    sizes_f2,
    explode=explode_f2,
    labels=labels_f2,
    colors=colors_f2,
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.78,
    textprops={"fontsize": 9},
)
for w in wedges:
    w.set_edgecolor("white")
    w.set_linewidth(0.5)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
ax2.set_title(
    "Distribuição Global dos Enquadramentos sobre IA\nno Controle Público (N = 388)",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
plt.tight_layout()
f2 = os.path.join(out_dir, "figura2_distribuicao_global.svg")
fig2.savefig(f2, format="svg", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"Figura 2 salva: {f2}")

print("Done!")
