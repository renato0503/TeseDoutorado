# PROGRAMAÇÃO DE CORREÇÃO SISTEMÁTICA — VULNERABILIDADES DA BANCA

**Data:** 10/07/2026
**Método:** Sprints sequenciais com dependências explícitas, entregáveis verificáveis e critérios de aceitação.

**Status consolidado (10/07/2026):**
- ✅ Artigo 01 (Diagnóstico): 6/6 sprints concluídas — ver `docs/sprints_artigo01.md`
- ✅ Artigo 02 (Copiloto): 6/6 sprints concluídas — ver abaixo
- ✅ Produto (Copiloto): 4/4 sprints concluídas — ver `imp.produto.md`
- ✅ Dataset acadêmico: 305 artigos, 6 APIs utilizadas

---

## VISÃO GERAL

| Status | Sprint | Foco | Vulnerabilidades | Duração | Depende de |
|--------|--------|------|-----------------|---------|------------|
| 🟢 Concluído | **S1** | Target real (back-end) | #1, #2, #4 | 4 dias | — |
| 🟢 Concluído | **S2** | XAI de verdade (back-end) | #5, #6, #7, #8 | 3 dias | S1 |
| 🟢 Concluído | **S3** | Correções do artigo (front-end) | #3, #10, #14, #16, #23, #24, #25 | 4 dias | S1, S2 |
| 🟢 Concluído | **S4** | Validação externa | #9, #18 | 4 dias | S1, S2 |
| 🟢 Concluído | **S5** | Polimento final | #11, #12, #13, #15, #17, #19, #20 | 2 dias | S1–S4 |
| 🟢 Concluído | **S6** | Português e conformidade acadêmica | #21, #22 | 3 dias | S3 |

**Total estimado:** 20 dias úteis · **Progresso:** 6/6 sprints concluídas · 20/20 dias executados · **100%**

> **Legenda de status:**
> 🔴 Não iniciado · 🟡 Em andamento · 🔵 Bloqueado (dependência externa) · 🟢 Concluído · ⚪ Pulado (não aplicável)

> **Notas:**
> - A coluna **Status** reflete a situação atual de cada sprint. Atualizar ao iniciar/concluir cada uma.
> - A conformidade com `escrita.md` é uma preocupação **transversal**. As tarefas de cada sprint já devem produzir texto em português brasileiro correto. A Sprint 6 é a revisão final sistemática de todo o artigo, parágrafo por parágrafo.
> - Para iniciar a S1, nenhuma dependência externa é necessária — todos os dados estão no repositório.

---

## SPRINT 1: TARGET REAL E BASELINE

**Objetivo central:** Substituir o target tautológico por desfechos observáveis do PNCP e estabelecer baselines comparativos.

**Vulnerabilidades atacadas:** #1 (target tautológico), #2 (sem desfecho real), #4 (sem baseline)

### 1.1. Construir variável dependente observável (2 dias)

**Entregável:** Novo script `scripts/construir_target_real.py`

```python
# Tarefa 1.1a: Cruzar contratos PNCP com eventos negativos
# Fontes sugeridas:
#   - Coluna "situacao" do PNCP (rescisão, cancelamento, concluído)
#   - Aditivos de valor (> X% do original = proxy de fracasso)
#   - Aditivos de prazo (> Y dias = proxy de problema)
#   - Base de sanções do CEIS/CGU (fornecedores punidos)

# Tarefa 1.1b: Criar target binário observável
# target_real = 1 se QUALQUER destes ocorrer:
#   - situacao IN ('rescindido', 'cancelado', 'anulado')
#   - aditivo_valor > 25% do valor original
#   - aditivo_prazo > 90 dias
#   - fornecedor consta no CEIS/CGU
# target_real = 0 caso contrário

# Tarefa 1.1c: Salvar target_real em coluna nova do CSV
# pncp_contratos_full.csv ganha coluna 'target_real'
```

**Critério de aceitação:**
- [ ] Coluna `target_real` existe no CSV com valores 0/1
- [ ] Distribuição documentada (ex: 12,3% positivos, 87,7% negativos)
- [ ] Matriz de correlação target_real × features preditoras gerada

### 1.2. Retreinar modelos com target real (1 dia)

**Entregável:** `train_models.py` atualizado

```python
# Tarefa 1.2a: Modificar train_models.py para usar target_real
# Em vez de: df["target_risco"] = (risk_score > median).astype(int)
# Usar:     y = df["target_real"]

# Tarefa 1.2b: Reexecutar treinamento completo
# TF-IDF + Isolation Forest (mantém, é não supervisionado)
# Random Forest com target_real

# Tarefa 1.2c: Atualizar métricas
# Gerar classification_report REAL com precision, recall, f1 por classe
# Salvar nova confusion_matrix
# Atualizar metricas.json
```

**Critério de aceitação:**
- [ ] Modelos retreinados com target_real
- [ ] Novas métricas documentadas (aceitar queda de desempenho — é esperado)
- [ ] `metricas.json` atualizado com `target_distribution` e `classification_report`

### 1.3. Implementar baselines comparativos (1 dia)

**Entregável:** Novo script `scripts/baseline_comparison.py`

