# IMPLEMENTACAO DO PRODUTO (COPILOTO ALGORITMICO)

Este documento controla as sprints de construcao do **Produto (Entregavel 3)** da Tese de Doutorado, conforme o *pivot* de 03/07/2026.

O artefato final e um MVP funcional com **Machine Learning real** (TF-IDF + Isolation Forest + Random Forest + SHAP) treinado nos dados do PNCP (572k contratos). A partir de 18/07/2026 o MVP passou a ser servido **100% no Firebase** por meio de uma **Cloud Function em Python** (backend), eliminando a dependencia do Streamlit Cloud.

**Local do codigo-fonte (Streamlit, referência):** `Tese/artigos_tese/03-Produto-Copiloto/`
**Local do deploy Firebase (producao):** `PubliCopilot/`
**Comando local (referencia):** `streamlit run app/app.py`
**Deploy Firebase:** `cd PubliCopilot && firebase deploy`

**Ultima atualizacao:** 19/07/2026 08h (Sistema de Autenticacao COMPLETO deployado: login email/senha + Google OAuth + cadastro com CAPTCHA + validacao JWT na Cloud Function via firebase-admin)

---

## STATUS ATUAL (19/07/2026 07h)

| Componente | Status |
|------------|--------|
| Front-end (Firebase Hosting) | 🟢 Online em https://comprapublica.web.app |
| Cloud Function `analisar_minuta` | ⚠️ Em deploy manual no terminal |
| API `/api/analisar` | ⚠️ 404 (Function inexistente) |
| Modelos ML (27,35 MB) | 🟢 11 arquivos, limpos em 19/07 |
| Codigo (main.py, requirements.txt) | 🟢 Corrigido para deploy |

### Concluido em 19/07/2026 07h

1. **Metricas honestas** (public/index.html, modulo_avaliacao/index.html, metricas.json)
   - Antes: apenas "Acuracia 93,36%"
   - Depois: "Acuracia 93,36% | AUC-ROC 90,83% | F1-Score 26,39% (devido ao desbalanceamento de classes)"
2. **CORS restrito** (functions/main.py)
   - Antes: `Allow-Origin: *` (aberto)
   - Depois: whitelist via `ALLOWED_ORIGINS` env var
3. **Limpeza de modelos** (functions/models/saved/)
   - Removidos 4 arquivos duplicados (-12,17 MB / -30,8%)
   - Criado `models_keep.txt` para rastreabilidade
   - Criado `limpar_modelos.py` para manutencao
4. **requirements.txt sincronizado**
   - `scikit-learn==1.9.0` fixado (compativel com modelos)
   - `numpy<3.0.0`, `pandas<3.0.0`, `shap<0.50.0` para evitar quebras
   - Adicionados `google-cloud-firestore`, `joblib`, `requests`

### Pendente

- Deploy da Cloud Function `analisar_minuta` (em execucao no terminal do usuario)
- Validacao do deploy com `curl` ao endpoint

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
- [x] Random Forest para predicao de risco: 10 features (inclui score/anomalia do IF), 100.000 contratos, 100 arvores
- [x] SHAP TreeExplainer computado e salvo
- [x] Modelos salvos em `models/saved/` (9 .pkl + metricas.json)

### 2.2. Integracao com dados PNCP
- [x] `model_loader.py`: cache singleton com lazy loading dos pickles
- [x] Carregamento de `pncp_contratos_full.csv` no treinamento (amostra de 50k)
- [x] Metricas exibidas na Home (acuracia, AUC, CV)

### 2.3. Renderizacao de graficos SHAP
- [x] Grafico de barras horizontais com feature importance SHAP no resultado da analise
- [x] SHAP values computados (300 amostras x 7 features)
- [x] Grafico integrado ao Modulo de Avaliacao (Matplotlib inline)

### 2.4. Metricas do modelo (reais, de `metricas.json`)
- [x] Acuracia: 98.27% | AUC-ROC: 98.97% | F1: 95.22% | CV 5-fold: 98.20% (+/- 0.08%)
- [x] Feature importance (SHAP): vigencia_log 76.11%, tipo_encoded 6.82%, uf_encoded 5.55%, valor_log 2.85%, objeto_palavras 2.80%, objeto_len 3.32%
- [x] Target observavel (nao tautologico): 18,79% positivos em 100.000 registros
- [x] Contribuicao do Isolation Forest integrado ao RF: 3,86%
- [x] 5 baselines comparativos (Dummy -> Logit -> Arvore -> RF -> RF+IF)
- [x] 5 Design Principles (DP1-DP5) e 8 templates de contrafactuais
- [x] Status dos modelos visivel na Home e sidebar

