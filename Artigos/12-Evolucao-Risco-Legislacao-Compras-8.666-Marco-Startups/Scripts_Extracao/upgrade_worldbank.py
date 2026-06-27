"""
ARTIGO 12 - Upgrade via World Bank
Contexto internacional de risco e legislacao
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\12-Evolucao-Risco-Legislacao-Compras-8.666-Marco-Startups"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)


def buscar_wdi(indicadores, paises, ano_inicio=2018, ano_fim=2024):
    """Busca indicadores WDI do World Bank."""
    all_data = []
    for ind in indicadores:
        print(f'Buscando {ind}...', end=' ', flush=True)
        try:
            codes = ';'.join(paises)
            url = f'https://api.worldbank.org/v2/country/{codes}/indicator/{ind}'
            params = {'format': 'json', 'date': f'{ano_inicio}:{ano_fim}', 'per_page': 500}
            r = requests.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1 and data[1]:
                    for item in data[1]:
                        all_data.append({
                            'indicador': ind,
                            'pais': item.get('countryiso3code'),
                            'ano': item.get('date'),
                            'valor': item.get('value'),
                        })
                    print(f'{len(data[1])} registros')
                else:
                    print('sem dados')
        except Exception as e:
            print(f'Erro: {e}')
        time.sleep(0.5)
    return pd.DataFrame(all_data)


def main():
    print('=== ARTIGO 12 - Upgrade World Bank ===\n')

    paises = ['BRA', 'USA', 'GBR', 'DEU', 'FRA', 'ESP', 'ITA', 'MEX', 'ARG', 'CHN']
    indicadores = [
        'GC.REV.XGRD.GD.ZS',  # Receitas governamentais (% PIB)
        'GC.XPN.TOTL.GD.ZS',  # Despesas publicas
        'IC.BUS.EASE.XQ',     # Facilidades de negocios
        'MS.MIL.XPRT.ZS',     # Gastos militares (% PIB)
        'SG.VAW.NEACH.ZS',    # Violencia contra mulheres (indicador de risco)
    ]

    df = buscar_wdi(indicadores, paises, 2018, 2024)
    output = os.path.join(RAW, 'artigo12_worldbank.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\nTotal: {len(df)} registros salvos em {output}')
    return df


if __name__ == '__main__':
    main()
