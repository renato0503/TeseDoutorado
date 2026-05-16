# Documentação do Projeto de Doutorado

---

## Visão Geral

**Projeto:** Copiloto Algorítmico para Compras Públicas Complexas

**Aluno:** Renato de Oliveira Rosa

**Programa:** PPGCont - Universidade Federal de Santa Catarina

**Orientador:** Prof. Dr. Olavo Venturim Caldas

**Instituição:** Fucape Business School - Vitória/ES

---

## Estrutura de Diretórios

```
Doutorado/
├── Tese/
│   └── tese_draft.html          # Draft da tese em formato multipaper
│
├── Artigos/
│   ├── 01-Opacidade-Institucional-Analise-Complexidade-Textual-Editais-Inovacao/
│   │   └── artigo_01.html
│   ├── 02-Auditoria-Continua-Deteccao-Anomalias-Precos/
│   │   └── artigo_02.html
│   ├── 03-Predicao-Fracasso-Risco-Aditivos-Cancelamentos/
│   │   └── artigo_03.html
│   ├── 04-Apagao-Canetas-Quantificado-Latencia-Decisoria/
│   │   └── artigo_04.html
│   ├── 05-Redes-Fornecimento-Oligopolios-Analise-Grafos/
│   │   └── artigo_05.html
│   ├── 06-Sobrevivencia-Contratos-Inovacao-Analise-Kaplan-Meier/
│   │   └── artigo_06.html
│   ├── 07-Governanca-Algoritmica-Benchmarking-Eficiencia/
│   │   └── artigo_07.html
│   ├── 08-XAI-Setor-Publico-Prova-Conceito-Tribunais-Contas/
│   │   └── artigo_08.html
│   ├── 09-Jurisprudencia-Medo-Analise-Discurso-Acordaos/
│   │   └── artigo_09.html
│   ├── 10-Uso-Retorico-Inovacao-Analise-Conteudo-Justificativas/
│   │   └── artigo_10.html
│   ├── 11-Voz-Mercado-Analise-Impugnacoes-Editais-Tecnologia/
│   │   └── artigo_11.html
│   ├── 12-Evolucao-Risco-Legislacao-Compras-8.666-Marco-Startups/
│   │   └── artigo_12.html
│   ├── 13-Dor-GovTechs-Netnografia-Ecosistema-Inovacao-Publica/
│   │   └── artigo_13.html
│   ├── 14-Discurso-Custo-Brasil-Politica-Industrial-Narrativas-Pratica/
│   │   └── artigo_14.html
│   ├── 15-Enquadramento-IA-Controle-Publico-Midia/
│   │   └── artigo_15.html
│   ├── 16-Caixa-Preta-Setor-Publico-Revisao-Sistematica-XAI-Gestao-Publica/
│   │   └── artigo_16.html
│   └── 17-DSR-Contabilidade-Publica-Mapeamento-Artefatos/
│       └── artigo_17.html
│
├── Direcionamento.md            # Documento de direcionamento da pesquisa
├── escrita.md                   # Guia de escrita acadêmica
├── pesquisa.md                  # Guia de pesquisa e APIs
├── estrategia_paper.md          # Estratégia de geração de artigos
└── processo.md                  # Padrões de engenharia de software
```

---

## Frente Quantitativa (8 artigos)

| # | Artigo | Metodologia | Fonte de Dados |
|---|--------|-------------|----------------|
| 1 | Opacidade Institucional | NLP - Legibilidade | API PNCP |
| 2 | Auditoria Contínua | ML - Detecção anomalias | Portal Transparência |
| 3 | Predição de Fracasso | ML - Classificação | PNCP + Transparência |
| 4 | Apagão das Canetas | Séries Temporais | API TCU + Compras.gov |
| 5 | Redes de Fornecimento | Teoria Grafos | CNPJs + PNCP |
| 6 | Sobrevivência Contratos | Kaplan-Meier | Portal Transparência |
| 7 | Governança Algorítmica | DSR + Benchmarking | Siconfi |
| 8 | XAI Tribunais de Contas | SHAP | Dados TCU |

---

## Frente Qualitativa (9 artigos)

| # | Artigo | Metodologia | Fonte de Dados |
|---|--------|-------------|----------------|
| 9 | Jurisprudência do Medo | ACD | API TCU |
| 10 | Uso Retórico Inovação | Análise Conteúdo | Termos Referência PNCP |
| 11 | Voz do Mercado | Análise Impugnações | Compras.gov.br |
| 12 | Evolução Risco Legislação | Análise Diacrônica | LexML |
| 13 | Dor das GovTechs | Netnografia | LinkedIn + Medium |
| 14 | Discurso Custo Brasil | ACD | Relatórios MDIC |
| 15 | IA na Mídia | Framing Analysis | NewsAPI |
| 16 | Caixa-Preta Setor Público | Revisão Sistemática | Scopus + WoS |
| 17 | DSR Contabilidade Pública | Scoping Review | Scielo + Spell |

---

## Repositório GitHub

