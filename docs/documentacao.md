# Documentação do Projeto de Doutorado

---

## Visão Geral

**Projeto:** Copiloto Algorítmico para Compras Públicas Complexas

**Aluno:** Renato de Oliveira Rosa

**Orientador:** Prof. Dr. Olavo Venturim Caldas

**Instituição:** Fucape Business School - Vitória/ES

**Padrão de Formatação:** APA 7ª Edição (unificado para todos os artigos)

---

## Estrutura de Diretórios

```
Doutorado/
├── Tese/
│   └── tese_draft.html          # Draft da tese em formato multipaper
│
├── Artigos/
│   ├── 01-Opacidade-Institucional/
│   ├── 02-Auditoria-Continua/
│   ├── 03-Predicao-Fracasso/
│   ├── 04-Apagao-Canetas/
│   ├── 05-Redes-Fornecimento/
│   ├── 06-Sobrevivencia-Contratos/
│   ├── 07-Governanca-Algoritmica/
│   ├── 08-XAI-Tribunais-Contas/
│   ├── 09-Jurisprudencia-Medo/
│   ├── 10-Uso-Retorico-Inovacao/
│   ├── 11-Voz-Mercado/
│   ├── 12-Evolucao-Risco-Legislacao/
│   ├── 13-Dor-GovTechs/
│   ├── 14-Discurso-Custo-Brasil/
│   ├── 15-Enquadramento-IA-Midia/
│   ├── 16-Caixa-Preta-XAI/
│   └── 17-DSR-Contabilidade/
│
├── css/
│   └── style_academico.css      # CSS unificado APA
│
├── docs/
│   ├── Direcionamento.md        # Documento de direcionamento
│   ├── escrita.md               # Guia de escrita APA
│   ├── regras_tabelas.md       # Regras de tabelas APA
│   ├── pesquisa.md              # Guia de pesquisa e APIs
│   └── processo.md              # Padrões de engenharia
│
└── Base_de_Dados_e_APIs/         # Dados e scripts
```

---

## Padrão APA 7ª Edição

Todos os artigos seguem o **padrão APA 7ª edição** conforme documento `docs/escrita.md`.

### Elementos Principais

| Elemento | Especificação |
|----------|---------------|
| Fonte | Times New Roman 12pt |
| Espaçamento | Duplo |
| Margens | 2,54 cm em todos os lados |
| Recuo de parágrafo | 1,27 cm (0,5 polegada) |
| Alinhamento | À esquerda |
| Citações | Sistema autor-data |
| Referências | Recuo francês (hanging indent) |

---

## Frente Quantitativa (8 artigos)

| # | Artigo | Metodologia | Estatísticas | Status |
|---|--------|-------------|-------------|--------|
| 1 | Opacidade Institucional | NLP - Regressão Múltipla | n=40, R² adj=0,862, FK adaptado (Martins) | ✅ |
| 2 | Auditoria Contínua | ML - Detecção anomalias | 10.5K registros | ✅ |
| 3 | Predição de Fracasso | ML - Random Forest | 12.5K registros, 78,24% acurácia | ✅ |
| 4 | Apagão das Canetas | Séries Temporais OLS | 9K registros, R²=90,64% | ✅ |
| 5 | Redes de Fornecimento | Teoria Grafos (NetworkX) | 400 nós, 1.1K arestas, Gini=0,907 | ✅ |
| 6 | Sobrevivência Contratos | Kaplan-Meier / Cox | 10K registros, C-Index=78,54% | ✅ |
| 7 | Governança Algorítmica | DSR + Benchmarking | 180 municípios, Siconfi | ✅ |
| 8 | XAI Tribunais de Contas | Random Forest + SHAP | 8.5K registros, 94,88% acurácia | ✅ |

---

## Frente Qualitativa (9 artigos)

| # | Artigo | Metodologia | Corpus | Status |
|---|--------|-------------|--------|--------|
| 9 | Jurisprudência do Medo | ACD (Fairclough) | 5 acórdãos TCU | ✅ |
| 10 | Uso Retórico Inovação | Análise Conteúdo (Bardin) | 350 justificativas PNCP | ✅ |
| 11 | Voz do Mercado | Análise Conteúdo (Bardin) | 150 impugnações | ✅ |
| 12 | Evolução Risco Legislação | Análise Lexicográfica | 5 marcos legais, χ²=216,14 | ✅ |
| 13 | Dor das GovTechs | Netnografia (Kozinets) | 60 relatos LinkedIn/Medium | ✅ |
| 14 | Discurso Custo Brasil | ACD (Fairclough) | 50 trechos MDIC/ABDI | ✅ |
| 15 | IA na Mídia | Framing Analysis (Entman) | 388 matérias, χ²=108,45 | ✅ |
| 16 | Caixa-Preta Setor Público | Revisão Sistemática (PRISMA) | 52 artigos OpenAlex | ✅ |
| 17 | DSR Contabilidade Pública | Scoping Review (PRISMA-ScR) | 42 artigos, matriz Gregor & Hevner | ✅ |

---

## Repositório GitHub

**URL:** https://github.com/renato0503/TeseDoutorado

---

## Referências Principais

### Teóricas
- Economia dos Custos de Transação (Williamson, 1985)
- Estado Empreendedor (Mazzucato, 2013)
- Transparência Algorítmica (Arrieta et al., 2020)
- Design Science Research (Hevner et al., 2004; Peffers et al., 2007)

### Metodológicas
- Revisão Sistemática (PRISMA)
- Método Delphi
- Processamento de Linguagem Natural
- Machine Learning para detecção de anomalias

### Dados
- Portal Nacional de Contratações Públicas (PNCP)
- Portal da Transparência (CGU)
- Tribunal de Contas da União (TCU)
- Compras.gov.br

---

## Estrutura CSS Unificada

O arquivo `css/style_academico.css` fornece:

1. **Visualização em tela**: Páginas simuladas A4 com margens
2. **Impressão**: PDF formatado corretamente
3. **Exportação**: HTML para abrir no Word

### Classes Principais

| Classe | Uso |
|--------|-----|
| `.paper-page` | Container de página simulada |
| `.abstract-box` | Box de Resumo/Abstract |
| `.abnt-table` | Tabela formatada APA |
| `.figure-container` | Container de figura/gráfico |
| `.control-panel` | Botões de exportação (não impresso) |
| `.ref-entry` | Entrada de referência bibliográfica |

---

## Exportação para Word

### Método Recomendado

1. Clique em **"Imprimir / Salvar PDF"** para obter PDF formatado
2. Ou use **"Baixar HTML (abrir no Word)"** e abra o arquivo no Microsoft Word
3. No Word, use "Salvar como" → "Documento Word (.docx)"

### Script de Exportação

```html
<script>
function exportarHTML() {
    const htmlContent = document.documentElement.outerHTML;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = document.title + '.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
</script>
```

---

*Última atualização: Maio 2026*
*Padrão: APA 7ª Edição*