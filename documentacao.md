
# 📄 Documento de Especificações v2 — Paper Builder App (Melhorado)

---

## 1. Visão Geral Atualizada

**Nome do App:** Paper Builder

**Objetivo:** Aplicativo local para construção modular de papers acadêmicos com auxílio de IAs gratuitas, com gestão completa de referências, dados, análises e exportação profissional.

**Stack:**

- **Frontend:** React + Vite
- **Estilização:** Tailwind CSS
- **Backend local:** Node.js (Express)
- **IAs Gratuitas:**
  - **MiniMax** (via OpenCode)
  - **Gemini Flash** (via Antigravity)
- **Bibliotecas auxiliares:**
  - `docxtemplater` ou `officegen` → gerar .docx
  - `papaparse` → ler CSVs
  - `chart.js` ou `plotly.js` → gerar gráficos
  - `pdf-parse` → extrair texto de PDFs
  - `mammoth` → converter docx para HTML
  - `marked` → renderizar Markdown
- **Futuro:** Firebase, APIs pagas (GPT-4, Claude)

---

## 2. Nova Estrutura de Pastas por Paper

```
/papers
│
├── /impacto-ia-educacao/
│   │
│   ├── 📋 metadata.json              # Configurações e status do paper
│   ├── 📋 contexto.json              # Contexto geral do paper para a IA
│   │
│   ├── /01-referencias/              # 📚 ARTIGOS BASE
│   │   ├── artigo-fulano-2023.pdf
│   │   ├── artigo-ciclano-2022.pdf
│   │   ├── artigo-beltrano-2024.pdf
│   │   └── _resumos_extraidos.json   # Resumos extraídos pela IA
│   │
│   ├── /02-dados/                    # 📊 DADOS DA PESQUISA
│   │   ├── dados-questionario.csv
│   │   ├── dados-experimento.csv
│   │   ├── dados-demograficos.csv
│   │   └── _analise_dados.json       # Metadados dos CSVs analisados
│   │
│   ├── /03-analises/                 # 📈 OUTPUTS DE ANÁLISES
│   │   ├── grafico-barras-q1.png
│   │   ├── grafico-correlacao.png
│   │   ├── tabela-descritiva.png
│   │   ├── grafico-pizza-demo.png
│   │   └── _descricao_graficos.json  # Descrições dos gráficos para a IA
│   │
│   ├── /04-secoes/                   # ✍️ SEÇÕES DO PAPER (Markdown)
│   │   ├── 01-titulo.md
│   │   ├── 02-resumo.md
│   │   ├── 03-palavras-chave.md
│   │   ├── 04-introducao.md
│   │   ├── 05-revisao-literatura.md
│   │   ├── 06-metodologia.md
│   │   ├── 07-resultados.md
│   │   ├── 08-discussao.md
│   │   ├── 09-conclusao.md
│   │   ├── 10-referencias.md
│   │   ├── 11-apendices.md
│   │   └── 12-agradecimentos.md
│   │
│   ├── /05-documento/                # 📄 DOCUMENTO FINAL
│   │   ├── paper-v1.docx
│   │   ├── paper-v2.docx
│   │   └── paper-final.docx
│   │
│   ├── /06-notas/                    # 📝 NOTAS E RASCUNHOS
│   │   ├── brainstorm.md
│   │   ├── ideias-gerais.md
│   │   └── feedback-orientador.md
│   │
│   ├── /07-prompts/                  # 🤖 HISTÓRICO DE PROMPTS
│   │   ├── prompts-introducao.json
│   │   ├── prompts-metodologia.json
│   │   └── prompts-discussao.json
│   │
│   └── /08-templates/                # 📐 TEMPLATES
│       ├── template-abnt.docx
│       └── template-apa.docx
```

---

## 3. Contexto Inteligente — `contexto.json`