```python
# Tarefa 1.3a: Baseline 1 — Regra de maioria (dummy classifier)
# Tarefa 1.3b: Baseline 2 — Regressão logística apenas com valor_log
# Tarefa 1.3c: Baseline 3 — Regressão logística com todas as 7 features
# Tarefa 1.3d: Baseline 4 — Árvore de decisão simples (max_depth=3)
# Tarefa 1.3e: Gerar tabela comparativa:
#   | Modelo               | Acurácia | AUC-ROC | F1  | Precisão | Recall |
#   | Dummy (majoritário)  |    xx%   |   xx%   | xx% |   xx%    |  xx%   |
#   | Logit (valor_log)    |    xx%   |   xx%   | xx% |   xx%    |  xx%   |
#   | Logit (7 features)   |    xx%   |   xx%   | xx% |   xx%    |  xx%   |
#   | Árvore (max_depth=3) |    xx%   |   xx%   | xx% |   xx%    |  xx%   |
#   | Random Forest (7 f)  |    xx%   |   xx%   | xx% |   xx%    |  xx%   |
```

**Critério de aceitação:**
- [ ] Tabela comparativa gerada com ≥ 4 baselines
- [ ] Ganho incremental da Random Forest sobre o melhor baseline documentado
- [ ] Se RF não superar significativamente a Logit, documentar como limitação honesta

---

## SPRINT 2: XAI DE VERDADE

**Objetivo central:** Substituir templates estáticos por explicações contrafactuais dinâmicas e integrar os dois motores.

**Vulnerabilidades atacadas:** #5 (SHAP ininteligível), #6 (sem contrafactuais), #7 (valor_log hardcoded), #8 (motores não integrados)

### 2.1. Corrigir valor_log na inferência (0.5 dia)

**Entregável:** `risk_engine.py` modificado

```python
# Tarefa 2.1a: Expor campo de valor no formulário do módulo Avaliação
# Adicionar st.number_input("Valor estimado do contrato (R$):")
# Passar valor como metadados para analisar_risco_contratual()

# Tarefa 2.1b: Usar valor real em _extrair_features_ml
# Antes:  "valor_log": np.log1p(10000),  # hardcoded!
# Depois: "valor_log": np.log1p(metadados.get("valor", 10000) if metadados else 10000),
```

**Critério de aceitação:**
- [ ] Campo de valor visível no módulo de Avaliação
- [ ] `valor_log` varia conforme input do usuário
- [ ] SHAP values recalculados dinamicamente com valor real

### 2.2. Explicações contrafactuais dinâmicas (1.5 dias)

**Entregável:** Novo módulo `models/counterfactual.py`

```python
# Tarefa 2.2a: Implementar geração de contrafactuais
# Para cada feature com alto peso SHAP:
#   1. Identificar o valor atual da feature
#   2. Gerar pergunta contrafactual: "Se [feature] fosse [valor_alternativo] 
#      em vez de [valor_atual], o risco cairia de X% para Y%"
#   3. Usar o modelo para simular a predição com o valor alterado

# Tarefa 2.2b: Implementar explicações textuais em linguagem natural
# Mapear nomes técnicos → português do gestor:
#   "valor_log"             → "Valor estimado do contrato"
#   "complexidade_lexica"   → "Densidade de termos técnicos no edital"
#   "score_tecnico"         → "Menções a tecnologia/inovação no objeto"
#   "objeto_palavras"       → "Nível de detalhamento da descrição"
#   "objeto_len"            → "Tamanho do texto do objeto"
#   "uf_encoded"            → "Estado da federação"
#   "tipo_encoded"          → "Tipo de instrumento contratual"

# Tarefa 2.2c: Substituir o gráfico SHAP técnico por visualização amigável
# Em vez de "uf_encoded: 0.0234", mostrar:
#   "Localização (UF): 0,86% de contribuição para o risco"
#   "Se o valor do contrato fosse 50% menor, o risco cairia de ALTO para MÉDIO"
```

**Critério de aceitação:**
- [ ] Contrafactuais dinâmicos gerados para top-3 features
- [ ] Tradução feature técnica → português implementada
- [ ] Explicações textuais aparecem no frontend no lugar de números crus
- [ ] Citação Wachter et al. (2017) agora respaldada por implementação real

### 2.3. Integrar Isolation Forest + Random Forest (1 dia)

**Entregável:** Modificações em `risk_engine.py`

```python
# Tarefa 2.3a: Criar pipeline integrado
# Fluxo atual (independente):
#   texto → Isolation Forest → flag anomalia
#   texto → Random Forest → score risco
# Fluxo novo (integrado):
#   texto → Isolation Forest → flag anomalia
#     ├─ Se anomalia = True → Random Forest em modo "alerta reforçado"
#     │  (threshold de risco reduzido em 15%, features ponderadas com peso extra)
#     └─ Se anomalia = False → Random Forest em modo padrão

# Tarefa 2.3b: Justificar a integração com teoria
# Anomalia linguística (direcionamento) é um sinal de risco que deve 
# AMPLIFICAR a sensibilidade do modelo preditivo, não apenas coexistir.
```

**Critério de aceitação:**
- [ ] Flag de anomalia altera o comportamento do Random Forest
- [ ] Documentar o racional teórico da integração no artigo

---

## SPRINT 3: CORREÇÕES DO ARTIGO

**Objetivo central:** Corrigir erros factuais, inconsistências, elevar o nível analítico do texto, operacionalizar teorias citadas e documentar iterações DSR.

