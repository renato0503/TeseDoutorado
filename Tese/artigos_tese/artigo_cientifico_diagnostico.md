# ARTIGO CIENTÍFICO 1: O Diagnóstico Empírico das Compras Complexas

**TÍTULO PROVISÓRIO:** 
Determinantes do Sucesso e Fracasso em Compras Públicas Complexas: Uma Análise Censitária das Entidades Governamentais no Brasil.

**OBJETIVO CENTRAL:** 
Mapear o universo de compras complexas no Portal Nacional de Contratações Públicas (PNCP), diferenciar seus resultados em relação às compras comuns (normais) e identificar as características determinantes (covariáveis) das Unidades Compradoras que explicam a probabilidade de sucesso ou fracasso nessas contratações.

---

## 1. INTRODUÇÃO
- **Contextualização:** O papel das compras públicas complexas (inovação, tecnologia, sustentabilidade) como indutoras de desenvolvimento e os altos custos de transação envolvidos.
- **Problema de Pesquisa:** Quais as características estruturais, orçamentárias e de pessoal das Unidades Compradoras que determinam o sucesso ou o fracasso na execução de compras públicas complexas?
- **Justificativa (Feedback Olavo):** A necessidade de compreender o problema sob a ótica real das entidades compradoras, sem apelar para bodes expiatórios ("apagão das canetas") ou culpar exclusivamente os órgãos de controle. Foco na redução da assimetria informacional e na superação da incompetência/paralisia institucional por meio de dados.

## 2. REFERENCIAL TEÓRICO
*(Reaproveitado do Capítulo 2 da Tese Original)*
- **2.1. O que são Compras Complexas?** (Definição, categorização por valor/objeto/modalidade, risco tecnológico e mercadológico).
- **2.2. Assimetria Informacional e Custos de Transação:** Abordagem de Williamson (1985) e Coase (1937) focada na racionalidade limitada do gestor diante da complexidade.
- **2.3. O Estado Empreendedor:** O poder de compra governamental (Mazzucato, 2018) focado na criação de mercados e inovação.
- *(Nota: XAI sai daqui e vai para a Metodologia do Artigo Tecnológico)*.

## 3. METODOLOGIA
- **3.1. Abordagem de Dados:** Estudo quantitativo, observacional e censitário.
- **3.2. População e Amostra:** 
  - *Fonte Primária:* PNCP (572.045 contratos de set/2021 a ago/2024).
  - *Filtragem (O GRANDE DESAFIO):* Como separar o subset de "Compras Complexas" do total populacional. *(Pendente de definição pelo autor)*.
- **3.3. Fontes de Dados Secundários (Determinantes da Unidade Compradora):** 
  - Integração com bases externas (ex: IBGE, Siconfi, RAIS, Tesouro) para buscar variáveis independentes:
    - *X1:* Porte do órgão (receita/orçamento).
    - *X2:* Tipo de pessoal (volume da folha de pagamento, % de servidores estáveis).
    - *X3:* Setor/Esfera (Federal vs Estadual/Municipal).
- **3.4. Variável Dependente (O Modelo de Sucesso/Fracasso):**
  - *Y:* Sucesso (Execução no prazo/sem aditivos graves) vs Fracasso (Rescisão antecipada, impugnação, atraso severo).
  - *Modelagem (Reaproveitada do Art. 03, 04, 07):* Regressão logística / Random Forest e modelos de sobrevida (Cox).

## 4. RESULTADOS (ESTRUTURA ESPERADA)
- **4.1. Panorama Geral (Estatística Descritiva):** Quem são as entidades que fazem compras complexas? Qual a diferença percentual da taxa de fracasso em comparação com as compras normais?
- **4.2. Perfil dos Fornecedores (Reaproveitado do Art. 05 e 11):** Análise do mercado ofertante (concentração, Gini, monopólio de TI).
- **4.3. Determinantes do Fracasso/Sucesso:** Os resultados da Regressão/Modelo preditivo evidenciando quais características da Unidade Compradora impactam significativamente a performance da contratação.

## 5. DISCUSSÃO E CONCLUSÕES
- A realidade empírica sobre a falha no planejamento vs a complexidade do objeto.
- Como o mercado (fornecedores oligopolistas) interage com a assimetria do comprador.
- **Ponte para o Produto:** A conclusão de que o déficit técnico (falta de pessoal especializado, assimetria informacional) identificado no diagnóstico exige a criação de um artefato de suporte à decisão (gancho para o Artigo Tecnológico e para o Produto).

---
*(Documento criado a partir do "Data Lake" dos 25 artigos empíricos, pivotado para o modelo Fucape)*