```json
{
  "paper_id": "impacto-ia-educacao",
  "tema_central": "Impacto da IA generativa na educação superior brasileira",
  "problema_pesquisa": "Como a IA generativa está transformando os métodos de ensino?",
  "hipotese": "O uso de IA generativa melhora o desempenho acadêmico em 30%",
  "objetivo_geral": "Analisar o impacto da IA generativa na educação superior",
  "objetivos_especificos": [
    "Mapear ferramentas de IA utilizadas",
    "Medir desempenho antes e depois da adoção",
    "Identificar desafios e oportunidades"
  ],
  "publico_alvo": "Estudantes de graduação em universidades públicas",
  "metodologia_resumo": "Pesquisa quantitativa com questionários aplicados a 200 alunos",
  "palavras_chave": ["inteligência artificial", "educação", "ensino superior"],
  "norma_formatacao": "ABNT",
  "idioma": "pt-BR",
  "tom_escrita": "formal-academico",
  "referencias_resumidas": [],
  "dados_resumidos": [],
  "graficos_disponiveis": []
}
```

> **Esse arquivo é o CÉREBRO do paper.** Toda vez que a IA for chamada, esse contexto é enviado junto para manter coerência.

---

## 4. Seções Completas do Paper

| #  | Seção                          | Arquivo                      | Descrição                                                             |
| -- | -------------------------------- | ---------------------------- | ----------------------------------------------------------------------- |
| 1  | **Título**                | `01-titulo.md`             | Título claro e descritivo do paper                                     |
| 2  | **Resumo / Abstract**      | `02-resumo.md`             | Síntese de 150-300 palavras: problema, método, resultados, conclusão |
| 3  | **Palavras-chave**         | `03-palavras-chave.md`     | 3 a 6 termos que definem o trabalho                                     |
| 4  | **Introdução**           | `04-introducao.md`         | Contextualização, justificativa, problema, objetivos                  |
| 5  | **Revisão da Literatura** | `05-revisao-literatura.md` | Estado da arte baseado nos PDFs da pasta `/01-referencias`            |
| 6  | **Metodologia**            | `06-metodologia.md`        | Tipo de pesquisa, amostra, instrumentos, procedimentos                  |
| 7  | **Resultados**             | `07-resultados.md`         | Apresentação dos dados + gráficos da pasta `/03-analises`          |
| 8  | **Discussão**             | `08-discussao.md`          | Interpretação dos resultados × literatura                            |
| 9  | **Conclusão**             | `09-conclusao.md`          | Síntese, contribuições, limitações, trabalhos futuros              |
| 10 | **Referências**           | `10-referencias.md`        | Lista formatada (ABNT/APA) de todas as fontes                           |
| 11 | **Apêndices**             | `11-apendices.md`          | Questionários, tabelas extras, dados complementares                    |
| 12 | **Agradecimentos**         | `12-agradecimentos.md`     | Agradecimentos a orientadores, instituições, etc.                     |

---

## 5. Telas do App (Atualizadas)

### **Tela 1 — Dashboard**

*(Igual à v1 mas com mais info)*