**Vulnerabilidades atacadas:** #3 (Gini=SHAP), #10 (artigo descritivo), #14 (inconsistências), #16 (referências faltantes), #23 (teorias não operacionalizadas), #24 (iterações DSR não documentadas), #25 (assimetria informacional não quantificada)

### 3.1. Corrigir Tabela 1 (Gini ≠ SHAP) (0.5 dia)

**Entregável:** HTML do artigo atualizado

```python
# Tarefa 3.1a: Recomputar Gini importance SEPARADAMENTE
# Extrair rf.feature_importances_ (Gini) 
# Extrair SHAP mean(|values|) separadamente
# Documentar AMBAS as colunas com valores REAIS e DIFERENTES

# Tarefa 3.1b: Atualizar Tabela 1 com valores corretos
# Se os valores forem muito próximos (ex: Gini 80.52, SHAP 79.87), 
# OK manter — mas NUNCA idênticos a menos que comprovado.

# Tarefa 3.1c: Atualizar o texto que acompanha a tabela
# Explicar a diferença conceitual entre Gini e SHAP
```

**Critério de aceitação:**
- [ ] Colunas Gini e SHAP com valores diferentes e corretos
- [ ] Nota explicativa sobre a diferença das métricas

### 3.2. Extrair design principles (1.5 dias)

**Entregável:** Nova seção no artigo e/ou novo documento `docs/design_principles.md`

```markdown
# Tarefa 3.2a: Derivar 4-6 design principles da experiência DSR
# Exemplos:
#   DP1: "Em sistemas XAI para o setor público, explicações devem ser 
#         expressas em unidades compreensíveis pelo agente administrativo 
#         (R$, dias, cláusulas), não em features de engenharia."
#   DP2: "Modelos de risco em compras públicas devem ter seu target 
#         ancorado em desfechos administrativos observáveis (rescisões, 
#         sanções), não em construtos puramente computacionais."
#   DP3: "A camada de detecção de anomalias (não supervisionada) deve 
#         modular a sensibilidade da camada preditiva (supervisionada), 
#         não operar como módulo independente."
#   DP4: ...

# Tarefa 3.2b: Inserir os design principles no artigo (nova subseção 5.2)
# "5.2 Contribuições Teóricas (Design Principles)"
```

**Critério de aceitação:**
- [ ] ≥ 4 design principles extraídos e justificados
- [ ] Cada DP ancorado em evidência do projeto (o que funcionou/não funcionou)
- [ ] Seção 5.2 adicionada ao artigo

### 3.2b. Operacionalizar referencial teórico (0.5 dia)

**Diagnóstico:** O artigo cita Williamson (1985), Jensen & Meckling (1976), Mazzucato (2014), mas não vincula **explicitamente** cada decisão arquitetural a esses referenciais. A banca perguntará: *"Onde está Williamson no seu código?"*

**Entregável:** Nova subseção "2.3 Operacionalização dos Construtos Teóricos" e/ou coluna adicional na Tabela 1

```markdown
# Tarefa 3.2b.1: Mapear teoria → feature/decisão de design

| Construto teórico | Autor | Operacionalização no Copiloto | Evidência |
|---|---|---|---|
| Custo de transação ex-ante | Williamson (1985) | valor_log: contratos maiores concentram risco de hold-up | Peso SHAP 80,52% |
| Complexidade contratual | Williamson (1985) | complexidade_lexica + objeto_palavras: especificidade de ativos | Peso SHAP 8,59% + 1,53% |
| Seleção adversa | Akerlof (1970) | Isolation Forest: detecta padrão anômalo = possível direcionamento | contamination=0.1 |
| Risco moral ex-post | Jensen & Meckling (1976) | score_tecnico: indicadores de monitoramento | Peso SHAP 4,47% |
| Lock-in tecnológico | Williamson (1985) | Lacuna "Propriedade Intelectual" + reescrita sugerida | Regex PI + template |
| Accountability estatal | Wachter et al. (2017) | SHAP contrafactuais + LGPD Art. 20 | Explicações dinâmicas |
| Estado empreendedor | Mazzucato (2014) | Lacuna "Inovação/Startups" + LC 182/2021 | Regex inovação + CPSI |

# Tarefa 3.2b.2: Inserir esta tabela no artigo como Tabela 4 ou na seção 2.3
```

**Critério de aceitação:**
- [ ] ≥ 6 construtos teóricos mapeados para features/decisões
- [ ] Cada mapeamento inclui: teoria, autor, operacionalização, evidência
- [ ] Tabela ou subseção adicionada ao artigo

### 3.2c. Documentar iterações de design (0.5 dia)

**Diagnóstico:** O artigo descreve o artefato final como se tivesse sido construído em uma única tentativa linear. DSR autêntica documenta iterações, becos sem saída e refinamentos. A banca perguntará: *"Quantas versões do Copiloto existiram antes desta? O que foi descartado e por quê?"*

**Entregável:** Nova subseção "3.0 Iterações de Design e Decisões Arquiteturais"

