# ARTIGO TECNOLÓGICO 2: Construção do Copiloto Algorítmico

**TÍTULO PROVISÓRIO:** 
Desenvolvimento de um Copiloto Algorítmico Baseado em Inteligência Artificial Explicável (XAI) para Apoio à Decisão em Compras Públicas Complexas.

**OBJETIVO CENTRAL:** 
Descrever detalhadamente a arquitetura, as decisões de design e a metodologia de construção do artefato tecnológico (Copiloto) desenvolvido para mitigar a assimetria informacional diagnosticada no Artigo 1, utilizando princípios de Explainable AI (XAI) para garantir conformidade e transparência no setor público.

---

## 1. INTRODUÇÃO
- **Contextualização do Problema Prático:** O déficit técnico e a assimetria informacional nas unidades compradoras mapeadas no diagnóstico empírico (Artigo 1) exigem ferramentas de suporte à decisão.
- **O Desafio da Opacidade:** A adoção de IA no setor público esbarra no "paradigma black-box" e na necessidade legal de motivação dos atos administrativos.
- **Objetivo Tecnológico:** Apresentar a engenharia e as etapas de desenvolvimento de um "exoesqueleto cognitivo" (Copiloto) focado em compras complexas.

## 2. METODOLOGIA DE DESENVOLVIMENTO (DSR & XAI)
*(Reaproveitado dos Artigos 08, 16 e 17)*
- **2.1. Paradigma Design Science Research (DSR):**
  - O framework de Peffers et al. (2007) aplicado à contabilidade e gestão pública.
  - O ciclo de rigor (ciência e literatura aplicadas a problemas práticos).
- **2.2. A Metodologia XAI (Explainable AI):**
  - Justificativa do uso de modelos explicáveis (SHAP/LIME) como solução para o direito à motivação e à prestação de contas (accountability) estatal.
  - A lógica das *explicações contrafactuais* em algoritmos públicos.

## 3. ARQUITETURA DO PRODUTO E DECISÕES DE DESIGN
- **3.1. Requisitos do Sistema:** Construção baseada na literatura acadêmica de compras complexas. O que a ferramenta precisa fazer para resolver o problema?
- **3.2. Módulo de Detecção de Anomalias (Auditoria Contínua):**
  - *(Reaproveitado do Artigo 02)* 
  - Uso de aprendizado não supervisionado (*Isolation Forest*) para detecção de editais e cláusulas com padrão anômalo.
- **3.3. Módulo de Compliance e Avaliação de Risco:**
  - *(Reaproveitado do Artigo 18 e 08)*
  - Treinamento do modelo supervisionado (*Random Forest*) que atingiu 93,36% de acurácia e 90,83% de AUC-ROC (pós-remediação de tautologia).
  - A integração da camada XAI (SHAP) para traduzir o peso numérico das features em explicações textuais (justificativas) para o gestor.
- **3.4. Stack Tecnológico:** 
  - Backend, Frontend (se aplicável), e APIs utilizadas para conectar o Copiloto ao ecossistema do PNCP/Transparência.

## 4. AVALIAÇÃO E TESTES DE DESEMPENHO
- **4.1. Métricas Algorítmicas:** Resultados da Acurácia, F1-Score, Curva ROC-AUC e o grau de explicabilidade gerado pelo SHAP Values (exibindo como o algoritmo justifica o risco de fracasso/impugnação para o gestor).
- **4.2. Eficiência Computacional:** Ganhos de processamento em larga escala comparados com a auditoria manual.

## 5. CONCLUSÕES TECNOLÓGICAS
- **5.1. Viabilidade de Implantação:** O artefato comprova que é viável aplicar machine learning avançada no setor público sem ferir o princípio da transparência.
- **5.2. Transição para o Mundo Real (O Produto):** A conclusão serve como ponte direta para o **Produto (Entregável 3)**, que será materializado na forma de um aplicativo/plataforma hospedada no GitHub operando em modelo freemium.

---
*(Documento criado a partir do núcleo tecnológico dos antigos artigos, pivotado para o modelo Fucape)*