```
┌───────────────────────────────────────────────────────┐
│  📚 PAPER BUILDER                        [⚙️ Config]  │
│───────────────────────────────────────────────────────│
│                                                       │
│  [+ Novo Paper]                    🔍 [Buscar...]     │
│                                                       │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 📄 Impacto da IA na Educação                    │  │
│  │ ████████░░░░░░░░░░ 40%                          │  │
│  │ 📚 5 refs  📊 3 CSVs  📈 4 gráficos            │  │
│  │ 🤖 MiniMax  |  Última edição: 20/01/2024        │  │
│  │ [Abrir]  [Exportar DOCX]  [Duplicar]  [Excluir] │  │
│  └─────────────────────────────────────────────────┘  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

---

### **Tela 2 — Criar Novo Paper (Wizard em Etapas)**

```
┌───────────────────────────────────────────────────────┐
│  📝 NOVO PAPER — Etapa 1 de 4                         │
│───────────────────────────────────────────────────────│
│  ● Básico  ○ Contexto  ○ Referências  ○ Dados        │
│                                                       │
│  Título do Paper:                                     │
│  [____________________________________________]       │
│                                                       │
│  Autor(es):                                           │
│  [____________________________________________]       │
│                                                       │
│  Idioma: (•) Português  ( ) Inglês                    │
│  Norma:  (•) ABNT  ( ) APA  ( ) Vancouver            │
│                                                       │
│  IA Principal:                                        │
│  (•) MiniMax (OpenCode - Free)                        │
│  ( ) Gemini Flash (Antigravity - Free)                │
│                                                       │
│                          [Próximo →]                   │
└───────────────────────────────────────────────────────┘
```

```
┌───────────────────────────────────────────────────────┐
│  📝 NOVO PAPER — Etapa 2 de 4                         │
│───────────────────────────────────────────────────────│
│  ○ Básico  ● Contexto  ○ Referências  ○ Dados        │
│                                                       │
│  Tema central:                                        │
│  [____________________________________________]       │
│                                                       │
│  Problema de pesquisa:                                │
│  [____________________________________________]       │
│                                                       │
│  Hipótese:                                            │
│  [____________________________________________]       │
│                                                       │
│  Objetivo geral:                                      │
│  [____________________________________________]       │
│                                                       │
│  Objetivos específicos:                               │
│  [____________________________________________]       │
│  [+ Adicionar objetivo]                               │
│                                                       │
│  Palavras-chave (separadas por vírgula):              │
│  [____________________________________________]       │
│                                                       │
│  💡 [Preencher com IA] — gera sugestões automáticas   │
│                                                       │
│              [← Voltar]    [Próximo →]                 │
└───────────────────────────────────────────────────────┘
```

```
┌───────────────────────────────────────────────────────┐
│  📝 NOVO PAPER — Etapa 3 de 4                         │
│───────────────────────────────────────────────────────│
│  ○ Básico  ○ Contexto  ● Referências  ○ Dados        │
│                                                       │
│  📚 Upload de Artigos Base (PDF):                     │
│                                                       │
│  ┌───────────────────────────────────────────┐        │
│  │                                           │        │
│  │     Arraste PDFs aqui ou clique            │        │
│  │     para fazer upload                     │        │
│  │                                           │        │
│  └───────────────────────────────────────────┘        │
│                                                       │
│  Arquivos carregados:                                 │
│  ✅ artigo-fulano-2023.pdf (2.3 MB)     [🗑️]         │
│  ✅ artigo-ciclano-2022.pdf (1.8 MB)    [🗑️]         │
│  🔄 Extraindo texto... artigo-beltrano.pdf            │
│                                                       │
│  💡 A IA vai extrair os pontos principais de cada     │
│     artigo para usar como contexto                    │
│                                                       │
│              [← Voltar]    [Próximo →]                 │
└───────────────────────────────────────────────────────┘
```

```
┌───────────────────────────────────────────────────────┐
│  📝 NOVO PAPER — Etapa 4 de 4                         │
│───────────────────────────────────────────────────────│
│  ○ Básico  ○ Contexto  ○ Referências  ● Dados        │
│                                                       │
│  📊 Upload de Dados (CSV/Excel):                      │
│                                                       │
│  ┌───────────────────────────────────────────┐        │
│  │                                           │        │
│  │     Arraste CSVs aqui ou clique            │        │
│  │     para fazer upload                     │        │
│  │                                           │        │
│  └───────────────────────────────────────────┘        │
│                                                       │
│  Arquivos carregados:                                 │
│  ✅ dados-questionario.csv — 200 linhas, 15 colunas  │
│     Colunas: idade, genero, curso, nota_antes...      │
│  ✅ dados-demograficos.csv — 200 linhas, 5 colunas   │
│                                                       │
│  ⚠️ Opcional: pode adicionar depois                   │
│                                                       │
│              [← Voltar]    [✅ Criar Paper]            │
└───────────────────────────────────────────────────────┘
```

---

### **Tela 3 — Painel do Paper (Hub Central)**

```
┌──────────────────────────────────────────────────────────────┐
│  📄 Impacto da IA na Educação              [⚙️] [📥 Export]  │
│  ████████████░░░░░░░░░░░░ 45%                                │
│──────────────────────────────────────────────────────────────│
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │ 📚 REFERÊNCIAS│ │ 📊 DADOS     │ │ 📈 ANÁLISES  │         │
│  │  5 artigos   │ │  3 CSVs      │ │  4 gráficos  │         │
│  │  [Gerenciar] │ │  [Gerenciar] │ │  [Gerenciar] │         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │ 📝 NOTAS     │ │ 🤖 PROMPTS   │ │ 📄 DOCUMENTO │         │
│  │  2 notas     │ │  12 prompts  │ │  v2.docx     │         │
│  │  [Gerenciar] │ │  [Ver hist.] │ │  [Abrir]     │         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
│                                                              │
│  ── SEÇÕES DO PAPER ─────────────────────────────────────    │
│                                                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │✅ Título    │ │✅ Resumo    │ │✅ Palavras  │               │
│  │ [Editar]   │ │ [Editar]   │ │  [Editar]  │               │
│  └────────────┘ └────────────┘ └────────────┘               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │🔄 Introdução│ │⬜ Rev.Lit.  │ │⬜ Metodo.   │               │
│  │ [Editar]   │ │ [Iniciar]  │ │ [Iniciar]  │               │
│  └────────────┘ └────────────┘ └────────────┘               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │⬜ Resultados│ │⬜ Discussão │ │⬜ Conclusão │               │
│  │ [Iniciar]  │ │ [Iniciar]  │ │ [Iniciar]  │               │
│  └────────────┘ └────────────┘ └────────────┘               │
│  ┌────────────┐ ┌────────────┐                              │
│  │⬜ Referênc. │ │⬜ Apêndices │                              │
│  │ [Iniciar]  │ │ [Iniciar]  │                              │
│  └────────────┘ └────────────┘                              │
│                                                              │
│  [← Dashboard]  [🔄 Gerar DOCX]  [📥 Exportar PDF]          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### **Tela 4 — Gerenciador de Referências**

