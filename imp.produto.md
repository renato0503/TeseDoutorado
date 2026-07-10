# IMPLEMENTACAO DO PRODUTO (COPILOTO ALGORITMICO)

Este documento controla as sprints de construcao do **Produto (Entregavel 3)** da Tese de Doutorado, conforme o *pivot* de 03/07/2026.

O artefato final e um MVP funcional em **Streamlit** ancorado nos dados reais do PNCP (572k contratos) e com modelos de Machine Learning treinados.

**Local:** `Tese/03-Produto-Copiloto/`
**Comando:** `streamlit run app/app.py`

---

## SPRINT 1: FUNDACAO DO PRODUTO (MVP Core) [CONCLUIDA 10/07/2026]

**Objetivo:** Estruturar o repositorio, criar o app Streamlit base com navegacao e os dois modulos principais.

### 1.1. Estrutura de diretorios
- [x] Criar `Tese/03-Produto-Copiloto/app/` (app principal)
- [x] Criar `Tese/03-Produto-Copiloto/models/` (motor de ML/NLP)
- [x] Criar `Tese/03-Produto-Copiloto/data/` (referencias e cache)
- [x] Criar `requirements.txt`
- [x] Atualizar `README.md`

### 1.2. App principal (app.py)
- [x] Configurar Streamlit com layout wide, titulo e sidebar
- [x] Implementar navegacao entre modulos (Home, Avaliacao, Geracao)
- [x] Pagina Home com metricas do PNCP e descricao do produto
- [x] Integrar CSS customizado (aproveitar design system do Copiloto)

### 1.3. Motor de NLP/ML (models/)
- [x] `preprocessor.py`: limpeza de texto, regex clausulas (16 padroes), deteccao de lacunas, scoring
- [x] `risk_engine.py`: motor de scoring heuristico + recomendacoes com fundamentos academicos
- [x] `anomaly_detector.py`: Isolation Forest wrapper com fallback offline
- [x] `xai_explainer.py`: templates XAI com referencias (Williamson, LGPD, LC 182, Jensen)

### 1.4. Modulo de Avaliacao (`01_Avaliacao.py`)
- [x] Textarea + file upload (.txt)
- [x] Exemplos carregaveis (Edital de TI, Contrato de Inovacao, Licitacao Sustentavel)
- [x] Analise de clausulas por regex
- [x] Deteccao de lacunas (alta/media/baixa)
- [x] Score de conformidade (0-100%) com circulo colorido
- [x] Recomendacoes com fundamento juridico/academico

### 1.5. Modulo de Geracao (`02_Geracao.py`)
- [x] Formulario com abas (Dados Basicos, Objeto, Clausulas Juridicas)
- [x] Geracao de minuta completa com clausulas pre-configuradas
- [x] Clausulas com justificativas XAI (Williamson, Jensen, LGPD)
- [x] Base de clausulas por tipo (TI, Inovacao, Sustentabilidade)
- [x] Download da minuta (.txt)

---

## SPRINT 2: ML REAL E DADOS PNCP [CONCLUIDA 10/07/2026]

**Objetivo:** Substituir regras heuristicas por modelos de Machine Learning treinados nos dados reais do PNCP.

### 2.1. Treinamento dos modelos
- [x] `train_models.py`: script unificado de treinamento
- [x] Isolation Forest sobre TF-IDF de 15.000 objetos de contratos (500 features, contamination=0.1)
- [x] Random Forest para predicao de risco: 7 features, 50.000 contratos, 100 arvores
- [x] SHAP TreeExplainer computado e salvo
- [x] Modelos salvos em `models/saved/` (7 arquivos: 6 .pkl + metricas.json)

### 2.2. Integracao com dados PNCP
- [x] `model_loader.py`: cache singleton com lazy loading dos pickles
- [x] Carregamento de `pncp_contratos_full.csv` no treinamento (amostra de 50k)
- [x] Metricas exibidas na Home (acuracia, AUC, CV)

### 2.3. Renderizacao de graficos SHAP
- [x] Grafico de barras horizontais com feature importance SHAP no resultado da analise
- [x] SHAP values computados (300 amostras x 7 features)
- [x] Grafico integrado ao Modulo de Avaliacao (Matplotlib inline)

### 2.4. Metricas do modelo
- [x] Acuracia: 99.13% | AUC-ROC: 99.97% | CV 5-fold: 98.77% (+/- 0.10%)
- [x] Feature importance: valor_log 80.52%, complexidade_lexica 8.59%, score_tecnico 4.47%, tipo_encoded 3.09%
- [x] Status dos modelos visivel na Home e sidebar