```markdown
# Tarefa 3.2c.1: Reconstruir a história real do desenvolvimento
# Iteração 0 (maio/2026): Protótipos HTML estáticos (Copiloto/modulo_avaliacao/)
#   → Decisão: HTML insuficiente, precisa de backend Python com ML real
# Iteração 1 (junho/2026): Scripts Python isolados + Jupyter notebooks
#   → Decisão: Funciona mas não é acessível a gestores, precisa de interface web
# Iteração 2 (julho/2026): MVP Streamlit com regras heurísticas (regex)
#   → Decisão: Heurísticas são frágeis, precisa de ML treinado em dados reais
# Iteração 3 (julho/2026): Integração PNCP + TF-IDF + Isolation Forest + Random Forest
#   → Decisão: Modelos supervisionados exigem target; target determinístico é frágil
# Iteração 4 (atual): Target observável + SHAP contrafactual + motores integrados
#   → Lição aprendida e design principle derivado

# Tarefa 3.2c.2: Para cada iteração, documentar:
# - O que foi tentado
# - O que funcionou
# - O que falhou
# - O design principle extraído da falha
```

**Critério de aceitação:**
- [ ] ≥ 4 iterações documentadas com datas e decisões
- [ ] Cada iteração inclui: objetivo, método, resultado, lição aprendida
- [ ] As iterações explicam a arquitetura atual como consequência de refinamentos, não como escolha inicial óbvia

### 3.2d. Operacionalizar "assimetria informacional" (0.25 dia)

**Diagnóstico:** O conceito central da tese ("assimetria informacional") é mencionado 11 vezes no artigo como motivação, mas nunca é **quantificado** ou **medido**. A banca perguntará: *"Quanto de assimetria existe? O Copiloto reduziu em quanto? Como o senhor mede isso?"*

**Entregável:** Nova subseção "4.5 Redução de Assimetria Informacional" e/ou métrica no artigo

```markdown
# Tarefa 3.2d.1: Definir proxy quantificável de assimetria informacional
# Opções:
#   (a) Distância entre complexidade léxica do edital e mediana do mercado
#       → Se o edital é 3σ acima da mediana, há assimetria alta
#   (b) Taxa de lacunas detectadas / total de cláusulas esperadas
#       → 8 lacunas em 16 cláusulas = 50% de assimetria
#   (c) Score SHAP de anomalia: quanto mais anômalo, mais assimétrico
#   (d) Comparação pré/pós: submeter edital "cru" vs edital "corrigido pelo Copiloto"
#       → Redução no score de risco = redução de assimetria

# Tarefa 3.2d.2: Calcular a métrica escolhida e reportar no artigo
# Exemplo: "O Copiloto reduziu a assimetria informacional média em X%,
# medida pela distância KL entre o perfil léxico do edital e o perfil
# mediano dos 15.000 objetos do PNCP (baseline de mercado)."
```

**Critério de aceitação:**
- [ ] Uma métrica de assimetria informacional definida e calculada
- [ ] Valor numérico reportado (ex: "assimetria média pré-Copiloto: 0.68; pós: 0.31")
- [ ] Subseção 4.5 ou parágrafo na Discussão com o cálculo

### 3.3. Corrigir inconsistências (0.5 dia)

**Entregável:** Verificação e correção de todos os números no artigo

```markdown
# Tarefa 3.3a: Auditar números contra metricas.json e train_models.py
# - n_estimators: artigo diz 100, metricas.json diz 150 → unificar
# - acurácia: holdout 99.13% vs CV 98.77% → distinguir claramente
# - registros: 50.000 treino total ou 40.000 treino + 10.000 teste?

# Tarefa 3.3b: Corrigir erros de digitação
# Abstract EN: "Brazilrsquo" → "Brazil's"
# "F1-Score de 99,11%" → verificar se é macro avg ou weighted avg

# Tarefa 3.3c: Verificar datas e versões
# PNCP: Set/2021 - Ago/2024 consistente em todo o texto
# Modelos: data de treinamento consistente com metricas.json
```

**Critério de aceitação:**
- [ ] Todos os números do artigo conferem com as fontes (código, JSON)
- [ ] Nenhum erro de digitação nos abstracts

### 3.4. Referências faltantes (0.5 dia)

**Entregável:** Bibliografia atualizada

```markdown
# Tarefa 3.4a: Adicionar referências citadas no código mas ausentes no artigo
# - Akerlof, G. A. (1970). The market for "lemons".
# - Martins & Gomes (2022) — referência de lock-in tecnológico
# - Gregor, S., & Hevner, A. R. (2013). Positioning and presenting 
#   design science research for maximum impact. MIS Quarterly.

# Tarefa 3.4b: Adicionar referências novas (design principles, contrafactuais)
# - Wachter et al. (2017) — já citada, verificar se implementação corresponde
# - Molnar, C. (2020). Interpretable Machine Learning. (referência geral XAI)
```

**Critério de aceitação:**
- [ ] Toda referência no código consta no artigo
- [ ] Toda referência no artigo é citada no texto
- [ ] Formatação APA 7ª edição consistente

---

## SPRINT 4: VALIDAÇÃO EXTERNA

**Objetivo central:** Produzir evidência qualitativa de que o artefato funciona para usuários reais.

**Vulnerabilidades atacadas:** #9 (sem validação externa), #18 (poucos exemplos)

### 4.1. Estudo de caso com editais reais (2 dias)

**Entregável:** Documento `docs/estudo_caso_validacao.md`