```
┌──────────────────────────────────────────────────────────────┐
│  📚 REFERÊNCIAS — Impacto da IA na Educação                  │
│──────────────────────────────────────────────────────────────│
│                                                              │
│  [📤 Upload PDF]   [🤖 Extrair resumos com IA]               │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 📄 artigo-fulano-2023.pdf                              │  │
│  │ Autor: Fulano de Tal | Ano: 2023                       │  │
│  │ Status: ✅ Resumo extraído                              │  │
│  │                                                        │  │
│  │ Resumo IA:                                             │  │
│  │ "Este artigo analisa o impacto da IA generativa no     │  │
│  │  ensino superior, demonstrando que ferramentas como    │  │
│  │  ChatGPT aumentaram a produtividade dos alunos..."     │  │
│  │                                                        │  │
│  │ Pontos-chave extraídos:                                │  │
│  │  • IA aumentou produtividade em 25%                    │  │
│  │  • 78% dos alunos aprovam o uso                        │  │
│  │  • Desafios: plágio e dependência                      │  │
│  │                                                        │  │
│  │ Citação ABNT:                                          │  │
│  │ FULANO, T. Impacto da IA no ensino. Rev. Ed., 2023.   │  │
│  │                                                        │  │
│  │ [📝 Editar resumo] [🗑️ Remover] [📋 Copiar citação]    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 📄 artigo-ciclano-2022.pdf                             │  │
│  │ Status: 🔄 Aguardando extração                         │  │
│  │ [🤖 Extrair agora]                                     │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  [← Voltar ao Painel]                                        │
└──────────────────────────────────────────────────────────────┘
```

**Funções:**

- Upload de PDFs
- Extração automática de texto dos PDFs
- IA resume cada artigo e extrai pontos-chave
- Geração automática de citação (ABNT/APA)
- Esses resumos alimentam o `contexto.json`

---

### **Tela 5 — Gerenciador de Dados**

```
┌──────────────────────────────────────────────────────────────┐
│  📊 DADOS — Impacto da IA na Educação                        │
│──────────────────────────────────────────────────────────────│
│                                                              │
│  [📤 Upload CSV]   [🤖 Analisar dados com IA]                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ 📊 dados-questionario.csv                              │  │
│  │ 200 linhas × 15 colunas                                │  │
│  │                                                        │  │
│  │ Preview:                                               │  │
│  │ ┌──────┬────────┬───────┬────────────┬──────────┐     │  │
│  │ │ id   │ idade  │ genero│ nota_antes │nota_depois│     │  │
│  │ ├──────┼────────┼───────┼────────────┼──────────┤     │  │
│  │ │ 1    │ 22     │ M     │ 6.5        │ 8.2      │     │  │
│  │ │ 2    │ 19     │ F     │ 7.0        │ 8.8      │     │  │
│  │ │ 3    │ 25     │ F     │ 5.5        │ 7.1      │     │  │
│  │ └──────┴────────┴───────┴────────────┴──────────┘     │  │
│  │                                                        │  │
│  │ Análise IA:                                            │  │
│  │  • Média nota_antes: 6.3 | nota_depois: 8.0           │  │
│  │  • Aumento médio: 27%                                  │  │
│  │  • Correlação idade×melhora: 0.42                      │  │
│  │  • Sugestões de gráficos: barras comparativas,         │  │
│  │    scatter plot, histograma                             │  │
│  │                                                        │  │
│  │ [📈 Gerar Gráficos]  [📝 Editar análise]  [🗑️ Remover] │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  [← Voltar ao Painel]                                        │
└──────────────────────────────────────────────────────────────┘
```

