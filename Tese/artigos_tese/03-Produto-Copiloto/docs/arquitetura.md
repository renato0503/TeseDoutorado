# Arquitetura do Copiloto (Design Science Research)

Este documento detalha o *pipeline* de dados e as engrenagens algoritmicas do Copiloto, fundamentado nas entregas academicas do Doutorado na Fucape Business School.

**Ultima atualizacao:** 18/07/2026 (Sprint 7 - Remediacao de Tautologia + 11 Features)

---

## 1. Visao Geral do Sistema

O sistema e construido sobre tres pilares de inteligencia:

1. **NLP Engine (Vetorizacao):** Transforma textos juridicos (editais/minutas) em features numericas via TF-IDF (500 features) e engenharia de features (7 variaveis: tamanho do texto, complexidade lexica, score tecnico, etc.).

2. **Motor de Anomalia (Nao Supervisionado):** Utiliza `Isolation Forest` (100 arvores, contamination=0.1) treinado na matriz TF-IDF de 15.000 objetos de contratos do PNCP. Identifica padroes atipicos que podem indicar direcionamento ou redacao irregular.

3. **Motor Preditivo (Supervisionado):** Utiliza `Random Forest` (100 arvores, max_depth=20) treinado em 100.000 contratos do PNCP com 11 features. Prediz o risco de fracasso contratual com 93.36% de acuracia e AUC-ROC de 90.83%.

## 2. Explainable AI (XAI) - O Diferencial

Modelos preditivos tradicionais retornam apenas um valor final (ex: "78% de risco"). No setor publico brasileiro, isso fere o principio da Motivacao. 
Por isso, a saida do Random Forest e interceptada pela biblioteca **SHAP (SHapley Additive exPlanations)**.

### Fluxo de Execucao SHAP:
- O `TreeExplainer` do SHAP calcula a contribuicao marginal de cada feature.
- As features com maior impacto SHAP sao destacadas no grafico de barras.
- O usuario visualiza quais caracteristicas do texto mais contribuiram para o score de risco.
- Explicacoes textuais em portugues traduzem os valores SHAP para linguagem acessivel.

### Features Utilizadas (Random Forest) - Modelo B (11 features):
| # | Feature | SHAP (%) | Descricao |
|---|---------|----------|-----------|
| 1 | `uf_encoded` | 20.91% | Unidade Federativa (27 estados) |
| 2 | `tipo_encoded` | 20.77% | Tipo de contrato (Empenho, Contrato, etc.) |
| 3 | `vigencia_log` | 14.40% | Log natural da duracao do contrato (dias) |
| 4 | `valor_log` | 11.31% | Log natural do valor global do contrato |
| 5 | `interacao_if_vigencia` | 9.98% | Interacao IF score x vigencia (modulacao de risco) |
| 6 | `objeto_palavras` | 6.33% | Numero total de palavras no objeto |
| 7 | `interacao_if_valor` | 6.89% | Interacao IF score x valor (modulacao de risco) |
| 8 | `complexidade_lexica` | 4.36% | Razao entre palavras unicas e total |
| 9 | `if_anomaly_score` | 4.33% | Escore de atipicidade do Isolation Forest |
| 10 | `if_is_anomaly` | 0.45% | Indicador binario de atipicidade |
| 11 | `score_tecnico` | 0.27% | Contagem de termos tecnicos (tecnologia, software, etc.) |

## 3. Integracao de Dados (PNCP)

A ferramenta foi treinada utilizando a base censitaria do PNCP (Portal Nacional de Contratacoes Publicas):

| Metrica | Valor |
|---------|-------|
| Contratos totais | 572.045 |
| Periodo | Set/2021 - Ago/2024 |
| Fornecedores unicos | 119.558 |
| Orgaos unicos | 6.567 |
| Valor total | R$ 491,9 bilhoes |
| Compras complexas (filtro NLP) | 5.687 (0.99%) |

