entend

# Relatório Metodológico e Status Geral de Execução (29.06.2026)

**Última atualização:** 29 de Junho de 2026
**Autor:** Renato de Oliveira Rosa — Fucape Business School — Doutorado em Contabilidade

---

## PARTE I: A TESE CENTRAL

### 1.1 Status Geral

**Arquivo:** `Tese/tese.html` (174 KB, 2.177 linhas)
**Título:** Copiloto Algorítmico para Compras Públicas Complexas: Um Artefato de Apoio à Decisão para Redução de Assimetrias na Contratação de Inovação e Sustentabilidade

---

### 1.2 O QUE FUNCIONA BEM

| Aspecto                                             | Status          | Observação                                                                                               |
| --------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------- |
| Estrutura formal ABNT                               | ✅ Excelente    | Capa, folha de rosto, aprovação, epígrafe, sumário, listas, referências, apêndices — todos corretos |
| Resumo/Abstract bilíngue                           | ✅ Sólido      | 19.640 contratos mencionados (verificar inconsistência)                                                   |
| Introdução (Cap 1)                                | ✅ Excelente    | Escrita formal, sem vícios de IA, problema de pesquisa claro                                              |
| Fundamentação teórica (Cap 2, seções 2.1–2.4) | ✅ Sólida      | Williamson, Mazzucato, XAI, DSR bem articulados                                                            |
| Metodologia (Cap 3)                                 | ✅ Correta      | DSR de Peffers, FEDS, Delphi — tabelas 4 e 5 coerentes                                                    |
| Considerações Finais (Cap 5)                      | ✅ Boas         | Implicações práticas, policy recommendations, agenda futura                                             |
| Referências                                        | ✅ Limpas       | 24 referências, foco e relevância                                                                        |
| Apêndices A, B, C                                  | ✅ Completos    | Roteiro Delphi, TCLE, Formulário de avaliação                                                           |
| Formatação CSS                                    | ✅ Profissional | page-break, footnotes, estilo ABNT/APA                                                                     |

---

### 1.3 PROBLEMAS CRÍTICOS DA TESE

#### 🔴 PROBLEMA 1: Inconsistência Numérica Grave

| Local                                  | Número Declarado                            |
| -------------------------------------- | -------------------------------------------- |
| Resumo (linha 199)                     | 19.640 licitações                          |
| Abstract (linha 203)                   | 19,640 primary procurement records           |
| Metodologia, Tabela 6 (linha 1795)     | 19.640 contratações                        |
| Capítulo 4, parágrafo 1 (linha 1882) | **819.175** processos, R$ 584 bilhões |

**Ação obrigatória:** Determinar o número real (19.640 é a amostra filtrada? 819.175 é o total populacional?) e padronizar em TODA a tese — resumo, abstract, metodologia e resultados.

---

#### 🔴 PROBLEMA 2: Tabelas Literárias 4, 5 e 6 (Seções 2.5, 2.6, 2.7) São Inviáveis

As três seções de "mapeamento literário" foram geradas por extração CrossRef sem filtro temático adequado. **Uma banca examinadora vai identificar isso em segundos.**

**Tabela 4 (2.5 — Posicionamento Macro) — Artigos Irrelevantes:**

| Artigo Listado                                                                   | Área Real             |
| -------------------------------------------------------------------------------- | ---------------------- |
| Folstein et al. — "Mini-mental state"                                           | Psiquiatria médica    |
| Metropolis et al. — "Equation of State Calculations by Fast Computing Machines" | Física/química       |
| Dixon et al. — "Ferroptosis: An Iron-Dependent Form of Nonapoptotic Cell Death" | Biologia celular       |
| YOLOv7: Trainable Bag-of-Freebies                                                | Visão computacional   |
| IQ-TREE 2: New Models for Phylogenetic Inference                                 | Bioinformática        |
| Vos et al. — "Global burden of 369 diseases..."                                 | Saúde pública global |
| Wang et al. — "YOLOv7..."                                                       | Visão computacional   |
| Abbott et al. — "Observation of Gravitational Waves..."                         | Astrofísica           |
| Wu et al. — "clusterProfiler 4.0"                                               | Bioinformática        |

**Tabela 5 (2.6 — Posicionamento Meso) — Artigos Irrelevantes:**

| Artigo Listado                                                     | Área Real                |
| ------------------------------------------------------------------ | ------------------------- |
| O'Regan et al. — "A low-cost, high-efficiency solar cell..."      | Energia solar             |
| Solow — "A Contribution to the Theory of Economic Growth"         | Macroeconomia (deslocado) |
| Baker et al. — "Measuring Economic Policy Uncertainty"            | Macroeconomia             |
| Hart et al. — "A Formal Basis for the Heuristic Determination..." | Ciência da computação  |
| Fischbacher — "z-Tree: Zurich toolbox..."                         | Economia experimental     |

**Tabela 6 (2.7 — Posicionamento Micro) — Artigos Irrelevantes:**

| Artigo Listado                                                | Área Real                                                       |
| ------------------------------------------------------------- | ---------------------------------------------------------------- |
| Ren et al. — "Faster R-CNN"                                  | Visão computacional                                             |
| Chawla et al. — "SMOTE"                                      | Machine learning (mas focado em dados desbalanceados genéricos) |
| Canny — "A Computational Approach to Edge Detection"         | Processamento de imagens                                         |
| Chen et al. — "DeepLab: Semantic Image Segmentation"         | Visão computacional                                             |
| Mallat — "A theory for multiresolution signal decomposition" | Processamento de sinais                                          |
| Badrinarayanan et al. — "SegNet"                             | Visão computacional                                             |
| Vos et al. — "Global burden of 369 diseases..."              | Saúde pública                                                  |
| Dijkstra — citation but not visible                          | cited as source                                                  |
| Turing — "Computing Machinery and Intelligence"              | IA (legítimo mas deslocado do tema compras/XAI)                 |

**Ação obrigatória:** OPÇÃO A — Remover as Tabelas 4, 5 e 6 inteiramente e substituir por narrativa discursiva da revisão de literatura. OPÇÃO B — Refazer a extração CrossRef com filtros temáticos rigorosos (apenas artigos de: governança pública, compras governamentais, transparência algorítmica, XAI no setor público, custos de transação em procurement).

---

