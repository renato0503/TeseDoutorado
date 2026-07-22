# PROTOCOLO DE AVALIAÇÃO COM ESPECIALISTAS

**Sprint 10.1 — Data: 18/07/2026**

## Objetivo

Submeter o Copiloto Algorítmico à avaliação de especialistas em compras públicas, controle externo e tecnologia governamental, coletando evidência qualitativa sobre utilidade, usabilidade, confiança, explicabilidade e intenção de uso.

---

## Perfil dos Avaliadores (Sugestão de Recrutamento)

| # | Perfil | Justificativa | Quantos |
|---|--------|--------------|---------|
| A | **Pregoeiro/Agente de Contratação** municipal ou estadual | Usuário-alvo primário. Avalia utilidade prática no dia a dia. | 1-2 |
| B | **Auditor de Controle Externo** (TCE/TCU/CGU) | Avalia conformidade legal, accountability e aderência à jurisprudência. | 1 |
| C | **Advogado especializado em Licitações** | Avalia correção jurídica das cláusulas, fundamentação legal. | 1 |
| D | **Fornecedor GovTech / Startup** | Avalia a perspectiva do mercado: o Copiloto reduz ou aumenta barreiras? | 1 |
| E | **Pesquisador acadêmico** (orientador ou convidado) | Avalia rigor metodológico, DSR, contribuição teórica. | 1 |

**Total sugerido:** 5 avaliadores

---

## Instrumento de Coleta

### Parte I — Perfil do Avaliador

- Nome (opcional):
- Instituição:
- Cargo/Função:
- Anos de experiência em compras públicas:
- Familiaridade com IA/ML (escala 1-5):

### Parte II — Tarefas Guiadas

O avaliador receberá acesso ao Copiloto (Streamlit Cloud) e executará as seguintes tarefas:

**Tarefa 1:** Carregar o exemplo "Edital de TI" e analisar os resultados.
**Tarefa 2:** Modificar o valor estimado do contrato e observar mudanças na predição.
**Tarefa 3:** Modificar a vigência prevista e observar mudanças na predição e nos contrafactuais.
**Tarefa 4:** Submeter um edital próprio (se disponível) ou edital fornecido pelo pesquisador.
**Tarefa 5:** Interpretar os contrafactuais exibidos e responder: "Você confiaria neste resultado para tomar uma decisão?"

### Parte III — Questionário Estruturado (Escala Likert 1-5)

Para cada afirmação, o avaliador atribui nota de 1 (discordo totalmente) a 5 (concordo totalmente).

#### Dimensão 1: Utilidade Percebida

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| U1 | O Copiloto me ajudaria a identificar riscos em editais antes da publicação | | | | | |
| U2 | As recomendações geradas são acionáveis (posso usá-las para corrigir o edital) | | | | | |
| U3 | O Copiloto reduziria o tempo que gasto revisando minutas de editais | | | | | |

#### Dimensão 2: Usabilidade

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| US1 | A interface é intuitiva e fácil de usar | | | | | |
| US2 | Consegui entender rapidamente o que cada métrica significa | | | | | |
| US3 | O fluxo de trabalho (colar texto → analisar → ler resultados) é eficiente | | | | | |

#### Dimensão 3: Confiança

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| C1 | Confio que as predições do Copiloto são baseadas em dados reais do PNCP | | | | | |
| C2 | O fato de o modelo ter acurácia de 93,36% e AUC-ROC de 90,83% me transmite confiança | | | | | |
| C3 | A exibição da distribuição do target (1,99% positivos, após remediação) aumenta minha confiança | | | | | |

#### Dimensão 4: Explicabilidade

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| E1 | As explicações contrafactuais me ajudam a entender POR QUE o risco é alto/baixo | | | | | |
| E2 | Consigo relacionar as features SHAP (ex: vigencia_log) com características reais do edital | | | | | |
| E3 | Prefiro receber explicações contrafactuais a receber apenas um número de risco | | | | | |

