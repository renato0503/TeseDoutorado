# 🏗️ Arquitetura do Copiloto (Design Science Research)

Este documento detalha o *pipeline* de dados e as engrenagens algorítmicas do Copiloto, fundamentado nas entregas acadêmicas do Doutorado na Fucape.

## 1. Visão Geral do Sistema

O sistema é construído sobre três pilares de inteligência:
1. **NLP Engine (Vetorização):** Transforma textos jurídicos (editais) em matrizes numéricas (TF-IDF).
2. **Motor de Anomalia (Não Supervisionado):** Utiliza `Isolation Forest` para identificar editais com escopo "direcionado" ou fora do padrão do PNCP.
3. **Motor Preditivo (Supervisionado):** Utiliza `Random Forest` treinado em bases de jurisprudência e impugnações para prever o risco matemático de fracasso.

## 2. Explainable AI (XAI) - O Diferencial
Modelos preditivos tradicionais retornam apenas um valor final (ex: "78% de risco"). No setor público brasileiro, isso fere o princípio da Motivação. 
Por isso, a saída do Random Forest é interceptada pela biblioteca **SHAP (SHapley Additive exPlanations)**.

### Fluxo de Execução SHAP:
- O algoritmo calcula a contribuição marginal de cada palavra da matriz TF-IDF.
- O *frontend* mapeia os pesos SHAP mais altos.
- O usuário visualiza o edital com os termos de maior risco grifados em vermelho, provendo interpretabilidade instantânea.

## 3. Integração de Dados (PNCP)
A ferramenta foi treinada utilizando a base censitária do PNCP (Portal Nacional de Contratações Públicas), abrangendo mais de 572 mil contratos (2021-2024), com cruzamento secundário de dados via BrasilAPI para enriquecimento das variáveis dos fornecedores e dos órgãos públicos (covariáveis de controle estrutural).

---
*Para ver os testes de robustez e curvas de acurácia, consulte o `Artigo Tecnológico 02` da Tese.*