#### 🟡 PROBLEMA 3: Capítulo 4 (Resultados) É Extemporaneamente Enxuto

O Capítulo 4 apresenta parágrafo único (metade de uma página) paraos resultados de 819 mil processos. Não há:

- Tabelas estatísticas com resultados de Random Forest ou Isolation Forest
- Matriz de confusão
- Output de modelos
- Testes de hipótese formais
- Figuras com distribuições

**Ação obrigatória:** Expandir o Capítulo 4 com seções numeradas (4.1, 4.2, etc.) contendo:

- Tabela de estatística descritiva da base PNCP
- Outputs do Isolation Forest (anomalias)
- Outputs do Random Forest (fracasso)
- Métricas de desempenho do Copiloto (88,74%)
- Resultados do Delphi (Kappa 0,86)

---

#### 🟡 PROBLEMA 4: Numeração de Tabelas Confusa

A tese usa numeração dupla — Tabelas 1-3 no referencial (seções 2.3-2.4), depois salta para Tabela 4 (ciclo DSR na seção 3.4), Tabela 5 (módulos em 3.2), Tabela 6 (fontes em 3.3), Tabela 7 (Delphi em 3.4).

Na Lista de Tabelas (pré-textual), a numeração é diferente.

**Ação recomendada:** Padronizar numeração única e sequencial para todo o documento, OU manter numeração por capítulo (ex: Tabela 3.1, 3.2 para capítulo 3).

---

#### 🟡 PROBLEMA 5: "Metodologia Mista" Mencionada mas Não Detalhada

O texto fala em "investigação de natureza mista" mas não apresenta matriz de métodos mistos (quantitativo + qualitativo integrados).

**Ação recomendada:** Adicionar uma subseção em 3.1 especificando como os métodos quanti (ML, NLP, Survival Analysis) e quali (ACD Fairclough, Bardin, Delphi) se articulam.

---

### 1.4 CHECKLIST DE CORREÇÕES DA TESE

| # | Ação                                                                                    | Prioridade |
| - | ----------------------------------------------------------------------------------------- | ---------- |
| 1 | Padronizar número de contratos (19.640 vs 819.175) em todo o documento                   | 🔴 Alta    |
| 2 | Remover ou refazer Tabelas 4, 5 e 6 (seções 2.5-2.7)                                    | 🔴 Alta    |
| 3 | Expandir Capítulo 4 com tabelas de resultados reais                                      | 🔴 Alta    |
| 4 | Padronizar numeração de tabelas                                                         | 🟡 Média  |
| 5 | Detalhar matriz de métodos mistos em 3.1                                                 | 🟡 Média  |
| 6 | Verificar consistência de "quase-experimento" citado no abstract vs metodologia descrita | 🟡 Média  |
| 7 | Leitura final de "verniz" pelo autor                                                      | 🟢 Baixa   |

---

## PARTE II: OS 25 ARTIGOS

### 2.1 Visão Geral do Status

| Categoria                                     | Artigos                                | Problema Principal                             |
| --------------------------------------------- | -------------------------------------- | ---------------------------------------------- |
| **Excelente (prontos)**                 | 01, 02, 03, 04, 05                     | Precisam de injeção de dados reais do PNCP   |
| **Estrutura OK, precisa dados reais**   | 06, 07, 08, 09, 10, 11, 12, 13, 14, 15 | Precisam de dados empíricos + limpeza textual |
| **Problemastextuais graves**            | 16, 25                                 | Texto gerado por IA em EN/PT misto             |
| **Muito curtos/incompletos**            | 17, 18                                 | Conteúdo insuficiente                         |
| **Placeholders / Artigo 3.1 duplicado** | 22, 23, 24                             | Seção 3.1 copiada de qualitative study       |
| **Fora do workflow HTML**               | 18                                     | Só existe como DOCX                           |

---

### 2.2 Análise Detalhada por Artigo

---

#### ARTIGO 01 — Opacidade Institucional: Análise de Complexidade Textual em Editais de Inovação

**Arquivo:** `Artigos/01-Opacidade-Institucional-Analise-Complexidade-Textual-Editais-Inovacao/artigo_01.html`
**Tamanho:** 274 linhas
**Metodologia:** NLP + Regressão Linear Múltipla (Flesch-Kincaid)

**✅ O que funciona:**

- Abstract bem estruturado com R² = 0,862
- Introdução e fundamentação teóricastandalone
- Metodologia clara (spaCy, NLTK, Martins 2020)
- Regressão com controles (valor, complexidade)
- Pressupostos testados (Shapiro-Wilk, Breusch-Pagan)

**❌ Problemas identificados:**

1. **Dado simulado visível na Tabela 1 (linha 97):** "Licitantes (Simulação)" — o número de licitantes ainda é marcado como simulação, não dado real extraído do PNCP
2. **Inconsistência de n:** Abstract fala em 40 editais; Metodologia fala em 126 editais; Tabela 1 lista n=126; texto diz "40 editais extraídos do PNCP e Compras.gov.br (2023-2024)"
3. **n inconsistente entre seções:**

   - Abstract: 40 editais
   - Seção 3.1: 40 editais
   - Tabela 1: n = 126
   - Figura 1: n = 126
   - Figura 1 legend: n = 126

**Ações necessárias:**

- [ ] Injetar dados reais de número de licitantes do PNCP
- [ ] Padronizar n (40 ou 126?) — decidir se é 40 editais com múltiplas observações ou 126 processos
- [ ] Remover marcador "(Simulação)" da tabela
- [ ] Rodar NLP real nos editais do PNCP

---

#### ARTIGO 02 — Auditoria Contínua e Detecção de Anomalias de Preços

**Arquivo:** `Artigos/02-Auditoria-Continua-Deteccao-Anomalias-Precos/artigo_02.html`
**Tamanho:** ~250 linhas (estimado)
**Metodologia:** Isolation Forest (não-supervisionado)

**✅ O que funciona:**

- Estrutura standalone completa
- Sem vícios de IA aparentes
- Metodologia de Isolation Forest corretamente descrita

**❌ Problemas identificados:**

1. **Abstract menciona 10.5K registros** — verificar se esse número bate com a tese (819.175)
2. **Seção de resultados** — não foi possível verificar se tem dados reais injetados ou placeholders

**Ações necessárias:**

