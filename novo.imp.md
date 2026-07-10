# NOVO IMPLEMENTACAO GERAL (PIVOT 03/07/2026)

Este documento centraliza o **novo planejamento e controle de execucao** da Tese de Doutorado em Contabilidade na Fucape Business School, apos o *pivot* estrutural exigido pelo orientador (Prof. Dr. Olavo Venturim Caldas).

O modelo "25 Artigos Empiricos" e a narrativa "Apagao das Canetas" foram oficialmente substituidos pelo **Modelo Fucape de 3 Entregaveis**, focado em **Compras Complexas** e reducao da assimetria informacional, ancorado no paradigma de Design Science Research (DSR).

**Ultima atualizacao:** 10/07/2026

---

## 1. A NOVA ESTRUTURA (3 ENTREGAVEIS)

A tese agora e composta estritamente pelas seguintes entregas:

1. **Artigo Cientifico 1 (Diagnostico Empirico):** Modelagem do PNCP para separar compras normais de complexas (tecnologia, inovacao, sustentabilidade). Foco em mapear as Unidades Compradoras e os determinantes de sucesso vs fracasso.
2. **Artigo Tecnologico 2 (A Ferramenta):** Relato da construcao metodologica do "Copiloto Algoritmico". Aborda DSR, aprendizado nao supervisionado (Isolation Forest) e modelos explicaveis (XAI/SHAP) para accountability e transparencia.
3. **O Produto (Copiloto):** Repositorio do codigo-fonte (hospedado no GitHub) contendo a ferramenta, com modelo de monetizacao/acesso Freemium que serve como esteira (lead) para a consultoria privada.

---

## 2. O QUE JA FIZEMOS (PROGRESSO ATUAL)

### 2.1. Reestruturacao Arquitetural
- O documento original foi arquivado em `Implementation.legado/imp.legado.md`.
- Criada a arvore de pastas padronizada:
  - `Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/` (Raw_Data, dados, Bibliografia, HTML esqueleto)
  - `Tese/artigos_tese/02-Artigo-Tecnologico-Copiloto/` (estrutura analoga, HTML esqueleto)
  - `Tese/03-Produto-Copiloto/` (artefato tecnologico completo)

### 2.2. Engenharia de Dados (Artigo Cientifico 1)
- **Filtro Semantico (NLP):** Script `scripts/identificar_compras_complexas.py` aplicou dicionario de Inovacao e Sustentabilidade sobre 572.045 contratos do PNCP.
  - **Resultado:** 5.687 Compras Complexas (0.99%), 3.098 fornecedores unicos, 1.622 orgaos unicos.
- **Enriquecimento (BrasilAPI):** Script `scripts/enriquecer_cnpjs_apis.py` extraiu dados de 200 CNPJs (Capital Social, Porte, Natureza, CNAE).
  - Gerada base `orgaos_proxies.csv` (Proxy de Porte/Orcamento por orgao).
- **Formatacao Bibliografica:** Todas as referencias em **APA 7 Edicao**. Referencias estruturais (Williamson, Mazzucato, Peffers, Lundberg) injetadas nos HTMLs.

### 2.3. Produto (Copiloto Algoritmico) - CONCLUIDO
- **MVP Streamlit** construido em `Tese/03-Produto-Copiloto/`:
  - `app/app.py` — Home com metricas PNCP, status dos modelos ML, navegacao
  - `app/pages/01_Avaliacao.py` — Modulo de Avaliacao de Minutas com ML real
  - `app/pages/02_Geracao.py` — Modulo de Geracao de Editais com XAI
- **Modelos de ML treinados** em `models/saved/`:
  - TF-IDF Vectorizer (500 features, 15.000 objetos PNCP)
  - Isolation Forest (deteccao de anomalias contratuais)
  - Random Forest (7 features, 50.000 contratos, acuracia 99.13%, AUC 99.97%)
  - SHAP TreeExplainer (explicabilidade em tempo real)
- **Modelo Freemium** implementado:
  - Limite de 3 analises gratuitas por sessao
  - Tela de upgrade para Premium
  - Link Consultoria Renato Rosa em todas as paginas
- **Arquitetura documentada** em `Tese/03-Produto-Copiloto/docs/arquitetura.md`
- **Sprints documentadas** em `imp.produto.md` (Sprints 1-3 concluidas, Sprint 4 pendente)
- Versao estatica de demonstracao em `PubliCopilot/` (Firebase: `comprapublica.web.app`)
- Prototipos HTML de referencia em `Copiloto/modulo_avaliacao/` e `Copiloto/modulo_geracao/`

### 2.4. Artigo Tecnologico 2 (Copiloto DSR)
- **Motor de ML executado:**
  - Isolation Forest treinado sobre matriz TF-IDF do corpus de objetos de contratos
  - Random Forest treinado com features de risco (valor, complexidade lexica, score tecnico, UF, tipo)
- **XAI/SHAP renderizado:**
  - Graficos de feature importance SHAP gerados e embutidos no app Streamlit
  - Explicacoes textuais baseadas em teoria (Williamson, Teoria da Agencia, LGPD, LC 182/2021)

---

## 3. O QUE FALTA FAZER (BACKLOG ATUAL)

### 3.1. Artigo Cientifico 1 (Diagnostico Empirico)
- **[ ] Execucao da Modelagem Estatistica:**
  - Codificar script Python unindo 5.687 contratos complexos aos dados enriquecidos (BrasilAPI/Proxies)
  - Rodar Regressao Logistica (Logit) e/ou Random Forest para isolar variaveis preditoras
- **[ ] Geracao de Tabelas e Graficos:**
  - Matriz de Correlacao das covariaveis
  - Forest Plot com significancia estatistica (Porte do Orgao, Capital da Empresa)
- **[ ] Redacao da Discussao e Conclusao:**
  - Interpretar coeficientes dentro do HTML do artigo
  - Secao de Limitacoes e Recomendacoes para Estudos Futuros

### 3.2. Artigo Tecnologico 2 (Copiloto DSR)
- **[ ] Redacao da Secao de Avaliacao (Evaluation):**
  - Detalhamento das metricas de Acuracia, F1-Score e Recall no HTML
  - Documentar testes de latencia (tempo IA vs tempo humano)
- **[ ] Embutir graficos SHAP no HTML do Artigo 2**
  - Waterfall plots e Force plots comprovando interpretabilidade

### 3.3. O Produto (Copiloto) — Sprint 4
- **[ ] Deploy no Streamlit Cloud**
- **[ ] Screencast/GIF demonstrativo (2-3 min) para a defesa**
- **[ ] Slides explicativos sobre a arquitetura DSR**
- **[ ] Revisao final, testes, documentacao**

---

> **Diretriz Maxima do Orientador:** O objeto principal agora e "entender o que e a compra complexa no mundo real" e fornecer uma solucao baseada em ciencia (literatura) para mitigar a opacidade/assimetria informacional, abolindo ataques focados unicamente na "omissao" do gestor.
