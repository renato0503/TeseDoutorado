# MATERIAL SUPLEMENTAR

Para garantir a total transparência e a reprodutibilidade empírica desta pesquisa, os dados consolidados e os códigos de programação utilizados na estimação dos modelos econométricos encontram-se disponibilizados publicamente.

## 1. Base de dados utilizada no script

O arquivo contendo a base de dados tratada e consolidada (após a etapa de auditoria e saneamento), que foi efetivamente carregada no ambiente de execução, pode ser acessado na íntegra através do seguinte link:

**https://raw.githubusercontent.com/renato0503/TeseDoutorado/main/Base_de_Dados_e_APIs/Raw_Data/Artigos_Quanti/18_Compliance_Algoritmico/dados_pncp_2024.csv**

A base de dados original foi obtida a partir do Portal Nacional de Contratações Públicas (PNCP) via repositório governamental dados.gov.br, referente ao exercício financeiro de 2024. Após o processo de auditoria e saneamento — que incluiu a remoção de outliers extremos (valores estimados superiores a R$ 1 bilhão), a filtragem temporal exclusiva para o ano de 2024 e a correção de falsos positivos no dicionário de inovação — a base final contém **273.309 registros** de contratações públicas.

## 2. Script em Python

O script contendo o código estruturado em linguagem Python — utilizado para o tratamento final dos dados, a estimação do modelo de regressão logística, a execução da floresta aleatória (random forest) e a extração das matrizes de confusão e tabelas de performance — está disponível no seguinte link:

**https://raw.githubusercontent.com/renato0503/TeseDoutorado/main/Base_de_Dados_e_APIs/Raw_Data/Artigos_Quanti/18_Compliance_Algoritmico/script_colab_artigo18.py**

O script implementa as seguintes etapas computacionais: (i) carregamento e tratamento da base de dados PNCP 2024; (ii) construção do escore ordinal de risco processual (escore_risco_regra); (iii) estimação do modelo de regressão logística; (iv) execução do algoritmo de floresta aleatória (random forest) com validação cruzada estratificada; (v) extração das métricas de performance (acurácia, F1 Macro, Kappa de Cohen); e (vi) geração das tabelas e matrizes de confusão.

## 3. Calculadora Interativa

Para simular o escore de risco processual de qualquer contratação, acesse a calculadora interativa desenvolvida para explicar a metodologia do framework:

**https://renato0503.github.io/TeseDoutorado/docs/calculadora_compliance.html**