- [ ] Injetar as 199 anomalias reais detectadas na base PNCP de 819K contratos
- [ ] Gerar gráficos de outliers reais (SVG)
- [ ] Atualizar Tabela de resultados com números reais
- [ ] Verificar consistência de n (10.5K vs 819K da tese)

---

#### ARTIGO 03 — Predição de Fracasso e Risco de Aditivos e Cancelamentos

**Arquivo:** `Artigos/03-Predicao-Fracasso-Risco-Aditivos-Cancelamentos/artigo_03.html`
**Tamanho:** ~300 linhas (estimado)
**Metodologia:** Random Forest supervisionado

**✅ O que funciona:**

- Estrutura standalone
- Sem vícios de IA aparentes
- Random Forest como metodologia apropriada

**❌ Problemas identificados:**

1. **Acurácia de 78,24%** mencionada — verificar se é resultado real ou simulado
2. **n de 12.5K contratos** — não está claro se é base real ou simulada

**Ações necessárias:**

- [ ] Treinar Random Forest nos 819K dados reais do PNCP
- [ ] Gerar matriz de confusão real
- [ ] Injetar outputs de feature importance
- [ ] Atualizar seções de resultados com métricas reais

---

#### ARTIGO 04 — O Apagão das Canetas Quantificado: Latência Decisória

**Arquivo:** `Artigos/04-Apagao-Canetas-Quantificado-Latencia-Decisoria/artigo_04.html`
**Tamanho:** ~300 linhas
**Metodologia:** OLS com Lags Autorressivos (Painel)

**✅ O que funciona:**

- Estrutura standalone completa
- R² = 90,64% citado
- Fundamentação em Williamson sólida
- Metodologia de painel (150 órgãos, 60 meses)

**❌ Problemas identificados:**

1. **n = 9.000 observações mensais** — não está claro se é dado real ou simulado
2. **"+8,80 dias de latência"** — verificar se é resultado real ou placeholder
3. **Não há tabela de resultados visível no artigo lido**

**Ações necessárias:**

- [ ] Calcular latência real em dias úteis entre abertura/fechamento dos contratos no PNCP
- [ ] Injetar coeficientes reais da regressão OLS
- [ ] Gerar Gráfico 2 (latência por órgão com efeito marginal das sanções TCU)
- [ ] Verificar se o valor de R² = 90,64% é real ou simulado

---

#### ARTIGO 05 — Redes de Fornecimento e Oligopólios: Análise de Grafos

**Arquivo:** `Artigos/05-Redes-Fornecimento-Oligopolios-Analise-Grafos/artigo_05.html`
**Tamanho:** 252 linhas
**Metodologia:** Teoria dos Grafos (NetworkX)

**✅ O que funciona:**

- Abstract com métricas impressionantes: Gini=0,9072, 87,21% market share top 3
- Rede bipartida (100 órgãos + 300 fornecedores, 1.111 arestas)
- Centralidades calculadas (grau, intermediação, proximidade)
- Figuras: curva de Lorenz e market share

**❌ Problemas identificados:**

1. **Empresa "TechGlobal Servicos Ltda", "Sistemas e Dados Gov", "Integradora Brasil"** — appear as if they are real Brazilian companies but are these verified real suppliers from PNCP or fictional composites?
2. **Tabela 2 mostra métricas específicas** (C_B = 0,2726 para líder) — não está claro se são reais ou simuladas
3. **Tensão:** Abstract diz "400 nós (100 compradores e 300 fornecedores)" mas a seção 2.1 refere-se à "Teoria da Dependência de Recursos (Pfeffer; Salancik, 1978)" como fundamentação — apropriado para o artigo mas não integrado à tese

**Ações necessárias:**

- [ ] Extrair CNPJs reais dos fornecedores winners do PNCP
- [ ] Desenhar grafo real com NetworkX
- [ ] Verificar se "TechGlobal", "Sistemas e Dados Gov", "Integradora Brasil" são nomes reais ou composições
- [ ] Recalcular Gini real se dados forem reais

---

#### ARTIGO 06 — Sobrevivência de Contratos de Inovação: Análise de Kaplan-Meier

**Arquivo:** `Artigos/06-Sobrevivencia-Contratos-Inovacao-Analise-Kaplan-Meier/artigo_06.html`
**Tamanho:** ~150-200 linhas (curto)
**Metodologia:** Kaplan-Meier + Cox Proportional Hazards

**✅ O que funciona:**

- Estrutura básica de artigo acadêmico
- Kaplan-Meier e Cox como metodologia apropriada

**❌ Problemas críticos:**

1. **🔴 TEXTO MISTURADO PT/EN:** O artigo contém segmentos em inglês que parecem geração de IA não revisada:

   - Referências a "BCB SGS API", "IPCA (433), CDI (4391)" aparecem soltas
   - Metodologia menciona "artigo06_macroeconomico_bcb.csv" — arquivo de dados externo
2. **Seção 3.1 "Confiabilidade e Rigor Metodológico"** — texto parece copiado de estudo qualitativo ("dupla revisão cega", "Kappa de Cohen") mas este é estudo quantitativo de sobrevivência — não se aplica
3. **Abstract menciona C-Index = 78,54%** — não verificável se real
4. **"artigo06_ipca.csv" e "artigo06_macroeconomico_bcb.csv"** — esses CSVs existem no repositório, sugerindo que há dados reais, mas o HTML não os referencia adequadamente

**Ações necessárias:**

- [ ] Reescrever todo o texto em português formal, removendo mistura EN/PT
- [ ] Remover ou corrigir seção 3.1 de "confiabilidade" (estudo quantitativo não tem codificação dupla cega)
- [ ] Integrar os CSVs de dados macroeconômicos (IPCA, CDI) explicitamente no artigo
- [ ] Verificar se C-Index = 78,54% é resultado real do modelo Cox

---

#### ARTIGO 07 — Governança Algorítmica: Benchmarking de Eficiência

**Arquivo:** `Artigos/07-Governanca-Algoritmica-Benchmarking-Eficiencia/artigo_07.html`
**Tamanho:** ~250 linhas
**Metodologia:** DEA (Data Envelopment Analysis) + Benchmarking Siconfi

**✅ O que funciona:**

- DEA é metodologia apropriada para benchmarking de eficiência governamental
- 180 municípios estratificados por porte

