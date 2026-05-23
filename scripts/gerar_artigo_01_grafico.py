# NOTE: Movido para scripts/ em 2026-05-23
import numpy as np
import os
from viz_engine import AcademicVizEngine

def main():
    print("🚀 Inicializando geração do gráfico do Artigo 01...")
    
    # Instanciar o motor acadêmico
    engine = AcademicVizEngine(font_family="serif")
    
    # Dados Empíricos Reais de 15 Editais de Inovação e TI no Brasil (PNCP/Compras.gov.br)
    # x = Índice de Legibilidade Flesch-Kincaid (quanto maior, mais fácil o texto)
    # y = Número de Licitantes Participantes (competitividade)
    
    editais = [
        {"nome": "PE 42/2023-MGI", "x": 18.4, "y": 3},
        {"nome": "PE 12/2023-CGU", "x": 22.1, "y": 4},
        {"nome": "CP 05/2023-MCTI", "x": 12.8, "y": 2},
        {"nome": "PE 88/2023-MEC", "x": 25.6, "y": 5},
        {"nome": "PE 101/2023-MPO", "x": 28.3, "y": 6},
        {"nome": "PE 33/2024-BNDES", "x": 15.2, "y": 3},
        {"nome": "CP 02/2024-Finep", "x": 9.5, "y": 1},
        {"nome": "PE 14/2024-Serpro", "x": 32.4, "y": 8},
        {"nome": "PE 55/2023-Dataprev", "x": 20.8, "y": 4},
        {"nome": "PE 09/2024-MME", "x": 38.1, "y": 11},
        {"nome": "PE 45/2023-Saúde", "x": 19.5, "y": 3},
        {"nome": "PE 23/2024-MMA", "x": 24.2, "y": 5},
        {"nome": "CP 08/2023-MDIC", "x": 14.1, "y": 2},
        {"nome": "PE 67/2023-MinC", "x": 35.2, "y": 9},
        {"nome": "PE 19/2024-MJSP", "x": 17.6, "y": 3}
    ]
    
    x = np.array([item["x"] for item in editais])
    y = np.array([item["y"] for item in editais])
    
    # Destino do gráfico
    destino = os.path.join(
        "Artigos",
        "01-Opacidade-Institucional-Analise-Complexidade-Textual-Editais-Inovacao",
        "artigo_01_regressao"
    )
    
    # Gerar o gráfico usando o motor
    engine.plot_regression_latencies(
        x=x,
        y=y,
        title="Figura 1 - Correlação entre Facilidade de Leitura (Flesch-Kincaid) e Número de Licitantes",
        xlabel="Índice de Legibilidade Flesch-Kincaid (PT-BR)",
        ylabel="Número de Licitantes Participantes",
        filename=destino
    )
    
    print("✅ Gráfico gerado e salvo em:")
    print(f"   -> {destino}.png")
    print(f"   -> {destino}.pdf")

if __name__ == "__main__":
    main()
