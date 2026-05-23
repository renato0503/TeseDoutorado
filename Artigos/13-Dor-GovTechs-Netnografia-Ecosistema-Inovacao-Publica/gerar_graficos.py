import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\13-Dor-GovTechs-Netnografia-Ecosistema-Inovacao-Publica"

# ============================================================
# FIGURA 1: Distribuicao das Barreiras por Ator Social
# ============================================================
categorias = ["C1: Regulatório", "C2: Financeiro", "C3: Técnica", "C4: Jurídica"]
fundador = [8, 7, 5, 5]
gestor = [4, 3, 6, 5]
consultor = [4, 4, 3, 6]

x = np.arange(len(categorias))
width = 0.25

fig, ax = plt.subplots(figsize=(7, 4.5))
bars1 = ax.bar(
    x - width,
    fundador,
    width,
    label="Fundador",
    color="#1A365D",
    edgecolor="black",
    linewidth=0.4,
)
bars2 = ax.bar(
    x,
    gestor,
    width,
    label="Gestor Público",
    color="#2b579a",
    edgecolor="black",
    linewidth=0.4,
)
bars3 = ax.bar(
    x + width,
    consultor,
    width,
    label="Consultor/Especialista",
    color="#6b9fd4",
    edgecolor="black",
    linewidth=0.4,
)

for bar in bars1:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
for bar in bars2:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(int(bar.get_height())),
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
for bar in bars3:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
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
    "Distribuição das Barreiras Transacionais por Categoria de Ator Social",
    fontsize=11,
    fontweight="bold",
    pad=12,
)
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
ax.set_ylim(0, 10.5)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f1 = os.path.join(out_dir, "figura1_barras_ator.svg")
fig.savefig(f1, format="svg", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"Figura 1 salva: {f1}")

# ============================================================
# FIGURA 2: Indices Sinteticos ILRF e IRTI
# ============================================================
atores = ["Fundador", "Gestor\nPúblico", "Consultor\nEspecialista"]
ilrf = [60.00, 38.89, 47.06]
irti = [88.00, 77.78, 82.35]

x2 = np.arange(len(atores))
width2 = 0.30

fig2, ax2 = plt.subplots(figsize=(6, 4.5))
bars_ilrf = ax2.bar(
    x2 - width2 / 2,
    ilrf,
    width2,
    label="ILRF (%)",
    color="#1A365D",
    edgecolor="black",
    linewidth=0.4,
)
bars_irti = ax2.bar(
    x2 + width2 / 2,
    irti,
    width2,
    label="IRTI (%)",
    color="#c0392b",
    edgecolor="black",
    linewidth=0.4,
)

for bar in bars_ilrf:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}%",
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )
for bar in bars_irti:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{bar.get_height():.1f}%",
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
    )

ax2.set_xticks(x2)
ax2.set_xticklabels(atores, fontsize=9)
ax2.set_ylabel("Percentual (%)", fontsize=10)
ax2.set_title(
    "Índices Sintéticos de Latência (ILRF) e Risco Transacional (IRTI)",
    fontsize=11,
    fontweight="bold",
    pad=12,
)
ax2.legend(fontsize=9, loc="upper right", framealpha=0.9)
ax2.set_ylim(0, 100)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f2 = os.path.join(out_dir, "figura2_indices_sinteticos.svg")
fig2.savefig(f2, format="svg", dpi=300, bbox_inches="tight")
plt.close(fig2)
print(f"Figura 2 salva: {f2}")

print("Done!")