**❌ Problemas identificados:**

1. **Redução de 88,74% no tempo** (de 45,66h para 5,14h) — mesmo número do abstract da tese. Verificar se é dado real ou compartilhado entre artigo e tese
2. **"R$ 334.785.849,51 anuais"** — economia projetada nacional — verificar se é real ou placeholder
3. **Tabela de efficiency scores** — não verificável se dados reais injetados

**Ações necessárias:**

- [ ] Extrair insumos/produtos reais dos órgãos via PNCP para DEA
- [ ] Verificar se o valor de 88,74% está correto e pode ser usado tanto na tese quanto no artigo
- [ ] Gerar frontier de eficiência real
- [ ] Confirmar economia projetada de R$ 334 mi

---

#### ARTIGO 08 — XAI no Setor Público: Prova de Conceito nos Tribunais de Contas

**Arquivo:** `Artigos/08-XAI-Setor-Publico-Prova-Conceito-Tribunais-Contas/artigo_08.html`
**Tamanho:** ~300 linhas
**Metodologia:** DSR + Random Forest + SHAP

**✅ O que funciona:**

- SHAP como método de explicabilidade apropriado
- Random Forest como classificador
- Prova de conceito com 8.500 processos

**❌ Problemas identificados:**

1. **Acurácia 94,88%, Precisão 86,61%, F1 71,66%** — verificar se são resultados reais ou placeholders
2. **"Histórico de sanções do vencedor" como feature dominante** (7,79% impacto) — verificar se é achado real ou inferência
3. **Necesidade de desvincular da tese** — artigo precisa ser standalone, mas menciona "copiloto algorítmico" que é o artefato central da tese

**Ações necessárias:**

- [ ] Treinar modelo RF real com dados de 8.500 processos (ou 819K se usar PNCP)
- [ ] Computar SHAP values reais (global e local)
- [ ] Desvincular do "copiloto" da tese — renomear como "sistema de apoio à auditoria"
- [ ] Gerar SHAP summary plot real

---

#### ARTIGO 09 — Jurisprudência do Medo: Análise de Discurso em Acórdãos do TCU

**Arquivo:** `Artigos/09-Jurisprudencia-Medo-Analise-Discurso-Acordaos/artigo_09.html`
**Tamanho:** ~250-300 linhas
**Metodologia:** ACD Tridimensional de Fairclough

**✅ O que funciona:**

- ACD Fairclough como metodologia apropriada para análise crítica
- 5 acórdãos do TCU
- Conexão com "apagão das canetas" e LINDB

**❌ Problemas identificados:**

1. **5 acórdãos** — número muito pequeno para generalização acadêmica
2. **"Dados simulados"** conforme imp29.06 — os 5 acórdãos são exemplos estruturados, não extração real da API do TCU (que está bloqueada)
3. **Seção de resultados** — não verificável se apresenta análise real dos 5 casos ou placeholders

**Ações necessárias:**

- [ ] Tentar extrair acórdãos reais via dadosabertos.tcu.gov.br (script `upgrade_tcu.py` existe)
- [ ] Se não conseguir dados reais, justificar academicamente a limitação e manter apenas os 5 como "casos ilustrativos"
- [ ] Expandir análise de cada acórdão com mais texto discursivo
- [ ] Gerar tabelas analíticas reais

---

#### ARTIGO 10 — Uso Retórico da Inovação: Análise de Conteúdo de Justificativas

**Arquivo:** `Artigos/10-Uso-Retorico-Inovacao-Analise-Conteudo-Justificativas/artigo_10.html`
**Tamanho:** ~300 linhas
**Metodologia:** Bardin (Análise de Conteúdo) + Qui-Quadrado

**✅ O que funciona:**

- Bardin como metodologia apropriada
- 4 categorias temáticas
- Qui-Quadrado como teste estatístico
- Abstract menciona χ² = 91,2540, p = 1,264 × 10⁻²¹

**❌ Problemas identificados:**

1. **350 justificativas PNCP** — confirmar se são reais ou simuladas
2. **Categorias percentuais** (Mimetismo 33,43%, Inovação Legítima 31,43%, etc.) — verificar se são resultados reais
3. **Rhetorical Score** (0,7574 vs 0,4308) — indicador composto criado para o artigo — não verificável
4. **Linha 174 do imp29.06 diz:** "Rodar extração nas justificativas reais que vieram no JSON do PNCP" — ainda não feito

**Ações necessárias:**

- [ ] Extrair justificativas reais dos JSONs do PNCP baixados
- [ ] Codificar com Bardin realmente nas 4 categorias
- [ ] Calcular Qui-Quadrado real
- [ ] Computar Rhetorical Score real
- [ ] Atualizar tabela de resultados com categorias e percentuais reais

---

#### ARTIGO 11 — A Voz do Mercado: Análise de Impugnações de Editais de Tecnologia

**Arquivo:** `Artigos/11-Voz-Mercado-Analise-Impugnacoes-Editais-Tecnologia/artigo_11.html`
**Tamanho:** ~250-300 linhas
**Metodologia:** Bardin + Qui-quadrado

**✅ O que funciona:**

- Metodologia apropriada (Bardin + χ²)
- 4 categorias de impugnações

**❌ Problemas identificados:**

1. **150 impugnações Compras.gov.br** — confirmar se são reais ou simuladas
2. **"taxa de acolhimento de 62,50% em objetos complexos vs. 21,43% em comuns"** — verificar se são números reais
3. **Segundo imp29.06:** "Higienização de texto, injetar amostragem de recursos administrativos reais" — ainda pendente

**Ações necessárias:**

- [ ] Raspar impugnações reais do Compras.gov.br (scraper existe?)
- [ ] Codificar Bardin real nas 4 categorias
- [ ] Calcular χ² real
- [ ] Atualizar resultados com números reais

---

#### ARTIGO 12 — Evolução do Risco na Legislação: Da Lei 8.666 ao Marco das Startups

**Arquivo:** `Artigos/12-Evolucao-Risco-Legislacao-Compras-8.666-Marco-Startups/artigo_12.html`
**Tamanho:** ~300 linhas
**Metodologia:** Análise Lexicográfica Diacrônica

**✅ O que funciona:**

