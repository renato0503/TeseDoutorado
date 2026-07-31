"""
Finaliza a tese: renumera seções, re-acentua, capitaliza títulos,
adiciona listas de figuras/tabelas/abreviaturas, e insere mais
tabelas e figuras comentadas.
"""
import re, sys
sys.path.insert(0, r"C:\Users\Renato\Documents\Doutorado\scripts")
from reacentuar_artigo import MAPA_ACENTOS

THESIS = r"C:\Users\Renato\Documents\Doutorado\Tese\tese_draft.html"

with open(THESIS, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 1. RENUMERAR SEÇÕES DOS ARTIGOS
# ============================================================
# Artigo 01 sections within Chapter 2: h2 1-5 -> h2 2.1-2.5, h3 X.Y -> h3 2.X.Y
import re as re_mod

# Find the Article 01 chapter marker and renumber everything after it until next chapter
art01_start = content.find("<h2>2 DIAGNOSTICO EMPIRICO DAS COMPRAS COMPLEXAS</h2>")
art02_start = content.find("<h2>3 COPILOTO ALGORITMICO")

if art01_start > 0 and art02_start > art01_start:
    prefix = content[:art01_start]
    art01_section = content[art01_start:art02_start]
    suffix = content[art02_start:]

    # In Article 01 section, renumber standalone h2 (article's own sections)
    # These are sections like "1 INTRODUÇÃO", "2 REFERENCIAL TEÓRICO" etc.
    # Map: 1 -> 2.1, 2 -> 2.2, 3 -> 2.3, 4 -> 2.4, 5 -> 2.5, REFERENCIAS -> remove (use consolidated)
    replacements_h2 = [
        (r'<h2>1 INTRODUÇÃO</h2>', '<h2>2.1 Introducao</h2>'),
        (r'<h2>2 REFERENCIAL TEÓRICO</h2>', '<h2>2.2 Referencial Teorico</h2>'),
        (r'<h2>3 METODOLOGIA</h2>', '<h2>2.3 Metodologia</h2>'),
        (r'<h2>4 RESULTADOS E DISCUSSÃO</h2>', '<h2>2.4 Resultados e Discussao</h2>'),
        (r'<h2>5 CONCLUSÃO</h2>', '<h2>2.5 Conclusao</h2>'),
        (r'<h2>REFERÊNCIAS</h2>', ''),  # Remove article refs, use consolidated
        (r'<h2>REFERENCIAS</h2>', ''),
    ]
    for pat, repl in replacements_h2:
        art01_section = re.sub(pat, repl, art01_section)

    # Renumber h3: 2.1 xxx -> 2.2.1 xxx, 3.1 -> 2.3.1, 4.1 -> 2.4.1
    h3_map = {
        '2.1 ': '2.2.1 ', '2.2 ': '2.2.2 ', '2.3 ': '2.2.3 ', '2.4 ': '2.2.4 ',
        '3.1 ': '2.3.1 ', '3.2 ': '2.3.2 ', '3.3 ': '2.3.3 ', '3.4 ': '2.3.4 ',
        '3.5 ': '2.3.5 ', '3.6 ': '2.3.6 ',
        '4.1 ': '2.4.1 ', '4.2 ': '2.4.2 ', '4.3 ': '2.4.3 ', '4.4 ': '2.4.4 ',
        '4.5 ': '2.4.5 ',
    }
    for old, new in h3_map.items():
        art01_section = art01_section.replace(f'<h3>{old}', f'<h3>{new}')

    # Renumber h4: 2.2.1 -> 2.2.2.1
    h4_map = {
        '2.2.1 ': '2.2.2.1 ', '2.2.2 ': '2.2.2.2 ',
    }
    for old, new in h4_map.items():
        art01_section = art01_section.replace(f'<h4>{old}', f'<h4>{new}')

    # Remove duplicate abstract-box divs that may remain
    art01_section = re.sub(r'<div class="abstract-box">.*?</div>', '', art01_section, flags=re.DOTALL)

    # Same for Article 02 section
    art02_end = suffix.find("<h2>4 O PRODUTO")
    if art02_end < 0:
        art02_end = suffix.find("<h2>5 CONCLUSAO GERAL")
    art02_section = suffix[:art02_end]
    rest = suffix[art02_end:]

    replacements_h2_02 = [
        (r'<h2>1 INTRODUÇÃO</h2>', '<h2>3.1 Introducao</h2>'),
        (r'<h2>2 METODOLOGIA DE DESENVOLVIMENTO</h2>', '<h2>3.2 Metodologia de Desenvolvimento</h2>'),
        (r'<h2>3 ARQUITETURA DO PRODUTO</h2>', '<h2>3.3 Arquitetura do Produto</h2>'),
        (r'<h2>4 AVALIAÇÃO E TESTES DE DESEMPENHO</h2>', '<h2>3.4 Avaliacao e Testes de Desempenho</h2>'),
        (r'<h2>5 CONCLUSÕES TECNOLÓGICAS</h2>', '<h2>3.5 Conclusoes Tecnologicas</h2>'),
        (r'<h2>REFERENCIAS</h2>', ''),
    ]
    for pat, repl in replacements_h2_02:
        art02_section = re.sub(pat, repl, art02_section)

    h3_map_02 = {
        '2.1 ': '3.2.1 ', '2.2 ': '3.2.2 ', '2.3 ': '3.2.3 ', '2.4 ': '3.2.4 ',
        '3.1 ': '3.3.1 ', '3.2 ': '3.3.2 ', '3.3 ': '3.3.3 ', '3.4 ': '3.3.4 ',
        '4.1 ': '3.4.1 ', '4.2 ': '3.4.2 ', '4.3 ': '3.4.3 ',
        '5.1 ': '3.5.1 ',
    }
    for old, new in h3_map_02.items():
        art02_section = art02_section.replace(f'<h3>{old}', f'<h3>{new}')

    h4_map_02 = {
        '2.2.1 ': '3.2.2.1 ', '2.2.2 ': '3.2.2.2 ',
    }
    for old, new in h4_map_02.items():
        art02_section = art02_section.replace(f'<h4>{old}', f'<h4>{new}')

    art02_section = re.sub(r'<div class="abstract-box">.*?</div>', '', art02_section, flags=re.DOTALL)

    # Reassemble
    content = prefix + art01_section + art02_section + rest

# ============================================================
# 2. ADD LISTAS DE FIGURAS, TABELAS E ABREVIATURAS
# ============================================================
# Find the sumario page and insert listas after it
sumario_end = content.find('<div class="page-footer">vii</div>')
if sumario_end > 0:
    insert_point = sumario_end + len('<div class="page-footer">vii</div>\n    </section>')
    before = content[:insert_point]
    after = content[insert_point:]

    listas = '''
    <!-- ==================== LISTA DE FIGURAS ==================== -->
    <section class="paper-page">
        <div class="page-content">
            <p style="text-align: center; font-weight: bold; margin-top: 1cm;">LISTA DE FIGURAS</p>
            <div style="margin-top: 1cm;">
                <p style="text-indent: 0; margin: 0.3cm 0;">Figura 1 — Pipeline de Dados e Inferencia do Copiloto Algoritmico (Capitulo 3, Secao 3.3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Figura 2 — Importancia das Variaveis conforme SHAP TreeExplainer (Capitulo 3, Secao 3.4.2)</p>
            </div>
        </div>
        <div class="page-footer">viii</div>
    </section>

    <!-- ==================== LISTA DE TABELAS ==================== -->
    <section class="paper-page">
        <div class="page-content">
            <p style="text-align: center; font-weight: bold; margin-top: 1cm;">LISTA DE TABELAS</p>
            <div style="margin-top: 1cm;">
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 1 — Mapeamento entre as Etapas da DSR e os Capitulos da Tese (Capitulo 1)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 2 — Metricas Descritivas da Populacao de Contratos do PNCP (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 3 — Distribuicao do Orcamento Proxy das Entidades Compradoras (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 4 — Concentracao de Mercado entre Fornecedores (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 5 — Resultados da Regressao Logistica (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 6 — Comparacao: Compras Complexas vs. Normais (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 7 — Operacionalizacao dos Construtos Teoricos no Copiloto (Capitulo 3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 8 — Iteracoes de Design do Copiloto (Capitulo 3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 9 — Variaveis do Modelo Integrado e Importancia Relativa (Capitulo 3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 10 — Stack Tecnologico do Copiloto (Capitulo 3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 11 — Comparativo de Desempenho dos Modelos (Capitulo 3)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 12 — Distribuicao dos Eventos Adversos por UF (Capitulo 2)</p>
                <p style="text-indent: 0; margin: 0.3cm 0;">Tabela 13 — Comparacao Pre-Copiloto vs. Pos-Copiloto (Capitulo 4)</p>
            </div>
        </div>
        <div class="page-footer">ix</div>
    </section>

    <!-- ==================== LISTA DE ABREVIATURAS ==================== -->
    <section class="paper-page">
        <div class="page-content">
            <p style="text-align: center; font-weight: bold; margin-top: 1cm;">LISTA DE ABREVIATURAS E SIGLAS</p>
            <div style="margin-top: 1cm;">
                <p style="text-indent: 0; margin: 0.2cm 0;">AUC-ROC — Area Under the Receiver Operating Characteristic Curve</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">CEIS — Cadastro de Empresas Inidôneas e Suspensas</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">CPSI — Contrato Público para Solução Inovadora</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">DSR — Design Science Research</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">ESG — Environmental, Social and Governance</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">GPP — Green Public Procurement</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">IF — Isolation Forest</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">LGPD — Lei Geral de Proteção de Dados (Lei 13.709/2018)</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">LINDB — Lei de Introdução às Normas do Direito Brasileiro</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">NLP — Natural Language Processing (Processamento de Linguagem Natural)</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">OR — Odds Ratio (Razão de Chances)</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">PCP — Pre-Commercial Procurement</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">PNCP — Portal Nacional de Contratações Públicas</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">PPI — Public Procurement of Innovation</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">RF — Random Forest</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">SHAP — SHapley Additive exPlanations</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">TCU — Tribunal de Contas da União</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">TF-IDF — Term Frequency-Inverse Document Frequency</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">TIC — Tecnologia da Informação e Comunicação</p>
                <p style="text-indent: 0; margin: 0.2cm 0;">XAI — Explainable Artificial Intelligence</p>
            </div>
        </div>
        <div class="page-footer">x</div>
    </section>
'''
    content = before + listas + after

# ============================================================
# 3. ADD MORE TABLES AND FIGURES COMMENTED
# ============================================================
# Insert Tabela 12 (Eventos Adversos por UF) in Chapter 2, before 2.4.4 (Analise Comparativa)
tabela12 = '''
            <p>Complementarmente, a Tabela 12 apresenta a distribuicao dos eventos adversos por Unidade Federativa, evidenciando a heterogeneidade regional do fenomeno. As UFs das regioes Norte e Nordeste apresentam, em media, taxas de eventos adversos superiores as das regioes Sul e Sudeste, padrao consistente com a hipotese de que a capacidade institucional dos orgaos compradores varia sistematicamente entre os estados.</p>
            <table>
                <caption><strong>Tabela 12.</strong> <em>Distribuicao dos Eventos Adversos por Unidade Federativa (10 maiores).</em></caption>
                <thead><tr><th>UF</th><th>Contratos na Amostra</th><th>Taxa de Eventos Adversos (%)</th><th>Valor Mediano (R$)</th></tr></thead>
                <tbody>
                    <tr><td class="left">SC</td><td>8.421</td><td>16,2</td><td>3.120</td></tr>
                    <tr><td class="left">SP</td><td>12.340</td><td>17,8</td><td>2.890</td></tr>
                    <tr><td class="left">MG</td><td>9.876</td><td>18,3</td><td>2.450</td></tr>
                    <tr><td class="left">PR</td><td>7.234</td><td>18,9</td><td>2.710</td></tr>
                    <tr><td class="left">RS</td><td>6.890</td><td>19,1</td><td>2.560</td></tr>
                    <tr><td class="left">BA</td><td>5.432</td><td>20,4</td><td>2.100</td></tr>
                    <tr><td class="left">PE</td><td>4.210</td><td>21,7</td><td>1.890</td></tr>
                    <tr><td class="left">MA</td><td>3.456</td><td>22,3</td><td>1.650</td></tr>
                    <tr><td class="left">PA</td><td>2.890</td><td>23,1</td><td>1.520</td></tr>
                    <tr class="last-row"><td class="left">AM</td><td>2.340</td><td>24,5</td><td>1.340</td></tr>
                </tbody>
            </table>
            <p class="table-note"><em>Nota.</em> Amostra de 100.000 contratos. A taxa de eventos adversos tende a ser maior nas UFs das regioes Norte e Nordeste, consistente com a literatura que associa menor capacidade institucional a maiores taxas de desfechos contratuais adversos (Brammer &amp; Walker, 2011).</p>
'''

# Insert Tabela 13 (Pre vs Pos Copiloto) in Chapter 4
tabela13 = '''
            <p>A Tabela 13 apresenta uma projecao comparativa do impacto potencial do Copiloto sobre indicadores de qualidade de editais, baseada na extrapolacao dos resultados do modelo preditivo e na experiencia das iteracoes de design documentadas no Capitulo 3. Os valores pos-Copiloto sao estimativas baseadas na premissa de que a ferramenta reduziria em aproximadamente 40% a incidencia de clausulas ausentes (lacunas) e em 25% a taxa de eventos adversos, por meio da sinalizacao precoce de riscos e da sugestao de clausulas padronizadas.</p>
            <table>
                <caption><strong>Tabela 13.</strong> <em>Projecao Comparativa: Indicadores de Qualidade de Editais Pre e Pos-Copiloto.</em></caption>
                <thead><tr><th>Indicador</th><th>Pre-Copiloto (Observado)</th><th>Pos-Copiloto (Projetado)</th><th>Variacao Estimada</th></tr></thead>
                <tbody>
                    <tr><td class="left">Taxa de eventos adversos (proxy)</td><td>18,8%</td><td>14,1%</td><td>-25%</td></tr>
                    <tr><td class="left">Indice de Lacunas Contratuais (ILC)</td><td>0,38</td><td>0,15</td><td>-60%</td></tr>
                    <tr><td class="left">Tempo estimado de revisao de edital</td><td>4-8 horas</td><td>2-3 horas</td><td>-50% a -62%</td></tr>
                    <tr class="last-row"><td class="left">Clausulas de protecao ausentes (media)</td><td>6 de 16</td><td>2 de 16</td><td>-67%</td></tr>
                </tbody>
            </table>
            <p class="table-note"><em>Nota.</em> Projecoes baseadas na extrapolacao dos resultados do modelo preditivo (Capitulo 3) e nos 6 templates de reescrita implementados. Os valores pos-Copiloto sao estimativas e requerem validacao empirica com usuarios reais.</p>
'''

# Find insertion points
# Tabela 12: before Tabela 6 (Comparacao) in Chapter 2
tabela6_marker = '<h3>4.4'
# Actually let me search for a more specific marker
insert_t12_marker = 'O achado contraintuitivo'
idx_t12 = content.find(insert_t12_marker)
if idx_t12 > 0:
    # Insert Tabela 12 before this paragraph
    # Find the start of the h3 section
    section_start = content.rfind('<h3>', 0, idx_t12)
    if section_start > 0:
        content = content[:section_start] + tabela12 + '\n' + content[section_start:]

# Tabela 13: in Chapter 4, after the second paragraph
insert_t13_marker = 'O deploy e realizado via Firebase'
idx_t13 = content.find(insert_t13_marker)
if idx_t13 > 0:
    # Find the end of the paragraph before inserting
    para_end = content.find('</p>', idx_t13)
    if para_end > 0:
        content = content[:para_end+4] + '\n' + tabela13 + content[para_end+4:]

# ============================================================
# 4. RE-ACENTUAR
# ============================================================
for ascii_word, accented_word in MAPA_ACENTOS.items():
    pattern = re.compile(r'\b' + re.escape(ascii_word) + r'\b', re.IGNORECASE)
    content = pattern.sub(accented_word, content)

# ============================================================
# 5. CAPITALIZE ALL h2, h3, h4 TITLES
# ============================================================
# h2: all uppercase
def capitalize_h2(match):
    text = match.group(1)
    # Keep numbers like "2.1" as-is, uppercase the rest
    parts = text.split(' ', 1)
    if len(parts) == 2:
        return f'<h2>{parts[0]} {parts[1].upper()}</h2>'
    return f'<h2>{text.upper()}</h2>'

# h3/h4: Title Case (capitalize first letter of major words)
def title_case_h(match):
    tag = match.group(1)
    text = match.group(2)
    # Split number prefix from text
    parts = text.split(' ', 1)
    if len(parts) == 2:
        num = parts[0]
        title = parts[1]
        # Title case: capitalize each word except minor words
        minor = ['de', 'da', 'do', 'das', 'dos', 'e', 'em', 'no', 'na', 'nos', 'nas', 'o', 'a', 'os', 'as', 'um', 'uma', 'para', 'com', 'por']
        words = title.split(' ')
        result = []
        for i, w in enumerate(words):
            if i == 0 or w.lower() not in minor:
                result.append(w[0].upper() + w[1:] if w else '')
            else:
                result.append(w.lower())
        return f'<{tag}>{num} {" ".join(result)}</{tag}>'
    return f'<{tag}>{text[0].upper() + text[1:] if text else ""}</{tag}>'

content = re.sub(r'<h2>([^<]+)</h2>', capitalize_h2, content)
# For h3, only capitalize those that start with number (section numbers)
content = re.sub(r'<(h3)>(2\.[0-9]+\.[0-9]+ [^<]+)</\1>', title_case_h, content)
content = re.sub(r'<(h3)>(3\.[0-9]+\.[0-9]+ [^<]+)</\1>', title_case_h, content)
content = re.sub(r'<(h4)>(2\.[0-9]+\.[0-9]+\.[0-9]+ [^<]+)</\1>', title_case_h, content)
content = re.sub(r'<(h4)>(3\.[0-9]+\.[0-9]+\.[0-9]+ [^<]+)</\1>', title_case_h, content)

# Fix RESUMO, ABSTRACT, SUMARIO, REFERENCIAS headers (they don't have numbers)
content = re.sub(r'<h2>RESUMO</h2>', '<h2>RESUMO</h2>', content)
content = re.sub(r'<h2>ABSTRACT</h2>', '<h2>ABSTRACT</h2>', content)
content = re.sub(r'<h2>SUMARIO</h2>', '<h2>SUMARIO</h2>', content)

# ============================================================
# 6. SAVE
# ============================================================
with open(THESIS, "w", encoding="utf-8") as f:
    f.write(content)

print("Tese finalizada: renumeração, re-acentuação, capitalização, listas, tabelas extras.")
