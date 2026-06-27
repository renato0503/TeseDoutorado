"""
ARTIGO 25 - Coleta via arXiv (fallback para OpenAlex)
Busca artigos relacionados a LLM multi-agent systems
"""
import os
import time
import pandas as pd
import requests
import re

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\25-Artigo AI Offline"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(RAW, exist_ok=True)
os.makedirs(IMG, exist_ok=True)


def buscar_arxiv(termo, max_resultados=100):
    """Busca preprints no arXiv por termo."""
    time.sleep(3)
    print(f'  Buscando: {termo}...', end=' ', flush=True)
    params = {
        'search_query': f'all:{termo}',
        'start': 0,
        'max_results': max_resultados,
        'sortBy': 'relevance',
    }
    try:
        r = requests.get('http://export.arxiv.org/api/query', params=params, timeout=60)
        if r.status_code == 200:
            registros = []
            entries = re.findall(r'<entry>(.*?)</entry>', r.text, re.DOTALL)
            for entry in entries:
                try:
                    titulo = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                    titulo = titulo.group(1).replace('\n', ' ').strip() if titulo else ''
                    autores = re.findall(r'<name>(.*?)</name>', entry)
                    data = re.search(r'<published>(.*?)</published>', entry)
                    ano = int(data.group(1)[:4]) if data else None
                    resumo = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                    resumo = resumo.group(1).replace('\n', ' ').strip()[:500] if resumo else ''
                    link = re.search(r'<id>(.*?)</id>', entry)
                    link = link.group(1) if link else ''
                    registros.append({
                        'titulo': titulo,
                        'autores': '; '.join(autores[:5]),
                        'ano': ano,
                        'resumo': resumo,
                        'link': link,
                    })
                except Exception:
                    continue
            print(f'{len(registros)} artigos')
            return registros
    except Exception as e:
        print(f'Erro: {e}')
    return []


def main():
    print('=== ARTIGO 25 - Coleta arXiv ===\n')

    termos = [
        'LLM multi-agent',
        'model cascading LLM',
        'LLM routing',
        'on-premises LLM',
        'federated LLM',
    ]

    todos = []
    for termo in termos:
        regs = buscar_arxiv(termo, 100)
        todos.extend(regs)

    df = pd.DataFrame(todos).drop_duplicates(subset='link').reset_index(drop=True)
    output = os.path.join(RAW, 'llm_multi_agent_arxiv.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\nTotal: {len(df)} artigos unicos salvos em {output}')
    return df


if __name__ == '__main__':
    main()