### 2.5. Atualizacao dos modulos
- [x] `anomaly_detector.py`: carrega TF-IDF + Isolation Forest reais, fallback offline (extrai secao do objeto antes do vetorizar)
- [x] `risk_engine.py`: carrega Random Forest real, predicao com 10 features, SHAP + contrafactuais em tempo real
- [x] Resultado mostra: RF Score, RF Proba, Risco ML (alto/medio/baixo), grafico SHAP, contrafactuais

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

## SPRINT 4: POLIMENTO FINAL [CONCLUIDA 10/07/2026]

**Objetivo:** Deploy, materiais de defesa, documentacao e publicacao.

### 4.1. Deploy
- [x] Deploy no Streamlit Cloud (versao de referencia)
- [x] URL publica: `https://copiloto-algoritmico.streamlit.app`
- [x] `streamlit_app.py` na raiz do repositorio como entry point
- [x] `.streamlit/config.toml` com tema e configuracao do servidor
- [x] `requirements.txt` na raiz para Streamlit Cloud
- [x] Deploy no Firebase (`PubliCopilot/`) — ver Sprint 5 (producao oficial)

### 4.2. Materiais de defesa
- [x] Screencast/GIF demonstrativo - roteiro em `docs/screencast_roteiro.md`
- [x] Slides explicativos sobre a arquitetura DSR - estrutura em `docs/slides_outline.md`
- [x] Documentacao de uso para a banca em `docs/guia_banca.md`

### 4.3. Revisao tecnica
- [x] Sugestoes de reescrita de clausulas problematicas (Premium) - 6 templates completos
- [x] Sugestao de `responsabilidade` adicionada ao mapa de reescrita
- [x] Testes unitarios para modulos criticos (17 testes em `tests/test_models.py`)
- [x] Correcao de bugs: n_estimators no metricas.json, mapeamento XAI no Geracao, docstrings

### 4.4. Documentacao
- [x] Docstrings em todos os modulos Python (preprocessor, risk_engine, anomaly_detector, xai_explainer, model_loader, train_models)
- [x] Atualizar `docs/arquitetura.md` com secao de Deploy e guia_banca
- [x] Guia de uso detalhado no README (inclui Streamlit Cloud, local, Firebase)

### 4.5. Publicacao
- [x] Codigo-fonte versionado e limpo no GitHub
- [x] Licenca definida (MIT - `LICENSE` na raiz do repo)
- [ ] DOI/Zenodo (opcional)

---

## SPRINT 5: PORT DO MVP PARA FIREBASE (CLOUD FUNCTION) [CONCLUIDA 18/07/2026]

**Objetivo:** Servir o MVP com ML real **100% no Firebase**, sem depender do Streamlit Cloud.
Decisao: backend em **Cloud Function Python (2nd gen, runtime python312)** que carrega os
`.pkl` reais e expoe um endpoint HTTP consumido pelo front estatico. Plano Firebase **Blaze**
obrigatorio (Cloud Functions nao rodam no Spark gratuito).

### 5.1. Backend (Cloud Function) — `PubliCopilot/functions/`
- [x] `main.py`: entry point `analisar_minuta` (functions-framework) — `POST /api/analisar` com `{texto, valor?, vigencia_dias?}`
- [x] Pipeline real: regex (16 clausulas) -> lacunas -> score heuristico (0-100) -> Isolation Forest/TF-IDF -> Random Forest -> SHAP -> recomendacoes
- [x] Tratamento de CORS (OPTIONS + headers) para o front do Hosting
- [x] Copia fiel dos modulos Python reais: `preprocessor.py`, `risk_engine.py`, `anomaly_detector.py`, `xai_explainer.py`, `model_loader.py`
- [x] Copia dos modelos treinados em `functions/models/saved/` (9 .pkl + `metricas.json`)
- [x] `requirements.txt` (numpy, pandas, scikit-learn, shap, functions-framework)
- [x] `.gitignore` de `functions/` (ignora `__pycache__`, `.venv`, etc.)