```markdown
# Tarefa 4.1a: Selecionar 5 editais reais do PNCP
# - 2 editais "saudáveis" (sem histórico de problemas)
# - 3 editais "problemáticos" (com impugnações ou rescisões conhecidas)

# Tarefa 4.1b: Submeter ao Copiloto e documentar
# Para cada edital:
#   - Score de conformidade (0-100)
#   - Predição Random Forest (risco alto/médio/baixo)
#   - Flag de anomalia (Isolation Forest)
#   - Top-3 features SHAP com contrafactuais
#   - Comparação com desfecho real conhecido

# Tarefa 4.1c: Tabela-resumo
# | Edital | Score | Risco RF | Anomalia | Desfecho Real | Concorda? |
# |--------|-------|----------|----------|---------------|-----------|
# | E01    |  82%  |  BAIXO   |   Não    | Sem problemas |    Sim    |
# | E02    |  45%  |  ALTO    |   Sim    | Impugnado     |    Sim    |
# | ...    |  ...  |   ...    |   ...    |     ...       |    ...    |
```

**Critério de aceitação:**
- [ ] ≥ 5 editais reais analisados
- [ ] Comparação predição × desfecho real documentada
- [ ] Taxa de acerto reportada honestamente (incluindo erros)

### 4.2. Avaliação com especialistas (2 dias)

**Entregável:** Documento `docs/avaliacao_especialistas.md`

```markdown
# Tarefa 4.2a: Preparar protocolo de avaliação
# - Questionário estruturado (escala Likert 1-5)
# - 5 dimensões: utilidade, usabilidade, confiança, explicabilidade, intenção de uso
# - Roteiro de tarefas: "Analise este edital e diga se confia no resultado"

# Tarefa 4.2b: Recrutar 3-5 avaliadores
# Sugestões de perfil:
#   - 1 pregoeiro municipal/estadual
#   - 1 auditor de controle externo (TCE/TCU)
#   - 1 advogado especializado em licitações
#   - 1 fornecedor GovTech
#   - 1 pesquisador acadêmico (orientador)

# Tarefa 4.2c: Aplicar, tabular e analisar
# - Média e desvio-padrão por dimensão
# - Comentários qualitativos transcritos
# - Comparação pré/pós interação (se aplicável)
```

**Critério de aceitação:**
- [ ] ≥ 3 avaliadores consultados
- [ ] Questionários respondidos e tabulados
- [ ] Seção de avaliação qualitativa adicionada ao artigo (4.5)

---

## SPRINT 5: POLIMENTO FINAL

**Objetivo central:** Corrigir problemas menores de produto, usabilidade e conformidade.

**Vulnerabilidades atacadas:** #11 (Freemium), #12 (NLP domain), #13 (recomendações estáticas), #15 (latência), #17 (typo EN), #19 (privacidade), #20 (retreinamento)

### 5.1. Conflito de interesses (Freemium) (0.5 dia)

**Entregável:** Modificações em `app/app.py` e páginas

```python
# Tarefa 5.1a: Adicionar disclaimer acadêmico visível
# "Esta ferramenta é parte de pesquisa de doutorado da Fucape Business School.
#  O uso é gratuito para fins acadêmicos e de avaliação. O modelo Premium 
#  destina-se a viabilizar a continuidade da pesquisa."

# Tarefa 5.1b: Separar claramente pesquisa vs consultoria
# - Página "Sobre" com informações do programa de doutorado
# - Link da consultoria com disclaimer: "Consultoria independente, não vinculada à Fucape"
# - Adicionar logo da Fucape no header
```

**Critério de aceitação:**
- [ ] Disclaimer acadêmico visível na Home
- [ ] Separação clara entre pesquisa e consultoria

### 5.2. NLP domain mismatch (0.5 dia)

**Entregável:** Modificações em `anomaly_detector.py`

```python
# Tarefa 5.2a: Na inferência, extrair apenas o OBJETO do texto completo
# Usar regex para isolar a seção "DO OBJETO" antes de passar ao TF-IDF
# Se não encontrar, usar primeiros 500 caracteres (heurística)

# Tarefa 5.2b: Alternativa: treinar segundo vetorizador em textos completos
# Coletar textos completos de editais (PDFs disponíveis no PNCP)
# Treinar TF-IDF alternativo com max_features=2000
```

**Critério de aceitação:**
- [ ] Texto passado ao TF-IDF é compatível com o domínio de treino
- [ ] Documentar a limitação se impossível obter textos completos

### 5.3. Recomendações com IA (0.5 dia)

**Entregável:** Modificações em `risk_engine.py`

```python
# Tarefa 5.3a: Substituir if/elif estático por ranking SHAP
# Em vez de recomendar "adicionar garantia" sempre:
#   1. Rodar SHAP no texto
#   2. Identificar top-3 features com maior peso positivo de risco
#   3. Gerar recomendação específica baseada na feature:
#      - complexidade_lexica alta → "Simplificar linguagem do objeto"
#      - score_tecnico baixo → "Detalhar requisitos técnicos"
#      - objeto_palavras baixo → "Expandir descrição do objeto (atual: X palavras)"

# Tarefa 5.3b: Manter fallback de lacunas como complemento
# SHAP-driven recommendations + lacunas de regex = relatório completo
```

**Critério de aceitação:**
- [ ] Recomendações variam conforme o conteúdo real do texto
- [ ] SHAP-driven recommendations implementadas para ≥ 3 features

### 5.4. Itens menores (0.5 dia)