**Funções:**

- Upload e parse de CSVs
- Preview tabular dos dados
- IA analisa os dados e sugere insights
- IA sugere tipos de gráficos relevantes
- Botão para gerar gráficos automaticamente

---

### **Tela 6 — Gerador de Gráficos/Análises**

```
┌──────────────────────────────────────────────────────────────┐
│  📈 ANÁLISES E GRÁFICOS                                      │
│──────────────────────────────────────────────────────────────│
│                                                              │
│  Dados: [dados-questionario.csv ▼]                           │
│                                                              │
│  Tipo de gráfico:                                            │
│  (•) Barras  ( ) Linha  ( ) Pizza  ( ) Scatter  ( ) Box     │
│                                                              │
│  Eixo X: [nota_antes ▼]    Eixo Y: [nota_depois ▼]          │
│  Agrupar por: [genero ▼]                                     │
│                                                              │
│  Título do gráfico:                                          │
│  [Comparação de notas antes e depois da IA]                  │
│                                                              │
│  [🤖 Sugerir gráfico com IA]  [📈 Gerar Gráfico]            │
│                                                              │
│  ┌────────────────────────────────────────────┐              │
│  │                                            │              │
│  │          [PREVIEW DO GRÁFICO]              │              │
│  │                                            │              │
│  │    █████████ 8.2                           │              │
│  │    ██████    6.5                           │              │
│  │    ──────────────                          │              │
│  │    Antes    Depois                         │              │
│  │                                            │              │
│  └────────────────────────────────────────────┘              │
│                                                              │
│  [💾 Salvar PNG]  [📝 Gerar descrição para o paper]           │
│                                                              │
│  Gráficos salvos:                                            │
│  🖼️ grafico-barras-comparacao.png                            │
│  🖼️ grafico-scatter-correlacao.png                           │
│                                                              │
│  [← Voltar ao Painel]                                        │
└──────────────────────────────────────────────────────────────┘
```

**Funções:**

- Seleção visual de tipo de gráfico
- Mapeamento de colunas do CSV para eixos
- IA sugere melhores gráficos para os dados
- Preview em tempo real
- Salvar como PNG na pasta `/03-analises`
- IA gera descrição textual do gráfico para inserir na seção de Resultados

---

### **Tela 7 — Editor de Seção (Melhorado)**