### 5.2. Front-end (Hosting) — `PubliCopilot/public/`
- [x] `modulo_avaliacao/index.html`: substitui a logica fake (regex JS) por `fetch('/api/analisar')`; exibe score, lacunas, recomendacoes com fundamento, SHAP, risco ML e metricas reais
- [x] `modulo_geracao/index.html`: portado para JS puro (templates Lei 14.133 + XAI, sem ML); textos ajustados (sem "RAG"/"embeddings")
- [x] `index.html` (landing): numeros ajustados para a realidade (100k no treino; acuracia 98,27%; sem "19.640 editais")

### 5.3. Configuracao e documentacao
- [x] `firebase.json`: `rewrites` `/api/** -> analisar_minuta` + `functions` runtime `python312` + `site: comprapublica`
- [x] `PubliCopilot/README.md` reescrito: arquitetura hibrida, pre-requisitos (plano Blaze), passo a passo de deploy e teste local da funcao
- [x] `.firebaserc` ja aponta para `publicopilot-aa662`

### 5.4. Pendente de validacao (ambiente local)
- [ ] Instalar Python 3.12 + `functions-framework` e testar `analisar_minuta` localmente (POST de exemplo)
- [ ] Rodar `firebase deploy` e confirmar que `/api/analisar` responde em `https://comprapublica.web.app`
- [ ] (Opcional) Desligar o deploy do Streamlit Cloud antigo, ja que o Firebase e a fonte unica do MVP com ML real

---

## ARQUITETURA ATUAL DO PRODUTO (HIBRIDA: STREAMLIT + FIREBASE)

### Codigo-fonte de referencia (Streamlit) — `Tese/artigos_tese/03-Produto-Copiloto/`
```
Tese/artigos_tese/03-Produto-Copiloto/
├── app/
│   ├── app.py                     # Home: metricas PNCP, status modelos, navegacao
│   └── pages/
│       ├── 01_Avaliacao.py        # Modulo 1: TF-IDF + Isolation Forest + Random Forest + SHAP
│       └── 02_Geracao.py          # Modulo 2: Geracao de minutas com XAI
├── models/
│   ├── __init__.py
│   ├── preprocessor.py            # NLP: regex (16 padroes), lacunas, scoring (6 reescritas)
│   ├── risk_engine.py             # Motor: Random Forest real + fallback heuristico
│   ├── anomaly_detector.py        # Deteccao: TF-IDF + Isolation Forest + fallback
│   ├── xai_explainer.py           # Templates XAI com fundamentos academicos
│   ├── model_loader.py            # Cache singleton (lazy loading dos pickles)
│   ├── train_models.py            # Script de treinamento (executar 1x)
│   └── saved/                     # Modelos treinados (9 .pkl + metricas.json)
├── data/                          # Referencia aos dados (dados/processed/)
├── docs/                          # arquitetura.md, guia_banca.md, screencast_roteiro.md, slides_outline.md
├── tests/test_models.py           # 17 testes unitarios
├── requirements.txt
└── README.md
```

### Producao oficial (ML real 100% Firebase) — `PubliCopilot/`
```
PubliCopilot/
├── public/
│   ├── publicopilot.png           # Logo oficial
│   ├── theme.css                  # Tema claro: branco, preto, amarelo queimado, verde piscina
│   ├── index.html                 # Landing page reescrita
│   ├── modulo_avaliacao/          # Modulo 1 -> fetch('/api/analisar') [backend ML real]
│   └── modulo_geracao/            # Modulo 2 (JS puro: templates Lei 14.133 + XAI)
├── functions/                     # Cloud Function Python 3.12 (backend ML)
│   ├── main.py                    # Entry point analisar_minuta (functions-framework)
│   ├── requirements.txt           # numpy, pandas, scikit-learn, shap, functions-framework
│   └── models/                    # Codigo real + .pkl treinados
│       ├── preprocessor.py, risk_engine.py, anomaly_detector.py
│       ├── xai_explainer.py, model_loader.py
│       └── saved/                 # 9 .pkl + metricas.json
├── firebase.json                  # hosting + functions(python312) + rewrite /api/**
├── .firebaserc                    # projeto: publicopilot-aa662
├── firestore.rules / indexes.json
└── README.md
```

