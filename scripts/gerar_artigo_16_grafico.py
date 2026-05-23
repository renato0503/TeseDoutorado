import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from viz_engine import AcademicVizEngine

def generate_artigo_16_chart():
    # Caminho dos dados e de destino
    csv_path = "Base_de_Dados_e_APIs/Raw_Data/Revisao_Sistematica/xai_public_sector.csv"
    output_path = "Artigos/16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica/artigo_16_evolucao"
    
    if not os.path.exists(csv_path):
        print(f"❌ Base de dados não encontrada em: {csv_path}")
        return
        
    # Carregar dados reais
    df = pd.read_csv(csv_path)
    
    # Limpar e converter coluna de ano
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df = df.dropna(subset=['ano'])
    df['ano'] = df['ano'].astype(int)
    
    # Agrupar publicações por ano
    publications_by_year = df.groupby('ano').size().reset_index(name='count')
    publications_by_year = publications_by_year.sort_values('ano')
    
    # Filtrar anos de 2017 a 2026
    publications_by_year = publications_by_year[(publications_by_year['ano'] >= 2017) & (publications_by_year['ano'] <= 2026)]
    
    # Instanciar o motor de visualização acadêmica
    engine = AcademicVizEngine(font_family="serif", style="white")
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    # Plotar gráfico de linha com marcadores circulares
    ax.plot(publications_by_year['ano'], publications_by_year['count'], 
            color=engine.colors["primary"], linewidth=2.5, marker='o', 
            markersize=7, label="Publicações / Ano", zorder=3)
    
    # Adicionar sombreado sob a curva (área)
    ax.fill_between(publications_by_year['ano'], publications_by_year['count'], 
                    color=engine.colors["primary"], alpha=0.1)
    
    # Rótulos dos dados em cada ponto
    for i, row in publications_by_year.iterrows():
        ax.text(row['ano'], row['count'] + 0.3, str(int(row['count'])), 
                ha='center', va='bottom', fontsize=9, fontweight='bold', 
                color=engine.colors["neutral"])
        
    ax.set_xlabel("Ano de Publicação")
    ax.set_ylabel("Quantidade de Artigos Publicados")
    ax.set_title("Evolução Temporal das Publicações sobre XAI no Setor Público (2017-2026)", pad=15)
    
    # Ajustar eixos
    ax.set_xlim(2016.5, 2026.5)
    ax.set_ylim(0, max(publications_by_year['count']) + 2)
    ax.set_xticks(range(2017, 2027))
    
    engine._remove_spines(ax)
    
    # Salvar nos formatos de alta resolução (PNG + PDF)
    engine.save_figure(fig, output_path)
    
if __name__ == "__main__":
    generate_artigo_16_chart()
