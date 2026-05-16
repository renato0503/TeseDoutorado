# Guia de Pesquisa - Doutorado em Contabilidade

---

## Visão Geral da Pesquisa

**Tema:** Copiloto Algorítmico para Compras Públicas Complexas: Um Artefato de Apoio à Decisão para Redução de Assimetrias na Contratação de Inovação e Sustentabilidade.

**Palavras-chave:** Compras Públicas Complexas; Design Science Research; Transparência Algorítmica; Inteligência Artificial; Método Delphi.

**Objetivo Geral:** Desenvolver e avaliar um artefato de apoio à cognição destinado à avaliação de riscos e à geração de editais para compras de governo no Brasil.

---

## Estrutura da Pesquisa

### Eixo 1: Transparência Algorítmica (Revisão Sistemática)
- Revisão bibliométrica sobre XAI em gestão pública
- Mapeamento de lacunas na literatura

### Eixo 2: Produto de Tecnologia
- Copiloto algorítmico para compras públicas
- Biblioteca de dados de editais históricos
- Módulos de avaliação e geração de texto

### Eixo 3: Validação Empirical (Método Delphi)
- Painel com 10 gestores de compras públicas
- Avaliação de barreiras institucionais

---

## APIs de Compras Públicas

### 1. Portal Nacional de Contratações Públicas (PNCP)

| Info | Detalhe |
|------|---------|
| **URL Base** | `https://pncp.gov.br/api/v1/` |
| **Autenticação** | API Key (gratuita via registro) |
| **Dados** | Editais, contratos, fornecedores |
| **Cobertura** | Todas as contratações públicas federais |

```bash
# Buscar editais
GET https://pncp.gov.br/api/v1/orgaos/07090100000120/contratacoes
    ?pagina=1
    &tamanhoPagina=20

# Buscar editais por termo
GET https://pncp.gov.br/api/v1/orgaos/07090100000120/contratacoes
    ?palavraChave=tecnologia
    &dataInicial=2024-01-01

# Detalhes de um edital específico
GET https://pncp.gov.br/api/v1/contratacoes/{id}
```

### 2. Portal da Transparência (CGU)

| Info | Detalhe |
|------|---------|
| **URL Base** | `https://portaldatransparencia.gov.br/api/v1` |
| **Autenticação** | Livre acesso |
| **Dados** | Empenhos, pagamentos, contratos |
| **Cobertura** | Execício orçamentária federal |

```bash
# Buscar contratos
GET https://portaldatransparencia.gov.br/api/v1/contratos
    ?ano=2024
    &pagina=1

# Buscar fornecedores
GET https://portaldatransparencia.gov.br/api/v1/fornecedores
    ?nome=Empresa%20X

# Detalhes de um contrato
GET https://portaldatransparencia.gov.br/api/v1/contratos/{id}
```

### 3. Compras.gov.br (SIASG)

| Info | Detalhe |
|------|---------|
| **URL** | `https://compras.dados.gov.br` |
| **Dados** | Pregões, atas, fornecedores |
| **Formato** | CSV, JSON |

```bash
# API de dados abertos
GET https://compras.dados.gov.br/licitacoes.json
    ?data_inicio=2024-01-01
    &modalidade=Pregão
```

### 4. TCU - Jurisprudência

| Info | Detalhe |
|------|---------|
| **URL Base** | `https://api.tcu.gov.br` |
| **Dados** | Acórdãos, decisões |
| **Autenticação** | Registro para API |

```bash
# Buscar jurisprudência
GET https://jurisprudencia.tcu.gov.br/api/v1/acordaos
    ?palavrasChave=licitação%20inovação
    &ano=2024
```

---

## APIs de Dados Governamentais

### 5. Dados.gov.br (Portal de Dados Abertos)

```bash
# Base de dados de contratos
GET https://dados.gov.br/api/v1/datasets?q=contratos

# Download de datasets
GET https://dados.gov.br/dataset/contratos-abertos
```

### 6. Siconfi (Finanças do Município)

```bash
# Dados contábeis
GET https://siconfi.tesouro.gov.br/api/v1/doc/conjunto_dados
    ?exercicio=2024
    &tipo=Balancete
```

---

## APIs Acadêmicas para Revisão de Literatura

### Semantic Scholar

```bash
GET https://api.semanticscholar.org/graph/v1/paper/search
    ?query=algorithmic%20transparency%20public%20procurement
    &limit=20
    &fields=title,abstract,year,citationCount
```

### OpenAlex

```bash
GET https://api.openalex.org/works
    ?filter=default.search:transparencia%20algoritmica%20governo
    &per_page=20
    &mailto=pesquisador@ufsc.br
```

### SciELO

```bash
GET https://search.scielo.org/?q=compras%20p%C3%BAblicas%20inovação
    &lang=pt
    &filter[year_cluster][]=2024
```

---