- Artigo predominantemente teórico/histórico
- 5 marcos legais analisados
- χ² = 216,14 mencionado

**❌ Problemas identificados:**

1. **Linguagem temporal** — imp29.06 menciona "remover 'hoje em dia'" — verificar se ainda existe
2. **"χ² = 216,14"** — para análise lexicográfica, esse valor parece de teste estatístico paramétrico, não de análise lexicográfica — possivelmente erro metodológico
3. **Artigo é mais revisão narrativa que análise empírica** — pode ser frágil para periódicos A

**Ações necessárias:**

- [ ] Verificar se χ² é metodologicamente correto para análise lexicográfica (ou é para outra análise?)
- [ ] Remover expressões temporais ("hoje em dia", "atualmente")
- [ ] Fortalecer base empírica com dados lexicais reais

---

#### ARTIGO 13 — A Dor das GovTechs: Netnografia do Ecossistema de Inovação Pública

**Arquivo:** `Artigos/13-Dor-GovTechs-Netnografia-Ecosistema-Inovacao-Publica/artigo_13.html`
**Tamanho:** ~300 linhas
**Metodologia:** Netnografia (Kozinets) + ILRF/IRTI

**✅ O que funciona:**

- Netnografia como metodologia apropriada para estudo qualitativo online
- ILRF e IRTI como índices de referência

**❌ Problemas identificados:**

1. **60 relatos LinkedIn/Medium** — confirmar se são reais ou simulados
2. **"dupla revisão cega"** na seção de confiabilidade — netnografia é qualitativa, mas esse texto parece padrão copiado de artigos quantitativos
3. **Artigo depends heavily on "relatos" from social media** — sem acesso real aos dados, é difícil verificar

**Ações necessárias:**

- [ ] Coletar relatos reais de LinkedIn/Medium (web scraping)
- [ ] Aplicar protocolo netnográfico completo de Kozinets
- [ ] Codificar com ILRF/IRTI
- [ ] Remover texto padrão de "dupla revisão cega" se não aplicável

---

#### ARTIGO 14 — O Discurso do Custo Brasil: Análise de Conteúdo de Discursos

**Arquivo:** `Artigos/14-Discurso-Custo-Brasil-Analise-Conteudo-Discursos/artigo_14.html` E `artigo_14_discurso_politica_industrial.html`
**Tamanho:** dois arquivos no mesmo diretório
**Metodologia:** Bardin + ACD

**✅ O que funciona:**

- Duas versões do artigo no mesmo diretório — indica trabalho em progresso

**❌ Problemas identificados:**

1. **🔴 DOIS ARQUIVOS HTML no mesmo diretório** — qual é a versão final? Isso causa confusão
2. **"artigo_14_discurso_politica_industrial.html"** — parece ser variante sobre "Políticas de Indústria 4.0" vs "Custo Brasil" — decidir qual é o artigo correto
3. **120 trechos MDIC/ABDI** mencionados no contexto.md — verificar se são reais

**Ações necessárias:**

- [ ] Decidir qual dos dois é o artigo final
- [ ] Eliminar o arquivo variante
- [ ] Verificar se dados de 120 trechos são reais
- [ ] Integrar Bardin ou ACD propriamente

---

#### ARTIGO 15 — O Enquadramento da IA no Controle Público pela Mídia

**Arquivo:** `Artigos/15-Enquadramento-IA-Controle-Publico-Midia/artigo_15.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Framing Analysis (Entman) + χ²

**✅ O que funciona:**

- Framing como metodologia apropriada para análise midiática
- 388 matérias de Conjur/Valor/Jota
- χ² = 108,45, p < 0,001
- Polarização Conjur vs Valor identificável

**❌ Problemas identificados:**

1. **388 matérias** — confirmar se são reais ou simuladas
2. **"Conjur: 40,8% compliance, 38,0% opacidade"** — números específicos — verificar procedência
3. **"Valor: 66,1%"** — frame de eficiência econômica — verificar
4. **imp29.06 diz:** "Substituir os 'resultados simulados' por raspagem real de notícias" — ainda pendente

**Ações necessárias:**

- [ ] Raspar notícias reais de Conjur, Valor e Jota (2021-2026)
- [ ] Codificar frames de fato (Entman)
- [ ] Calcular χ² real
- [ ] Atualizar distribuições percentuais com números reais

---

#### ARTIGO 16 — A Caixa-Preta do Setor Público: Revisão Sistemática XAI

**Arquivo:** `Artigos/16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica/artigo_16.html`
**Tamanho:** 245 linhas
**Metodologia:** PRISMA + CrossRef

**✅ O que funciona:**

- PRISMA como metodologia de revisão sistemática
- 278 artigos CrossRef

**❌ Problemas CRÍTICOS:**

1. **🔴 TEXTO COMPLETAMENTE GERADO POR IA SEM REVISÃO:**

   ```
   "This study employs a quantitative approach combining Natural Language Processing
   and multiple linear regression. The research employs a quantitative approach..."

   "employs" (inglês) aparece repetidamente

   "retrieved from Crossref" (inglês)

   "The search strategy included terms such as: 'explainable AI government',
   'XAI public sector'..." (texto em inglês sem tradução)
   ```

2. **Artigo mix de EN/PT** — abstract em PT mas corpo em EN mal traduzido
3. **"278 Crossref articles"** mas Tabela 1 mostra artigos genéricos de computação, não XAI em gestão pública
4. **Metodologia PRISMA parece aplicada corretamente** mas os resultados são claramente fictícios

**Ações necessárias:**

- [ ] Reescrever TODO o artigo em português formal
- [ ] Refazer busca empírica no CrossRef com termos rigorosos de XAI + government/public sector
- [ ] Filtrar resultados para remover falsos positivos (artigos de cybersecurity, healthcare)
- [ ] Gerar tabela PRISMA real com números de inclusão/exclusão
- [ ] Construir network visualization real das citações
- [ ] Escrever discussão com base nos achados reais

---

#### ARTIGO 17 — DSR na Contabilidade Pública: Mapeamento Sistemático de Artefatos

**Arquivo:** `Artigos/17-DSR-Contabilidade-Publica-Mapeamento-Artefatos/artigo_17.html`
**Tamanho:** ~150-200 linhas (muito curto)
**Metodologia:** Scoping Review + OpenAlex/CrossRef

**✅ O que funciona:**

- Scoping Review como metodologia apropriada
- Artigo referenciado na tese como base para DSR

**❌ Problemas CRÍTICOS:**

1. **🔴 MUITO CURTO** — 150-200 linhas é insuficiente para um artigo acadêmico completo
2. **42 artigos mencionados** — confirmar se são reais ouPLACEHOLDER
3. **"matriz Gregor & Hevner"** —referência correta mas sem aplicação visible no artigo
4. **Abstract diz:** "42 artigos, 4.456 citações" — número muito específico mas não verificável

**Ações necessárias:**

- [ ] Expandir artigo para pelo menos 400-500 linhas
- [ ] Refazer extração real de 42+ artigos via OpenAlex/CrossRef
- [ ] Aplicar matriz Gregor & Hevner visiblemente aos artigos encontrados
- [ ] Gerar tabela de caracterização dos 42 artigos
- [ ] Construir network visualization de coautorias

---

#### ARTIGO 18 — Compliance Algorítmico Integrado

**Arquivo:** `Artigos/18-Compliance-Algoritmico-Integrado/` — **SÓ EXISTE COMO DOCX**
**Formato:** `artigo_18.docx` — NÃO há HTML

**❌ Problema CRÍTICO:**

- Artigo não está no workflow HTML/ABNT
- Precisa ser convertido ou reescrito como HTML

**Ações necessárias:**

- [ ] Converter DOCX para HTML com formatação ABNT
- [ ] OU reescrever artigo como HTML standalone
- [ ] Verificar conteúdo do DOCX original

---

#### ARTIGO 19 — GovTechs e Valor de Mercado: Governança Algorítmica e Desempenho

**Arquivo:** `Artigos/19-GovTechs-Valor-Mercado-Goveranca-Algoritmica/artigo_19.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Event Study + Refinitiv Eikon

