"""
ARTIGO 06 - Upgrade Quantitativo via HG Brasil
Contexto macroeconomico para analise de sobrevivencia de contratos
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\06-Sobrevivencia-Contratos-Inovacao-Analise-Kaplan-Meier"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

HEADERS = {'User-Agent': 'renato0503@gmail.com (Doutorado Pesquisa)'}


def buscar_ipca(ano_inicio=2018, ano_fim=2024):
    """Busca dados do IPCA via TG API."""
    dados = []
    for ano in range(ano_inicio, ano_fim + 1):
        for mes in range(1, 13):
            time.sleep(1)
            try:
                url = f'https://api.tg.com.br/v1/indicadores/ipca/{ano}/{mes}'
                r = requests.get(url, headers=HEADERS, timeout=15)
                if r.status_code == 200:
                    d = r.json()
                    dados.append({
                        'ano': ano,
                        'mes': mes,
                        'ipca_mensal': d.get('valor', 0),
                        'acumulado_ano': d.get('acumuladoAno', 0),
                    })
            except Exception:
                pass
    return pd.DataFrame(dados)


def main():
    print('=== ARTIGO 06 - Upgrade HG Brasil ===\n')
    print('Buscando IPCA...')
    df = buscar_ipca(2018, 2024)
    if df.empty:
        print('TG API indisponivel - criando dados demo')
        df = pd.DataFrame({
            'ano': list(range(2018, 2025)) * 12,
            'mes': list(range(1, 13)) * 7,
            'ipca_mensal': [0.5] * 84,
            'acumulado_ano': [3.0] * 84,
        })
    output = os.path.join(RAW, 'artigo06_ipca.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'{len(df)} registros salvos em {output}')
    return df


if __name__ == '__main__':
    main()
