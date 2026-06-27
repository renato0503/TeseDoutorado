"""
ARTIGO 05 - Upgrade Quantitativo via yfinance
Adicionar market share financeiro das empresas do estudo
"""
import os
import pandas as pd
import yfinance as yf

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\05-Redes-Fornecimento-Oligopolios-Analise-Grafos"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)


def coletar_dados_yfinance(tickers, anos=5):
    """Coleta dados financeiros de tickers."""
    dados = []
    for ticker in tickers:
        print(f'Coletando: {ticker}...', end=' ', flush=True)
        try:
            emp = yf.Ticker(ticker)
            info = emp.info
            hist = emp.history(period=f'{anos}y')
            dados.append({
                'ticker': ticker,
                'nome': info.get('longName', ''),
                'setor': info.get('sector', ''),
                'market_cap': info.get('marketCap', 0),
                'receita': info.get('totalRevenue', 0),
                'lucro': info.get('netIncomeToCommon', 0),
                'preco_atual': info.get('currentPrice', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'num_acoes': hist.shape[0] if not hist.empty else 0,
            })
            print(f'OK ({hist.shape[0]} dias)')
        except Exception as e:
            print(f'Erro: {e}')
    return pd.DataFrame(dados)


def main():
    print('=== ARTIGO 05 - Upgrade yfinance ===\n')

    # Tickers de empresas de fornecimento/tecnologia relevantes
    tickers = [
        'ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA',  # Bancos brasileiros
        'VALE3.SA', 'PETROBRAS3.SA', 'BRF3.SA',  # Commodities
        'CSNA3.SA', 'GGBR4.SA',  # Siderurgia
        'HAPV3.SA', 'MEAL3.SA',  # Alimentos
    ]

    df = coletar_dados_yfinance(tickers)
    output = os.path.join(RAW, 'artigo05_yfinance.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\n{len(df)} empresas salvas em {output}')
    return df


if __name__ == '__main__':
    main()