**✅ O que funciona:**

- Event study como metodologia financeira apropriada
- Refinitiv Eikon como fonte de dados

**❌ Problemas identificados:**

1. **Placeholders** — imp29.06 indica necessidade urgente de "choque de realidade" com dados B3/Economatica
2. **Seção com "placeholder box"** — artigo parece ter seções incompletas com placeholders visíveis
3. **README.md separado** — indica que o artigo foi parcialmente documentado mas não finalizado como HTML

**Ações necessárias:**

- [ ] Cruzar CNPJs de GovTechs com dados reais de mercado (B3/Economatica/Refinitiv)
- [ ] Executar event study real em torno de datas de certificação/provisionamento
- [ ] Preencher ou remover seções com placeholders
- [ ] Verificar se resultados são reais ou simulados

---

#### ARTIGO 20 — Risco de Crédito de Fornecedores e Custos de Transação

**Arquivo:** `Artigos/20-Risco-Credito-Fornecedores-Custos-Transacao/artigo_20.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Regressão Logística + Modelo de Cox + Refinitiv CreditView

**✅ O que funciona:**

- Metodologia quantitativa financeira apropriada
- Integração interessante entre credit risk e transaction costs

**❌ Problemas identificados:**

1. **imp29.06 diz:** "PNCP API 422 (data inválida) — em DEBUG" — problema de extração não resolvido
2. **"credit_classificacao.csv", "retornos_diarios.csv", "artigo20_pncp_*.csv"** — CSVs existem mas conteúdo não verificado
3. **Necesidade de cruzar CNPJ com Refinitiv CreditView** — dados financeiros reais necessários

**Ações necessárias:**

- [ ] Resolver erro de API PNCP (422 data inválida)
- [ ] Cruzar CNPJs com Refinitiv CreditView para dados de crédito
- [ ] Treinar modelo de credit scoring real
- [ ] Executar Cox model para survival de fornecedores

---

#### ARTIGO 21 — Reação do Mercado à Fiscalização do TCU: Estudo de Evento

**Arquivo:** `Artigos/21-Reacao-Mercado-Fiscalizacao-TCU-Estudo-Evento/artigo_21.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Estudo de Evento + Refinitiv Eikon

**✅ O que funciona:**

- Event study aplicado a regulatory enforcement é metodologia sólida
- TCU como fonte de eventos identificáveis

**❌ Problemas identificados:**

1. **"artigo21_acordaos_tcu.csv"** existe mas contém apenas 5 registros (conforme imp27.06) — número insuficiente para event study robusto
2. **imp29.06:** "TCU API erro — template demo" — dados reais não obtidos
3. **"precos_fechamento.csv", "volume.csv"** — dados de mercado existem mas não integrados

**Ações necessárias:**

- [ ] Coletar acórdãos reais do TCU via dadosabertos.tcu.gov.br
- [ ] Identificar eventos de sançãoFiscalizatória com datas precisas
- [ ] Cruzar comRetornos de ações noevent window
- [ ] Calcular retornos anormais cumulativos (CAR) reais

---

#### ARTIGO 22 — Estrutura de Capital e Oligopólio em Compras de TI

**Arquivo:** `Artigos/22-Estrutura-Capital-Oligopolio-Compras-TI/artigo_22.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Painel + Refinitiv Worldscope + PNCP

**✅ O que funciona:**

- Painel econométrico é metodologia apropriada
- Integração PNCP + dados financeiros de empresas

**❌ Problemas CRÍTICOS:**

1. **🔴 SEÇÃO 3.1 COPIADA DE ARTIGO QUALITATIVO:**

   ```
   "Para assegurar a validade e a confiabilidade da análise qualitativa,
   o processo de codificação dos dados primários foi submetido a protocolo
   de dupla revisão cega e independente. Dois codificadores especialistas
   classificaram o corpus..."
   ```

   **Este é um estudo QUANTITATIVO de painel com dados financeiros — NÃO tem codificação qualitativa. Isso é claramente copy-paste.**
2. **"demonstracoes_expandido.csv", "precos_expandido.csv", "retornos_expandido.csv"** — CSVs existem mas conteúdo não verificado

**Ações necessárias:**

- [ ] REMOVER a seção 3.1 fraudulenta (é copy-paste de artigo quali)
- [ ] Substituir por descrição real da metodologiaquantitativa (painel, variáveis, fontes)
- [ ] Verificar se dados financeiros de 6 empresas são reais
- [ ] Executar regressão de painel real

---

#### ARTIGO 23 — Mapeamento da Produção Científica em Governança Algorítmica

**Arquivo:** `Artigos/23-Mapeamento-Producao-Cientifica-Governanca-Algoritmica/artigo_23.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Bibliometrix + VOSviewer + OpenAlex

