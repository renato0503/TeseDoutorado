# Dicionário de Dados - Mapeamento 5W2H

## Visão Geral

Este documento consolida o mapeamento completo das necessidades de dados para os 17 artigos científicos e o artefato Copiloto da tese de doutorado.

---

## PARTE I: ARTIGOS QUANTITATIVOS (01-08)

---

### Artigo 01 - Complexidade Textual em Editais de Inovação

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Texto integral de editais de inovação (extração HTML/PDF via API) |
| **Why** | Calcular índices de legibilidade (Flesch-Kincaid via spaCy/NLTK) e correlacionar com número de fornecedores via regressão multivariada |
| **Where** | API PNCP (`https://pncp.gov.br/api/v1/contratacoes`) |
| **When** | 2021-2026 (pós Nova Lei de Licitações 14.133/2021) |
| **Who** | Órgãos da Administração Pública Federal que publicaram editais de inovação e sustentabilidade |
| **How** | Script Python: paginação API + parsing HTML + extração texto |
| **How much** | Estimativa: 500-1.000 editais de inovação/sustentabilidade |

**Features necessárias:** `texto_edital`, `numero_proposta`, `modalidade`, `data_publicacao`, `orgao`, `numero_fornecedores`

---

### Artigo 02 - Detecção de Anomalias de Preços

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Dados de preços de itens de contratação (valores unitários por item) |
| **Why** | Treinar algoritmos não-supervisionados (Isolation Forest/One-Class SVM) para detecção de outliers de sobrepreço |
| **Where** | Portal Transparência (`https://portaldatransparencia.gov.br/api/v1/empenhos`) + Painel de Preços Gov Federal |
| **When** | 2021-2026 |
| **Who** | Contratações da União via Pregão, Dispensa, Inexigibilidade |
| **How** | Script: extração API + normalização de itens via descrição |
| **How much** | Estimativa: 50.000-100.000 registros de itens de contratação |

**Features necessárias:** `codigo_item`, `descricao_item`, `valor_unitario`, `quantidade`, `uasg`, `modalidade`, `ano`

---

### Artigo 03 - Predição de Fracasso de Contratos

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Contratos, termos aditivos, cancelamentos e rescisões |
| **Why** | Modelagem preditiva (regressão logística/Random Forest) para identificar risco de fracasso (atraso, aditivo, cancelamento) |
| **Where** | API PNCP + Portal Transparência (contratos) |
| **When** | 2021-2026 |
| **Who** | Contratos de serviços de tecnologia e inovação |
| **How** | Script: extração contratos + feature engineering (tempo, valor, tipo serviço) |
| **How much** | Estimativa: 10.000-20.000 contratos de TI/inovação |

**Features necessárias:** `numero_contrato`, `data_inicio`, `data_fim`, `valor_inicial`, `valor_atual`, `quantidade_aditivos`, `motivo_cancelamento`, `tipo_servico`

---

### Artigo 04 - "Apagão das Canetas": Latência Decisória

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Acórdãos sancionatórios (datas) + timestamps de editais (publicação, abertura, homologação) |
| **Why** | Análise de séries temporais (ARIMA/Prophet) para correlacionar jurisprudência sancionatória com duração de licitações |
| **Where** | API Jurisprudência TCU + API PNCP/Compras.gov |
| **When** | 2017-2026 (pré e pós Nova Lei 13.888/2019 e 14.133/2021) |
| **Who** | Gestores federais com decisões sancionatórias + processos de contratação de tecnologia |
| **How** | Extração API jurisprudência + logs temporais de editais |
| **How much** | Estimativa: 500-1.000 acórdãos relevantes + série temporal de 5.000-10.000 licitações |

**Features necessárias:** `data_acordao`, `tipo_sancao`, `tema`, `data_publicacao_edital`, `data_abertura_proposta`, `data_homologacao`, `duracao_dias`

---

