"""
ARTIGO 22 - Upgrade: Expandir Amostra
Mais anos e mais empresas para analise de estrutura de capital
"""
import os
import pandas as pd
import yfinance as yf

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\22-Estrutura-Capital-Oligopolio-Compras-TI"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

TICKERS_AMPLIADO = [
    "TOTS3.SA", "LWSA3.SA", "LINX3.SA", "SYNA3.SA",
    "QUAL3.SA", "RADL3.SA", "MULT3.SA", "LOGIN3.SA",
    "SEQL3.SA", "LVTC3.SA", "CASH3.SA", "ALSO3.SA",
    "INTB3.SA", "BMOB3.SA", "SOMA3.SA", "NGRD3.SA",
]

START = "2015-01-01"
END = "2024-12-31"


def coletar_demonstracoes(tickers):
    """Coleta demonstracoes financeiras de empresas."""
    dados = []
    for ticker in tickers:
        print(f'Coletando: {ticker}...', end=' ', flush=True)
        try:
            emp = yf.Ticker(ticker)
            info = emp.info
            balanco = emp.balancesheet
            dre = emp.financials
            cfl = emp.cashflow

            linha = {
                'ticker': ticker,
                'nome': info.get('longName', ''),
                'setor': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'total_assets': balanco.get('Total Assets', pd.Series()).iloc[0] if not balanco.empty and 'Total Assets' in balanco.index else None,
                'total_liabilities': balanco.get('Total Liabilities', pd.Series()).iloc[0] if not balanco.empty and 'Total Liabilities' in balanco.index else None,
                'total_equity': balanco.get('Stockholders Equity', pd.Series()).iloc[0] if not balanco.empty and 'Stockholders Equity' in balanco.index else None,
                'receita_liquida': dre.get('Net Income', pd.Series()).iloc[0] if not dre.empty and 'Net Income' in dre.index else None,
                'ebitda': dre.get('EBITDA', pd.Series()).iloc[0] if not dre.empty and 'EBITDA' in dre.index else None,
                'divida_bruta': balanco.get('Long Term Debt', pd.Series()).iloc[0] if not balanco.empty and 'Long Term Debt' in balanco.index else None,
            }
            dados.append(linha)
            print('OK')
        except Exception as e:
            print(f'Erro: {e}')
    return pd.DataFrame(dados)


def coletar_series_temporais(tickers, anos=10):
    """Coleta precos historicos para serie temporal."""
    print(f'\nColetando series temporais {anos} anos...')
    precos = yf.download(tickers, period=f'{anos}y', auto_adjust=True, progress=False)
    if isinstance(precos.columns, pd.MultiIndex):
        close = precos['Close']
    else:
        close = precos[['Close']]
    close.to_csv(os.path.join(RAW, 'precos_expandido.csv'))
    retornos = close.pct_change().dropna(how='all')
    retornos.to_csv(os.path.join(RAW, 'retornos_expandido.csv'))
    print(f'{len(close)} dias de precos')
    return close


def main():
    print('=== ARTIGO 22 - Upgrade Expansao Amostra ===\n')
    df = coletar_demonstracoes(TICKERS_AMPLIADO)
    output = os.path.join(RAW, 'demonstracoes_expandido.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\n{len(df)} empresas salvas em {output}')

    series = coletar_series_temporais(TICKERS_AMPLIADO, 10)
    print(f'Series temporais salvas')
    return df


if __name__ == '__main__':
    main()
