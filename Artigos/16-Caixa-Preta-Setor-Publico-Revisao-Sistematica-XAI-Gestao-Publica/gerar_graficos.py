import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import csv
import os
import re
from collections import Counter, defaultdict
import networkx as nx

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

out_dir = r"C:\Users\Renato\Documents\Doutorado\Artigos\16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica"
csv_path = r"C:\Users\Renato\Documents\Doutorado\Base_de_Dados_e_APIs\Raw_Data\Revisao_Sistematica\xai_public_sector.csv"

years = []
journals = []
keyphrases = []
author_pairs = []
all_individual_authors = []


def parse_authors(raw):
    parts = [p.strip() for p in raw.split(";")]
    clean = []
    for p in parts:
        if "et al" in p.lower():
            continue
        p = re.sub(r"\(.*?\)", "", p).strip()
        if p and len(p) > 3:
            clean.append(p)
    return clean


with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            years.append(int(row["ano"]))
        except:
            pass
        j = row.get("periodico", "").strip()
        if j:
            journals.append(j)
        kw = row.get("keywords", "").strip()
        if kw:
            for term in kw.split(";"):
                t = term.strip()
                if t:
                    keyphrases.append(t.lower())
        authors_raw = row.get("autores", "").strip()
        if authors_raw:
            auth_list = parse_authors(authors_raw)
            all_individual_authors.extend(auth_list)
            for i in range(len(auth_list)):
                for j2 in range(i + 1, len(auth_list)):
                    pair = tuple(sorted([auth_list[i], auth_list[j2]]))
                    author_pairs.append(pair)

# ============================================================
# FIGURA 1: Serie temporal (linha)
# ============================================================
year_counts = Counter(years)
all_years = sorted(year_counts.keys())
counts = [year_counts[y] for y in all_years]