## APIs de Mídia e Opinião

### NewsAPI (para cobertura de mídia)

```bash
GET https://newsapi.org/v2/everything
    ?q=inteligência artificial compras públicas
    &language=pt
    &apiKey={API_KEY}
```

### LinkedIn (via Google Dork)

```
site:linkedin.com/pulse "compras públicas" tecnologia
```

---

## Fontes para Pesquisa Qualitativa

### 1. LinkedIn - GovTechs e Inovação Pública
- hashtags: #GovTech, #InovaçãoPública, #ComprasPúblicas
- Perfis de gestores de compras
- Empresas de tecnologia para governo

### 2. Reddit
- Subreddits: r/brdev, r/administracao
- Discussões sobre burocracia

### 3. Sites Jurídicos
- Conjur - análises sobre licitações
- Jota - notícias sobre tecnologia no governo
- Valor Econômico - cobertura de política industrial

---

## Palavras-chave para Busca

### Português
- Compras públicas inovação
- Transparência algorítmica governo
- Inteligência artificial administração pública
- Copiloto editais compras
- Apagão canetas licitações

### Inglês
- Algorithmic transparency public procurement
- AI government contracting
- Public procurement innovation
- Explainable AI public sector
- E-procurement challenges

---

## Ferramentas de Descoberta

- **Connected Papers**: Mapa de papers relacionados
- **Consensus**: Respostas baseadas em evidências
- **Litmaps**: Timeline de citações

---

## Base de Referências (APA)

### Transparência Algorítmica
- Arrieta et al. (2020) - XAI concepts
- Passotti et al. (2022) - Governing Algorithms
- Freedman et al. (2020) - Algorithmic Accountability

### Compras Públicas
- Edler & Georghiou (2007) - Public procurement and innovation
- Mazzucato (2013, 2018) - Estado Empreendedor

### Design Science Research
- Hevner et al. (2004) - DSR in IS research
- Peffers et al. (2007) - DSR methodology

### Economia Institucional
- Williamson (1985, 1996) - Custos de Transação
- Coase (1937) - Nature of the firm

---

## 3. Fontes de Dados e APIs (Status: Mapeamento em Andamento)

### 3.1 Fontes Identificadas e Viabilidade

| Fonte | URL/Endpoint | Status | Observações |
|-------|--------------|--------|--------------|
| **PNCP API** | `https://pncp.gov.br/api/v1/` | ✅ Viável | API REST oficial, requer registro para key |
| **Compras.gov.br** | `https://compras.dados.gov.br` | ✅ Viável | Dados abertos em JSON/CSV |
| **Portal Transparência** | `https://portaldatransparencia.gov.br/api/v1` | ✅ Viável | Livre acesso, dados de execução |
| **Dados.gov.br** | `https://dados.gov.br` | ✅ Viável | Repositório de datasets |
| **TCU Jurisprudência** | `https://jurisprudencia.tcu.gov.br` | ⚠️ Parcial | RequerAPI key para extração estruturada |
| **ComprasNet** | `https://pncp.gov.br` (novo) | ✅ Viável | Integração via PNCP |

### 3.2 Detalhamento por Fonte

#### PNCP (Portal Nacional de Contratações Públicas)
- **URL Base:** `https://pncp.gov.br/api/v1/`
- **Autenticação:** API Key gratuita via registro no portal
- **Dados disponíveis:** Editais, contratos, fornecedores, atas
- **Cobertura:** Administrações direta/indireta federal
- **Gargalos:** Rate limit de 100 req/min, necessidade de paginação

#### Portal da Transparência (CGU)
- **URL Base:** `https://portaldatransparencia.gov.br/api/v1`
- **Autenticação:** Livre acesso
- **Dados disponíveis:** Empenhos, pagamentos, contratos
- **Gargalos:** Dados de execução, não de planejamento

#### Dados.gov.br
- **URL Base:** `https://dados.gov.br/api/v3`
- **Autenticação:** Livre acesso para datasets públicos
- **Dados disponíveis:** Diversos datasets de compras
- **Gargalos:** Formatos heterogêneos, necessidade de ETL

### 3.3 Gargalos e Desafios

1. **Autenticação:** PNCP requer API Key (processo de registro em andamento)
2. **Volume:** Base histórica a partir de 2020 - limite temporal
3. **Formato:** HTML em editais，需要 parsing de PDF para texto
4. **Rate Limits:** Necessidade de controle de requisições
5. **Estrutura:** Dados de planejamento vs execução em APIs distintas

### 3.4 Próximos Passos

- [ ] Registrar-se no PNCP para obter API Key
- [ ] Testar endpoints de busca por palavra-chave (inovação, sustentabilidade)
- [ ] Desenvolver script de extração em Python
- [ ] Estruturar dados em formato JSON na pasta `Raw_Data/`
- [ ] Documentar dicionário de variáveis para alimentação do Copiloto