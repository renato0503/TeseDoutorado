import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\17-DSR-Contabilidade-Publica-Mapeamento-Artefatos"

# ============================================================
# FIGURA 5: Matriz de Conhecimento de Gregor & Hevner (2013)
# 2x2 com bolhas representando os 42 artigos
# ============================================================
fig5, ax5 = plt.subplots(figsize=(6, 5.5))

ax5.set_xlim(-0.5, 5.5)
ax5.set_ylim(-0.5, 5.5)

# Draw quadrant lines
ax5.axhline(y=2.5, color="black", linewidth=1.2)
ax5.axvline(x=2.5, color="black", linewidth=1.2)

# Quadrant labels
ax5.text(
    1.25,
    4.25,
    "Improvement\n(aprimoramento)\n26 artigos (61,9%)",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#1A365D",
)
ax5.text(
    3.75,
    4.25,
    "Invention\n(inovação)\n7 artigos (16,7%)",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#2b579a",
)
ax5.text(
    1.25,
    1.25,
    "Routine Design\n(rotina)\n5 artigos (11,9%)",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#6b9fd4",
)
ax5.text(
    3.75,
    1.25,
    "Exaptation\n(exaptação)\n4 artigos (9,5%)",
    ha="center",
    va="center",
    fontsize=9,
    fontweight="bold",
    color="#4a8bc2",
)

# Bubble at center of Improvement quadrant
circle1 = plt.Circle(
    (1.25, 3.75), 1.1, color="#1A365D", alpha=0.15, ec="#1A365D", linewidth=1.5
)
ax5.add_patch(circle1)
ax5.text(
    1.25,
    3.75,
    "26\n61,9%",
    ha="center",
    va="center",
    fontsize=11,
    fontweight="bold",
    color="#1A365D",
)

# Small bubble for Invention
circle2 = plt.Circle(
    (3.75, 3.75), 0.6, color="#2b579a", alpha=0.15, ec="#2b579a", linewidth=1.5
)
ax5.add_patch(circle2)
ax5.text(
    3.75,
    3.75,
    "7\n16,7%",
    ha="center",
    va="center",
    fontsize=10,
    fontweight="bold",
    color="#2b579a",
)

# Small bubble for Routine
circle3 = plt.Circle(
    (1.25, 1.25), 0.5, color="#6b9fd4", alpha=0.15, ec="#6b9fd4", linewidth=1.5
)
ax5.add_patch(circle3)
ax5.text(
    1.25,
    1.25,
    "5\n11,9%",
    ha="center",
    va="center",
    fontsize=10,
    fontweight="bold",
    color="#3a7ba0",
)

# Small bubble for Exaptation
circle4 = plt.Circle(
    (3.75, 1.25), 0.45, color="#4a8bc2", alpha=0.15, ec="#4a8bc2", linewidth=1.5
)
ax5.add_patch(circle4)
ax5.text(
    3.75,
    1.25,
    "4\n9,5%",
    ha="center",
    va="center",
    fontsize=10,
    fontweight="bold",
    color="#2b579a",
)

# Axes labels
ax5.text(
    2.5,
    -0.25,
    "Problema (Problem Maturity)",
    ha="center",
    va="top",
    fontsize=10,
    fontweight="bold",
)
ax5.text(
    -0.25,
    2.5,
    "Solução\n(Solution\nMaturity)",
    ha="center",
    va="center",
    fontsize=10,
    fontweight="bold",
    rotation=90,
)

# Tick labels
ax5.text(1.25, -0.12, "Conhecido", ha="center", va="top", fontsize=8, color="#666")
ax5.text(3.75, -0.12, "Novo", ha="center", va="top", fontsize=8, color="#666")
ax5.text(-0.12, 4.25, "Nova", ha="center", va="center", fontsize=8, color="#666")
ax5.text(-0.12, 1.25, "Conhecida", ha="center", va="center", fontsize=8, color="#666")

ax5.set_title(
    "Classificação dos 42 Artigos na Matriz de\nContribuição de Conhecimento de DSR",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax5.axis("off")
plt.tight_layout()
f5 = os.path.join(out_dir, "figura5_matriz_gregor_hevner.png")
fig5.savefig(f5, format="png", dpi=300, bbox_inches="tight")
plt.close(fig5)
print(f"Figura 5 salva: {f5}")

print("Done!")
