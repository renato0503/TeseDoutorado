"""
ARTIGO 24 - Indicadores WGI via download manual
Como a API do World Bank nao expoe os WGI diretamente,
criamos um script para processar o dataset baixado manualmente.

Download manual em: https://www.worldbank.org/en/publication/worldwide-governance-indicators
1. Va em "Data" -> "Download"
2. Baixe "WGI 2024 Update" (formato Excel)
3. Salve em Raw_Data/wgi_raw.xlsx
4. Execute este script
"""
import os
import pandas as pd

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country\Raw_Data"


def processar_wgi():
    caminho_xlsx = os.path.join(OUT_DIR, "wgi_raw.xlsx")
    if not os.path.exists(caminho_xlsx):
        print(f"Arquivo nao encontrado: {caminho_xlsx}")
        print("Baixe manualmente em https://www.worldbank.org/en/publication/worldwide-governance-indicators")
        print("Salve como:", caminho_xlsx)
        return

    # Ler planilha WGI (geralmente a aba "WGI_Data" tem a estrutura tidy)
    try:
        xls = pd.ExcelFile(caminho_xlsx)
        for aba in xls.sheet_names:
            print(f"Aba disponivel: {aba}")
    except Exception as e:
        print(f"Erro ao ler: {e}")
        return

    # Tentar abas comuns do dataset WGI
    for aba in ["WGI_Data", "data", "WGI"]:
        try:
            df = pd.read_excel(caminho_xlsx, sheet_name=aba)
            print(f"Processando aba: {aba} ({len(df)} linhas)")
            print(f"  Colunas: {df.columns.tolist()[:10]}")
            if "countrycode" in df.columns and "year" in df.columns:
                # Filtrar 2015-2024
                df = df[(df["year"] >= 2015) & (df["year"] <= 2024)]
                df.to_csv(os.path.join(OUT_DIR, "wgi_processado.csv"), index=False)
                print(f"  -> Salvo: {len(df)} registros")
                return
        except Exception:
            continue


if __name__ == "__main__":
    processar_wgi()
