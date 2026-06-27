"""
ARTIGO 23 - Coleta de dados bibliometricos via Refinitiv Web of Science
Mapeamento da Producao Cientifica em Governanca Algoritmica

Coleta:
1. Buscar artigos por termos sobre governanca algoritmica + setor publico
2. Extrair metadados (autores, instituicoes, paises, periodicos, citacoes)
3. Construir matriz de cocitacao de autores

Saida:
- Raw_Data/artigos_brutos.csv (todos os artigos retornados)
- Raw_Data/artigos_filtrados.csv (apos criterios de eligibilidade)
- Raw_Data/matriz_cocitacao.csv (autores x frequencia de cocitacao)
"""
import os
import sys

# Web of Science via Refinitiv nao tem API Python oficial tao robusta quanto Scopus
# Recomendado: usar a interface Web of Science diretamente e exportar como CSV/tab delimited
# Script abaixo mostra como processar arquivos exportados

try:
    import pandas as pd
except ImportError:
    print("Instale pandas: pip install pandas")
    sys.exit(1)

QUERY = (
    'TS=("algorithmic governance" OR "algorithm governance" OR "governance by algorithm") '
    'AND TS=("public sector" OR government OR "public procurement" OR "public administration")'
)


def instrucoes_exportacao():
    print("=" * 70)
    print("INSTRUCOES PARA COLETA NA WEB OF SCIENCE (Refinitiv)")
    print("=" * 70)
    print()
    print("1. Acesse: https://www.webofscience.com/wos")
    print(f"2. Use a query:")
    print(f"   {QUERY}")
    print("3. Periodo: 2010-2024")
    print("4. Document Types: Article")
    print("5. Exportar resultado completo em formato 'Tab delimited file'")
    print("6. Salvar como Raw_Data/wos_export.txt")
    print()
    print("Apos exportacao, execute este script novamente para processar.")


def processar_exportacao():
    caminho = "Raw_Data/wos_export.txt"
    if not os.path.exists(caminho):
        print(f"ERRO: arquivo {caminho} nao encontrado.")
        instrucoes_exportacao()
        return

    try:
        df = pd.read_csv(caminho, sep="\t", low_memory=False)
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    print(f"Total de registros: {len(df)}")
    cols_interesse = ["TI", "AU", "PY", "SO", "WC", "C1", "DE", "TC"]
    cols_disponiveis = [c for c in cols_interesse if c in df.columns]
    df_filtrado = df[cols_disponiveis].copy()
    df_filtrado.columns = [
        "titulo", "autores", "ano", "periodico", "categoria", "afiliacao",
        "palavras_chave", "total_citacoes",
    ][:len(cols_disponiveis)]
    df_filtrado.to_csv("Raw_Data/artigos_brutos.csv", index=False)
    print(f"  -> Artigos brutos salvos em Raw_Data/artigos_brutos.csv")

    # Filtrar artigos com abstract e idioma conhecido
    if "AB" in df.columns:
        df_com_abs = df[df["AB"].notna()].copy()
        if "LA" in df.columns:
            df_com_abs = df_com_abs[df_com_abs["LA"].isin(["English", "Portuguese", "Spanish"])]
        df_com_abs[cols_disponiveis].to_csv("Raw_Data/artigos_filtrados.csv", index=False)
        print(f"  -> Artigos filtrados salvos em Raw_Data/artigos_filtrados.csv ({len(df_com_abs)} artigos)")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    processar_exportacao()
    instrucoes_exportacao()