```markdown
# Tarefa 5.4a: Validar latência experimentalmente
# - Script: medir tempo de 100 execuções do pipeline completo
# - Reportar média, mediana, p95, p99

# Tarefa 5.4b: Corrigir typo no abstract EN
# "Brazilrsquo" → "Brazil's"

# Tarefa 5.4c: Adicionar política de privacidade
# - Nova página "Privacidade" no app
# - Textos NÃO são armazenados após a sessão
# - Nenhum dado é compartilhado com terceiros

# Tarefa 5.4d: Adicionar mais exemplos carregáveis
# - Edital de Obras (construção civil)
# - Contrato de Facilities (terceirização)
# - Pregão de Medicamentos (saúde)

# Tarefa 5.4e: Pipeline de retreinamento
# - Script scripts/update_models.sh (ou .ps1)
# - Documentar no README: periodicidade sugerida (trimestral)
```

---

## CRONOGRAMA CONSOLIDADO

```
Dia 01-02: [S1] Target real — construir desfechos observáveis
Dia 03-04: [S1] Retreinar modelos + baselines
Dia 05-06: [S2] XAI real — contrafactuais dinâmicos
Dia 07:    [S2] Corrigir valor_log + integrar motores
Dia 08-09: [S3] Corrigir artigo — Tabela 1, design principles
Dia 10:    [S3] Operacionalizar teorias + iterações DSR + métrica de assimetria
Dia 11:    [S3] Inconsistências + referências
Dia 12-13: [S4] Estudo de caso com editais reais
Dia 14-15: [S4] Avaliação com especialistas
Dia 16:    [S5] Freemium, NLP, recomendações IA
Dia 17:    [S5] Itens menores, validação final
Dia 18:    [S6] Re-acentuação pt-BR + eliminar travessões
Dia 19:    [S6] Palavras proibidas IA + conectivos após ponto
Dia 20:    [S6] Tempos verbais + citações APA + checklist final
```

---

## VULNERABILIDADES — LISTA COMPLETA

| # | Vulnerabilidade | Sprint | Gravidade |
|---|----------------|--------|-----------|
| 1 | Target tautológico (construído com as mesmas features) | S1 | Crítica |
| 2 | Ausência de variável dependente observável real | S1 | Crítica |
| 3 | Tabela 1: Gini = SHAP (impossível matematicamente) | S3 | Alta |
| 4 | Sem baseline comparativo (Dummy, Logit, Árvore) | S1 | Alta |
| 5 | SHAP explica features de engenharia, não conteúdo jurídico | S2 | Alta |
| 6 | Explicações são templates estáticos, não contrafactuais | S2 | Alta |
| 7 | `valor_log` hardcoded (`np.log1p(10000)`) na inferência | S2 | Alta |
| 8 | Isolation Forest e Random Forest justapostos, não integrados | S2 | Média |
| 9 | Sem validação externa/qualitativa com usuários reais | S4 | Média |
| 10 | Artigo descritivo, sem design principles (contribuição teórica) | S3 | Média |
| 11 | Modelo Freemium com link de consultoria (conflito de interesses) | S5 | Média |
| 12 | NLP: TF-IDF treinado em objetos curtos, aplicado a textos longos | S5 | Média |
| 13 | Recomendações são if/elif estático, não usam IA | S5 | Média |
| 14 | Inconsistências: n_estimators 100 vs 150; acurácia treino × CV | S3 | Baixa |
| 15 | Latência "< 2 segundos" e ganho "7.200×" não validados | S5 | Baixa |
| 16 | Referências incompletas (Martins & Gomes 2022, Akerlof 1970) | S3 | Baixa |
| 17 | Typo no abstract EN: "Brazilrsquo" | S5 | Baixa |
| 18 | Apenas 2 exemplos carregáveis no app | S4 | Baixa |
| 19 | Sem política de privacidade ou termos de uso | S5 | Baixa |
| 20 | Sem pipeline de retreinamento dos modelos | S5 | Baixa |
| 21 | Artigo em ASCII (sem acentos, ç, ~) — não é pt-BR | S6 | Alta |
| 22 | Artigo não-conforme com `docs/escrita.md` (travessões, IA-words, conectivos, tempos verbais) | S6 | Alta |
| 23 | Referencial teórico citado mas não operacionalizado (onde está Williamson no código?) | S3 | Média |
| 24 | DSR descrita como processo linear — não documenta iterações, falhas e refinamentos | S3 | Média |
| 25 | "Assimetria informacional" (conceito central) nunca é quantificada ou medida | S3 | Média |

---

## SPRINT 6: PORTUGUÊS BRASILEIRO E CONFORMIDADE ESCRITA.MD

**Objetivo central:** Revisar integralmente o artigo para português brasileiro com acentuação completa e conformidade estrita com o guia `docs/escrita.md`.

**Vulnerabilidades atacadas:** #21 (texto sem acentos — ASCII), #22 (não-conformidade com `escrita.md`)

**Dependência:** Sprint 3 (artigo já corrigido em conteúdo) — a revisão linguística é a última camada, para não desperdiçar esforço em texto que ainda será alterado.

### 6.1. Re-acentuação completa do artigo (1 dia)

**Diagnóstico:** O arquivo HTML atual (`artigo_02_tecnologico.html`) foi escrito com caracteres ASCII para evitar problemas de encoding durante a geração. Todas as palavras perderam acentos e cedilhas. Exemplos:

| Atual (ASCII) | Deveria ser (pt-BR) |
|---|---|
| `deficit tecnico` | `déficit técnico` |
| `impoem barreiras` | `impõem barreiras` |
| `contratacoes de inovacao` | `contratações de inovação` |
| `nao supervisionado` | `não supervisionado` |
| `arvores` | `árvores` |
| `explicacoes contrafactuais` | `explicações contrafactuais` |
| `conclusoes tecnologicas` | `conclusões tecnológicas` |
| `codigo-fonte` | `código-fonte` |
| `publicas` | `públicas` |
| `metodologia` | `metodologia` (ok, mas conferir) |