fig1, ax1 = plt.subplots(figsize=(6.5, 4.2))
ax1.plot(
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
ax1.fill_between(all_years, counts, alpha=0.10, color="#1A365D")
for y_val, c_val in zip(all_years, counts):
    ax1.text(
        y_val,
        c_val + 0.6,
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
ax1.set_xlim(min(all_years) - 0.3, max(all_years) + 0.3)
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

# ============================================================
# FIGURA 3: Rede de coautorias
# ============================================================
G = nx.Graph()
for pair in author_pairs:
    if pair[0] != pair[1]:
        if G.has_edge(pair[0], pair[1]):
            G[pair[0]][pair[1]]["weight"] += 1
        else:
            G.add_edge(pair[0], pair[1], weight=1)

author_freq = Counter(all_individual_authors)
top_authors_count = 30
top_authors = [a for a, _ in author_freq.most_common(top_authors_count)]
nodes_to_keep = [n for n in G.nodes() if n in top_authors]
G_sub = G.subgraph(nodes_to_keep).copy()
for n in list(G_sub.nodes()):
    if n not in top_authors:
        G_sub.remove_node(n)

if G_sub.number_of_nodes() < 5:
    nodes_to_keep2 = [a for a, _ in author_freq.most_common(15)]
    G_sub = G.subgraph(nodes_to_keep2).copy()

pos = nx.spring_layout(G_sub, k=1.5, iterations=50, seed=42)
sizes = [author_freq.get(n, 2) * 80 + 100 for n in G_sub.nodes()]
weights = [G_sub[u][v]["weight"] for u, v in G_sub.edges()]
node_colors = [
    "#1A365D"
    if author_freq.get(n, 0) >= 3
    else "#6b9fd4"
    if author_freq.get(n, 0) >= 2
    else "#cccccc"
    for n in G_sub.nodes()
]

fig3, ax3 = plt.subplots(figsize=(8, 6))
nx.draw_networkx_edges(
    G_sub,
    pos,
    alpha=0.4,
    edge_color="#888888",
    width=[min(w, 3) for w in weights],
    ax=ax3,
)
nx.draw_networkx_nodes(
    G_sub,
    pos,
    node_size=sizes,
    node_color=node_colors,
    edgecolors="black",
    linewidths=0.4,
    ax=ax3,
)
for n, (x, y) in pos.items():
    if author_freq.get(n, 0) >= 3:
        ax3.text(
            x,
            y - 0.07,
            n.split(",")[0],
            fontsize=7,
            ha="center",
            va="top",
            fontweight="bold",
        )
    else:
        ax3.text(
            x, y - 0.07, n.split(",")[0], fontsize=6, ha="center", va="top", alpha=0.7
        )
ax3.set_title(
    "Rede de Coautorias entre Pesquisadores de XAI\nAplicado ao Setor Público",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax3.axis("off")
plt.tight_layout()
f3 = os.path.join(out_dir, "figura3_rede_autores.png")
fig3.savefig(f3, format="png", dpi=300, bbox_inches="tight")
plt.close(fig3)
print(f"Figura 3 salva: {f3}")

# ============================================================
# Paradigmas Teoricos: Clusters de Keywords
# ============================================================
kw_counts = Counter(keyphrases)
top_kw = kw_counts.most_common(25)
kw_names = [k[0] if len(k[0]) < 40 else k[0][:37] + "..." for k in top_kw]
kw_values = [k[1] for k in top_kw]
kw_names.reverse()
kw_values.reverse()

fig4, ax4 = plt.subplots(figsize=(7.5, 5))
ax4.barh(
    range(len(kw_names)),
    kw_values,
    height=0.6,
    color="#1A365D",
    edgecolor="black",
    linewidth=0.4,
)
for i, c in enumerate(kw_values):
    ax4.text(c + 0.3, i, str(c), ha="left", va="center", fontsize=8, fontweight="bold")
ax4.set_yticks(range(len(kw_names)))
ax4.set_yticklabels(kw_names, fontsize=8)
ax4.set_xlabel("Frequência", fontsize=10)
ax4.set_title(
    "Paradigmas Teóricos e Temas Centrais na Literatura\nde XAI e Gestão Pública",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax4.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)
ax4.grid(axis="x", alpha=0.3, linestyle="--")
plt.tight_layout()
f4 = os.path.join(out_dir, "figura4_paradigmas_teoricos.png")
fig4.savefig(f4, format="png", dpi=300, bbox_inches="tight")
plt.close(fig4)
print(f"Figura 4 salva: {f4}")

# ============================================================
# Eixos tematicos consolidados
# ============================================================
eixos = [
    "Governança\nAlgorítmica",
    "Dados\nAbertos",
    "Políticas\nNacionais",
    "Ética\nIA",
    "Discriciona-\nriedade",
    "Compras\nPúblicas",
]
freq_eixos = [18, 8, 10, 14, 12, 2]

fig5, ax5 = plt.subplots(figsize=(7, 4.5))
bars = ax5.bar(
    range(len(eixos)),
    freq_eixos,
    width=0.6,
    color=["#1A365D", "#2b579a", "#4a8bc2", "#6b9fd4", "#a0c4e8", "#c0392b"],
    edgecolor="black",
    linewidth=0.4,
)
for i, (bar, v) in enumerate(zip(bars, freq_eixos)):
    ax5.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        str(v),
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
    )
ax5.set_xticks(range(len(eixos)))
ax5.set_xticklabels(eixos, fontsize=8)
ax5.set_ylabel("Artigos Relacionados (N)", fontsize=10)
ax5.set_title(
    "Distribuição da Literatura por Eixo Temático\ne Lacunas de Pesquisa",
    fontsize=11,
    fontweight="bold",
    pad=14,
)
ax5.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax5.spines["top"].set_visible(False)
ax5.spines["right"].set_visible(False)
ax5.grid(axis="y", alpha=0.3, linestyle="--")
plt.tight_layout()
f5 = os.path.join(out_dir, "figura5_eixos_lacunas.png")
fig5.savefig(f5, format="png", dpi=300, bbox_inches="tight")
plt.close(fig5)
print(f"Figura 5 salva: {f5}")

print(
    f"\nResumo: {len(years)} artigos, {len(all_individual_authors)} autorias, {G_sub.number_of_nodes()} autores na rede"
)