**URL:** https://github.com/renato0503/TeseDoutorado

**GitHub Pages:** https://renato0503.github.io/TeseDoutorado/

---

## Cronograma Estimado

- **Ano 1:** Revisão de literatura + Desenvolvimento biblioteca de dados
- **Ano 2:** Desenvolvimento do artefato + Artigos quantitativos
- **Ano 3:** Validação Delphi + Artigos qualitativos
- **Ano 4:** Defesa da tese

---

## Referências Principais

### Teóricas
- Economia dos Custos de Transação (Williamson)
- Estado Empreendedor (Mazzucato)
- Transparência Algorítmica (Arrieta et al.)
- Design Science Research (Hevner et al., Peffers et al.)

### Metodológicas
- Revisão Sistemática (PRISMA)
- Método Delphi
- Processamento de Linguagem Natural
- Machine Learning para detecção de anomalias

### Dados
- Portal Nacional de Contratações Públicas (PNCP)
- Portal da Transparência (CGU)
- Tribunal de Contas da União (TCU)
- Compras.gov.br

---

## Arquitetura de Extração de Dados

### Estrutura de Diretórios

```
Base_de_Dados_e_APIs/
├── Raw_Data/                    # Dados brutos extraídos
│   ├── editais_json/           # Editais em formato JSON
│   ├── contratos_json/         # Contratos em formato JSON
│   └── preprocessamento/      # Dados processados antes do treinamento
│
├── Scripts_Extracao/            # Códigos de consumo de API
│   ├── pncp_client.py          # Cliente Python para PNCP
│   ├── transparencia_client.py # Cliente para Portal Transparência
│   └── pipeline.py             # Pipeline de ETL completo
│
└── README.md                    # Documentação técnica
```

### Endpoints Principais

#### PNCP (Portal Nacional de Contratações Públicas)
| Endpoint | Método | Descrição |
|----------|--------|------------|
| `/api/v1/orgaos` | GET | Lista órgãos cadastrados |
| `/api/v1/contratacoes` | GET | Busca editais por filtros |
| `/api/v1/contratacoes/{id}` | GET | Detalhes de contratação |
| `/api/v1/fornecedores` | GET | Busca fornecedores |

#### Portal da Transparência
| Endpoint | Método | Descrição |
|----------|--------|------------|
| `/api/v1/contratos` | GET | Lista contratos |
| `/api/v1/empenhos` | GET | Lista empenhos |
| `/api/v1/fornecedores/{cpf-cnpj}` | GET | Dados fornecedor |

### Dicionário de Dados (Campos para Alimentação da IA)

| Campo | Tipo | Descrição | Prioridade |
|-------|------|-----------|------------|
| `numero_edital` | string | Número único do edital | Alta |
| `objeto` | text | Descrição do objeto da contratação | Alta |
| `modalidade` | string | Pregão, RDC, etc. | Alta |
| `valor_estimado` | decimal | Valor estimado da contratação | Alta |
| `data_publicacao` | date | Data de publicação no DOU | Alta |
| `unidade_compradora` | string | Nome do órgão comprador | Alta |
| `cnpj_unidade` | string | CNPJ da unidade | Alta |
| `regime_contratual` | string | Lei 8.666, Pregão, etc. | Média |
| `criterio_julgamento` | string | Menor preço, técnica e preço | Média |
| `prazo_execucao` | integer | Prazo em meses | Média |
| `garantia` | string | Tipo de garantia exigida | Baixa |
| `anexos` | array | Links para arquivos PDF | Alta |
| `categorias` | array | Tags: inovação, TI, sustentabilidade | Alta |
| `clausulas_especificas` | text | Cláusulas especiais identificadas | Alta |
| `fornecedores_participantes` | array | CNPJ/CPF participantes | Média |
| `resultado` | string | Fracassado, Homologado, etc. | Média |

### Pipeline de Extração

```
1. Coleta (Extract)
   ├─ API PNCP → JSON editais
   ├─ API Transparência → JSON contratos
   └─ Web Scraping → PDFs de anexos (se necessário)

2. Transformação (Transform)
   ├─ Limpeza de texto (normalização)
   ├─ Extração de entidades (NER)
   ├─ Classificação de categoria (inovação/TI/sustentabilidade)
   └─ Identificação de cláusulas específicas

3. Carregamento (Load)
   ├─ Armazenamento em JSON estruturado
   ├─ Indexação para busca vetorial
   └─ Exportação para treinamento do modelo
```

### Tecnologias Recomendadas

- **Linguagem:** Python 3.10+
- **Bibliotecas:** requests, pandas, BeautifulSoup4, spacy
- **Armazenamento:** JSON local + vector database (opcional)
- **Orquestração:** Apache Airflow ou Prefect (para pipelines)

### Status de Implementação

- [ ] Registro no PNCP para API Key
- [ ] Desenvolvimento cliente Python
- [ ] Teste de endpoints
- [ ] Extração de amostra (100 editais)
- [ ] Validação de estrutura de dados
- [ ] Indexação para Copiloto