#### Dimensão 5: Intenção de Uso

| # | Afirmação | 1 | 2 | 3 | 4 | 5 |
|---|-----------|---|---|---|---|---|
| I1 | Eu usaria o Copiloto no meu trabalho se estivesse disponível | | | | | |
| I2 | Eu recomendaria o Copiloto a colegas da área de compras públicas | | | | | |
| I3 | O modelo Freemium (3 análises grátis) é um modelo justo de acesso | | | | | |

### Parte IV — Questões Abertas

1. Qual aspecto do Copiloto você considerou **mais útil**? Por quê?

2. Qual aspecto você considerou **menos útil** ou **confuso**? Por quê?

3. Que funcionalidade você **gostaria que existisse** mas não encontrou?

4. Você identifica algum **risco legal ou ético** no uso deste tipo de ferramenta em compras públicas?

5. Comentários adicionais ou sugestões:

---

## Procedimento de Aplicação

1. **Pré-sessão (5 min):** Explicar o contexto da pesquisa (DSR, doutorado Fucape), o objetivo do Copiloto e o protocolo de avaliação. Esclarecer que não há resposta certa ou errada.

2. **Sessão guiada (20 min):** O avaliador executa as 5 tarefas enquanto o pesquisador observa e registra comentários espontâneos, hesitações e dúvidas.

3. **Questionário (10 min):** O avaliador preenche as Partes III e IV.

4. **Debriefing (5 min):** Discussão aberta sobre a experiência.

**Tempo total por avaliador:** ~40 minutos

---

## Análise dos Dados

### Análise Quantitativa

Para cada dimensão, calcular:
- Média e desvio-padrão das notas Likert
- Coeficiente de concordância entre avaliadores (se n ≥ 5)
- Comparação entre perfis (ex: pregoeiro vs. auditor vs. advogado)

### Análise Qualitativa

- Análise de conteúdo das questões abertas (Bardin, 2011)
- Categorização de comentários espontâneos durante a sessão
- Identificação de temas recorrentes e outliers

---

## Resultados Esperados

Com base na versão atual do artefato (Sprint 10, modelo pós-remediação), espera-se:

| Dimensão | Média esperada | Justificativa |
|----------|---------------|---------------|
| Utilidade | 4.0 - 4.5 | O Copiloto resolve um problema real com dados reais do PNCP (100k contratos) |
| Usabilidade | 3.5 - 4.0 | Interface Streamlit é funcional mas não é uma UI profissional |
| Confiança | 3.5 - 4.0 | Acurácia 93,36% / AUC-ROC 90,83% + alvo observável + baselines aumentam credibilidade |
| Explicabilidade | 3.5 - 4.5 | Contrafactuais normativos são inovadores, mas termos técnicos (SHAP) persistem |
| Intenção de Uso | 3.5 - 4.0 | Freemium pode gerar resistência inicial |

---

## Status do Modelo (Atualização Sprint 10)

O modelo do Copiloto passou por remediação metodológica (Sprint 6), resultando em:
- **Acurácia:** 93,36% (antes: 98,27%)
- **AUC-ROC:** 90,83% (antes: 98,97%)
- **F1-Score:** 26,39% (devido ao desbalanceamento severo: 1,99% positivos)
- **Alvo:** eventos adversos observáveis (aditivos >10% ou ≥2 retificações)
- A queda nas métricas reflete a correção de tautologia, não degradação do modelo

Os avaliadores devem ser informados sobre otarget desbalanceado e as implicações para interpretação das métricas.

---

## Aprovação Ética

Este protocolo deve ser submetido ao comitê de ética da Fucape Business School antes da aplicação com avaliadores externos. O Termo de Consentimento Livre e Esclarecido (TCLE) deve ser assinado por todos os participantes.

---

## Referência

Bardin, L. (2011). *Análise de conteúdo*. Edições 70.