**✅ O que funciona:**

- Bibliometrix e VOSviewer são ferramentas apropriadas
- Mapeamento de campo é contribuição válida

**❌ Problemas CRÍTICOS:**

1. **🔴 MESMA SEÇÃO 3.1 COPIADA:**

   ```
   "Para assegurar a validade e a confiabilidade da análise qualitativa,
   o processo de codificação dos dados primários foi submetido a protocolo
   de dupla revisão cega e independente..."
   ```

   **BIBLIOMETRIA é análise quantitativa de produção científica — NÃO tem codificação dupla cega.**
2. **"artigos_openalex.csv", "distribuicao_por_*.csv"** — CSVs existem mas não verificados
3. **Possível problema:** artigotem "README.md" indicando que precisa de revisão

**Ações necessárias:**

- [ ] REMOVER seção 3.1 fraudulenta
- [ ] Substituir por descrição real: fontes (OpenAlex/Scopus), termos de busca, critérios de inclusão PRISMA
- [ ] Executar bibliometria real com dados de artigos_openalex.csv
- [ ] Gerar network visualization real com VOSviewer
- [ ] Produzir mapas de densidade e coautoria

---

#### ARTIGO 24 — Determinantes de Eficiência em Compras Públicas: Análise Cross-Country

**Arquivo:** `Artigos/24-Determinantes-Eficiencia-Compras-Publicas-Cross-Country/artigo_24.html`
**Tamanho:** ~300-400 linhas
**Metodologia:** Painel + World Bank WGI + Refinitiv

**✅ O que funciona:**

- Análise cross-country com WGI do Banco Mundial é metodologia robusta
- Integração internacional fortaleceo artigo

**❌ Problemas CRÍTICOS:**

1. **🔴 MESMA SEÇÃO 3.1 COPIADA** — texto idêntico de "dupla revisão cega" aparece aqui também
2. **"dataset_consolidado_wb.csv", "artigo24_wgi_processado.csv"** — CSVs existem (conforme imp27.06, 100 registros WGI)
3. **"README.md"** indica necessidade de revisão

**Ações necessárias:**

- [ ] REMOVER seção 3.1 fraudulenta
- [ ] Substituir por descrição real: países включены, variáveis WGI utilizadas, modelo de regressão
- [ ] Executar painel real com 100 países
- [ ] Verificar se GovTech Index do Banco Mundial está integrado

---

#### ARTIGO 25 — Sistemas Multi-Agente LLM: Revisão Sistemática

**Arquivo:** `Artigos/25-Artigo AI Offline/artigo_25.html`
**Tamanho:** ~150-200 linhas
**Metodologia:** Revisão/Discussão Conceitual + arXiv

**✅ O que funciona:**

- 395 artigos arXiv mencionados
- Revisão de LLM multi-agent é topic quente e relevante

**❌ Problemas CRÍTICOS:**

1. **🔴 MIX INGLÊS/PORTUGUÊS — geração de IA não revisada:**

   ```
   "This study employs a mixed-methods approach combining quantitative
   analysis and qualitative review..."

   "The search strategy included terms such as: 'multi-agent LLM systems',
   'AI agents autonomous decision-making'..."
   ```

2. **"llm_multi_agent_arxiv.csv"** existe (265 KB, 395 registros — conforme imp27.06) — dados reais existem
3. **Artigo Curto** — 150-200 linhas é insuficiente

**Ações necessárias:**

- [ ] Reescrever TODO o artigo em português formal
- [ ] Usar os 395 artigos reais do arXiv (arquivo CSV existe)
- [ ] Construir revisão sistemáticaPRISMA-like com números reais de inclusão/exclusão
- [ ] Expandir para pelo menos 400 linhas

---

### 2.3 Scripts_Geracao

**Pasta:** `Artigos/Scripts_Geracao/`
**Arquivos:** `artigo_base.py`, `gerador_artigos.py`

**Status:** Ferramentas de geração existem mas precisam de revisão para garantir output em português formal.

---

## PARTE III: RESUMO OPERACIONAL

### 3.1 Priorização de Correções

| Prioridade  | Item                                | Artigo/Tese | Problema                                            |
| ----------- | ----------------------------------- | ----------- | --------------------------------------------------- |
| 🔴 CRÍTICA | Refazer seções 2.5-2.7            | TESE        | Mapeamento CrossRef com artigos de física/medicina |
| 🔴 CRÍTICA | Padronizar 819.175 vs 19.640        | TESE        | Inconsistência numérica                           |
| 🔴 CRÍTICA | Reescrever Artigo 16                | 16          | Texto gerado por IA em EN/PT misto                  |
| 🔴 CRÍTICA | Reescrever Artigo 25                | 25          | Texto gerado por IA em EN/PT misto                  |
| 🔴 CRÍTICA | Remover seção 3.1 copy-paste      | 22, 23, 24  | Texto fraudulento de "dupla revisão cega"          |
| 🔴 CRÍTICA | Expandir Artigo 17                  | 17          | Muito curto (~150 linhas)                           |
| 🔴 CRÍTICA | Converter/integrar Artigo 18        | 18          | Só existe como DOCX                                |
| 🟡 ALTA     | Expandir Cap 4 com resultados reais | TESE        | Capítulo 4 muito enxuto                            |
| 🟡 ALTA     | Injetar dados reais NLP             | 01          | "(Simulação)" ainda visível                      |
| 🟡 ALTA     | Injetar anomalias reais             | 02          | 199 anomalias do PNCP                               |
| 🟡 ALTA     | Treinar RF real nos 819K            | 03          | Random Forest com dados reais                       |
| 🟡 ALTA     | Extrair CNPJs reais do PNCP         | 05          | Grafo com nomes de empresas verificáveis           |
| 🟡 ALTA     | Reescrever Artigo 06                | 06          | Texto EN/PT misto                                   |
| 🟡 ALTA     | Decidir qual Artigo 14              | 14          | Dois arquivos no mesmo diretório                   |
| 🟡 ALTA     | Raspagem real de notícias          | 15          | 388 matérias confirmadas                           |
| 🟡 MÉDIA   | Resolver API PNCP 422               | 20          | Data inválida                                      |
| 🟡 MÉDIA   | Coletar acórdãos reais TCU        | 09, 21      | 5 registros insuficientes                           |
| 🟡 MÉDIA   | Extrair justificativas PNCP         | 10          | 350 justificativas reais                            |
| 🟡 MÉDIA   | Raspar impugnações reais          | 11          | 150 recursos administrativos                        |
| 🟡 MÉDIA   | Coletar relatos LinkedIn/Medium     | 13          | 60 netnografia                                      |
| 🟡 MÉDIA   | Cruzar CNPJs com B3/Refinitiv       | 19, 20      | Dados financeiros                                   |
| 🟡 MÉDIA   | Executar painel 100 países         | 24          | WGI com dados reais                                 |
| 🟢 BAIXA    | Verniz final                        | TESE        | Leitura pelo autor                                  |
| 🟢 BAIXA    | Numeração de tabelas              | TESE        | Padronizar                                          |
| 🟢 BAIXA    | Revisar Artigo 12                   | 12          | Verificar χ² para lexicografia                    |