### Artigo 05 - Redes de Fornecimento e Oligopólios

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Dados de fornecedores (CNPJ, razão social, contratos, valores) |
| **Why** | Construção de grafos de rede (NetworkX) para detectar padrões de concentração, oligopólios e centralidade de fornecedores |
| **Where** | API PNCP + Portal Transparência (fornecedores) |
| **When** | 2021-2026 |
| **Who** | Fornecedores de tecnologia, software e serviços de inovação |
| **How** | Script: extração fornecedores + marriages entre contratos + análise de rede |
| **How much** | Estimativa: 5.000-10.000 fornecedores únicos, ~50.000-100.000 arestas |

**Features necessárias:** `cnpj_fornecedor`, `razao_social`, `numero_contratos`, `valor_total`, `orgao_contratante`, `tipo_servico`

---

### Artigo 06 - Análise de Sobrevivência (Kaplan-Meier)

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Datas de início, vigência, término e rescisões de contratos |
| **Why** | Análise de sobrevivência: estimador Kaplan-Meier + modelo de Cox para comparar sobrevida de contratos de inovação vs convencionais |
| **Where** | API Portal Transparência (contratos) + PNCP |
| **When** | 2021-2026 |
| **Who** | Contratos de inovação versus contratos convencionais (comparação) |
| **How** | Extração de datas contratuais + censoring para contratos vigentes |
| **How much** | Estimativa: 10.000-15.000 contratos (5.000 inovação + 10.000 convencionais) |

**Features necessárias:** `numero_contrato`, `data_inicio`, `data_fim_contratual`, `data_termino_real`, `status_contrato`, `tipo_contrato`, `categoria_inovacao`

---

### Artigo 07 - Governança Algorítmica: Benchmarking de Eficiência

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Métricas de desempenho de processos de contratação por órgão |
| **Why** | Criar benchmarks e indicadores comparativos de eficiência entre órgãos (tempo médio, preço médio, competitividade) |
| **Where** | API PNCP + Portal Transparência |
| **When** | 2021-2026 |
| **Who** | Órgãos da Administração Pública Federal |
| **How** | Extração + agregação de métricas por órgão |
| **How much** | Estimativa: 150-200 órgãos com dados suficientes |

**Features necessárias:** `orgao`, `quantidade_licitacoes`, `tempo_medio`, `valor_medio`, `numero_licitantes_media`, `indice_competitividade`, `indice_economia`

---

### Artigo 08 - XAI em Prova de Conceito: Tribunais de Contas

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Dados de auditoria de Tribunais de Contas (decisões, recomendações, sanções) |
| **Why** | Aplicar técnicas de XAI (SHAP/LIME) para explicitar critérios de decisão em modelos de detecção de irregularidades |
| **Where** | TCE-SP, TCE-MG, TCE-RS (APIs institucionais ou scraping) |
| **When** | 2021-2026 |
| **Who** | Contratações de estados e municípios (amostras) |
| **How** | Web scraping de portais de jurisprudência ou API institucional |
| **How much** | Estimativa: 1.000-2.000 decisões de auditoria |

**Features necessárias:** `numero_processo`, `tipo_decisao`, `irregularidade_identificada`, `valor_envolvido`, `orgao_auditado`, `data_decisao`

---

## PARTE II: ARTIGOS QUALITATIVOS (09-17)

---

### Artigo 09 - "Jurisprudência do Medo": Análise de Discurso

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Texto integral de acórdãos do TCU relacionados a sanções em contratos de inovação |
| **Why** | Análise Crítica do Discurso (ACD) para mapear matrizes discursivas de risco, dolo e responsabilização |
| **Where** | API Jurisprudência TCU (`https://jurisprudencia.tcu.gov.br/api/v1/acordaos`) |
| **When** | 2017-2026 |
| **Who** | TCU - decisões sobre sanções em contratações de inovação e tecnologia |
| **How** | Extração API + análise textual com spaCy/NLTK (tokenização, POS tagging, análise semântica) |
| **How much** | Estimativa: 200-500 acórdãos relevantes |

**Features necessárias:** `numero_acordao`, `texto_inteiro`, `data_sessao`, `unidade_tecnica`, `relator`, `tipo_decisao`, `tema`

---