**Entregável:** Script `scripts/reacentuar_artigo.py`

```python
# Tarefa 6.1a: Mapeamento reverso ASCII → pt-BR (automático)
# Como o texto foi escrito consistentemente sem acentos, um script pode
# aplicar substituições sistemáticas usando um dicionário de mapeamento:
#   "caixa-preta" → "caixa-preta" (não muda, hífen ok)
#   "contratacoes" → "contratações"
#   "deficit" → "déficit"
#   "publicas" → "públicas"
#   ... etc.

# Tarefa 6.1b: Revisão manual pós-script
# Nenhum script é 100% — ambiguidades como "e" (verbo ser ou conjunção "e")
# exigem revisão humana parágrafo por parágrafo.

# Tarefa 6.1c: Atenção especial ao Abstract em inglês
# O abstract NÃO deve ser re-acentuado (inglês não usa acentos).
# "Brazil's" deve permanecer com apóstrofe, não "Brazilrsquo".
```

**Critério de aceitação:**
- [ ] Zero palavras sem acento onde a norma exige
- [ ] Zero erros de cedilha (ç)
- [ ] Til (~) correto em todas as nasalizações (não, condições, etc.)
- [ ] Crase aplicada onde obrigatório (à, às)
- [ ] Abstract em inglês preservado sem acentos

### 6.2. Eliminar TODOS os travessões (0.5 dia)

**Diagnóstico:** O artigo atual contém travessões (`&mdash;`) em diversas passagens. O `escrita.md` §4.3 proíbe taxativamente: **"O travessão (—) não é elemento da escrita acadêmica formal."**

**Entregável:** Correção manual de cada ocorrência

| Atual (com travessão) | Correção (sem travessão) |
|---|---|
| `Diante desse impasse — a urgência...` | `Diante desse impasse, a urgência...` (vírgula) |
| `SHAP — SHapley Additive exPlanations` | `SHAP (SHapley Additive exPlanations)` (parênteses) |
| `variável-alvo — construída como` | `variável-alvo, construída como` (vírgula) |
| `Conclusões —` como separador | Reescrever a frase ou usar dois-pontos |

```python
# Tarefa 6.2a: Script de detecção
# grep ou regex para localizar TODAS as ocorrências de &mdash; e —
import re
with open('artigo.html') as f:
    for i, line in enumerate(f, 1):
        if '&mdash;' in line or '—' in line:
            print(f"Linha {i}: travessão detectado")

# Tarefa 6.2b: Substituição caso a caso
# Cada ocorrência exige decisão editorial:
# - Informação parentética curta → vírgulas
# - Explicação de sigla → parênteses
# - Separação de orações → reescrever como frase independente
# - Ênfase → incorporar à frase principal
```

**Critério de aceitação:**
- [ ] Zero travessões no artigo completo (HTML + abstracts)
- [ ] Cada substituição preserva o sentido original
- [ ] Nenhum parágrafo ficou truncado ou sem pontuação

### 6.3. Eliminar palavras proibidas e marcadores de IA (0.5 dia)

**Diagnóstico:** O `escrita.md` §9 lista palavras que denunciam texto gerado por IA e devem ser eliminadas. O artigo atual contém pelo menos uma ocorrência de "crucial" (p.4, linha 127: "Crucialmente, o escore numérico...").

**Lista de verificação (palavras a buscar e substituir):**

```python
# Tarefa 6.3a: Script de varredura
PALAVRAS_PROIBIDAS = [
    "crucial", "inovador", "holístico", "delve", "landscape",
    "revolucionar", "de ponta", "alavancar", "robusto",
    "fomentar", "vasto", "profundamente", "notável",
    "impressionante", "excelente", "enorme", "gigantesco",
    "incrível", "maravilhoso", "brilhante",
]

# Para cada palavra, localizar ocorrências e propor substituição

# Tarefa 6.3b: Substituições específicas já identificadas
# "Crucialmente" → "De forma relevante" ou "Nesse sentido"
# (verificar se há outras após re-acentuação)
```

**Critério de aceitação:**
- [ ] Zero palavras da lista de proibidas do §9.1
- [ ] Zero adjetivações valorativas (§4.1)
- [ ] Zero expressões informais/coloquiais (§4.2)
- [ ] Zero padrões de escrita que denunciam IA (§9.2)

### 6.4. Verificação de conectivos após ponto final (0.5 dia)

**Diagnóstico:** O `escrita.md` §5.1 estabelece a regra de ouro: **"Toda frase que inicia após um ponto final (.) deve começar com um conectivo ou elemento de coesão que a vincule à frase anterior."** O artigo atual precisa ser verificado frase por frase.

**Entregável:** Revisão parágrafo por parágrafo