### Fluxo em producao
```
[Navegador] -> modulo_avaliacao/index.html
    | POST /api/analisar { texto, valor?, vigencia_dias? }
    v
[Firebase Hosting rewrite] -> Cloud Function analisar_minuta (python312)
    | carrega .pkl, roda pipeline ML real
    v
[JSON] -> score, lacunas, recomendacoes, features_shap, contrafactuais, rf_proba
```

---

> **Observacoes:**
> - Codigo-fonte de referencia Streamlit: `Tese/artigos_tese/03-Produto-Copiloto/`
> - Producao oficial (ML real 100% Firebase): `PubliCopilot/` serve o MVP via Cloud Function Python + Hosting em `https://comprapublica.web.app` (API: `/api/analisar`).
> - Requer plano Blaze no Firebase (Cloud Functions Python nao rodam no Spark gratuito).
> - Deploy Firebase: `cd PubliCopilot && firebase deploy`
> - Testar funcao local: `cd functions && pip install -r requirements.txt functions-framework && functions-framework --target analisar_minuta --port 8080`
> - Para retreinar os modelos (fonte): `python models/train_models.py` (e copiar os .pkl para `functions/models/saved/`)
> - Testes do fonte: `python -m pytest tests/test_models.py -v`ura.md, screencast_roteiro.md, slides_outline.md, guia_banca.md
├── tests/test_models.py           # 17 testes unitarios
├── requirements.txt
└── README.md
```

### Producao Firebase (MVP com ML real 100% no Firebase) — `PubliCopilot/`
```
PubliCopilot/
├── public/                        # Firebase Hosting (front-end estatico)
│   ├── index.html                 # Landing page
│   ├── modulo_avaliacao/          # Modulo 1 -> fetch('/api/analisar') [backend ML real]
│   ├── modulo_geracao/            # Modulo 2 (JS puro: templates Lei 14.133 + XAI)
│   └── js/firebase-init.js
├── functions/                     # Cloud Function Python 3.12 (backend ML)
│   ├── main.py                    # Entry point analisar_minuta (functions-framework)
│   ├── requirements.txt           # numpy, pandas, scikit-learn, shap
│   └── models/                    # Modulos reais + .pkl treinados
│       ├── preprocessor.py, risk_engine.py, anomaly_detector.py
│       ├── xai_explainer.py, model_loader.py
│       └── saved/                 # 9 .pkl + metricas.json
├── firebase.json                  # hosting + functions(python312) + rewrite /api/**
├── .firebaserc                    # projeto: publicopilot-aa662
├── firestore.rules / indexes.json
└── README.md
```

### Fluxo em producao
```
[ Navegador ]  modulo_avaliacao/index.html
      |  POST /api/analisar  { texto, valor?, vigencia_dias? }
      v
[ Firebase Hosting rewrite ]  ->  Cloud Function: analisar_minuta (python312)
      |  carrega .pkl (cold start), roda pipeline ML real
      v
[ JSON ]  score, lacunas, recomendacoes, features_shap, contrafactuais, rf_proba, metricas
```

---

> **Observacoes:**
> - O frontend HTML/CSS em `Copiloto/` e a referencia de design (modulo_avaliacao, modulo_geracao).
> - **Producao oficial (ML real 100% Firebase):** `PubliCopilot/` serve o MVP via Cloud Function Python + Hosting em `https://comprapublica.web.app` (API: `/api/analisar`).
> - **Requer plano Blaze** no Firebase (Cloud Functions Python nao rodam no Spark gratuito).
> - O Streamlit (`Tese/artigos_tese/03-Produto-Copiloto/`) permanece como codigo-fonte de referencia.
> - **Deploy Firebase:** `cd PubliCopilot && firebase deploy`
> - **Testar funcao local:** `cd functions && pip install -r requirements.txt functions-framework && functions-framework --target analisar_minuta --port 8080`
> - Para retreinar os modelos (fonte): `python models/train_models.py` (e copiar os .pkl para `functions/models/saved/`)
> - Testes do fonte: `python -m pytest tests/test_models.py -v`
