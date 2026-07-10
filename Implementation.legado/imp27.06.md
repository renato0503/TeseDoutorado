# Plano de Upgrades - 27/06/2026

## Contexto
Identificacao de oportunidades de expansao dos artigos 1-18 a partir das APIs gratuitas
utilizadas nos artigos 19-24 (yfinance, OpenAlex, World Bank, HG Brasil), alem de
melhorias nos artigos 19-24 ja existentes.

## Sprints

### Sprint 1: Upgrades Bibliometricos (Crossref)
- Artigo 16 (Caixa-Preta / XAI): Validar 52 artigos locais contra base Crossref
- Artigo 17 (DSR Contabilidade): Expandir busca com Crossref para 42+ artigos

### Sprint 2: Upgrades Quantitativos (yfinance + World Bank + BCB SGS)
- Artigo 05 (Redes de Fornecimento): Adicionar market share financeiro via yfinance
- Artigo 06 (Sobrevivencia Contratos): Contexto macro via BCB SGS
- Artigo 07 (Benchmarking Siconfi): Comparativo cross-country via World Bank
- Artigo 08 (XAI Tribunais): Analise de empresas de auditoria listadas via yfinance
- Artigo 12 (Evolucao Risco Legislacao): Contexto internacional via World Bank

### Sprint 3: Melhorias nos Artigos 19-24
- Artigo 20: Cruzar CNPJ/RIQ dos fornecedores com PNCP
- Artigo 21: Coletar acordaos reais do TCU
- Artigo 22: Expandir amostra (mais anos e mais empresas)
- Artigo 24: Incorporar WGI do World Bank

### Artigo 25: Coleta LLM Multi-Agent
- Coleta de dados sobre LLM multi-agent systems

## Tarefa 4: Geracao de Artigos com Analises e Metodologias

### Objetivo
Gerar artigos completos com secoes (Introducao, Fundamentacao, Metodologia, Resultados, Discussao, Conclusao) utilizando os dados extraidos.

### Artigos a Gerar
1. **Artigo 16** - Revisao Sistematica XAI: 278 artigos Crossref
2. **Artigo 17** - DSR Contabilidade: 284 artigos Crossref
3. **Artigo 25** - LLM Multi-Agent: 395 artigos arXiv
4. **Artigo 06** - Macroeconomico BCB: 420 registros (IPCA, CDI, divida, INPC, IGP-M)

### Fontes de Dados para Artigos

| Artigo | Dados | Registros | Fonte |
|--------|-------|-----------|-------|
| Artigo 16 | artigo16_crossref.csv | 278 | Crossref |
| Artigo 17 | artigo17_crossref.csv | 284 | Crossref |
| Artigo 25 | llm_multi_agent_arxiv.csv | 395 | arXiv |
| Artigo 06 | artigo06_macroeconomico_bcb.csv | 420 | BCB SGS |

## APIs Testadas para Pesquisa Academica

| API | Status | Observacao |
|-----|--------|------------|
| **Semantic Scholar** | 429 (rate limited) | Precisa de API key |
| **Crossref** | 200 OK | 1.48M papers, funciona bem |
| **arXiv** | 200 OK | 100 results/termo, gratuito sem key |
| **PubMed** | 200 OK | 191 papers, gratuito |
| **OpenAlex** | 429 (bloqueado) | Rate limit excedido (polite pool implementado) |
| **PNCP** | 400 (parametro obrigatorio) | Requer codigoModalidadeContratacao |
| **TCU** | Erro | API de jurisprudencia indisponivel |
| **BCB SGS** | 200 OK | Substituto do HG Brasil |

## Status de Execucao

### Sprint 1 - Extracao (Concluido)
| Artigo | Status | Resultado |
|--------|--------|-----------|
| Artigo 16 | [x] Concluido | 278 artigos (Crossref) |
| Artigo 17 | [x] Concluido | 284 artigos (Crossref) |

### Sprint 2 - Extracao (Concluido)
| Artigo | Status | Resultado |
|--------|--------|-----------|
| Artigo 05 | [x] Concluido | 10 empresas (yfinance) |
| Artigo 06 | [x] Concluido | 420 registros (BCB SGS) |
| Artigo 07 | [x] Concluido | 224 registros (World Bank) |
| Artigo 08 | [x] Concluido | 6 empresas (yfinance) |
| Artigo 12 | [x] Concluido | 70 registros (World Bank) |

### Sprint 3 - Extracao (Em Andamento)
| Artigo | Status | Resultado |
|--------|--------|-----------|
| Artigo 20 | [x] Parcial | PNCP API 422 (data inválida) - em DEBUG |
| Artigo 21 | [x] Parcial | TCU API erro - template demo |
| Artigo 22 | [x] Concluido | 6 empresas + series temporais |
| Artigo 24 | [x] Concluido | 100 registros WGI |

### Artigo 25 - Extracao (Concluido)
| Artigo | Status | Resultado |
|--------|--------|-----------|
| Artigo 25 | [x] Alternativo | 395 artigos (arXiv) |

