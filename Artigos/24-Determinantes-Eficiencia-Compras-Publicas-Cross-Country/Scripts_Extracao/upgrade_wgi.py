"""
ARTIGO 24 - Upgrade: Processar WGI do World Bank
Os indicadores WGI processados estao em arquivos CSV com colunas:
pais, pais_nome, ano, valor
"""
import os
import pandas as pd

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)


def processar_wgi_para_paises(paises_selecionados=None, anos=None):
    """
    Processa WGI a partir dos CSVs ja baixados do World Bank.
    Os arquivos tem colunas: pais, pais_nome, ano, valor
    """
    arquivos = [f for f in os.listdir(RAW) if f.startswith('wb_') and f.endswith('.csv')]
    if not arquivos:
        print(f'Nenhum arquivo wb_*.csv encontrado em {RAW}')
        return None

    paises_selecionados = paises_selecionados or ['BRA', 'USA', 'GBR', 'DEU', 'FRA', 'CHN', 'IND', 'MEX', 'ARG', 'JPN']
    anos = anos or list(range(2015, 2025))

    todos = []
    for arquivo in arquivos:
        indicador = arquivo.replace('wb_', '').replace('.csv', '')
        print(f'Processando {indicador}...', end=' ', flush=True)
        try:
            df = pd.read_csv(os.path.join(RAW, arquivo))
            if 'pais' in df.columns:
                df = df[df['pais'].isin(paises_selecionados)]
                if 'ano' in df.columns:
                    df = df[df['ano'].isin(anos)]
                df = df.rename(columns={'pais': 'Country Code', 'pais_nome': 'Country Name', 'ano': 'ano', 'valor': indicador})
                cols_keep = ['Country Code', 'Country Name', 'ano', indicador]
                df = df[cols_keep]
                todos.append(df)
                print(f'{len(df)} registros')
            else:
                print('coluna pais nao encontrada')
        except Exception as e:
            print(f'Erro: {e}')

    if todos:
        resultado = todos[0]
        for df in todos[1:]:
            resultado = resultado.merge(df, on=['Country Code', 'Country Name', 'ano'], how='outer')
        return resultado
    return None


def main():
    print('=== ARTIGO 24 - Upgrade WGI ===\n')
    df = processar_wgi_para_paises()
    if df is not None and not df.empty:
        output = os.path.join(RAW, 'artigo24_wgi_processado.csv')
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f'\n{len(df)} registros WGI salvos em {output}')
    else:
        print('Nenhum dado processado')
    return df


if __name__ == '__main__':
    main()