### Artigo 10 - Uso Retórico da Inovação em Justificativas

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Texto de justificativas, fundamentação e cláusulas em editais de inovação |
| **Why** | Análise de conteúdo e análise retórica para identificar padrões de uso do termo "inovação" e fundamentação |
| **Where** | API PNCP |
| **When** | 2021-2026 |
| **Who** | Editais de compras de inovação e sustentabilidade |
| **How** | Extração de campos de justificativa + análise de frequência + topic modeling (LDA) |
| **How much** | Estimativa: 300-500 editais |

**Features necessárias:** `texto_justificativa`, `fundamentacao_legal`, `objeto_descricao`, `criterio_tecnico`

---

### Artigo 11 - "Voz do Mercado": Impugnações de Editais

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Editais impugnados e respectivos memoriais de impugnação |
| **Why** | Identificar barreiras de mercado, padrões de contestação e dificuldades de participação |
| **Where** | API PNCP (campo resultado julgamento) + Compras.gov |
| **When** | 2021-2026 |
| **Who** | Editais de tecnologia e inovação com impugnação |
| **How** | Extração + categorização por tipo de irregularidade alegada |
| **How much** | Estimativa: 100-200 impugnações |

**Features necessárias:** `numero_edital`, `motivo_impugnacao`, `resultado`, `tema_tecnico`, `empresa_impugnante`

---

### Artigo 12 - Evolução da Legislação de Compras

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Textos legislativos: Lei 8.666/93, Lei 13.888/2019, Lei 14.133/2021, Marco Legal de Startups |
| **Why** | Análise diacrônica de evolução de dispositivos de gestão de risco em contratações públicas |
| **Where** | Download direto (Planalto, Câmara) + análise documental |
| **When** | 1993-2026 (evolução histórica) |
| **Who** | Legislação federal de licitações e contratos |
| **How** | Download PDF + parsing + análise qualitativa de dispositivos |
| **How much** | Estimativa: 20-30 textos legislativos/normativos relevantes |

**Features necessárias:** `lei_numero`, `data_publicacao`, `artigo`, `dispositivo`, `tema_risco`, `historico_alteracao`

---

### Artigo 13 - "Dor das GovTechs": Netnografia

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Posts, comentários e discussões em plataformas digitais |
| **Why** | Netnografia para compreender experiências, dores e percepções do ecossistema GovTech |
| **Where** | LinkedIn + Reddit (r/brdev, r/administracao) + Groups do Facebook |
| **When** | 2020-2026 |
| **Who** | Empreendedores de GovTechs, gestores públicos, investidores |
| **How** | Web scraping + análise etnográfica digital |
| **How much** | Estimativa: 1.000-2.000 interações/posts |

**Features necessárias:** `texto_post`, `autor`, `data`, `plataforma`, `hashtags`, `sentimento`

---

### Artigo 14 - Discurso do "Custo Brasil" e Política Industrial

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Notícias, artigos e documentos sobre "Custo Brasil" e política industrial |
| **Why** | Análise de enquadramento (framing) para identificar narrativas dominantes sobre burocracia e inovação |
| **Where** | Portais de notícia (G1, Folha, Valor, ConJur) + APIs de notícias |
| **When** | 2015-2026 |
| **Who** | Mídia brasileira sobre compras, inovação, política industrial |
| **How** | Google Dorks + API NewsAPI + análise de conteúdo |
| **How much** | Estimativa: 500-1.000 notícias/artigos |

**Features necessárias:** `titulo`, `texto`, `data_publicacao`, `veiculo`, `autor`, `tema_principal`, `quadro_interpretativo`

---

### Artigo 15 - Enquadramento da IA no Controle Público pela Mídia

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Cobertura jornalística sobre IA, algoritmos e controle público |
| **Why** | Análise de enquadramento midiático sobre uso de IA no setor público e controle |
| **Where** | APIs de notícias + Google Dorks |
| **When** | 2018-2026 (período de popularização de IA) |
| **Who** | Mídia brasileira e internacional |
| **How** | Extração via API + análise de framing |
| **How much** | Estimativa: 300-500 notícias |

**Features necessárias:** `titulo`, `texto`, `data`, `veiculo`, `tema_ia`, `enquadramento_positivo_negativo`

---