```
┌─────────────────────────────────────────────────────────────────┐
│  ✍️ Editando: 05 - Revisão da Literatura                        │
│─────────────────────────────────────────────────────────────────│
│                                                                 │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │  🤖 PAINEL IA        │  │  📝 EDITOR                       │ │
│  │                      │  │                                  │ │
│  │  Modelo:             │  │  # Revisão da Literatura         │ │
│  │  (•) MiniMax (Free)  │  │                                  │ │
│  │  ( ) Gemini Flash    │  │  Segundo Fulano (2023), a        │ │
│  │                      │  │  inteligência artificial tem     │ │
│  │  ── Ações ──         │  │  demonstrado resultados          │ │
│  │                      │  │  promissores na educação...      │ │
│  │  [🤖 Gerar do zero]  │  │                                  │ │
│  │  [✨ Melhorar]        │  │  ┌─────────────────────────┐    │ │
│  │  [📏 Expandir]        │  │  │  👁️ PREVIEW FORMATADO   │    │ │
│  │  [✂️ Resumir]         │  │  │                         │    │ │
│  │  [🔬 Academicizar]    │  │  │  Texto renderizado      │    │ │
│  │  [📚 Citar fontes]    │  │  │  com formatação...      │    │ │
│  │                      │  │  └─────────────────────────┘    │ │
│  │  ── Contexto ──      │  │                                  │ │
│  │  [v] Contexto geral  │  │                                  │ │
│  │  [v] Refs extraídas  │  │                                  │ │
│  │  [v] Dados analisados│  │                                  │ │
│  │  [ ] Seção anterior  │  │                                  │ │
│  │  [ ] Todas as seções │  │                                  │ │
│  │                      │  │                                  │ │
│  │  ── Prompt Custom ── │  │                                  │ │
│  │  ┌────────────────┐  │  │                                  │ │
│  │  │ Escreva a rev. │  │  │                                  │ │
│  │  │ da literatura  │  │  │                                  │ │
│  │  │ usando os 5    │  │  │                                  │ │
│  │  │ artigos base   │  │  │                                  │ │
│  │  └────────────────┘  │  │                                  │ │
│  │                      │  │                                  │ │
│  │  [📨 Enviar]         │  │                                  │ │
│  │                      │  │                                  │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
│                                                                 │
│  [← Voltar]  [💾 Salvar]  [📄 Atualizar DOCX]  [✅ Concluir]    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Ações novas da IA:**

- **Academicizar:** transforma texto informal em linguagem acadêmica
- **Citar fontes:** insere citações dos artigos base automaticamente
- **Contexto inteligente:** checkbox para incluir resumos das referências, análises dos dados, gráficos disponíveis

---

### **Tela 8 — Gerador de Documento DOCX**

```
┌──────────────────────────────────────────────────────────────┐
│  📄 GERAR DOCUMENTO — Impacto da IA na Educação              │
│──────────────────────────────────────────────────────────────│
│                                                              │
│  Template: [ABNT ▼]                                          │
│                                                              │
│  Seções a incluir:                                           │
│  [v] Título                                                  │
│  [v] Resumo                                                  │
│  [v] Palavras-chave                                          │
│  [v] Introdução                                              │
│  [v] Revisão da Literatura                                   │
│  [v] Metodologia                                             │
│  [v] Resultados (incluir gráficos: ✅)                       │
│  [v] Discussão                                               │
│  [v] Conclusão                                               │
│  [v] Referências                                             │
│  [ ] Apêndices                                               │
│  [v] Agradecimentos                                          │
│                                                              │
│  Gráficos a inserir nos Resultados:                          │
│  [v] grafico-barras-comparacao.png                           │
│  [v] grafico-scatter-correlacao.png                          │
│  [ ] grafico-pizza-demo.png                                  │
│                                                              │
│  Versão: [v3 ▼]                                              │
│                                                              │
│  [📄 Gerar DOCX]  [📥 Gerar PDF]                             │
│                                                              │
│  Versões anteriores:                                         │
│  📄 paper-v1.docx (15/01/2024)                               │
│  📄 paper-v2.docx (18/01/2024)                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. Fluxo Completo do Usuário

```
[Abre App]
    │
    ▼
[Dashboard] ─────────────────────────────────────┐
    │                                             │
    ├── Novo Paper (Wizard 4 etapas)              │
    │       │                                     │
    │       ├─ 1. Info básica                     │
    │       ├─ 2. Contexto (problema, objetivos)  │
    │       ├─ 3. Upload PDFs referências          │
    │       └─ 4. Upload CSVs dados               │
    │               │                             │
    │               ▼                             │
    │         [Cria pasta completa]               │
    │               │                             │
    ▼               ▼                             │
[Painel do Paper] ◄──────────────────────────────┘
    │
    ├──→ [Gerenciar Referências]
    │         ├── Upload PDFs
    │         ├── IA extrai resumos
    │         └── Gera citações
    │
    ├──→ [Gerenciar Dados]
    │         ├── Upload CSVs
    │         ├── IA analisa dados
    │         └── Sugere gráficos
    │
    ├──→ [Gerar Gráficos]
    │         ├── Seleciona tipo
    │         ├── Configura eixos
    │         ├── Preview
    │         └── Salva PNG
    │
    ├──→ [Editar Seção] (×12 seções)
    │         ├── Escreve manualmente
    │         ├── Gera com IA (contexto completo)
    │         ├── Melhora / Expande / Resume
    │         └── Salva .md
    │
    ├──→ [Notas e Rascunhos]
    │
    └──→ [Gerar DOCX/PDF]
              ├── Seleciona seções
              ├── Inclui gráficos
              ├── Aplica template
              └── Salva versão
```