### 2.5. Atualizacao dos modulos
- [x] `anomaly_detector.py`: carrega TF-IDF + Isolation Forest reais, fallback offline
- [x] `risk_engine.py`: carrega Random Forest real, predicao com 7 features, SHAP em tempo real
- [x] Resultado mostra: RF Score, RF Proba, Risco ML (alto/medio/baixo), grafico SHAP

---

## SPRINT 3: EXPERIENCIA DO USUARIO E FREEMIUM [CONCLUIDA 10/07/2026]

**Objetivo:** Modelo Freemium, link de consultoria, exportacao de relatorio.

### 3.1. Modelo Freemium
- [x] Limite de 3 analises/geracoes por sessao na versao gratuita
- [x] Tela de upgrade para Premium com features destacadas
- [x] Link "Fale com a Consultoria Renato Rosa" em todas as paginas
- [x] Sidebar com status do plano e progresso de uso

### 3.2. Interface Premium
- [x] Exportacao de relatorio (.txt) disponivel na versao premium
- [x] Historico de uso via `st.session_state`
- [x] Sidebar com metricas do modelo (acuracia, AUC, CV) no modulo de avaliacao

### 3.3. Status visivel do sistema
- [x] Home mostra: modelos carregados (ON/OFF), acuracia em tempo real
- [x] Sidebar do modulo de avaliacao: TF-IDF OK, Isolation Forest OK, ML Treinado SIM/NAO
- [x] Badge "ML Treinado (PNCP)" no header

---

## SPRINT 4: POLIMENTO FINAL [PENDENTE]

**Objetivo:** Deploy, materiais de defesa, documentacao e publicacao.

### 4.1. Deploy
- [ ] Deploy no Streamlit Cloud (gratuito)
- [ ] URL publica: `https://copiloto-algoritmico.streamlit.app`
- [ ] Configurar GitHub Actions (opcional)

### 4.2. Materiais de defesa
- [ ] Screencast/GIF demonstrativo (2-3 min) operando o Copiloto
- [ ] Slides explicativos sobre a arquitetura DSR
- [ ] Documentacao de uso para a banca

### 4.3. Revisao tecnica
- [ ] Sugestoes de reescrita de clausulas problematicas (Premium)
- [ ] Testes unitarios para modulos criticos
- [ ] Correcao de bugs visuais e funcionais

### 4.4. Documentacao
- [ ] Docstrings em todos os modulos Python
- [ ] Atualizar `docs/arquitetura.md`
- [ ] Guia de uso detalhado no README

### 4.5. Publicacao
- [ ] Codigo-fonte versionado e limpo no GitHub
- [ ] Licenca definida
- [ ] DOI/Zenodo (opcional)

---

## ARQUITETURA ATUAL DO PRODUTO

```
Tese/03-Produto-Copiloto/
├── app/
│   ├── app.py                     # Home: metricas PNCP, status modelos, navegacao
│   └── pages/
│       ├── 01_Avaliacao.py        # Modulo 1: TF-IDF + Isolation Forest + Random Forest + SHAP
│       └── 02_Geracao.py          # Modulo 2: Geracao de minutas com XAI
├── models/
│   ├── __init__.py
│   ├── preprocessor.py            # NLP: regex (16 padroes), lacunas, scoring
│   ├── risk_engine.py             # Motor: Random Forest real + fallback heuristico
│   ├── anomaly_detector.py        # Deteccao: TF-IDF + Isolation Forest + fallback
│   ├── xai_explainer.py           # Templates XAI com fundamentos academicos
│   ├── model_loader.py            # Cache singleton (lazy loading dos pickles)
│   ├── train_models.py            # Script de treinamento (executar 1x)
│   └── saved/                     # Modelos treinados (gerados por train_models.py)
│       ├── tfidf_vectorizer.pkl
│       ├── isolation_forest.pkl
│       ├── random_forest.pkl
│       ├── shap_explainer.pkl
│       ├── shap_background.pkl
│       ├── shap_values_sample.pkl
│       ├── label_encoder_uf.pkl
│       ├── label_encoder_tipo.pkl
│       ├── feature_columns.pkl
│       └── metricas.json
├── data/                          # Referencia aos dados (dados/processed/)
├── docs/
│   └── arquitetura.md             # Arquitetura DSR detalhada
├── requirements.txt
└── README.md
```

---

> **Observacoes:**
> - O frontend HTML/CSS em `Copiloto/` e a referencia de design (modulo_avaliacao, modulo_geracao).
> - O deploy no Firebase (`PubliCopilot/`) permanece como versao estatica em `comprapublica.web.app`.
> - O Streamlit e a plataforma oficial do produto (backend Python real com ML).
> - Para retreinar os modelos: `python models/train_models.py`
> - Para rodar: `streamlit run app/app.py`