### Artigo 16 - Revisão Sistemática XAI em Gestão Pública

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Artigos acadêmicos sobre XAI (Explainable AI) em gestão pública |
| **Why** | Revisão sistemática (Protocolo PRISMA) + bibliometria para mapear estado da arte |
| **Where** | Scopus + Web of Science + Semantic Scholar |
| **When** | 2017-2026 (período de emergência de XAI) |
| **Who** | Artigos acadêmicos internacionais |
| **How** | API Semantic Scholar/OpenAlex + export .bib + VOSviewer |
| **How much** | Estimativa: 200-500 artigos (após filtro PRISMA) |

**Features necessárias:** `titulo`, `abstract`, `autores`, `ano`, `citacoes`, `keywords`, `期刊`, `tipo_estudo`

---

### Artigo 17 - DSR em Contabilidade Pública: Mapeamento

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Artigos acadêmicos sobre Design Science Research em contabilidade e gestão pública |
| **Why** | Mapeamento sistemático de artefatos DSR no campo de contabilidade pública |
| **Where** | Scopus + Web of Science + Spell + SciELO |
| **When** | 2004-2026 (período DSR) |
| **Who** | Artigos de contabilidade pública, administração pública, sistemas de informação |
| **How** | API acadêmicas + exportação + revisão sistemática |
| **How much** | Estimativa: 100-200 artigos |

**Features necessárias:** `titulo`, `abstract`, `autores`, `ano`, `problema`, `artefato`, `avaliacao`, `contribuicao`

---

## PARTE III: ARTEFATO COPILOTO

---

### Copiloto Algorítmico - Biblioteca de Treinamento

| Dimensão | Detalhamento |
|----------|---------------|
| **What** | Corpus de editais históricos de inovação e sustentabilidade + contratos anexos |
| **Why** | Treinar modelo de linguagem para: (1) avaliação de minutas, (2) geração de cláusulas, (3) identificação de riscos |
| **Where** | API PNCP (editais + contratos + atas) |
| **When** | 2020-2026 |
| **Who** | Editais de inovação, sustentabilidade, tecnologia e serviços correlatos |
| **How** | Script de extração + preprocessing (limpeza, tokenização, embeddings) |
| **How much** | Estimativa: 3.000-5.000 editais completos + 10.000-20.000 contratos |

**Features necessárias:** 
- Corpus textual: `texto_edital`, `texto_contrato`, `texto_ata`
- Metadados: `orgao`, `modalidade`, `valor`, `data`, `categoria`, `termos_chave`
- Estruturado: `clausulas`, `itens`, `criterios_tecnicos`

---

## RESUMO: FONTES DE DADOS POR API

| Fonte | Artigos | Tipo de Dados | Volume Estimado |
|-------|---------|---------------|------------------|
| **PNCP API** | 01, 03, 05, 06, 10, 11 | Editais, contratos, fornecedores | 50.000+ registros |
| **Portal Transparência** | 02, 03, 05, 06, 07 | Empenhos, pagamentos | 200.000+ registros |
| **TCU Jurisprudência** | 04, 09 | Acórdãos, decisões | 5.000+ registros |
| **TCEs (SP, MG, RS)** | 08 | Decisões de auditoria | 2.000+ registros |
| **Semantic Scholar** | 16 | Artigos acadêmicos | 500+ artigos |
| **Scopus/Web of Science** | 16, 17 | Artigos acadêmicos | 300+ artigos |
| **NewsAPI** | 14, 15 | Notícias | 1.000+ notícias |
| **Web Scraping** | 13 | Posts, comentários | 2.000+ interações |
| **Legislação** | 12 | Leis, decrees | 30+ textos |

---

## ESTRUTURA DE PASTAS DEFINITIVA

