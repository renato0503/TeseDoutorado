# Guia de Uso do Copiloto Algoritmico para a Banca Examinadora

**Tese:** Copiloto Algoritmico para Compras Publicas Complexas
**Autor:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Doutorado em Contabilidade - Fucape Business School

---

## 1. Acesso

| Opcao | URL | Descricao |
|-------|-----|-----------|
| Firebase (producao) | `https://publicopilot.web.app` | MVP funcional (recomendado) — ML + IA generativa |
| Local (referencia academica) | `streamlit run app/app.py` | Clone do GitHub |

## 2. Funcionalidades

### Home
- Metricas PNCP: 572.045 contratos, 5.687 compras complexas
- Status dos modelos ML (Isolation Forest, Random Forest, SHAP)
- Pipeline XAI explicado em 3 passos

### Modulo 1: Avaliacao de Minutas
1. Cole o texto ou carregue exemplo
2. Pipeline: TF-IDF + Isolation Forest + Random Forest + SHAP
3. Saidas: score 0-100%, lacunas, recomendacoes, grafico SHAP

### Modulo 2: Geracao de Editais
1. Preencha orgao, UASG, modalidade, tipo (TI/Inovacao/Sustentavel)
2. Minuta completa com clausulas pre-configuradas
3. Cada clausula com justificativa XAI (Williamson, LGPD, LC 182)
4. Download .txt

## 3. Modelo Freemium

| Recurso | Gratuito | Premium |
|---------|----------|---------|
| Analises/sessao | 3 | Ilimitado |
| Score + Random Forest + SHAP | Sim | Sim |
| Sugestao de reescrita | Nao | Sim |
| Relatorio auditoria (.txt) | Nao | Sim |

## 4. Arquitetura Resumida

```
Usuario -> Firebase Hosting
  -> preprocessor.py (NLP, 16 regex)
  -> anomaly_detector.py (TF-IDF + Isolation Forest, 15k objetos PNCP)
  -> risk_engine.py (Random Forest 7 features, 50k contratos, acc 99.13%)
  -> SHAP TreeExplainer (explicabilidade em tempo real)
  -> xai_explainer.py (templates XAI com referencias academicas)
```

## 5. Modelos Treinados

| Modelo | Amostra | Metricas |
|--------|---------|----------|
| TF-IDF | 15.000 objetos | 500 features, ngrams (1,2) |
| Isolation Forest | 15.000 objetos | 100 arvores, contamination=0.1 |
| Random Forest | 50.000 contratos | acc=99.13%, AUC=99.97%, CV=98.77% |
| SHAP | 500 background | TreeExplainer, 7 features |

## 6. Metodo Cientifico (DSR)

Peffers et al. (2007) - 6 etapas:
1. Identificacao do problema (assimetria informacional)
2. Objetivos da solucao (XAI para compras complexas)
3. Design e desenvolvimento (MVP Firebase + Scikit-Learn)
4. Demonstracao (app funcional com dados reais PNCP)
5. Avaliacao (metricas ML: acc 99.13%, AUC 99.97%)
6. Comunicacao (artigos, repositorio, defesa)

## 7. Referencias Academicas

- Williamson (1985) - Custos de Transacao
- Jensen & Meckling (1976) - Teoria da Agencia
- Akerlof (1970) - Selecao Adversa
- Lundberg & Lee (2017) - SHAP
- Peffers et al. (2007) - DSR
- Liu et al. (2008) - Isolation Forest
- Lei 14.133/2021, LC 182/2021, LGPD

---

**Contato:** Renato Rosa | github.com/renato0503/TeseDoutorado
