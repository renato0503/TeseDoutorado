"""
Limpeza final dos artigos e reconstrucao da tese.
1. Remove travessoes e em-dashes dos artigos
2. Re-acentua ambos
3. Capitaliza titulos
4. Reconstroi tese_draft.html com artigos limpos + renumeracao completa
"""
import re, sys
sys.path.insert(0, r"C:\Users\Renato\Documents\Doutorado\scripts")
from reacentuar_artigo import MAPA_ACENTOS

ART01 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\01-Artigo-Cientifico-Diagnostico\artigo_01_diagnostico.html"
ART02 = r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese\02-Artigo-Tecnologico-Copiloto\artigo_02_tecnologico.html"
THESIS = r"C:\Users\Renato\Documents\Doutorado\Tese\tese_draft.html"

def clean_article(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove all travessoes and em-dashes
    content = content.replace("&mdash;", "").replace("\u2014", "").replace("\u2013", "")
    # Remove stray dashes in table cells (standalone "-" in <td>)
    content = re.sub(r'<td>\s*-\s*</td>', '<td></td>', content)

    # Re-acentuar
    for ascii_word, accented_word in MAPA_ACENTOS.items():
        pattern = re.compile(r'\b' + re.escape(ascii_word) + r'\b', re.IGNORECASE)
        content = pattern.sub(accented_word, content)

    # Capitalize h2 (all caps for numbered sections)
    def fix_h2(m):
        text = m.group(1)
        return f"<h2>{text.upper()}</h2>"
    content = re.sub(r'<h2>([^<]+)</h2>', fix_h2, content)

    # Capitalize h3 (Title Case after number)
    def fix_h3(m):
        text = m.group(1)
        # Split number from text
        match = re.match(r'(\d+\.\d+)\s+(.+)', text)
        if match:
            num, title = match.groups()
            minor = ['de','da','do','das','dos','e','em','no','na','nos','nas','o','a','os','as','um','uma','para','com','por']
            words = title.split()
            result = []
            for i, w in enumerate(words):
                if i == 0 or w.lower() not in minor:
                    result.append(w[0].upper() + w[1:] if len(w) > 1 else w.upper())
                else:
                    result.append(w.lower())
            return f"<h3>{num} {' '.join(result)}</h3>"
        return f"<h3>{text[0].upper() + text[1:] if text else ''}</h3>"
    content = re.sub(r'<h3>([^<]+)</h3>', fix_h3, content)

    # Capitalize h4 (Title Case)
    def fix_h4(m):
        text = m.group(1)
        match = re.match(r'(\d+\.\d+\.\d+)\s+(.+)', text)
        if match:
            num, title = match.groups()
            minor = ['de','da','do','das','dos','e','em','no','na','nos','nas','o','a','os','as','um','uma','para','com','por']
            words = title.split()
            result = []
            for i, w in enumerate(words):
                if i == 0 or w.lower() not in minor:
                    result.append(w[0].upper() + w[1:] if len(w) > 1 else w.upper())
                else:
                    result.append(w.lower())
            return f"<h4>{num} {' '.join(result)}</h4>"
        return f"<h4>{text[0].upper() + text[1:] if text else ''}</h4>"
    content = re.sub(r'<h4>([^<]+)</h4>', fix_h4, content)

    # Ensure RESUMO and ABSTRACT stay uppercase
    content = content.replace('<h2>resumo</h2>', '<h2>RESUMO</h2>')
    content = content.replace('<h2>abstract</h2>', '<h2>ABSTRACT</h2>')

    # Fix table captions: capitalize first letter after "Tabela X. "
    def fix_caption(m):
        text = m.group(1)
        # "Tabela 1. metrica..." -> "Tabela 1. Metrica..."
        text = re.sub(r'(Tabela \d+\.)\s+([a-z])', lambda x: f"{x.group(1)} {x.group(2).upper()}", text)
        return f"<caption>{text}</caption>"
    content = re.sub(r'<caption>([^<]+)</caption>', fix_caption, content)

    # Fix table first column labels (capitalize first letter)
    def fix_td_left(m):
        text = m.group(1).strip()
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        return f'<td class="left">{text}</td>'
    content = re.sub(r'<td class="left">([^<]+)</td>', fix_td_left, content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # Count remaining issues
    dashes = content.count("\u2014") + content.count("&mdash;")
    print(f"  {path.split(chr(92))[-1]}: {dashes} travessoes restantes, {len(content)} bytes")

clean_article(ART01)
clean_article(ART02)

# ============================================================
# REBUILD THESIS
# ============================================================
print("\nReconstruindo tese...")

with open(THESIS, "r", encoding="utf-8") as f:
    thesis = f.read()

with open(ART01, "r", encoding="utf-8") as f:
    art01 = f.read()
with open(ART02, "r", encoding="utf-8") as f:
    art02 = f.read()

# Extract body from articles
art01_body = art01.split("<body>")[1].split("</body>")[0]
art02_body = art02.split("<body>")[1].split("</body>")[0]

# Remove control panels, abstract boxes, page-footers, author info, paper titles
for body_var in ['art01_body', 'art02_body']:
    body = locals()[body_var]
    body = re.sub(r'<div class="control-panel[^>]*>.*?</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="abstract-box">.*?</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<h1 class="paper-title">.*?</h1>', '', body, flags=re.DOTALL)
    body = re.sub(r'<p class="author-info">.*?</p>', '', body, flags=re.DOTALL)
    body = re.sub(r'<div class="page-footer">.*?</div>', '', body)
    body = body.replace('<section class="paper-page">', '').replace('</section>', '')
    body = body.replace('<div class="page-content">', '').replace('</div>', '')
    locals()[body_var] = body

# Renumber Article 01 for Chapter 2: h2 1..5 -> 2.1..2.5, h3 X.Y -> 2.X-1.Y
art01_body = re.sub(r'<h2>1 INTRODUÇÃO</h2>', '<h2>2.1 Introdução</h2>', art01_body)
art01_body = re.sub(r'<h2>2 REFERENCIAL TEÓRICO</h2>', '<h2>2.2 Referencial Teórico</h2>', art01_body)
art01_body = re.sub(r'<h2>3 METODOLOGIA</h2>', '<h2>2.3 Metodologia</h2>', art01_body)
art01_body = re.sub(r'<h2>4 RESULTADOS E DISCUSSÃO</h2>', '<h2>2.4 Resultados e Discussão</h2>', art01_body)
art01_body = re.sub(r'<h2>5 CONCLUSÃO</h2>', '<h2>2.5 Conclusão</h2>', art01_body)
art01_body = re.sub(r'<h2>REFERÊNCIAS</h2>', '', art01_body)

# Renumber Article 01 h3: 2.1 -> 2.2.1, 2.2 -> 2.2.2, 3.1 -> 2.3.1, 4.1 -> 2.4.1
renum_01 = {
    '2.1 ': '2.2.1 ', '2.2 ': '2.2.2 ', '2.3 ': '2.2.3 ', '2.4 ': '2.2.4 ',
    '3.1 ': '2.3.1 ', '3.2 ': '2.3.2 ', '3.3 ': '2.3.3 ', '3.4 ': '2.3.4 ', '3.5 ': '2.3.5 ', '3.6 ': '2.3.6 ',
    '4.1 ': '2.4.1 ', '4.2 ': '2.4.2 ', '4.3 ': '2.4.3 ', '4.4 ': '2.4.4 ', '4.5 ': '2.4.5 ',
}
for old, new in renum_01.items():
    art01_body = art01_body.replace(f'<h3>{old}', f'<h3>{new}')

# Renumber Article 01 h4: 2.2.1 -> 2.2.2.1
art01_body = art01_body.replace('<h4>2.2.1 ', '<h4>2.2.2.1 ')
art01_body = art01_body.replace('<h4>2.2.2 ', '<h4>2.2.2.2 ')

# Renumber Article 02 for Chapter 3
art02_body = re.sub(r'<h2>1 INTRODUÇÃO</h2>', '<h2>3.1 Introdução</h2>', art02_body)
art02_body = re.sub(r'<h2>2 METODOLOGIA DE DESENVOLVIMENTO</h2>', '<h2>3.2 Metodologia de Desenvolvimento</h2>', art02_body)
art02_body = re.sub(r'<h2>3 ARQUITETURA DO PRODUTO</h2>', '<h2>3.3 Arquitetura do Produto</h2>', art02_body)
art02_body = re.sub(r'<h2>4 AVALIAÇÃO E TESTES DE DESEMPENHO</h2>', '<h2>3.4 Avaliação e Testes de Desempenho</h2>', art02_body)
art02_body = re.sub(r'<h2>5 CONCLUSÕES TECNOLÓGICAS</h2>', '<h2>3.5 Conclusões Tecnológicas</h2>', art02_body)
art02_body = re.sub(r'<h2>REFERÊNCIAS</h2>', '', art02_body)

renum_02 = {
    '2.1 ': '3.2.1 ', '2.2 ': '3.2.2 ', '2.3 ': '3.2.3 ', '2.4 ': '3.2.4 ',
    '3.1 ': '3.3.1 ', '3.2 ': '3.3.2 ', '3.3 ': '3.3.3 ', '3.4 ': '3.3.4 ',
    '4.1 ': '3.4.1 ', '4.2 ': '3.4.2 ', '4.3 ': '3.4.3 ',
    '5.1 ': '3.5.1 ',
}
for old, new in renum_02.items():
    art02_body = art02_body.replace(f'<h3>{old}', f'<h3>{new}')

art02_body = art02_body.replace('<h4>2.2.1 ', '<h4>3.2.2.1 ')
art02_body = art02_body.replace('<h4>2.2.2 ', '<h4>3.2.2.2 ')

# Get thesis pre-textual part (everything before Chapter 1)
ch1_marker = '<h2>1 INTRODUÇÃO GERAL</h2>'
parts = thesis.split(ch1_marker, 1)
pre = parts[0] if len(parts) > 1 else thesis

# Get Chapter 4 and 5 and refs from thesis
ch4_marker = '<h2>4 O PRODUTO: COPILOTO ALGORITMICO</h2>'
ch5_marker = '<h2>5 CONCLUSÃO GERAL</h2>'
refs_marker = '<h2>REFERÊNCIAS CONSOLIDADAS</h2>'

rest = thesis[thesis.find(ch4_marker):] if ch4_marker in thesis else ""

# Rebuild thesis
new_thesis = pre.rstrip('</body>\n</html>')
new_thesis += '\n' + ch1_marker + '\n'
# Add Chapter 1 content from thesis
ch1_start = thesis.find(ch1_marker) + len(ch1_marker)
ch1_end = thesis.find('<h2>2 DIAGNÓSTICO EMPÍRICO DAS COMPRAS COMPLEXAS</h2>')
if ch1_end < 0:
    ch1_end = thesis.find('<h2>2 DIAGNOSTICO EMPIRICO')
ch1_content = thesis[ch1_start:ch1_end] if ch1_end > 0 else ""
new_thesis += ch1_content

# Chapter 2: Article 01
new_thesis += '\n<section class="paper-page">\n<div class="page-content">\n<h2>2 DIAGNÓSTICO EMPÍRICO DAS COMPRAS COMPLEXAS</h2>\n'
new_thesis += art01_body
new_thesis += '\n</div>\n<div class="page-footer">5</div>\n</section>\n'

# Chapter 3: Article 02
new_thesis += '\n<section class="paper-page">\n<div class="page-content">\n<h2>3 COPILOTO ALGORÍTMICO: DESENVOLVIMENTO E VALIDAÇÃO</h2>\n'
new_thesis += art02_body
new_thesis += '\n</div>\n<div class="page-footer">13</div>\n</section>\n'

# Chapters 4, 5, Refs from thesis
new_thesis += rest
new_thesis += '\n</body>\n</html>'

# Final re-acentuation pass
for ascii_word, accented_word in MAPA_ACENTOS.items():
    pattern = re.compile(r'\b' + re.escape(ascii_word) + r'\b', re.IGNORECASE)
    new_thesis = pattern.sub(accented_word, new_thesis)

# Remove any remaining stray dashes
new_thesis = new_thesis.replace("&mdash;", "").replace("\u2014", "").replace("\u2013", "")

with open(THESIS, "w", encoding="utf-8") as f:
    f.write(new_thesis)

print(f"Tese reconstruida: {len(new_thesis)} bytes")

# Final stats
import os
for name, path in [("Artigo 01", ART01), ("Artigo 02", ART02), ("Tese", THESIS)]:
    size = os.path.getsize(path)
    with open(path, encoding="utf-8") as f:
        c = f.read()
    dashes = c.count("\u2014") + c.count("&mdash;")
    tables = c.count("<table>")
    refs = c.count("ref-entry")
    pages = c.count("page-footer")
    print(f"  {name}: {size/1024:.0f}KB | {tables} tabs | {refs} refs | {dashes} trav | {pages} pgs")