```
Base_de_Dados_e_APIs/
├── Raw_Data/
│   ├── Artigos_Quanti/
│   │   ├── 01_Complexidade_Textual/
│   │   │   ├── editais_json/
│   │   │   └── analise/
│   │   ├── 02_Anomalias_Precos/
│   │   │   ├── precos_csv/
│   │   │   └── modelos/
│   │   ├── 03_Predicao_Fracasso/
│   │   │   ├── contratos_json/
│   │   │   └── feature_engineering/
│   │   ├── 04_Apagao_Canetas/
│   │   │   ├── acordaos_tcu_json/
│   │   │   └── series_temporais/
│   │   ├── 05_Redes_Fornecimento/
│   │   │   ├── fornecedores_json/
│   │   │   └── grafos/
│   │   ├── 06_Sobrevivencia/
│   │   │   ├── contratos_datas_json/
│   │   │   └── analise_cox/
│   │   ├── 07_Benchmarking/
│   │   │   ├── metricas_orgaos_csv/
│   │   │   └── dashboards/
│   │   └── 08_XAI_TCEs/
│   │       ├── decisoes_tce_json/
│   │       └── explicacoes_shap/
│   │
│   ├── Artigos_Quali/
│   │   ├── 09_Jurisprudencia_Medo/
│   │   │   ├── acordaos_tcu_json/
│   │   │   └── analise_discurso/
│   │   ├── 10_Retorica_Inovacao/
│   │   │   ├── editais_json/
│   │   │   └── topicos_lda/
│   │   ├── 11_Impugnacoes/
│   │   │   ├── editais_impugnados_json/
│   │   │   └── categorizacao/
│   │   ├── 12_Evolucao_Legislacao/
│   │   │   └── textos_legais/
│   │   ├── 13_Netnografia_GovTechs/
│   │   │   ├── linkedin_csv/
│   │   │   └── reddit_csv/
│   │   ├── 14_Custo_Brasil/
│   │   │   ├── noticias_json/
│   │   │   └── enquadramento/
│   │   └── 15_IA_Controle_Midia/
│   │       ├── noticias_json/
│   │       └── analise_framing/
│   │
│   ├── Revisao_Sistematica/
│   │   ├── 16_XAI_Gestao_Publica/
│   │   │   ├── scopus_bib/
│   │   │   ├── wos_bib/
│   │   │   └── vosviewer/
│   │   └── 17_DSR_Contabilidade/
│   │       ├── artigos_bib/
│   │       └── mapeamento/
│   │
│   └── Artefato_Copiloto/
│       ├── corpus_editais/
│       ├── corpus_contratos/
│       ├── embeddings/
│       └── modelos_treinados/
│
└── Scripts_Extracao/
    ├── extrator_pncp.py
    ├── extrator_transparencia.py
    ├── extrator_tcu.py
    ├── extrator_academico.py
    ├── extrator_noticias.py
    └── web_scraping/
        ├── scraper_linkedin.py
        ├── scraper_tces.py
        └── scraper_legislacao.py
```

---

## PRÓXIMOS PASSOS - ORDEM DE EXTRAÇÃO

### Fase 1: Fundamentais para Copiloto
1. `extrator_pncp.py` - Extrair editais de inovação → Artefato + Art 01, 10, 11
2. `extrator_academico.py` - Extrair artigos XAI → Art 16

### Fase 2: Artigos Quantitativos
3. `extrator_transparencia.py` - Preços e contratos → Art 02, 03, 06, 07
4. `extrator_tcu.py` - Jurisprudência → Art 04, 09
5. `web_scraping_tces.py` - Dados TCEs → Art 08

### Fase 3: Artigos Qualitativos
6. `extrator_noticias.py` - Mídia → Art 14, 15
7. `web_scraping_govtechs.py` - Netnografia → Art 13
8. `scraper_legislacao.py` - Leis → Art 12

---

## Imagens SVG

| Arquivo | Descrição | Tipo |
|---------|-----------|------|
| grafico1_complexidade_textual.svg | Boxplot de legibilidade por modalidade | Gráfico |
| grafico2_sobrevivencia.svg | Curvas Kaplan-Meier | Gráfico |
| grafico3_latencia_decisoria.svg | Latência por sanção TCU | Gráfico |
| grafico4_shap_summary.svg | Importância SHAP | Gráfico |
| grafico5_framing_midia.svg | Enquadramento midiático | Gráfico |
| figura1_arquitetura_copiloto.svg | Arquitetura do sistema | Figura |
| figura2_ciclo_dsr.svg | Ciclo DSR de Hevner | Figura |
| figura3_pipeline_nlp.svg | Pipeline NLP | Figura |
| figura4_interface_avaliacao.svg | Interface do copiloto | Figura |
| figura5_rede_fornecimento.svg | Rede de adjudicações | Figura |