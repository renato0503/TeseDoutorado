"""
ARTIGO 24 - Coleta via World Bank API e HG Brasil
Determinantes da Eficiencia em Compras Publicas cross-country

Fontes gratuitas:
- World Bank API: PIB per capita, inflacao, governanca
- HG Brasil: indicadores macro BR (complementar)
"""
import os
import json
import time
import urllib.request
import urllib.error
import pandas as pd

OUT_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country\Raw_Data"
os.makedirs(OUT_DIR, exist_ok=True)

# 67 paises com dados historicos consistentes no World Bank
PAISES = [
    "ARG", "AUS", "AUT", "BEL", "BOL", "BRA", "BGR", "CAN", "CHL", "CHN",
    "COL", "CRI", "HRV", "CYP", "CZE", "DNK", "ECU", "EGY", "SLV", "ESP",
    "EST", "FIN", "FRA", "DEU", "GRC", "GTM", "HUN", "ISL", "IND", "IDN",
    "IRL", "ISR", "ITA", "JPN", "KOR", "LVA", "LTU", "LUX", "MYS", "MEX",
    "MAR", "NLD", "NZL", "NOR", "PAK", "PAN", "PER", "PHL", "POL", "PRT",
    "ROU", "RUS", "SAU", "SGP", "SVK", "SVN", "ZAF", "ESP", "SWE", "CHE",
    "THA", "TUR", "ARE", "GBR", "USA", "URY", "VEN", "VNM", "TWN",
]

INDICADORES = {
    "NY.GDP.PCAP.CD": "pib_per_capita_usd",
    "NY.GDP.MKTP.KD.ZG": "crescimento_pib_pct",
    "FP.CPI.TOTL.ZG": "inflacao_pct",
    "NE.TRD.GNFS.ZS": "abertura_comercial_pct_pib",
    "IT.NET.USER.ZS": "usuarios_internet_pct",
    "IT.CEL.SETS.P2": "celulares_por_100",
    "GE.EST": "governance_effectiveness_estimativa",
    "RQ.EST": "regulatory_quality_estimativa",
    "RL.EST": "rule_of_law_estimativa",
    "CC.EST": "control_corruption_estimativa",
    "PV.EST": "political_stability_estimativa",
    "VA.EST": "voice_accountability_estimativa",
    "SE.XPD.TOTL.GD.ZS": "gasto_publico_educacao_pct_pib",
    "GB.XPD.RSDV.GD.ZS": "gasto_pesquisa_desenvolvimento_pct_pib",
    "EG.ELC.ACCS.ZS": "acesso_eletricidade_pct",
}

WB_URL = "https://api.worldbank.org/v2/country/{paises}/indicator/{indicador}?format=json&date={start}:{end}&per_page=2000"


def fetch_wb(indicador, start=2015, end=2024):
    """Busca dados de um indicador do World Bank."""
    time.sleep(1)
    paises_str = ";".join(PAISES)
    url = WB_URL.format(paises=paises_str, indicador=indicador, start=start, end=end)
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
            if len(data) < 2 or not data[1]:
                return []
            registros = []
            for item in data[1]:
                registros.append({
                    "pais": item.get("countryiso3code") or item.get("country", {}).get("id"),
                    "pais_nome": item.get("country", {}).get("value"),
                    "ano": item.get("date"),
                    "valor": item.get("value"),
                })
            return registros
    except urllib.error.HTTPError as e:
        print(f"  ! HTTP {e.code} para {indicador}: {e.reason}")
        return []
    except Exception as e:
        print(f"  ! Erro em {indicador}: {e}")
        return []


def main():
    print(f"Coletando {len(INDICADORES)} indicadores do World Bank para {len(PAISES)} paises (2015-2024)...")
    dfs = {}
    for ind_code, ind_name in INDICADORES.items():
        print(f"  - {ind_code} ({ind_name})...", end=" ", flush=True)
        regs = fetch_wb(ind_code, 2015, 2024)
        print(f"{len(regs)} registros")
        if regs:
            df = pd.DataFrame(regs)
            df.to_csv(os.path.join(OUT_DIR, f"wb_{ind_name}.csv"), index=False)
            dfs[ind_name] = df

    print("\nConstruindo dataset consolidado...")
    base = dfs.get("pib_per_capita_usd", pd.DataFrame()).copy()
    base = base.rename(columns={"valor": "pib_per_capita_usd"})
    base = base.drop(columns=["pais_nome"], errors="ignore")

    for ind_name, df in dfs.items():
        if ind_name == "pib_per_capita_usd":
            continue
        df_temp = df.rename(columns={"valor": ind_name})[["pais", "ano", ind_name]]
        base = base.merge(df_temp, on=["pais", "ano"], how="left")

    base = base.sort_values(["pais", "ano"]).reset_index(drop=True)
    base.to_csv(os.path.join(OUT_DIR, "dataset_consolidado_wb.csv"), index=False)
    print(f"  -> Dataset final: {len(base)} linhas, {len(base.columns)} colunas")
    print(f"  -> Paises com dados: {base['pais'].nunique()}")

    # Dummy de governanca algoritmica (template para preenchimento)
    template = pd.DataFrame({
        "pais": PAISES,
        "tem_compras_eletronicas": [None] * len(PAISES),
        "tem_auditoria_continua": [None] * len(PAISES),
        "tem_xai_contratacao": [None] * len(PAISES),
        "fonte": [None] * len(PAISES),
    })
    template.to_csv(os.path.join(OUT_DIR, "governanca_algoritmica_template.csv"), index=False)
    print(f"  -> Template de governanca algoritmica salvo")

    print("\nConcluido. Arquivos em:", OUT_DIR)


if __name__ == "__main__":
    main()
