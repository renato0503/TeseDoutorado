# MATERIAL SUPLEMENTAR

Para garantir a total transparência e a reprodutibilidade empírica desta pesquisa, os dados consolidados, os códigos de programação e o artefato de software encontram-se disponibilizados publicamente.

## 1. Base de dados utilizada

O arquivo contendo a base de dados tratada e consolidada (após auditoria e saneamento), efetivamente carregada no ambiente de execução, pode ser acessado na íntegra através do seguinte link:

**https://raw.githubusercontent.com/renato0503/TeseDoutorado/main/Base_de_Dados_e_APIs/Raw_Data/Artigos_Quanti/18_Compliance_Algoritmico/dados_pncp_2024.csv**

A base de dados original foi obtida a partir do Portal Nacional de Contratações Públicas (PNCP) via repositório governamental dados.gov.br, referente ao exercício financeiro de 2024. Após saneamento — remoção de outliers extremos (valores superiores a R$ 1 bilhão), filtragem temporal para 2024 e correção de falsos positivos no dicionário de inovação — a base final contém **273.309 registros** de contratações públicas.

## 2. Scripts em Python

### 2.1. Script econométrico (Artigo Científico 1)
Script utilizado para tratamento final dos dados, estimação do modelo de regressão logística, execução do Random Forest e extração de métricas de performance:

**https://raw.githubusercontent.com/renato0503/TeseDoutorado/main/Base_de_Dados_e_APIs/Raw_Data/Artigos_Quanti/18_Compliance_Algoritmico/script_colab_artigo18.py**

Etapas: (i) carregamento e tratamento da base PNCP 2024; (ii) construção do escore ordinal de risco processual; (iii) estimação da regressão logística; (iv) Random Forest com validação cruzada estratificada; (v) extração de métricas (acurácia, F1 Macro, Kappa de Cohen); (vi) geração de tabelas e matrizes de confusão.

### 2.2. Artefato de software (Artigo Tecnológico 2 — Copiloto Algoritmico)
O código-fonte completo do Copiloto Algoritmico está disponível em:

**https://github.com/renato0503/TeseDoutorado/tree/main/Tese/artigos_tese/03-Produto-Copiloto**

Estrutura principal:
- `models/preprocessor.py` — NLP: regex (16 padrões), detecção de lacunas, scoring de conformidade
- `models/risk_engine.py` — Motor de risco: Random Forest + SHAP + contrafactuais
- `models/anomaly_detector.py` — Isolation Forest + TF-IDF para detecção de anomalias textuais
- `models/xai_explainer.py` — Templates XAI com fundamentos acadêmicos (Williamson, LGPD, LC 182)
- `models/train_models.py` — Script de treinamento (executar 1x para retreinar os modelos)

Modelos treinados (`.pkl`):
- TF-IDF Vectorizer (500 features, 15.000 objetos PNCP)
- Isolation Forest (100 árvores, contamination=0.1)
- Random Forest Classifier (100 árvores, 10 features, 100.000 contratos)
- SHAP TreeExplainer (explicabilidade em tempo real)
- Label Encoders (UF e tipo)
- Scaler e colunas de feature

## 3. Deploy em produção (Firebase)

O MVP com ML real está servido 100% no Firebase (plano Blaze), com front-end estático em Hosting + backend Python em Cloud Function (2nd gen):

**URL da aplicação:** https://comprapublica.web.app

**API de análise:** `POST https://comprapublica.web.app/api/analisar`
```json
{
  "texto": "texto da minuta do edital...",
  "valor": 1500000,
  "vigencia_dias": 720
}
```

**Arquitetura:**
```
[Navegador] -> modulo_avaliacao/index.html (Firebase Hosting)
    | POST /api/analisar
    v
[Cloud Function] analisar_minuta (Python 3.12)
    | carrega .pkl, executa: regex -> TF-IDF/IF -> RF -> SHAP
    v
[JSON] score, lacunas, recomendações, features_shap, contrafactuais, rf_proba
```

## 4. Calculadora interativa

Para simular o escore de risco processual de qualquer contratação, acesse a calculadora interativa:

**https://renato0503.github.io/TeseDoutorado/docs/calculadora_compliance.html**

---

## 5. Repro processamento PNCP (Filtro Semântico)

Script utilizado para identificar compras complexas no PNCP via dicionário de Inovação e Sustentabilidade:

**Script:** `scripts/identificar_compras_complexas.py`

**Resultado:** 5.687 Compras Complexas (0,99% de 572.045 contratos), 3.098 fornecedores únicos, 1.622 órgãos únicos.

---

## 6. Reprodutibilidade

Para executar o pipeline completo localmente:

```bash
# 1. Clone o repositório
git clone https://github.com/renato0503/TeseDoutorado.git
cd TeseDoutorado/Tese/artigos_tese/03-Produto-Copiloto

# 2. Instale dependências
pip install -r requirements.txt

# 3. (Opcional) Retreine os modelos
python models/train_models.py

# 4. Rode o app Streamlit (referência local)
streamlit run app/app.py

# 5. Ou rode a Cloud Function localmente (produção Firebase)
cd PubliCopilot/functions
pip install -r requirements.txt functions-framework
functions-framework --target analisar_minuta --port 8080
```

---

## 7. Notas metodológicas (Sprint 6 — remediação em andamento)

**Aviso:** As métricas de desempenho do modelo (`acuracia`, `AUC-ROC`, `F1`) estão em processo de remediação metodológica (Sprint 6). A versão atual do `metricas.json` reflete um modelo com target observável, mas ainda em avaliação quanto a data leakage. A nova versão (alvo ex-post puro, sem "vigência < 30 dias") terá métricas distintas e será publicada após retreinamento e validação.

**Mudança de título do Artigo 2:** O título está sendo revisado de "Copiloto Algorítmico NLP" para "Modelo Híbrido de Estimativa de Risco em Compras Públicas: DSR + XAI", refletindo que a camada de NLP (Isolation Forest + TF-IDF) contribui com ~4% da predição, funcionando como camada de triagem complementar, e não como motor principal.

---

**Pesquisador:** Renato de Oliveira Rosa  
**Programa:** Doutorado Profissional em Ciências Contábeis e Administração — Fucape Business School  
**Data:** Julho de 2026  
**Última atualização:** 18/07/2026
