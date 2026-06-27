"""
ARTIGO 08 - Upgrade via yfinance
Analise de empresas de auditoria listadas na B3
"""
import os
import pandas as pd
import yfinance as yf

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\08-XAI-Setor-Publico-Prova-Conceito-Tribunais-Contas"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)


def coletar_auditoras(tickers, anos=3):
    """Coleta dados de empresas de auditoria/consultoria."""
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
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'receita': info.get('totalRevenue', 0),
                'ebitda': info.get('ebitda', 0),
                'preco_atual': info.get('currentPrice', 0),
                'beta': info.get('beta', 0),
                'num_acoes': hist.shape[0] if not hist.empty else 0,
            })
            print(f'OK')
        except Exception as e:
            print(f'Erro: {e}')
    return pd.DataFrame(dados)


def main():
    print('=== ARTIGO 08 - Upgrade yfinance ===\n')

    # Empresas de auditoria/consultoria listadas
    tickers = [
        'DOHL3.SA',  # Deloitte
        'RSID3.SA',  # Rossi
        'MGLU3.SA',  # Magazine Luiza (varejo)
        'YDUQ3.SA',  # Yduqs (educacao)
        'BTOW3.SA',  # B2W (varejo)
        'VVAR3.SA',  # Via Varejo
    ]

    df = coletar_auditoras(tickers)
    output = os.path.join(RAW, 'artigo08_yfinance.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\n{len(df)} empresas salvas em {output}')
    return df


if __name__ == '__main__':
    main()