---

## 7. Rotas da API Local (Atualizadas)

```
# Papers
GET     /api/papers                         → Lista papers
POST    /api/papers                         → Cria paper
GET     /api/papers/:id                     → Detalhes
DELETE  /api/papers/:id                     → Exclui
PUT     /api/papers/:id/contexto            → Atualiza contexto.json

# Seções
GET     /api/papers/:id/secoes              → Lista seções
GET     /api/papers/:id/secoes/:secao       → Lê .md
PUT     /api/papers/:id/secoes/:secao       → Salva .md
PATCH   /api/papers/:id/secoes/:secao       → Atualiza status

# Referências
GET     /api/papers/:id/referencias         → Lista PDFs
POST    /api/papers/:id/referencias         → Upload PDF
DELETE  /api/papers/:id/referencias/:file   → Remove PDF
POST    /api/papers/:id/referencias/extrair → IA extrai resumos

# Dados
GET     /api/papers/:id/dados               → Lista CSVs
POST    /api/papers/:id/dados               → Upload CSV
DELETE  /api/papers/:id/dados/:file         → Remove CSV
POST    /api/papers/:id/dados/analisar      → IA analisa dados
GET     /api/papers/:id/dados/:file/preview → Preview do CSV

# Análises/Gráficos
GET     /api/papers/:id/analises            → Lista gráficos
POST    /api/papers/:id/analises/gerar      → Gera gráfico
DELETE  /api/papers/:id/analises/:file      → Remove gráfico

# IA
POST    /api/ia/gerar                       → Gera texto
POST    /api/ia/melhorar                    → Melhora texto
POST    /api/ia/expandir                    → Expande
POST    /api/ia/resumir                     → Resume
POST    /api/ia/academicizar               → Torna acadêmico
POST    /api/ia/sugerir-graficos           → Sugere gráficos

# Documento
POST    /api/papers/:id/documento/gerar     → Gera DOCX
GET     /api/papers/:id/documento/versoes   → Lista versões

# Config
GET     /api/config                         → Lê config
PUT     /api/config                         → Salva config

# Notas
GET     /api/papers/:id/notas               → Lista notas
POST    /api/papers/:id/notas               → Cria nota
PUT     /api/papers/:id/notas/:file         → Edita nota
```

---

## 8. Fases de Desenvolvimento (Atualizadas)

| Fase         | Descrição                                    | Prioridade |
| ------------ | ---------------------------------------------- | ---------- |
| **1**  | Setup projeto + Backend (CRUD papers + pastas) | 🔴 Alta    |
| **2**  | Dashboard + Criar Paper (Wizard)               | 🔴 Alta    |
| **3**  | Painel do Paper + Cards de seções            | 🔴 Alta    |
| **4**  | Editor de seção (manual, sem IA)             | 🔴 Alta    |
| **5**  | Integração MiniMax (OpenCode) — gerar texto | 🔴 Alta    |
| **6**  | Integração Gemini Flash (Antigravity)        | 🟡 Média  |
| **7**  | Upload + gerenciamento de PDFs (referências)  | 🟡 Média  |
| **8**  | Extração de texto de PDFs + resumos IA       | 🟡 Média  |
| **9**  | Upload + parse de CSVs                         | 🟡 Média  |
| **10** | Análise de dados com IA                       | 🟡 Média  |
| **11** | Geração de gráficos (Chart.js)              | 🟡 Média  |
| **12** | Gerador de DOCX com template                   | 🟢 Baixa   |
| **13** | Sistema de notas                               | 🟢 Baixa   |
| **14** | Histórico de prompts                          | 🟢 Baixa   |
| **15** | Exportar PDF                                   | 🟢 Baixa   |
| **16** | Firebase (futuro)                              | ⚪ Futuro  |

---

Quer que eu comece a desenvolver a **Fase 1** (setup do projeto + backend básico)?
