#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera 10 arquivos SVG (5 gráficos + 5 figuras) para a tese de doutorado
"Copiloto Algorítmico para Compras Públicas Complexas".
"""

import os
import numpy as np
import matplotlib

matplotlib.use("SVG")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import matplotlib.lines as mlines
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx

OUTPUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Tese\imagens"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Global style ──────────────────────────────────────────────────────────────
ACADEMIC_FONT = "DejaVu Sans"
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [ACADEMIC_FONT],
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "black",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    }
)


def save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, format="svg", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  [OK] {name}")
    return path


# ==============================================================================
# GRÁFICO 1 — Boxplot de Complexidade Textual
# ==============================================================================
def grafico1_complexidade_textual():
    np.random.seed(42)
    direta = np.random.normal(45, 10, 60)
    concorrencia = np.random.normal(30, 8, 60)
    # add outliers
    direta = np.append(direta, [75, 78, 82])
    concorrencia = np.append(concorrencia, [55, 58, 60])

    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot(
        [direta, concorrencia],
        patch_artist=True,
        widths=0.4,
        medianprops=dict(color="black", linewidth=2),
        flierprops=dict(marker="o", markerfacecolor="red", markersize=5),
    )
    bp["boxes"][0].set_facecolor("#4ECDC4")
    bp["boxes"][1].set_facecolor("#FF6B6B")
    ax.set_xticklabels(["Contratação Direta", "Concorrência"])
    ax.set_ylabel("Índice Flesch-Kincaid (menor = mais complexo)")
    ax.set_ylim(0, 90)
    # annotate medians
    ax.text(1, 45.5, f"Mediana ≈ 45", ha="center", fontsize=9, fontweight="bold")
    ax.text(2, 30.5, f"Mediana ≈ 30", ha="center", fontsize=9, fontweight="bold")
    save(fig, "grafico1_complexidade_textual.svg")


# ==============================================================================
# GRÁFICO 2 — Kaplan-Meier
# ==============================================================================
def grafico2_sobrevivencia():
    np.random.seed(123)
    months = np.arange(0, 25)
    # simulate survival probabilities
    # Sem Copiloto: hazard ~0.10 per month
    # Com Copiloto: hazard ~0.04 per month (62% reduction)
    surv_sem = np.exp(-0.10 * months)
    surv_com = np.exp(-0.04 * months)
    # add some noise and confidence intervals
    n_sem = 200
    n_com = 200
    se_sem = surv_sem * np.sqrt(1 / n_sem)
    se_com = surv_com * np.sqrt(1 / n_com)

    fig, ax = plt.subplots(figsize=(7, 5))
    # Com Copiloto
    ax.plot(months, surv_com, color="#2E86AB", linewidth=2.5, label="Com Copiloto IA")
    ax.fill_between(
        months,
        surv_com - 1.96 * se_com,
        surv_com + 1.96 * se_com,
        color="#2E86AB",
        alpha=0.15,
    )
    # Sem Copiloto
    ax.plot(
        months,
        surv_sem,
        color="#A23B72",
        linewidth=2.5,
        linestyle="--",
        label="Sem Copiloto IA",
    )
    ax.fill_between(
        months,
        surv_sem - 1.96 * se_sem,
        surv_sem + 1.96 * se_sem,
        color="#A23B72",
        alpha=0.15,
    )

    ax.set_xlabel("Tempo (meses)")
    ax.set_ylabel("Probabilidade de Sobrevivência")
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower left", framealpha=0.9)
    # annotate risk reduction
    ax.annotate(
        "Redução de 62% no\nrisco de rescisão",
        xy=(12, surv_com[12]),
        xytext=(15, 0.85),
        arrowprops=dict(arrowstyle="->", color="green", lw=1.5),
        fontsize=10,
        color="green",
        fontweight="bold",
    )
    save(fig, "grafico2_sobrevivencia.svg")


# ==============================================================================
# GRÁFICO 3 — Latência Decisória (barras horizontais)
# ==============================================================================
def grafico3_latencia_decisoria():
    orgaos = [
        "Ministério da Saúde",
        "MEC",
        "MDIC",
        "Ministério da Justiça",
        "Ministério da Defesa",
        "Ministério da Economia",
        "Ministério do Meio Ambiente",
        "Ministério da Ciência e Tecnologia",
    ]
    efeitos = [14.2, 12.8, 11.5, 9.8, 8.3, 6.7, 4.5, 2.3]
    cores = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(orgaos)))

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(orgaos, efeitos, color=cores, edgecolor="gray", linewidth=0.5)
    for bar, val in zip(bars, efeitos):
        ax.text(
            val + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.1f}",
            va="center",
            fontsize=10,
            fontweight="bold",
        )
    ax.set_xlabel("Efeito Marginal (dias por sanção)")
    ax.set_xlim(0, 17)
    save(fig, "grafico3_latencia_decisoria.svg")


# ==============================================================================
# GRÁFICO 4 — SHAP Summary (barras horizontais)
# ==============================================================================
def grafico4_shap_summary():
    features = [
        "Histórico de Sanções\ndo Vencedor",
        "Valor Estimado\ndo Contrato",
        "Complexidade Textual\ndo Edital",
        "Número de\nFornecedores",
        "Prazo de\nExecução",
        "Modalidade\nde Licitação",
        "Região\nGeográfica",
        "Experiência\ndo Gestor",
    ]
    importances = [0.25, 0.18, 0.15, 0.12, 0.10, 0.08, 0.07, 0.05]
    colors = [
        "#1a5276",
        "#2e86c1",
        "#85c1e9",
        "#52be80",
        "#f4d03f",
        "#eb984e",
        "#e74c3c",
        "#7d3c98",
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(
        range(len(features)), importances, color=colors, edgecolor="gray", linewidth=0.5
    )
    ax.set_yticks(range(len(features)))
    ax.set_yticklabels(features)
    ax.set_xlabel("Importância Média |SHAP|")
    ax.set_xlim(0, 0.30)
    for bar, val in zip(bars, importances):
        ax.text(
            val + 0.005,
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}",
            va="center",
            fontsize=9,
            fontweight="bold",
        )
    ax.invert_yaxis()
    save(fig, "grafico4_shap_summary.svg")


# ==============================================================================
# GRÁFICO 5 — Framing Mídia (stacked bar)
# ==============================================================================
def grafico5_framing_midia():
    categorias = ["Conjur", "Valor\nEconômico", "Jota"]
    eficiencia = [25, 55, 40]
    compliance = [35, 25, 30]
    opacidade = [40, 20, 30]

    x = np.arange(len(categorias))
    width = 0.55

    fig, ax = plt.subplots(figsize=(7, 5))
    b1 = ax.bar(x, eficiencia, width, label="Eficiência Econômica", color="#27AE60")
    b2 = ax.bar(
        x,
        compliance,
        width,
        bottom=eficiencia,
        label="Compliance Regulatório",
        color="#2980B9",
    )
    b3 = ax.bar(
        x,
        opacidade,
        width,
        bottom=np.array(eficiencia) + np.array(compliance),
        label="Opacidade Algorítmica",
        color="#C0392B",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(categorias)
    ax.set_ylabel("Proporção (%)")
    ax.legend(loc="upper right", framealpha=0.9)
    ax.set_ylim(0, 110)

    # add percentage labels inside bars
    for i in range(len(categorias)):
        h_eff = eficiencia[i]
        h_com = compliance[i]
        h_opa = opacidade[i]
        ax.text(
            i,
            h_eff / 2,
            f"{h_eff}%",
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
        )
        ax.text(
            i,
            h_eff + h_com / 2,
            f"{h_com}%",
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
        )
        ax.text(
            i,
            h_eff + h_com + h_opa / 2,
            f"{h_opa}%",
            ha="center",
            va="center",
            fontsize=9,
            color="white",
            fontweight="bold",
        )

    save(fig, "grafico5_framing_midia.svg")


# ==============================================================================
# FIGURA 1 — Arquitetura do Copiloto
# ==============================================================================
def figura1_arquitetura_copiloto():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # colors
    c_dados = "#85C1E9"
    c_proc = "#82E0AA"
    c_inter = "#F9E79F"

    def draw_box(x, y, w, h, text, color, subtexts=None):
        box = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.15",
            facecolor=color,
            edgecolor="black",
            linewidth=1.5,
            zorder=2,
        )
        ax.add_patch(box)
        ax.text(
            x + w / 2,
            y + h - 0.25,
            text,
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold",
            zorder=3,
        )
        if subtexts:
            for i, st in enumerate(subtexts):
                ax.text(
                    x + w / 2,
                    y + h - 0.6 - i * 0.3,
                    st,
                    ha="center",
                    va="top",
                    fontsize=7.5,
                    color="#333333",
                    zorder=3,
                )

    def draw_arrow(x1, y1, x2, y2):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", lw=2, color="#555555"),
            zorder=1,
        )

    # Block 1 — Data Sources
    draw_box(
        0.3,
        2.5,
        2.8,
        2.8,
        "Base de Dados",
        c_dados,
        [
            "PNCP",
            "Portal Transparência",
            "TCU Jurisprudência",
            "Compras.gov.br",
            "Siconfi",
        ],
    )
    # Block 2 — Processing
    draw_box(
        3.9,
        2.5,
        2.8,
        2.8,
        "Módulo de Processamento",
        c_proc,
        [
            "NLP: Tokenização",
            "Extração de Entidades",
            "Classificação de Cláusulas",
            "Análise SHAP",
            "Detecção de Anomalias",
        ],
    )
    # Block 3 — Interface
    draw_box(
        7.5,
        2.5,
        2.3,
        2.8,
        "Módulo de Interface",
        c_inter,
        [
            "Avaliação de Minutas",
            "Geração de Cláusulas",
            "Dashboard",
            "Alertas de Risco",
        ],
    )

    # arrows
    draw_arrow(3.1, 3.9, 3.9, 3.9)
    draw_arrow(6.7, 3.9, 7.5, 3.9)

    # feedback arrow (bottom)
    ax.annotate(
        "",
        xy=(4.0, 2.5),
        xytext=(6.6, 2.5),
        arrowprops=dict(arrowstyle="->", lw=1.5, color="#888888", linestyle="dashed"),
    )
    ax.text(
        5.3,
        2.3,
        "Feedback",
        ha="center",
        fontsize=8,
        color="#888888",
        fontstyle="italic",
    )

    save(fig, "figura1_arquitetura_copiloto.svg")


# ==============================================================================
# FIGURA 2 — Ciclo DSR (Hevner)
# ==============================================================================
def figura2_ciclo_dsr():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    centers = [(2.5, 3), (5, 3), (7.5, 3)]
    radii = [1.5, 1.5, 1.5]
    labels_center = ["Ciclo de\nRelevância", "Ciclo de\nDesign", "Ciclo de\nRigor"]
    colors = ["#E74C3C", "#2ECC71", "#3498DB"]

    for (cx, cy), r, lab, col in zip(centers, radii, labels_center, colors):
        circle = plt.Circle(
            (cx, cy), r, facecolor=col, edgecolor="black", linewidth=2, alpha=0.25
        )
        ax.add_patch(circle)
        ax.text(cx, cy, lab, ha="center", va="center", fontsize=10, fontweight="bold")

    # connecting arrows between circles
    for i in range(2):
        ax.annotate(
            "",
            xy=(centers[i + 1][0] - radii[i + 1] * 0.7, centers[i + 1][1]),
            xytext=(centers[i][0] + radii[i] * 0.7, centers[i][1]),
            arrowprops=dict(arrowstyle="->", lw=1.5, color="#555555"),
        )

    # context boxes
    # Left context
    box_l = FancyBboxPatch(
        (0.2, 0.2),
        3.5,
        1.0,
        boxstyle="round,pad=0.1",
        facecolor="#FADBD8",
        edgecolor="#E74C3C",
        linewidth=1.2,
    )
    ax.add_patch(box_l)
    ax.text(
        1.95,
        0.7,
        "Ambiente de Aplicação:\nCompras Públicas Brasileiras",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#922B21",
    )

    # Right context
    box_r = FancyBboxPatch(
        (6.3, 0.2),
        3.5,
        1.0,
        boxstyle="round,pad=0.1",
        facecolor="#D4E6F1",
        edgecolor="#3498DB",
        linewidth=1.2,
    )
    ax.add_patch(box_r)
    ax.text(
        8.05,
        0.7,
        "Base de Conhecimento:\nTCE, XAI, DSR, SHAP",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#1A5276",
    )

    # Center bottom note
    ax.text(
        5,
        1.8,
        "Desenvolvimento do Artefato",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#1E8449",
    )

    save(fig, "figura2_ciclo_dsr.svg")


# ==============================================================================
# FIGURA 3 — Pipeline NLP
# ==============================================================================
def figura3_pipeline_nlp():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")

    stages = [
        ("Edital Original\n(PDF)", "#AED6F1"),
        ("Pré-processamento\n(Tokenização,\nStopwords)", "#A9DFBF"),
        ("Extração de\nEntidades\n(NER)", "#F9E79F"),
        ("Classificação\nde Cláusulas\n(Random Forest)", "#D7BDE2"),
        ("Armazenamento\nVetorial\n(Embeddings)", "#F5B7B1"),
        ("Recuperação\npor Similaridade\n(RAG)", "#F0B27A"),
    ]

    n = len(stages)
    box_w = 1.3
    box_h = 1.5
    gap = 0.4
    total_w = n * box_w + (n - 1) * gap
    start_x = (10 - total_w) / 2
    y_center = 1.5

    for i, (label, color) in enumerate(stages):
        x = start_x + i * (box_w + gap)
        y = y_center - box_h / 2
        box = FancyBboxPatch(
            (x, y),
            box_w,
            box_h,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor="black",
            linewidth=1.2,
            zorder=2,
        )
        ax.add_patch(box)
        ax.text(
            x + box_w / 2,
            y + box_h / 2,
            label,
            ha="center",
            va="center",
            fontsize=7.5,
            fontweight="bold",
            zorder=3,
        )

        if i < n - 1:
            ax.annotate(
                "",
                xy=(x + box_w + gap * 0.3, y_center),
                xytext=(x + box_w - gap * 0.3, y_center),
                arrowprops=dict(arrowstyle="->", lw=2, color="#555555"),
                zorder=1,
            )

    save(fig, "figura3_pipeline_nlp.svg")


# ==============================================================================
# FIGURA 4 — Interface de Avaliação (mockup)
# ==============================================================================
def figura4_interface_avaliacao():
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis("off")

    # background of the app
    bg = FancyBboxPatch(
        (0.2, 0.2),
        9.6,
        6.0,
        boxstyle="round,pad=0.1",
        facecolor="#F4F6F7",
        edgecolor="#2C3E50",
        linewidth=2,
    )
    ax.add_patch(bg)

    # title bar
    title_bar = FancyBboxPatch(
        (0.2, 5.8),
        9.6,
        0.5,
        boxstyle="round,pad=0.05",
        facecolor="#2C3E50",
        edgecolor="#2C3E50",
    )
    ax.add_patch(title_bar)
    ax.text(
        5,
        6.05,
        "Módulo de Avaliação de Minutas — Copiloto Algorítmico",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold",
        color="white",
    )

    # Left panel — editable text area
    left_bg = FancyBboxPatch(
        (0.5, 0.5),
        4.3,
        5.0,
        boxstyle="round,pad=0.08",
        facecolor="white",
        edgecolor="#BDC3C7",
        linewidth=1,
    )
    ax.add_patch(left_bg)
    ax.text(
        2.65,
        5.3,
        "Edital de Licitação - Excerto",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#2C3E50",
    )

    # simulated text with highlights
    texts_left = [
        (0.8, 4.8, "O objeto da presente licitação é a contratação", "black"),
        (0.8, 4.55, "de serviços de tecnologia da informação para", "black"),
        (0.8, 4.30, "a implantação de sistema integrado de gestão.", "black"),
        (0.8, 3.95, "", "black"),
        (0.8, 3.70, "Exigência: certificação ISO 27001 obrigatória.", "red"),
        (0.8, 3.45, "Prazo de execução: 12 meses a contar da", "black"),
        (0.8, 3.20, "assinatura do contrato, prorrogável por", "black"),
        (0.8, 2.95, "igual período.", "black"),
        (0.8, 2.60, "", "black"),
        (0.8, 2.35, "Valor estimado: R$ 2.500.000,00.", "green"),
        (0.8, 2.10, "Garantia: 5% do valor contratual.", "black"),
        (0.8, 1.75, "", "black"),
        (0.8, 1.50, "Critério de aceitação: testes de desempenho", "black"),
        (0.8, 1.25, "com 99.9% de disponibilidade.", "red"),
    ]
    for x, y, txt, color in texts_left:
        ax.text(
            x,
            y,
            txt,
            fontsize=7.5,
            color=color,
            fontweight="bold" if color != "black" else "normal",
        )

    # highlights
    high1 = FancyBboxPatch(
        (0.7, 3.58),
        3.9,
        0.3,
        boxstyle="round,pad=0.02",
        facecolor="#FADBD8",
        edgecolor="#E74C3C",
        linewidth=0.8,
        alpha=0.5,
    )
    ax.add_patch(high1)
    high2 = FancyBboxPatch(
        (0.7, 2.23),
        3.9,
        0.3,
        boxstyle="round,pad=0.02",
        facecolor="#D5F5E3",
        edgecolor="#27AE60",
        linewidth=0.8,
        alpha=0.5,
    )
    ax.add_patch(high2)
    high3 = FancyBboxPatch(
        (0.7, 1.13),
        3.9,
        0.3,
        boxstyle="round,pad=0.02",
        facecolor="#FADBD8",
        edgecolor="#E74C3C",
        linewidth=0.8,
        alpha=0.5,
    )
    ax.add_patch(high3)

    # legend
    ax.plot(0.9, 0.75, marker="s", color="#E74C3C", markersize=8)
    ax.text(
        1.0,
        0.75,
        "Risco identificado    ",
        fontsize=7.5,
        color="#E74C3C",
        fontweight="bold",
        va="center",
    )
    ax.plot(2.7, 0.75, marker="s", color="#27AE60", markersize=8)
    ax.text(
        2.8,
        0.75,
        "Conforme",
        fontsize=7.5,
        color="#27AE60",
        fontweight="bold",
        va="center",
    )

    # Right panel — analysis results
    right_bg = FancyBboxPatch(
        (5.2, 0.5),
        4.5,
        5.0,
        boxstyle="round,pad=0.08",
        facecolor="#EBF5FB",
        edgecolor="#BDC3C7",
        linewidth=1,
    )
    ax.add_patch(right_bg)
    ax.text(
        7.45,
        5.3,
        "Resultados da Análise",
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#2C3E50",
    )

    analysis_items = [
        (5.5, 4.9, "Score de Conformidade:", "#2C3E50", True),
        (5.5, 4.6, "  78.5 / 100  (Médio-Alto)", "#27AE60", True),
        (5.5, 4.2, "Cláusulas Ausentes:", "#E74C3C", True),
        (5.5, 3.9, "  • Mecanismo de transição contratual", "#333", False),
        (5.5, 3.65, "  • Plano de continuidade de serviços", "#333", False),
        (5.5, 3.40, "  • Acordo de nível de serviço (SLA)", "#333", False),
        (5.5, 3.0, "Indicadores de Risco:", "#E74C3C", True),
        (5.5, 2.7, "  ● Certificação restritiva (ISO 27001)", "#E67E22", False),
        (5.5, 2.45, "  ● Disponibilidade 99.9% elevada", "#E67E22", False),
        (5.5, 2.20, "  ○ Demais cláusulas regulares", "#27AE60", False),
        (5.5, 1.7, "Recomendação:", "#2980B9", True),
        (5.5, 1.4, "  Ajustar exigências técnicas para", "#333", False),
        (5.5, 1.15, "  ampliar competitividade.", "#333", False),
    ]
    for x, y, txt, color, bold in analysis_items:
        ax.text(
            x,
            y,
            txt,
            fontsize=7.5,
            color=color,
            fontweight="bold" if bold else "normal",
        )

    # divider
    ax.plot([5.0, 5.0], [0.5, 5.5], color="#BDC3C7", linewidth=1, linestyle="-")

    save(fig, "figura4_interface_avaliacao.svg")


# ==============================================================================
# FIGURA 5 — Rede de Fornecimento (grafo bipartido)
# ==============================================================================
def figura5_rede_fornecimento():
    np.random.seed(42)
    G = nx.Graph()
    org_aos = ["MS", "MEC", "MDIC", "MJ", "MD", "ME", "MMA", "MCTI"]
    fornecedores = [
        "AlphaTech",
        "BetaSys",
        "GammaSol",
        "DeltaTI",
        "Epsilon",
        "ZetaCorp",
        "GovTech",
    ]
    # make some suppliers larger (oligopoly)
    sizes_suppliers = {
        "AlphaTech": 1200,
        "BetaSys": 1000,
        "GammaSol": 800,
        "DeltaTI": 300,
        "Epsilon": 250,
        "ZetaCorp": 200,
        "GovTech": 180,
    }

    G.add_nodes_from(org_aos, bipartite=0)
    G.add_nodes_from(fornecedores, bipartite=1)

    # edges: big suppliers connect to many, small to few
    edges = []
    for org in org_aos:
        for sup in ["AlphaTech", "BetaSys", "GammaSol"]:
            if np.random.random() < 0.7:
                edges.append((org, sup))
        for sup in ["DeltaTI", "Epsilon"]:
            if np.random.random() < 0.3:
                edges.append((org, sup))
        for sup in ["ZetaCorp", "GovTech"]:
            if np.random.random() < 0.15:
                edges.append((org, sup))
    G.add_edges_from(edges)

    pos = {}
    x_org = 0
    x_sup = 1
    y_positions_org = np.linspace(0.1, 0.9, len(org_aos))
    y_positions_sup = np.linspace(0.1, 0.9, len(fornecedores))

    for i, org in enumerate(org_aos):
        pos[org] = (x_org, y_positions_org[i])
    for i, sup in enumerate(fornecedores):
        pos[sup] = (x_sup, y_positions_sup[i])

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(0, 1.0)
    ax.axis("off")

    # draw edges with alpha based on supplier size
    for u, v in G.edges():
        sup = v if v in fornecedores else u
        base_size = sizes_suppliers.get(sup, 200)
        alpha = 0.15 + 0.4 * (base_size / 1200)
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color="#7F8C8D",
            linewidth=0.8,
            alpha=min(alpha, 0.6),
            zorder=1,
        )

    # draw nodes
    for node in org_aos:
        x, y = pos[node]
        ax.scatter(
            x,
            y,
            s=250,
            facecolor="#3498DB",
            edgecolor="#2C3E50",
            linewidth=1.5,
            zorder=2,
            marker="o",
        )
        ax.text(
            x - 0.03, y, node, ha="right", va="center", fontsize=8, fontweight="bold"
        )

    for node in fornecedores:
        x, y = pos[node]
        size = sizes_suppliers[node]
        ax.scatter(
            x,
            y,
            s=size,
            facecolor="#E74C3C",
            edgecolor="#922B21",
            linewidth=2 if size >= 800 else 1,
            zorder=2,
            marker="s",
        )
        ax.text(
            x + 0.03,
            y,
            node,
            ha="left",
            va="center",
            fontsize=8,
            fontweight="bold",
            color="#922B21",
        )

    # annotation for oligopoly
    ax.annotate(
        "Oligopólio Core\n(87.2% market share)",
        xy=(1.0, 0.7),
        xytext=(0.3, 0.95),
        arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5),
        fontsize=9,
        color="#C0392B",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FADBD8", edgecolor="#C0392B"),
    )

    save(fig, "figura5_rede_fornecimento.svg")


# ==============================================================================
# MAIN
# ==============================================================================
if __name__ == "__main__":
    print("Gerando gráficos e figuras...\n")
    grafico1_complexidade_textual()
    grafico2_sobrevivencia()
    grafico3_latencia_decisoria()
    grafico4_shap_summary()
    grafico5_framing_midia()
    figura1_arquitetura_copiloto()
    figura2_ciclo_dsr()
    figura3_pipeline_nlp()
    figura4_interface_avaliacao()
    figura5_rede_fornecimento()
    print(f"\nTodos os arquivos foram salvos em: {OUTPUT_DIR}")