### Tarefa 4 - Geracao de Artigos (CONCLUIDA)
| Artigo | Status | Prioridade |
|--------|--------|------------|
| Artigo 16 | [x] Concluido | Alta |
| Artigo 17 | [x] Concluido | Alta |
| Artigo 25 | [x] Concluido | Alta |
| Artigo 06 | [x] Concluido | Media |

## Arquivos Gerados

| Artigo | Arquivo | Tamanho | Registros |
|--------|---------|---------|-----------|
| Artigo 16 | artigo16_crossref.csv | 37 KB | 278 |
| Artigo 17 | artigo17_crossref.csv | 45 KB | 284 |
| Artigo 05 | artigo05_yfinance.csv | 1 KB | 10 |
| Artigo 06 | artigo06_macroeconomico_bcb.csv | 19 KB | 420 |
| Artigo 06 | artigo06_ipca.csv | 1 KB | 84 |
| Artigo 07 | artigo07_worldbank.csv | 8 KB | 224 |
| Artigo 08 | artigo08_yfinance.csv | 1 KB | 6 |
| Artigo 12 | artigo12_worldbank.csv | 3 KB | 70 |
| Artigo 20 | artigo20_pncp_orgaos.csv | 5 B | 0 |
| Artigo 21 | artigo21_acordaos_tcu.csv | 1 KB | 5 |
| Artigo 22 | demonstracoes_expandido.csv | 249 B | 6 |
| Artigo 22 | precos_expandido.csv | 388 KB | 2492 |
| Artigo 22 | retornos_expandido.csv | 433 KB | 2492 |
| Artigo 24 | artigo24_wgi_processado.csv | 13 KB | 100 |
| Artigo 25 | llm_multi_agent_arxiv.csv | 265 KB | 395 |

## Artigos Gerados (HTML)

| Artigo | Arquivo | Tamanho |
|--------|---------|---------|
| Artigo 16 | artigo_16.html | 19 KB |
| Artigo 17 | artigo_17.html | 19 KB |
| Artigo 25 | artigo_25.html | 18 KB |
| Artigo 06 | artigo_06.html | 8 KB |

## Scripts Criados

### Sprint 1
- `Artigo 16/Scripts_Extracao/upgrade_crossref.py`
- `Artigo 17/Scripts_Extracao/upgrade_crossref.py`

### Sprint 2
- `Artigo 05/Scripts_Extracao/upgrade_yfinance.py`
- `Artigo 06/Scripts_Extracao/upgrade_bcb_sgs.py` (REFATORADO - BCB SGS)
- `Artigo 07/Scripts_Extracao/upgrade_worldbank.py`
- `Artigo 08/Scripts_Extracao/upgrade_yfinance.py`
- `Artigo 12/Scripts_Extracao/upgrade_worldbank.py`

### Sprint 3
- `Artigo 20/Scripts_Extracao/upgrade_pncp.py` (REFATORADO - novo endpoint)
- `Artigo 21/Scripts_Extracao/upgrade_tcu.py` (REFATORADO - dados abertos CSV)
- `Artigo 22/Scripts_Extracao/upgrade_expansao.py`
- `Artigo 24/Scripts_Extracao/upgrade_wgi.py`

### Artigo 25
- `Artigo 25/Scripts_Extracao/coletar_openalex.py` (REFATORADO - polite pool)
- `Artigo 25/Scripts_Extracao/coletar_arxiv.py`

### Tarefa 4 - Geracao de Artigos
- `Artigo 16/Scripts_Extracao/gerar_artigo.py`
- `Artigo 17/Scripts_Extracao/gerar_artigo.py`
- `Artigo 25/Scripts_Extracao/gerar_artigo.py`
- `Artigo 06/Scripts_Extracao/gerar_artigo.py`

## Correcoes Implementadas

### 1. OpenAlex (Rate Limit 429)
- Adicionado cabecalho `User-Agent: mailto:gestor.renatorosa@gmail.com`
- Entrada no Polite Pool para evitar rate limit

### 2. PNCP (Endpoint 404/400)
- Novo endpoint: `https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao`
- Parametro obrigatorio: `codigoModalidadeContratacao`
- Script refatorado com fallback

### 3. TCU (API Descontinuada)
- Substituido por download de CSV via dadosabertos.tcu.gov.br
- Funcao generica para download de datasets

### 4. HG Brasil (Indisponivel)
- Substituido por BCB SGS API
- Series: IPCA (433), CDI (4391), divida_federal (27842), INPC (188), IGP-M (189)

## Pendencias
- PNCP: Resolver erro 422 (Data Inicial inválida) - formato data?
- TCU: Validar URLs de datasets abertos
- Artigo 14: Unificar duas pastas em uma (CONCLUIDO)

## Atualizacoes Recentes (27/06/2026)
- Artigo 14: Unificadas pastas "14-Discurso-Custo-Brasil-Analise-Conteudo-Discursos" e "14-Discurso-Custo-Brasil-Politica-Industrial-Narrativas-Pratica"
- PNCP: Testado endpoint `/contratacoes/publicacao` com `codigoModalidadeContratacao` - erro 422 persiste
- Campo data Inicial deve estar em formato específico (API indica "deve estar no...")
