"""
ARTIGO 16 - Upgrade Bibliometrico via Crossref
Validacao de 52 artigos locais contra base Crossref
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

HEADERS = {'User-Agent': 'renato0503@gmail.com (Doutorado Pesquisa - renato0503@gmail.com)'}


def buscar_por_termo(termo, ano_inicio=2018, ano_fim=2024):
    """Busca artigos por termo com filtro de ano."""
    time.sleep(1.1)
    params = {
        'query': termo,
        'rows': 100,
    }
    try:
        r = requests.get('https://api.crossref.org/works', params=params, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            items = r.json().get('message', {}).get('items', [])
            registros = []
            for item in items:
                try:
                    titulo = item.get('title', [''])[0] if item.get('title') else ''
                    autores = item.get('author', [])
                    autor_nomes = '; '.join([f'{a.get("family","")}' for a in autores])
                    date_parts = item.get('published-print', {}).get('date-parts', [[None]])
                    if not date_parts or not date_parts[0] or not date_parts[0][0]:
                        date_parts = item.get('published-online', {}).get('date-parts', [[None]])
                    ano = date_parts[0][0] if date_parts and date_parts[0] and date_parts[0][0] else None
                    if ano and (ano < ano_inicio or ano > ano_fim):
                        continue
                    registros.append({
                        'doi': item.get('DOI'),
                        'titulo': titulo,
                        'ano': ano,
                        'autores': autor_nomes,
                        'periodico': item.get('container-title', [''])[0] if item.get('container-title') else None,
                        'citacoes': item.get('is-referenced-by-count', 0),
                    })
                except Exception:
                    continue
            return registros
    except Exception as e:
        print(f'  ! Erro: {e}')
    return []


def main():
    print('=== ARTIGO 16 - Upgrade Crossref ===\n')

    termos = [
        'explainable AI government',
        'XAI public sector',
        'interpretable machine learning government',
        'black box AI accountability',
        'AI transparency public administration',
    ]

    todos = []
    for termo in termos:
        print(f'Buscando: {termo}...', end=' ', flush=True)
        regs = buscar_por_termo(termo, 2018, 2024)
        print(f'{len(regs)} artigos')
        todos.extend(regs)

    df = pd.DataFrame(todos).drop_duplicates(subset='doi').reset_index(drop=True)
    output = os.path.join(RAW, 'artigo16_crossref.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\nTotal: {len(df)} artigos unicos salvos em {output}')
    return df


if __name__ == '__main__':
    main()