```python
# Tarefa 6.4a: Script de análise
# Extrair primeiras palavras após cada ponto final
# Sinalizar frases que não começam com conectivo
import re

CONECTIVOS_VALIDOS = [
    "Além disso", "Ademais", "Nessa perspectiva", "Soma-se a isso",
    "Contudo", "Entretanto", "No entanto", "Todavia", "Por outro lado",
    "Em razão disso", "Devido a esse fato", "Em decorrência disso",
    "Dessa forma", "Assim sendo", "Por conseguinte", "Como resultado",
    "Portanto", "Logo", "Em síntese", "Diante do exposto",
    "Conforme", "Segundo", "De acordo com", "Nesse sentido",
    "Em contrapartida", "De maneira análoga", "Similarmente",
    "Posteriormente", "Em seguida", "Paralelamente",
    "A título de exemplo", "Nesse contexto", "Para ilustrar",
    "Com efeito", "De fato", "Vale ressaltar que",
    "Para tanto", "Com esse propósito", "A fim de",
    "Embora", "Ainda que", "Não obstante",
    "O", "A", "Os", "As",  # Artigos (aceitável em continuação)
    "Este", "Esse", "Esta", "Essa",  # Pronomes demonstrativos
]

# Tarefa 6.4b: Correção manual das frases sinalizadas
# Adicionar conectivo apropriado ou reescrever para garantir coesão
```

**Critério de aceitação:**
- [ ] ≥ 90% das frases após ponto final iniciam com conectivo ou elemento coesivo
- [ ] Nenhum parágrafo com duas frases soltas consecutivas
- [ ] Conectivos variados (sem repetir o mesmo 3x seguidas)

### 6.5. Verificação de tempos verbais por seção (0.25 dia)

**Diagnóstico:** O `escrita.md` §4.5 define tempos verbais específicos para cada seção.

```python
# Tarefa 6.5a: Mapear seção → tempo verbal esperado
# Introdução:         Presente + Pretérito Perfeito (contexto)
# Fundamentação (2):  Presente + Pretérito Perfeito (literatura)
# Metodologia (DSR):  Pretérito Perfeito (o que foi feito)
# Arquitetura (3):    Presente (descrição do sistema) ← EXCEÇÃO: descreve o artefato existente
# Avaliação (4):      Pretérito Perfeito (métricas obtidas)
# Conclusão (5):      Presente (síntese) + Pretérito (achados)

# Tarefa 6.5b: Auditar tempos verbais
# Verificar se a seção de Metodologia usa "Foi utilizado", "Realizou-se"
# Verificar se a seção de Resultados usa "Os dados indicaram", "Observou-se"
# Verificar se a Discussão/Conclusão usa "Os resultados sugerem" (presente)
```

**Critério de aceitação:**
- [ ] Tempos verbais consistentes por seção
- [ ] Metodologia e Resultados no pretérito perfeito
- [ ] Discussão e Conclusão no presente

### 6.6. Verificação de citações (APA 7ª ed.) (0.25 dia)

**Diagnóstico:** `escrita.md` §6 e §7 definem o formato APA para citações.

```python
# Tarefa 6.6a: Verificar citações no texto
# Todas no formato (Autor, Ano) ou Autor (Ano)
# 3+ autores: et al. (não "e colaboradores")
# Citações diretas: incluem página

# Tarefa 6.6b: Verificar lista de referências
# Recuo francês (hanging indent) em todas
# Itálico em títulos de periódicos e livros
# DOI em formato https://doi.org/...
# Sobrenome em maiúscula/minúscula conforme APA (não ABNT)
```

**Critério de aceitação:**
- [ ] Toda afirmação não própria tem citação
- [ ] Formato APA 7ª ed. consistente em todas as citações
- [ ] Referências conferem com citações no texto (via script)

---

## CHECKLIST FINAL PRÉ-DEFESA

### Checklist Técnico (S1–S2)
- [ ] Target é observável (não tautológico)
- [ ] Baseline comparison documentado
- [ ] Tabela 1 tem Gini ≠ SHAP (valores reais)
- [ ] Contrafactuais dinâmicos implementados
- [ ] valor_log não é hardcoded
- [ ] Motores integrados (não justapostos)

### Checklist de Conteúdo (S3)
- [ ] Design principles extraídos (≥ 4)
- [ ] Teorias operacionalizadas (tabela teoria→feature, ≥ 6 mapeamentos)
- [ ] Iterações DSR documentadas (≥ 4 iterações com lições aprendidas)
- [ ] Métrica de assimetria informacional definida e calculada
- [ ] Todas as referências completas (APA 7)
- [ ] Nenhum número inconsistente artigo × código
- [ ] English abstract sem erros de digitação

### Checklist de Validação (S4)
- [ ] Estudo de caso documentado (≥ 5 editais)
- [ ] Avaliação com especialistas (≥ 3)

### Checklist de Produto (S5)
- [ ] Disclaimer acadêmico visível
- [ ] Política de privacidade no app
- [ ] Pipeline de retreinamento documentado
- [ ] Recomendações SHAP-driven implementadas

### Checklist de Linguagem (S6) — `escrita.md`
- [ ] Zero palavras sem acento (pt-BR completo)
- [ ] Zero travessões no texto
- [ ] Zero palavras proibidas (§9.1)
- [ ] Zero adjetivações valorativas (§4.1)
- [ ] Zero expressões coloquiais (§4.2)
- [ ] ≥ 90% frases iniciam com conectivo após ponto final (§5.1)
- [ ] Tempos verbais corretos por seção (§4.5)
- [ ] Citações 100% APA 7ª ed. (§6, §7)
- [ ] Estrutura macro→micro em todas as seções (§3)
- [ ] Texto impessoal (3ª pessoa ou 1ª plural) (§2.2)
