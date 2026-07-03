"""
ARTIGO 16 - Extração CrossRef com Filtros Rigorosos
XAI em Gestão Pública -only
Exclui: Física, Psiquiatria, Biologia Celular, Astrofísica
"""
import os
import time
import pandas as pd
import requests

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica"
RAW = os.path.join(ART_DIR, "Raw_Data")
os.makedirs(RAW, exist_ok=True)

HEADERS = {'User-Agent': 'renato0503@gmail.com (Doutorado Pesquisa - renato0503@gmail.com)'}

SUBJECTOS_EXCLUIR = [
    'Physics', 'Astrophysics', 'Astronomy', 'Particle Physics', 'Nuclear Physics',
    'Psychiatry', 'Psychology', 'Clinical Psychology', 'Neuroscience', 'Neurology',
    'Cell Biology', 'Molecular Biology', 'Genetics', 'Biochemistry', 'Microbiology',
    'Chemistry', 'Materials Science', 'Engineering', 'Mathematics',
    'Astrophysics', 'Cosmology', 'Space Science'
]

PALAVRAS_EXCLUIR_TITULO = [
    'physics', 'astrophysic', 'psychiatr', 'psycholog', 'cell biol', 'molecular',
    'genetic', 'biochem', 'microbiol', 'astronom', 'chemistry', 'materials',
    'neuroscience', 'neuropathy', 'genome', 'sequenc', 'proteom', 'quantum',
    'particle', 'nuclear', 'cosmolog', 'spacecraft', 'telescope',
    'cancer', 'tumor', 'oncolog', 'biomarker', 'carcinoma',
    'fetal', 'maternal', 'pregnancy', 'birth ',
    'drug', 'pharmaceutical', 'medication', 'clinical trial',
    'genomic', 'proteomic', 'metabolomic',
    'climate', 'ecosystem', 'biodiversity',
    'energy system', 'power grid', 'renewable energy',
]

PALAVRAS_EXIGIR_TITULO = [
    'public', 'government', 'governance', 'administration', 'policy',
    'accountability', 'transparency', 'audit', 'oversight',
    'decision', 'management', 'regulation', 'law',
]


def titulo_relevante(titulo):
    """Verifica se título contém palavras-chave relevantes e não contém excluídas."""
    if not titulo:
        return False
    titulo_lower = titulo.lower()

    for kw in PALAVRAS_EXCLUIR_TITULO:
        if kw in titulo_lower:
            return False

    tem_relevante = any(kw in titulo_lower for kw in PALAVRAS_EXIGIR_TITULO)
    return tem_relevante


def subject_relevante(subjects):
    """Verifica se pelo menos um subject é relevante."""
    if not subjects:
        return True
    for s in subjects:
        s_lower = s.lower()
        for excl in SUBJECTOS_EXCLUIR:
            if excl.lower() in s_lower:
                return False
    return True


def buscar_por_termo(termo, ano_inicio=2018, ano_fim=2024):
    """Busca artigos com filtros rigorosos de tema e ano."""
    time.sleep(1.1)
    params = {
        'query': termo,
        'rows': 100,
        'filter': 'from-pub-date:' + str(ano_inicio) + ',until-pub-date:' + str(ano_fim),
    }
    try:
        r = requests.get('https://api.crossref.org/works', params=params, headers=HEADERS, timeout=30)
        if r.status_code == 200:
            items = r.json().get('message', {}).get('items', [])
            registros = []
            for item in items:
                try:
                    titulo = item.get('title', [''])[0] if item.get('title') else ''
                    if not titulo_relevante(titulo):
                        continue

                    subjects = item.get('subject', [])
                    if subjects and not subject_relevante(subjects):
                        continue

                    autores = item.get('author', [])
                    autor_nomes = '; '.join([f'{a.get("family","")}' for a in autores])
                    date_parts = item.get('published-print', {}).get('date-parts', [[None]])
                    if not date_parts or not date_parts[0] or not date_parts[0][0]:
                        date_parts = item.get('published-online', {}).get('date-parts', [[None]])
                    ano = date_parts[0][0] if date_parts and date_parts[0] and date_parts[0][0] else None
                    if ano and (ano < ano_inicio or ano > ano_fim):
                        continue

                    container = item.get('container-title', [])
                    periodico = container[0] if container else None

                    if periodico:
                        p_lower = periodico.lower()
                        for excl in SUBJECTOS_EXCLUIR:
                            if excl.lower() in p_lower:
                                continue

                    registros.append({
                        'doi': item.get('DOI'),
                        'titulo': titulo,
                        'ano': ano,
                        'autores': autor_nomes,
                        'periodico': periodico,
                        'citacoes': item.get('is-referenced-by-count', 0),
                        'subjects': '; '.join(subjects[:5]) if subjects else '',
                    })
                except Exception:
                    continue
            return registros
    except Exception as e:
        print(f'  ! Erro: {e}')
    return []


def main():
    print('=== ARTIGO 16 - Extração CrossRef Rigorosa ===\n')
    print('Filtros ativos:')
    print('  - Exclui campos: Física, Psiquiatria, Biologia Celular, Astrofísica')
    print('  - Exclui títulos com: physics, astrophysic, psycholog, cell biol, etc.')
    print('  - Período: 2018-2024\n')

    termos = [
        'explainable AI government transparency accountability',
        'XAI public administration decision making',
        'interpretable machine learning public sector',
        'explainable AI public management governance',
        'AI explainability government audit oversight',
        'algorithmic accountability public sector',
        'machine learning explainability government',
        'AI transparency public policy',
    ]

    todos = []
    for termo in termos:
        print(f'Buscando: "{termo[:50]}..."', end=' ', flush=True)
        regs = buscar_por_termo(termo, 2018, 2024)
        print(f'{len(regs)} artigos relevantes')
        todos.extend(regs)
        time.sleep(0.5)

    df = pd.DataFrame(todos).drop_duplicates(subset='doi').reset_index(drop=True)
    df = df.sort_values('citacoes', ascending=False).reset_index(drop=True)

    output = os.path.join(RAW, 'artigo16_crossref.csv')
    df.to_csv(output, index=False, encoding='utf-8-sig')
    print(f'\nTotal: {len(df)} artigos únicos relevantes')
    print(f'Arquivo: {output}')

    if len(df) > 0:
        print(f'\nAmostra (Top 10 por citações):')
        print(df[['titulo', 'ano', 'citacoes']].head(10).to_string())

    return df


if __name__ == '__main__':
    main()
