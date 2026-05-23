import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional

# Configurações globais de estilo
class AcademicVizEngine:
    """
    Motor unificado para geração de visualizações científicas de alto impacto.
    Garante conformidade com normas de publicação e estética acadêmica premium.
    """
    
    def __init__(self, font_family: str = "serif", style: str = "white"):
        self._setup_style(font_family, style)
        self.colors = {
            "primary": "#1A365D",      # Azul Escuro Corporativo
            "secondary": "#4A5568",    # Cinza Ardósia
            "accent": "#9B2C2C",       # Vermelho Tijolo
            "neutral": "#2D3748",      # Carvão Escuro
            "grid": "#E2E8F0",         # Cinza Claro para Grid
            "light_accent": "#DD6B20"  # Amarelo Ouro Queimado
        }
        
    def _setup_style(self, font_family: str, style: str):
        """Aplica configurações do Matplotlib."""
        plt.style.use('default')
        sns.set_style(style)
        
        plt.rcParams.update({
            "font.family": font_family,
            "font.serif": ["Times New Roman", "DejaVu Serif", "Liberation Serif"],
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.titlesize": 14,
            "pdf.fonttype": 42,  # Evita problemas de fontes no PDF
            "ps.fonttype": 42
        })

    def _remove_spines(self, ax):
        """Remove bordas desnecessárias da figura."""
        sns.despine(ax=ax, top=True, right=True, left=False, bottom=False)
        ax.grid(True, linestyle="--", alpha=0.5, color=self.colors["grid"])

    def save_figure(self, fig, path: str, dpi: int = 300):
        """Salva a figura nos formatos PNG e PDF."""
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        fig.savefig(path + ".png", dpi=dpi, bbox_inches="tight")
        fig.savefig(path + ".pdf", format="pdf", bbox_inches="tight")
        plt.close(fig)
        print(f"✅ Gráfico salvo com sucesso em: {path}.png e {path}.pdf")

    # ================= Gráfico 1: Redes de Oligopólios (Artigo 5) =================
    def plot_oligopoly_network(self, nodes: List[str], edges: List[Tuple[str, str, float]], 
                               degrees: Dict[str, float], title: str, filename: str):
        """Gera um grafo de redes para o Artigo 5."""
        import networkx as nx
        
        fig, ax = plt.subplots(figsize=(8, 6))
        G = nx.Graph()
        
        for u, v, w in edges:
            G.add_edge(u, v, weight=w)
            
        pos = nx.spring_layout(G, seed=42)
        node_sizes = [degrees.get(n, 1.0) * 800 for n in G.nodes()]
        
        # Desenhar arestas
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.4, edge_color=self.colors["secondary"], width=1.5)
        
        # Desenhar nós
        nodes_drawn = nx.draw_networkx_nodes(
            G, pos, ax=ax, node_color=self.colors["primary"],
            node_size=node_sizes, edgecolors="#FFFFFF", linewidths=1.5
        )
        
        # Rótulos
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_family="serif", font_weight="bold")
        
        ax.set_title(title, pad=15)
        ax.axis("off")
        self.save_figure(fig, filename)

    # ================= Gráfico 2: Análise de Sobrevivência (Artigo 6) =================
    def plot_survival_curve(self, timeline: np.ndarray, survival_function: np.ndarray, 
                            confidence_intervals: Optional[Tuple[np.ndarray, np.ndarray]], 
                            label: str, title: str, xlabel: str, ylabel: str, filename: str):
        """Plota curvas de sobrevivência de Kaplan-Meier para o Artigo 6."""
        fig, ax = plt.subplots(figsize=(7, 4.5))
        
        ax.step(timeline, survival_function, where="post", label=label, 
                color=self.colors["primary"], linewidth=2)
        
        if confidence_intervals is not None:
            lower, upper = confidence_intervals
            ax.fill_between(timeline, lower, upper, step="post", 
                            color=self.colors["primary"], alpha=0.15)
            
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, pad=15)
        ax.set_ylim(-0.05, 1.05)
        self._remove_spines(ax)
        ax.legend(frameon=True, facecolor="white", edgecolor="none")
        
        self.save_figure(fig, filename)

    # ================= Gráfico 3: Dendrograma / Análise Lexical (Artigos 9, 10, 11, 14, 15) =================
    def plot_lexical_dendrogram(self, linkage_matrix, labels: List[str], title: str, filename: str):
        """Gera um dendrograma de classificação hierárquica descendente para análise de conteúdo."""
        from scipy.cluster.hierarchy import dendrogram
        
        fig, ax = plt.subplots(figsize=(8, 5))
        
        dendrogram(
            linkage_matrix, labels=labels, ax=ax, orientation="left",
            color_threshold=None, above_threshold_color=self.colors["secondary"]
        )
        
        # Colorir ramos com estilo acadêmico
        ax.set_title(title, pad=15)
        ax.set_xlabel("Distância Euclidiana / Dissimilaridade")
        self._remove_spines(ax)
        
        self.save_figure(fig, filename)

    # ================= Gráfico 4: Eficiência de Benchmarking (Artigo 7) =================
    def plot_benchmarking_efficiency(self, scores: List[float], labels: List[str], 
                                     frontier_x: List[float], frontier_y: List[float],
                                     title: str, xlabel: str, ylabel: str, filename: str):
        """Plota a fronteira de eficiência DEA para o Artigo 7."""
        fig, ax = plt.subplots(figsize=(7, 5))
        
        # Fronteira de eficiência
        ax.plot(frontier_x, frontier_y, color=self.colors["accent"], linestyle="--", 
                linewidth=2, label="Fronteira Eficiente")
        
        # Unidades de tomada de decisão (DMUs)
        ax.scatter(scores, [1.0]*len(scores), color=self.colors["primary"], s=100, 
                   edgecolors="white", linewidths=1, zorder=3, label="DMUs Analisadas")
        
        for i, txt in enumerate(labels):
            ax.annotate(txt, (scores[i], 1.0), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontsize=8)
            
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, pad=15)
        self._remove_spines(ax)
        ax.legend(frameon=True)
        
        self.save_figure(fig, filename)

    # ================= Gráfico 5: Ponderação e SHAP de XAI (Artigo 8) =================
    def plot_explainable_ai_weights(self, features: List[str], shap_values: List[float], 
                                    title: str, filename: str):
        """Gera um gráfico de importância de atributos baseado em SHAP para o Artigo 8."""
        df = pd.DataFrame({"Atributo": features, "Impacto (SHAP)": shap_values})
        df = df.sort_values(by="Impacto (SHAP)", ascending=True)
        
        fig, ax = plt.subplots(figsize=(7, 4.5))
        
        # Barras horizontais
        bars = ax.barh(df["Atributo"], df["Impacto (SHAP)"], 
                       color=self.colors["primary"], height=0.6)
        
        # Colorir valores positivos em azul e negativos em vermelho
        for i, bar in enumerate(bars):
            if df["Impacto (SHAP)"].iloc[i] < 0:
                bar.set_color(self.colors["accent"])
                
        ax.axvline(0, color=self.colors["secondary"], linewidth=0.8, linestyle="--")
        ax.set_xlabel("Impacto médio na decisão do modelo (|SHAP value|)")
        ax.set_title(title, pad=15)
        self._remove_spines(ax)
        
        self.save_figure(fig, filename)

    # ================= Gráfico 6: Regressão de Latência Decisória / Opacidade (Artigos 1, 2, 3, 4) =================
    def plot_regression_latencies(self, x: np.ndarray, y: np.ndarray, 
                                  title: str, xlabel: str, ylabel: str, filename: str):
        """Plota a dispersão com a reta de regressão ajustada para latência decisória."""
        fig, ax = plt.subplots(figsize=(7, 4.5))
        
        # Dispersão
        ax.scatter(x, y, color=self.colors["primary"], alpha=0.6, s=40, edgecolors="black", linewidth=0.8)
        
        # Ajuste de reta
        m, b = np.polyfit(x, y, 1)
        # Gerar pontos para a reta
        x_line = np.linspace(min(x), max(x), 100)
        ax.plot(x_line, m*x_line + b, color=self.colors["accent"], linewidth=2, label=f"Reta de Regressão (R² = {self.calculate_r2(x, y):.3f})")
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, pad=15)
        self._remove_spines(ax)
        ax.legend(frameon=True)
        
        self.save_figure(fig, filename)

    def calculate_r2(self, x: np.ndarray, y: np.ndarray) -> float:
        """Calcula o coeficiente de determinação R²."""
        correlation_matrix = np.corrcoef(x, y)
        correlation_xy = correlation_matrix[0,1]
        return correlation_xy**2

    # ================= Gráfico 7: Frequência de Dores da Netnografia (Artigo 13) =================
    def plot_netnography_dolor_frequency(self, categories: List[str], frequencies: List[int], 
                                         title: str, filename: str):
        """Plota o gráfico de dores GovTech (Netnografia) do Artigo 13."""
        df = pd.DataFrame({"Dor": categories, "Frequência": frequencies})
        df = df.sort_values(by="Frequência", ascending=True)
        
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        
        # Barras horizontais limpas
        bars = ax.barh(df["Dor"], df["Frequência"], color=self.colors["primary"], height=0.55)
        
        # Rótulos de dados no final das barras
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1.5, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                    va='center', ha='left', fontsize=9, fontweight='bold', color=self.colors["neutral"])
            
        ax.set_xlabel("Frequência de Menções nas Comunidades / Fóruns")
        ax.set_title(title, pad=15)
        ax.set_xlim(0, max(frequencies) * 1.15)
        self._remove_spines(ax)
        
        self.save_figure(fig, filename)