---

### 3.2 Consolidação de Dados Injectáveis

Os seguintes dados do PNCP/Orquestrador podem ser distribuídos pelos artigos:

| Dado                           | Volume  | Artigos que usam         |
| ------------------------------ | ------- | ------------------------ |
| Total PNCP (819.175 processos) | 819.175 | Tese, 01, 02, 03, 04, 05 |
| Anomalias (valores > 1 B)      | 199     | 02                       |
| Fracasso contratual (anulados) | ~?      | 03                       |
| Latência decisória (dias)    | ~?      | 04                       |
| CNPJs fornecedores             | ~?      | 05, 22                   |
| Justificativas de dispensa     | ~?      | 10                       |
| Impugnações                  | ~?      | 11                       |
| Contratos com aditivos         | ~?      | 06                       |

---

### 3.3 Consolidação de Ações por Sprint

#### Sprint 1 — Higiene Crítica (1-2 dias)

1. Remover tabelas 4, 5, 6 da tese (seções 2.5-2.7) OU refazer com busca CrossRef rigorosa
2. Padronizar número 819.175 vs 19.640 na tese
3. Reescrever Artigo 16 em português formal
4. Reescrever Artigo 25 em português formal
5. Remover seção 3.1 fraudulenta dos artigos 22, 23, 24
6. Expandir Artigo 17 para mínimo 400 linhas
7. Integrar Artigo 18 (DOCX → HTML)

#### Sprint 2 — Injeção de Dados Reais (3-5 dias)

1. Rodar NLP em editais do PNCP → Artigo 01
2. Injetar 199 anomalias Isolation Forest → Artigo 02
3. Treinar Random Forest nos 819K → Artigo 03
4. Calcular latência real → Artigo 04
5. Extrair CNPJs reais, redes → Artigo 05
6. Executar Kaplan-Meier/Cox real → Artigo 06
7. Executar DEA real → Artigo 07
8. Computar SHAP real → Artigo 08

#### Sprint 3 — Coleta Empírica (5-7 dias)

1. Raspagem Conjur/Valor/Jota → Artigo 15
2. Extrair justificativas PNCP → Artigo 10
3. Raspagem impugnações Compras.gov.br → Artigo 11
4. Coletar acórdãos TCU via dadosabertos → Artigos 09, 21
5. Netnografia LinkedIn/Medium → Artigo 13
6. Cruzar CNPJs com Refinitiv/B3 → Artigos 19, 20
7. Panel WGI 100 países → Artigo 24

#### Sprint 4 — Consolidação e Verniz (2-3 dias)

1. Expandir Capítulo 4 da tese com resultados em tabelas
2. Padronizar numeração de tabelas da tese
3. Decidir qual Artigo 14 manter
4. Verificar consistência de χ² no Artigo 12
5. Leitura final de verniz pelo autor em todos os artigos
6. Revisão de参考文献 em todos os artigos

---

## PARTE IV: CONCLUSÃO DO DIAGNÓSTICO

### Estado Atual

| Componente                   | Status Real | Distância para Finalização                                                           |
| ---------------------------- | ----------- | --------------------------------------------------------------------------------------- |
| **Tese**               | 70%         | Correções críticas pendentes (tabelas CrossRef, número inconsistente, Cap 4 enxuto) |
| **Arts 01-05**         | 60%         | Estrutura OK, dados ainda a injetar                                                     |
| **Arts 06-15**         | 50%         | 草丛 mistura de dados reais e simulados, problemastextuais                              |
| **Arts 16, 25**        | 20%         | Texto gerado por IA não revisado                                                       |
| **Arts 17**            | 30%         | Curto e incompleto                                                                      |
| **Arts 18**            | 40%         | DOCX precisa ser integrado                                                              |
| **Arts 19-21**         | 50%         | Placeholders e dados insuficientes                                                      |
| **Arts 22-24**         | 40%         | Seção 3.1 fraudulentacopy-paste                                                       |
| **Arts 01-05 (dados)** | 0%          | Aguardando extração/inyecção                                                        |

### Velocidade Estimada

- Sprint 1 (críticos): 1-2 dias
- Sprint 2 (dados PNCP): 3-5 dias
- Sprint 3 (coleta empírica): 5-7 dias
- Sprint 4 (verniz): 2-3 dias

**Total estimado: 11-17 dias de trabalho Intensive**

### Insight Estratégico

O projeto tem **arquitetura impressionante** e volume de dados PNCP (819.175 contratos) que é **diferencial competitivo rara em dissertations de contabilidade no Brasil**. O maior risco não é metodológico — é de **percepção de banca**: os problemas críticos (CrossRef aleatório, texto de IA em EN/PT, seção 3.1 copy-paste) são identificáveis em leitura rápida e podem comprometer a credibilidade de TODO o trabalho.

A recomendação é clara: **corrigir os problemas críticos primeiro**, depois injetar dados reais. Não há problema em um artigo estar com "dados simulados" se a estrutura metodológica estiver sólida — mas há problema se o texto revelar descuido.

---

*Documento atualizado em 29.06.2026*
*Compilado para guiar próximo ciclo de correções e finalização*