### Pipeline de Dados:
```
PNCP Raw (CSV/JSON)
    -> consolidar_dados_pncp.py (572k contratos)
    -> identificar_compras_complexas.py (NLP: 5.687 complexas)
    -> enriquecer_cnpjs_apis.py (BrasilAPI: 200 CNPJs + proxies orgaos)
    -> train_models.py (TF-IDF + Isolation Forest + Random Forest + SHAP)
    -> model_loader.py (cache em memoria)
    -> Streamlit app (inferencia em tempo real)
```

## 4. Metodo Cientifico (Design Science Research)

O desenvolvimento segue o framework DSR de Peffers et al. (2007):

1. **Identificacao do Problema:** Assimetria informacional em compras complexas (inovacao, TI, ESG).
2. **Objetivos da Solucao:** Ferramenta XAI que audita editais e explica riscos.
3. **Design e Desenvolvimento:** MVP Streamlit com modelos Scikit-Learn + SHAP.
4. **Demonstracao:** App funcional com 2 modulos e dados reais do PNCP.
5. **Avaliacao:** Metricas honestas de acuracia (93.36%), AUC (90.83%), validadas por cross-validation.
6. **Comunicacao:** Artigos academicos, repositorio GitHub, defesa de tese.

## 5. Estrutura do Codigo

```
Tese/03-Produto-Copiloto/
├── app/
│   ├── app.py                     # Home: metricas, status modelos, navegacao
│   └── pages/
│       ├── 01_Avaliacao.py        # Modulo 1: analise com ML real
│       └── 02_Geracao.py          # Modulo 2: geracao de minutas XAI
├── models/
│   ├── preprocessor.py            # NLP: regex (16 padroes), TF-IDF, lacunas
│   ├── risk_engine.py             # Random Forest + SHAP + fallback
│   ├── anomaly_detector.py        # Isolation Forest + fallback
│   ├── xai_explainer.py           # Templates XAI (16 referencias)
│   ├── model_loader.py            # Cache singleton de modelos
│   ├── train_models.py            # Script de treinamento
│   └── saved/                     # Modelos treinados (.pkl + .json)
├── docs/
│   ├── arquitetura.md             # Este documento
│   ├── screencast_roteiro.md      # Roteiro para gravacao da demo
│   ├── slides_outline.md          # Estrutura dos slides de defesa
│   └── guia_banca.md              # Guia de uso para banca examinadora
├── requirements.txt
└── README.md
```

## 6. Deploy e Infraestrutura

O produto esta preparado para deploy automatico no Streamlit Cloud:

- `streamlit_app.py` na raiz do repositorio redireciona para `Tese/03-Produto-Copiloto/app/app.py`
- `.streamlit/config.toml` com tema e configuracao do servidor
- `requirements.txt` na raiz com todas as dependencias
- URL publica: `https://copiloto-algoritmico.streamlit.app`

## 7. Stack Tecnologico

| Camada | Tecnologia | Versao |
|--------|-----------|--------|
| Frontend | Streamlit | >=1.32.0 |
| ML Engine | Scikit-Learn | >=1.3.0 |
| XAI | SHAP | >=0.43.0 |
| Dados | Pandas, NumPy | >=2.0.0, >=1.24.0 |
| Graficos | Matplotlib | >=3.7.0 |
| Infra | Streamlit Cloud | Gratuito |

## 7. Referencias Academicas

- Williamson, O. E. (1985). *The Economic Institutions of Capitalism*.
- Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm.
- Peffers, K. et al. (2007). A design science research methodology.
- Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions (SHAP).
- Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest.
- Mazzucato, M. (2014). *The Entrepreneurial State*.
- Lei 14.133/2021. Nova Lei de Licitacoes e Contratos Administrativos.
- Lei Complementar 182/2021. Marco Legal das Startups.
- Lei 13.709/2018. Lei Geral de Protecao de Dados (LGPD).

---

*Para metricas detalhadas, execute `python models/train_models.py`.*
*Para rodar o app: `streamlit run app/app.py`*
