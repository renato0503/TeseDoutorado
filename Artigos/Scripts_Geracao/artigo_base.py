"""
GERADOR DE ARTIGOS ACADEMICOS - FORMATO APA 7a EDICAO
USA CSS CENTRALIZADO: ../../css/style_academico.css
"""
import os
import pandas as pd

CSS_PATH = r"C:\Users\Renato\Documents\Doutorado\css\style_academico.css"


def carregar_css():
    """Carrega o CSS centralizado."""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def gerar_artigo_base(titulo, autor, email, resumo, abstract, palavras_chave, keywords,
                      secoes, referencias_html):
    """Gera artigo base usando CSS centralizado."""

    css_custom = """
        .figure-container { margin: 0.5cm 0; text-align: center; }
        .figure-container img { max-width: 90%; height: auto; }
        .figure-caption { text-indent: 0 !important; margin: 0.2cm 0 0 0; font-size: 10pt; }
        .figure-note { text-indent: 0 !important; font-size: 10pt; margin-top: 0.05cm; margin-bottom: 0.3cm; line-height: 1.2; }
        .table-note { text-indent: 0 !important; font-size: 10pt; margin-top: 0.1cm; margin-bottom: 0.3cm; line-height: 1.2; }
        .ref-entry { text-indent: -1.27cm; padding-left: 1.27cm; margin: 0 0 0.3cm 0; text-align: justify; font-size: 11pt; }
        h3 { font-size: 12pt; font-weight: bold; font-style: italic; margin: 0.6cm 0 0.3cm 0; }
        code { font-size: 9pt; font-family: "Courier New", monospace; }
    """

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{titulo}</title>
    <link rel="stylesheet" href="../../css/style_academico.css">
    <style>
{css_custom}
    </style>
</head>
<body>

    <div class="control-panel no-print">
        <button onclick="window.print()" class="btn-print">🖨️ Imprimir / Salvar PDF</button>
        <button onclick="exportarDocx()" class="btn-docx">📄 Baixar DOCX</button>
    </div>

    <section class="paper-page">
        <div class="page-content">
            <h1 class="paper-title">{titulo.upper()}</h1>

            <p class="author-info"><strong>{autor}</strong><br>
            <span style="font-size: 10pt; color: #555;">Fucape Business School • Doutorado Profissional<br>E-mail: {email}</span></p>

            <div class="abstract-box">
                <h2>RESUMO</h2>
                {resumo}
                <p><strong>Palavras-chave:</strong> {palavras_chave}.</p>
            </div>

            <div class="abstract-box">
                <h2>ABSTRACT</h2>
                {abstract}
                <p><strong>Keywords:</strong> {keywords}.</p>
            </div>

            {secoes}

            <h2>REFERÊNCIAS</h2>
            {referencias_html}
        </div>
        <div class="page-footer"></div>
    </section>

</body>
</html>"""

    return html


def gerar_tabela_html(df, colunas, titulo):
    """Gera tabela HTML."""
    if df.empty:
        return "<p>Dados nao disponiveis.</p>"

    cols_exist = [c for c in colunas if c in df.columns]
    if not cols_exist:
        return "<p>Dados nao disponiveis.</p>"

    df_sub = df[cols_exist].head(15)

    html = f'<p class="table-caption"><strong>Tabela 1.</strong> {titulo}</p>\n'
    html += '<table>\n<thead>\n<tr>'
    for c in cols_exist:
        html += f'<th>{c.title()}</th>'
    html += '</tr>\n</thead>\n<tbody>\n'

    for _, row in df_sub.iterrows():
        html += '<tr>'
        for c in cols_exist:
            val = row[c]
            if pd.isna(val):
                val = '-'
            elif isinstance(val, float):
                val = f'{val:.2f}'
            elif not isinstance(val, str):
                val = str(val)
            if len(val) > 50:
                val = val[:50] + '...'
            html += f'<td>{val}</td>'
        html += '</tr>\n'

    html += '</tbody>\n</table>\n'
    html += '<p class="table-note">Fonte: Elaboracao propria.</p>'

    return html


def calcular_estatisticas(df, col_ano='ano'):
    """Calcula estatisticas basicas."""
    stats = {}
    if col_ano in df.columns:
        stats['total'] = len(df)
        stats['periodo'] = f"{int(df[col_ano].min())} - {int(df[col_ano].max())}"
    return stats


def salvar(html, caminho):
    """Salva HTML."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Salvo: {caminho}")
