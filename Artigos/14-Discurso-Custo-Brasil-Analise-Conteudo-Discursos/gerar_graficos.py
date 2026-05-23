import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\14-Discurso-Custo-Brasil-Analise-Conteudo-Discursos"

# ============================================================
# FIGURA 1: Enquadramentos por Tipo de Ator
# ============================================================
categorias = [
    "F1: Eficiência",
    "F2: Ônus\nRegulatório",
    "F3: Barreira\nà Inovação",
    "F4: Responsab.\nFiscal",
]
governamental = [24, 13, 12, 11]
empresarial = [15, 22, 18, 5]

x = np.arange(len(categorias))
width = 0.30

fig, ax = plt.subplots(figsize=(6.5, 4.5))
bars1 = ax.bar(
    x - width / 2,
    governamental,
    width,
    label="Governamental",
    color="#1A365D",
    edgecolor="black",
    linewidth=0.4,
)
bars2 = ax.bar(
    x + width / 2,
    empresarial,
    width,
    label="Empresarial",
    color="#c0392b",
    edgecolor="black",
    linewidth=0.4,
)

for bar in bars1:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
for bar in bars2:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )

ax.set_xticks(x)
ax.set_xticklabels(categorias, fontsize=9)
ax.set_ylabel("Frequência Absoluta", fontsize=10)
ax.set_title(
    "Distribuição dos Enquadramentos Discursivos sobre o Custo Brasil\npor Tipo de Ator",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax.legend(fontsize=9, loc="upper right", framealpha=0.9)
ax.set_ylim(0, 30)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f1 = os.path.join(out_dir, "figura1_enquadramentos_ator.svg")
fig.savefig(f1, format="svg", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Figura 1 salva: {f1}")

print("Done!")
