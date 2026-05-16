```markdown
# 🔍 Guia Completo de Pesquisa Acadêmica — APIs, Plataformas e Estratégias

---

## Sumário

1. [Visão Geral e Estratégia de Pesquisa](#1-visão-geral-e-estratégia-de-pesquisa)
2. [APIs Acadêmicas Gratuitas](#2-apis-acadêmicas-gratuitas)
3. [Plataformas Acadêmicas com Acesso Web](#3-plataformas-acadêmicas-com-acesso-web)
4. [Ferramentas de Descoberta com IA](#4-ferramentas-de-descoberta-com-ia)
5. [Bases Brasileiras e em Português](#5-bases-brasileiras-e-em-português)
6. [Pesquisa em Redes Sociais (APIs)](#6-pesquisa-em-redes-sociais-apis)
7. [Pesquisa em Sites de Notícias (APIs)](#7-pesquisa-em-sites-de-notícias-apis)
8. [Pesquisa Geral na Web (Google e Outros)](#8-pesquisa-geral-na-web-google-e-outros)
9. [Estratégias de Busca Avançada](#9-estratégias-de-busca-avançada)
10. [Fluxo Completo de Pesquisa para o App](#10-fluxo-completo-de-pesquisa-para-o-app)
11. [Implementação no Paper Builder](#11-implementação-no-paper-builder)

---

## 1. Visão Geral e Estratégia de Pesquisa

### 1.1 Tipos de Fontes por Necessidade

| Necessidade | Fonte Ideal | APIs/Plataformas |
|---|---|---|
| Artigos científicos revisados por pares | Bases acadêmicas | Semantic Scholar, OpenAlex, CrossRef, PubMed |
| Artigos brasileiros | Bases nacionais | SciELO, SPELL, BDTD, CAPES |
| Artigos em acesso aberto | Repositórios abertos | CORE, Unpaywall, DOAJ, arXiv |
| Mapeamento de conexões entre papers | Ferramentas visuais | Connected Papers, Litmaps, Research Rabbit |
| Respostas baseadas em evidências | IA acadêmica | Consensus, Elicit |
| Falas e opiniões de pessoas | Redes sociais | Twitter/X API, Reddit API, YouTube API |
| Dados de mídia e notícias | Portais de notícias | NewsAPI, GDELT, Google News |
| Pesquisa ampla e exploratória | Buscadores gerais | Google Scholar, Google Custom Search |

### 1.2 Ordem Recomendada de Pesquisa

```

1º → Google Scholar / Semantic Scholar (visão geral)
2º → OpenAlex / CrossRef (dados estruturados)
3º → SciELO / SPELL (artigos brasileiros)
4º → Connected Papers / Litmaps (descobrir papers relacionados)
5º → Consensus / Elicit (respostas baseadas em evidências)
6º → CORE / Unpaywall (acesso aberto / PDFs gratuitos)
7º → PubMed / arXiv (áreas específicas)
8º → Redes Sociais (falas, opiniões, tendências)
9º → News APIs (cobertura midiática, dados recentes)

```

---

## 2. APIs Acadêmicas Gratuitas

### 2.1 Semantic Scholar API ⭐ (RECOMENDADA)

> **A melhor API gratuita para pesquisa acadêmica.**
> Mantida pelo Allen Institute for AI. Acesso a mais de 200 milhões de papers.

| Info | Detalhe |
|---|---|
| **URL Base** | `https://api.semanticscholar.org/graph/v1` |
| **Autenticação** | Opcional (API Key gratuita para mais requests) |
| **Rate Limit** | 100 requests/5 min (sem key) / 1 request/seg (com key) |
| **Dados** | Título, abstract, autores, citações, referências, DOI, PDF links |
| **Cobertura** | 200M+ papers, todas as áreas |
| **Documentação** | https://api.semanticscholar.org/ |

**Endpoints principais:**

```bash
# Buscar papers por termo
GET https://api.semanticscholar.org/graph/v1/paper/search
    ?query=inteligencia+artificial+educacao
    &limit=10
    &offset=0
    &fields=title,abstract,authors,year,citationCount,url,openAccessPdf

# Detalhes de um paper específico (por DOI, ArXiv ID, etc.)
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}
    ?fields=title,abstract,authors,year,references,citations,tldr

# Buscar citações de um paper
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations
    ?fields=title,authors,year
    &limit=50

# Buscar referências de um paper
GET https://api.semanticscholar.org/graph/v1/paper/{paper_id}/references
    ?fields=title,authors,year
    &limit=50

# Buscar autor
GET https://api.semanticscholar.org/graph/v1/author/search
    ?query=João+Silva
    &fields=name,paperCount,citationCount,papers

# Recomendações de papers similares
POST https://api.semanticscholar.org/recommendations/v1/papers/
    Body: { "positivePaperIds": ["paper_id_1", "paper_id_2"] }
```

**Exemplo de resposta:**

```json
{
  "total": 15432,
  "offset": 0,
  "data": [
    {
      "paperId": "abc123",
      "title": "Impact of Generative AI on Higher Education",
      "abstract": "This study examines...",
      "year": 2023,
      "citationCount": 45,
      "authors": [
        { "authorId": "456", "name": "João Silva" }
      ],
      "openAccessPdf": {
        "url": "https://arxiv.org/pdf/2301.xxxxx.pdf"
      },
      "tldr": {
        "text": "This paper demonstrates that generative AI improves..."
      }
    }
  ]
}
```

**Implementação no App:**

```javascript
// services/semanticScholar.js

const BASE_URL = 'https://api.semanticscholar.org/graph/v1';

export async function searchPapers(query, limit = 10, offset = 0) {
  const fields = 'title,abstract,authors,year,citationCount,url,openAccessPdf,tldr';
  const response = await fetch(
    `${BASE_URL}/paper/search?query=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}&fields=${fields}`,
    {
      headers: {
        // Opcional: 'x-api-key': 'SUA_API_KEY'
      }
    }
  );
  return response.json();
}

export async function getPaperDetails(paperId) {
  const fields = 'title,abstract,authors,year,references,citations,tldr,openAccessPdf';
  const response = await fetch(
    `${BASE_URL}/paper/${paperId}?fields=${fields}`
  );
  return response.json();
}

export async function getReferences(paperId, limit = 50) {
  const fields = 'title,authors,year,citationCount';
  const response = await fetch(
    `${BASE_URL}/paper/${paperId}/references?fields=${fields}&limit=${limit}`
  );
  return response.json();
}

export async function getCitations(paperId, limit = 50) {
  const fields = 'title,authors,year,citationCount';
  const response = await fetch(
    `${BASE_URL}/paper/${paperId}/citations?fields=${fields}&limit=${limit}`
  );
  return response.json();
}

export async function getSimilarPapers(paperIds) {
  const response = await fetch(
    'https://api.semanticscholar.org/recommendations/v1/papers/',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ positivePaperIds: paperIds })
    }
  );
  return response.json();
}
```

---

### 2.2 OpenAlex API ⭐ (RECOMENDADA)

> **Substituto do Microsoft Academic. 100% gratuita, sem necessidade de API key.**
> Mais de 250 milhões de trabalhos acadêmicos indexados.

| Info                     | Detalhe                                         |
| ------------------------ | ----------------------------------------------- |
| **URL Base**       | `https://api.openalex.org`                    |
| **Autenticação** | Nenhuma (email no header para "polite pool")    |
| **Rate Limit**     | 100K requests/dia (com email) / 10 requests/seg |
| **Dados**          | Works, Authors, Institutions, Venues, Concepts  |
| **Cobertura**      | 250M+ works                                     |
| **Documentação** | https://docs.openalex.org/                      |

**Endpoints principais:**

```bash
# Buscar papers (works)
GET https://api.openalex.org/works
    ?search=inteligencia artificial educacao
    &filter=from_publication_date:2020-01-01
    &sort=cited_by_count:desc
    &per_page=10
    &mailto=seuemail@email.com

# Buscar com filtros avançados
GET https://api.openalex.org/works
    ?filter=default.search:artificial intelligence education,
            from_publication_date:2020-01-01,
            language:pt,
            is_oa:true,
            type:article
    &sort=publication_date:desc

# Detalhes de um work específico
GET https://api.openalex.org/works/{openalex_id}

# Buscar por DOI
GET https://api.openalex.org/works/doi:10.1234/xxxxx

# Buscar autores
GET https://api.openalex.org/authors
    ?search=João Silva
    &filter=last_known_institution.country_code:BR

# Buscar instituições
GET https://api.openalex.org/institutions
    ?search=Universidade de São Paulo

# Buscar conceitos/temas
GET https://api.openalex.org/concepts
    ?search=artificial intelligence

# Agrupar resultados (analytics)
GET https://api.openalex.org/works
    ?filter=default.search:AI education
    &group_by=publication_year
```

**Filtros úteis do OpenAlex:**

```
from_publication_date:2020-01-01     → A partir de 2020
language:pt                          → Apenas português
language:en                          → Apenas inglês
is_oa:true                          → Apenas acesso aberto
type:article                        → Apenas artigos
type:book-chapter                   → Apenas capítulos
has_doi:true                        → Apenas com DOI
cited_by_count:>50                  → Mais de 50 citações
authorships.countries:BR            → Autores do Brasil
authorships.institutions.id:I123    → Instituição específica
concepts.id:C12345                  → Conceito específico
```

**Implementação no App:**

```javascript
// services/openAlex.js

const BASE_URL = 'https://api.openalex.org';
const EMAIL = 'seuemail@email.com';

export async function searchWorks(query, options = {}) {
  const {
    fromDate = '2019-01-01',
    language = null,
    openAccess = false,
    sort = 'cited_by_count:desc',
    perPage = 10,
    page = 1
  } = options;

  let filters = [`default.search:${query}`, `from_publication_date:${fromDate}`];
  if (language) filters.push(`language:${language}`);
  if (openAccess) filters.push('is_oa:true');

  const filterStr = filters.join(',');
  const url = `${BASE_URL}/works?filter=${encodeURIComponent(filterStr)}&sort=${sort}&per_page=${perPage}&page=${page}&mailto=${EMAIL}`;

  const response = await fetch(url);
  return response.json();
}

export async function getWorkByDoi(doi) {
  const response = await fetch(
    `${BASE_URL}/works/doi:${doi}?mailto=${EMAIL}`
  );
  return response.json();
}

export async function searchAuthors(name, country = null) {
  let url = `${BASE_URL}/authors?search=${encodeURIComponent(name)}&mailto=${EMAIL}`;
  if (country) url += `&filter=last_known_institution.country_code:${country}`;
  const response = await fetch(url);
  return response.json();
}

export async function getRelatedWorks(workId) {
  const response = await fetch(
    `${BASE_URL}/works/${workId}?mailto=${EMAIL}`
  );
  const data = await response.json();
  return data.related_works || [];
}

export async function getTrendingByYear(query) {
  const url = `${BASE_URL}/works?filter=default.search:${encodeURIComponent(query)}&group_by=publication_year&mailto=${EMAIL}`;
  const response = await fetch(url);
  return response.json();
}
```

---

### 2.3 CrossRef API

> **API oficial dos DOIs. Excelente para metadados de publicações.**

| Info                     | Detalhe                                        |
| ------------------------ | ---------------------------------------------- |
| **URL Base**       | `https://api.crossref.org`                   |
| **Autenticação** | Nenhuma (email no header recomendado)          |
| **Rate Limit**     | 50 requests/seg (com email)                    |
| **Dados**          | DOI, metadados, citações, editora, ISSN      |
| **Cobertura**      | 130M+ registros                                |
| **Documentação** | https://api.crossref.org/swagger-ui/index.html |

**Endpoints principais:**

```bash
# Buscar works
GET https://api.crossref.org/works
    ?query=artificial+intelligence+education
    &rows=10
    &offset=0
    &sort=relevance
    &order=desc
    &filter=from-pub-date:2020,language:pt
    &mailto=seuemail@email.com

# Buscar por DOI
GET https://api.crossref.org/works/10.1234/xxxxx

# Buscar em periódico específico
GET https://api.crossref.org/journals/{issn}/works
    ?query=artificial intelligence
    &rows=10

# Buscar por autor
GET https://api.crossref.org/works
    ?query.author=João+Silva
    &rows=10
```

**Filtros do CrossRef:**

```
from-pub-date:2020              → A partir de 2020
until-pub-date:2024             → Até 2024
language:pt                     → Português
type:journal-article            → Artigos de periódico
has-abstract:true               → Apenas com abstract
has-references:true             → Apenas com referências
is-open-access:true             → Acesso aberto (via Unpaywall)
has-orcid:true                  → Autor com ORCID
```

**Implementação:**

```javascript
// services/crossref.js

const BASE_URL = 'https://api.crossref.org';
const EMAIL = 'seuemail@email.com';

export async function searchCrossRef(query, options = {}) {
  const {
    rows = 10,
    offset = 0,
    fromDate = '2020',
    sort = 'relevance'
  } = options;

  const url = `${BASE_URL}/works?query=${encodeURIComponent(query)}&rows=${rows}&offset=${offset}&sort=${sort}&filter=from-pub-date:${fromDate}&mailto=${EMAIL}`;

  const response = await fetch(url);
  const data = await response.json();
  return data.message;
}

export async function getByDoi(doi) {
  const response = await fetch(`${BASE_URL}/works/${doi}?mailto=${EMAIL}`);
  const data = await response.json();
  return data.message;
}

export async function searchByAuthor(authorName, rows = 10) {
  const url = `${BASE_URL}/works?query.author=${encodeURIComponent(authorName)}&rows=${rows}&mailto=${EMAIL}`;
  const response = await fetch(url);
  const data = await response.json();
  return data.message;
}
```

---

### 2.4 CORE API

> **Maior coleção de artigos em acesso aberto do mundo. Acesso a PDFs gratuitos.**

| Info                     | Detalhe                                  |
| ------------------------ | ---------------------------------------- |
| **URL Base**       | `https://api.core.ac.uk/v3`            |
| **Autenticação** | API Key gratuita (registro obrigatório) |
| **Rate Limit**     | 10 requests/seg                          |
| **Dados**          | Texto completo, PDFs, metadados          |
| **Cobertura**      | 300M+ artigos, 250M+ em acesso aberto    |
| **Documentação** | https://api.core.ac.uk/docs/v3           |
| **Registro**       | https://core.ac.uk/register              |

**Endpoints:**

```bash
# Buscar artigos
GET https://api.core.ac.uk/v3/search/works
    ?q=artificial intelligence education
    &limit=10
    &offset=0
    Headers: Authorization: Bearer {API_KEY}

# Buscar com filtros
GET https://api.core.ac.uk/v3/search/works
    ?q=inteligencia artificial educacao
    &limit=10
    &filter=yearPublished>=2020,language=pt

# Detalhes de um artigo
GET https://api.core.ac.uk/v3/works/{core_id}

# Download do PDF/texto completo
GET https://api.core.ac.uk/v3/works/{core_id}/download
```

**Implementação:**

```javascript
// services/core.js

const BASE_URL = 'https://api.core.ac.uk/v3';
const API_KEY = process.env.CORE_API_KEY;

export async function searchCore(query, options = {}) {
  const { limit = 10, offset = 0, yearFrom = 2020, language = null } = options;

  let filters = [`yearPublished>=${yearFrom}`];
  if (language) filters.push(`language=${language}`);

  const url = `${BASE_URL}/search/works?q=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}&filter=${filters.join(',')}`;

  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${API_KEY}` }
  });
  return response.json();
}

export async function downloadFullText(coreId) {
  const response = await fetch(`${BASE_URL}/works/${coreId}/download`, {
    headers: { 'Authorization': `Bearer ${API_KEY}` }
  });
  return response;
}
```

---

### 2.5 Unpaywall API

> **Encontra versões gratuitas (acesso aberto) de artigos por DOI.**
> Perfeita para complementar buscas no CrossRef ou OpenAlex.

| Info                     | Detalhe                                |
| ------------------------ | -------------------------------------- |
| **URL Base**       | `https://api.unpaywall.org/v2`       |
| **Autenticação** | Email como parâmetro                  |
| **Rate Limit**     | 100K requests/dia                      |
| **Dados**          | Links para versões OA, tipo de acesso |
| **Documentação** | https://unpaywall.org/products/api     |

```bash
# Verificar se um paper tem versão aberta
GET https://api.unpaywall.org/v2/{doi}
    ?email=seuemail@email.com

# Exemplo
GET https://api.unpaywall.org/v2/10.1038/nature12373
    ?email=seuemail@email.com
```

**Resposta:**

```json
{
  "doi": "10.1038/nature12373",
  "title": "...",
  "is_oa": true,
  "best_oa_location": {
    "url": "https://europepmc.org/articles/pmc3814466",
    "url_for_pdf": "https://europepmc.org/articles/pmc3814466?pdf=render",
    "license": "cc-by",
    "version": "publishedVersion"
  }
}
```

**Implementação:**

```javascript
// services/unpaywall.js

const BASE_URL = 'https://api.unpaywall.org/v2';
const EMAIL = 'seuemail@email.com';

export async function findOpenAccess(doi) {
  const response = await fetch(`${BASE_URL}/${doi}?email=${EMAIL}`);
  const data = await response.json();
  
  return {
    isOpenAccess: data.is_oa,
    pdfUrl: data.best_oa_location?.url_for_pdf || null,
    webUrl: data.best_oa_location?.url || null,
    license: data.best_oa_location?.license || null
  };
}

// Buscar PDF gratuito para uma lista de DOIs
export async function findOpenAccessBatch(dois) {
  const results = [];
  for (const doi of dois) {
    try {
      const result = await findOpenAccess(doi);
      results.push({ doi, ...result });
      await new Promise(r => setTimeout(r, 100)); // Rate limit
    } catch (e) {
      results.push({ doi, isOpenAccess: false, pdfUrl: null });
    }
  }
  return results;
}
```

---

### 2.6 PubMed / NCBI API

> **Essencial para pesquisas em saúde, medicina e ciências biológicas.**

| Info                     | Detalhe                                           |
| ------------------------ | ------------------------------------------------- |
| **URL Base**       | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils` |
| **Autenticação** | API Key gratuita (opcional, mas recomendada)      |
| **Rate Limit**     | 3 req/seg (sem key) / 10 req/seg (com key)        |
| **Cobertura**      | 35M+ artigos biomédicos                          |
| **Documentação** | https://www.ncbi.nlm.nih.gov/books/NBK25500/      |

```bash
# Buscar IDs de artigos
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
    ?db=pubmed
    &term=artificial+intelligence+education
    &retmax=10
    &retmode=json
    &sort=relevance
    &api_key={API_KEY}

# Obter detalhes dos artigos
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
    ?db=pubmed
    &id=12345678,87654321
    &retmode=xml

# Obter resumos (abstracts)
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi
    ?db=pubmed
    &id=12345678,87654321
    &retmode=json
```

**Implementação:**

```javascript
// services/pubmed.js

const BASE_URL = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils';
const API_KEY = process.env.PUBMED_API_KEY || '';

export async function searchPubMed(query, maxResults = 10) {
  // Passo 1: Buscar IDs
  const searchUrl = `${BASE_URL}/esearch.fcgi?db=pubmed&term=${encodeURIComponent(query)}&retmax=${maxResults}&retmode=json&sort=relevance&api_key=${API_KEY}`;
  
  const searchResponse = await fetch(searchUrl);
  const searchData = await searchResponse.json();
  const ids = searchData.esearchresult.idlist;
  
  if (ids.length === 0) return [];
  
  // Passo 2: Obter detalhes
  const summaryUrl = `${BASE_URL}/esummary.fcgi?db=pubmed&id=${ids.join(',')}&retmode=json&api_key=${API_KEY}`;
  
  const summaryResponse = await fetch(summaryUrl);
  const summaryData = await summaryResponse.json();
  
  return Object.values(summaryData.result).filter(item => item.uid);
}
```

---

### 2.7 arXiv API

> **Preprints de física, matemática, ciência da computação e áreas correlatas.**

| Info                     | Detalhe                          |
| ------------------------ | -------------------------------- |
| **URL Base**       | `http://export.arxiv.org/api`  |
| **Autenticação** | Nenhuma                          |
| **Rate Limit**     | 1 request/3 seg                  |
| **Cobertura**      | 2M+ preprints                    |
| **Documentação** | https://info.arxiv.org/help/api/ |

```bash
# Buscar artigos
GET http://export.arxiv.org/api/query
    ?search_query=all:artificial+intelligence+AND+all:education
    &start=0
    &max_results=10
    &sortBy=submittedDate
    &sortOrder=descending
```

**Implementação:**

```javascript
// services/arxiv.js

export async function searchArxiv(query, maxResults = 10) {
  const url = `http://export.arxiv.org/api/query?search_query=all:${encodeURIComponent(query)}&start=0&max_results=${maxResults}&sortBy=submittedDate&sortOrder=descending`;
  
  const response = await fetch(url);
  const xmlText = await response.text();
  
  // Parser XML → JSON (usar biblioteca como fast-xml-parser)
  // Retorna: title, summary, authors, published, links (PDF)
  return parseArxivXml(xmlText);
}
```

---

### 2.8 DOAJ API (Directory of Open Access Journals)

> **Diretório de periódicos em acesso aberto verificados.**

| Info                     | Detalhe                         |
| ------------------------ | ------------------------------- |
| **URL Base**       | `https://doaj.org/api`        |
| **Autenticação** | Nenhuma (API Key para escrita)  |
| **Rate Limit**     | Sem limite especificado         |
| **Cobertura**      | 9M+ artigos de 19K+ periódicos |
| **Documentação** | https://doaj.org/api/docs       |

```bash
# Buscar artigos
GET https://doaj.org/api/search/articles/inteligencia%20artificial%20educacao
    ?page=1
    &pageSize=10

# Buscar periódicos
GET https://doaj.org/api/search/journals/education%20technology
    ?page=1
    &pageSize=10
```

---

## 3. Plataformas Acadêmicas com Acesso Web

### 3.1 Google Scholar (Scraping Controlado)

> **Maior buscador acadêmico do mundo. Não possui API oficial.**
> É necessário usar scraping ou bibliotecas que simulam acesso.

| Info                   | Detalhe                                      |
| ---------------------- | -------------------------------------------- |
| **URL**          | `https://scholar.google.com`               |
| **API Oficial**  | ❌ Não existe                               |
| **Alternativas** | SerpAPI (paga), scholarly (Python), scraping |
| **Cobertura**    | 389M+ documentos                             |

**Opção 1 — SerpAPI (paga, mas tem free tier):**

```bash
GET https://serpapi.com/search.json
    ?engine=google_scholar
    &q=inteligencia artificial educacao
    &hl=pt-br
    &num=10
    &api_key={SERPAPI_KEY}
```

**Opção 2 — Google Scholar via URL direta (para o app abrir no navegador):**

```javascript
// services/googleScholar.js

export function buildGoogleScholarUrl(query, options = {}) {
  const {
    yearFrom = null,
    yearTo = null,
    language = 'pt',
    sortByDate = false
  } = options;

  let url = `https://scholar.google.com/scholar?q=${encodeURIComponent(query)}&hl=${language}`;
  
  if (yearFrom) url += `&as_ylo=${yearFrom}`;
  if (yearTo) url += `&as_yhi=${yearTo}`;
  if (sortByDate) url += '&scisbd=1';
  
  return url;
}

// Abre no navegador do usuário
export function openGoogleScholar(query, options) {
  const url = buildGoogleScholarUrl(query, options);
  window.open(url, '_blank');
}
```

**Dica de busca avançada no Google Scholar:**

```
# Busca exata
"inteligência artificial" "educação superior"

# Autor específico
author:"João Silva"

# Em periódico específico
source:"Revista Brasileira de Educação"

# Excluir termos
inteligência artificial educação -"ensino médio"

# Intervalo de anos (via URL)
&as_ylo=2020&as_yhi=2024
```

---

### 3.2 Web of Science

> **Uma das bases mais prestigiadas. Acesso institucional geralmente necessário.**

| Info                           | Detalhe                                          |
| ------------------------------ | ------------------------------------------------ |
| **URL**                  | `https://www.webofscience.com`                 |
| **API**                  | Web of Science API Expanded (paga/institucional) |
| **Alternativa gratuita** | Busca manual ou OpenAlex (indexa dados do WoS)   |
| **Cobertura**            | 171M+ registros                                  |

```bash
# API (requer credenciais institucionais)
GET https://api.clarivate.com/apis/wos-starter/v1/documents
    ?q=TS=(artificial intelligence education)
    &limit=10
    &page=1
    Headers: X-ApiKey: {WOS_API_KEY}
```

**Alternativa prática:** Usar OpenAlex com filtro de fonte indexada no WoS.

---

### 3.3 Scopus

> **Base da Elsevier. Excelente cobertura, mas acesso institucional necessário.**

| Info                | Detalhe                                                                |
| ------------------- | ---------------------------------------------------------------------- |
| **URL**       | `https://www.scopus.com`                                             |
| **API**       | Scopus Search API (requer Elsevier Developer Key)                      |
| **API Key**   | Gratuita para fins acadêmicos (registro em https://dev.elsevier.com/) |
| **Cobertura** | 91M+ registros                                                         |

```bash
GET https://api.elsevier.com/content/search/scopus
    ?query=TITLE-ABS-KEY(artificial intelligence education)
    &count=10
    &start=0
    &sort=citedby-count
    Headers: X-ELS-APIKey: {SCOPUS_API_KEY}
             Accept: application/json
```

---

## 4. Ferramentas de Descoberta com IA

### 4.1 Consensus

> **Motor de busca que usa IA para responder perguntas com base em papers.**
> Ideal para validar hipóteses e encontrar evidências.

| Info                  | Detalhe                                                |
| --------------------- | ------------------------------------------------------ |
| **URL**         | `https://consensus.app`                              |
| **API**         | ❌ Não possui API pública                            |
| **Uso**         | Interface web gratuita (limite de buscas/dia)          |
| **Diferencial** | Responde SIM/NÃO com base em evidências científicas |
| **Cobertura**   | 200M+ papers                                           |

**Como usar no fluxo do app:**

```javascript
// Abrir Consensus no navegador com a pergunta de pesquisa
export function openConsensus(researchQuestion) {
  const url = `https://consensus.app/results/?q=${encodeURIComponent(researchQuestion)}`;
  window.open(url, '_blank');
}

// Exemplo de perguntas para Consensus:
// "Does artificial intelligence improve student performance?"
// "Is generative AI effective for education?"
// "What are the risks of AI in higher education?"
```

**Dica:** O Consensus funciona melhor com perguntas em inglês no formato:

- "Does X cause Y?"
- "Is X effective for Y?"
- "What is the impact of X on Y?"

---

### 4.2 Connected Papers

> **Gera grafos visuais de papers relacionados a partir de um paper semente.**
> Perfeito para descobrir papers que você não encontraria por busca textual.

| Info                  | Detalhe                                       |
| --------------------- | --------------------------------------------- |
| **URL**         | `https://www.connectedpapers.com`           |
| **API**         | ❌ Não possui API pública                   |
| **Uso**         | Interface web (5 grafos gratuitos/mês)       |
| **Diferencial** | Visualização de rede de papers relacionados |
| **Base**        | Semantic Scholar                              |

**Como usar no fluxo do app:**

```javascript
// Abrir Connected Papers para um DOI ou título
export function openConnectedPapers(paperIdentifier) {
  // Pode ser DOI, ArXiv ID, ou URL do Semantic Scholar
  const url = `https://www.connectedpapers.com/search?q=${encodeURIComponent(paperIdentifier)}`;
  window.open(url, '_blank');
}

// Alternativa: usar a API do Semantic Scholar para simular
// Buscar referências e citações de um paper = rede de conexões
export async function buildPaperNetwork(paperId) {
  const refs = await semanticScholar.getReferences(paperId);
  const cites = await semanticScholar.getCitations(paperId);
  
  return {
    seed: paperId,
    references: refs,
    citations: cites,
    network: [...refs, ...cites]
  };
}
```

---

### 4.3 Elicit

> **Assistente de pesquisa com IA. Extrai dados de papers automaticamente.**

| Info                  | Detalhe                                                        |
| --------------------- | -------------------------------------------------------------- |
| **URL**         | `https://elicit.com`                                         |
| **API**         | ❌ Não possui API pública                                    |
| **Uso**         | Interface web (créditos gratuitos limitados)                  |
| **Diferencial** | Extrai dados estruturados de papers, cria tabelas comparativas |

```javascript
export function openElicit(query) {
  const url = `https://elicit.com/search?q=${encodeURIComponent(query)}`;
  window.open(url, '_blank');
}
```

---

### 4.4 Research Rabbit

> **"Spotify de papers" — descobre artigos baseado nos que você já tem.**
> 100% gratuito.

| Info                  | Detalhe                                                 |
| --------------------- | ------------------------------------------------------- |
| **URL**         | `https://www.researchrabbit.ai`                       |
| **API**         | ❌ Não possui API pública                             |
| **Uso**         | Interface web gratuita                                  |
| **Diferencial** | Recomendações personalizadas, alertas de novos papers |

---

### 4.5 Litmaps

> **Mapas visuais de literatura com timeline. Excelente para revisão sistemática.**

| Info                  | Detalhe                              |
| --------------------- | ------------------------------------ |
| **URL**         | `https://www.litmaps.com`          |
| **API**         | ❌ Não possui API pública          |
| **Uso**         | Free tier com limitações           |
| **Diferencial** | Timeline visual + mapa de citações |

---

## 5. Bases Brasileiras e em Português

### 5.1 SciELO

> **Principal base de periódicos científicos da América Latina.**

| Info                | Detalhe                           |
| ------------------- | --------------------------------- |
| **URL**       | `https://scielo.org`            |
| **API**       | SciELO API (REST)                 |
| **URL API**   | `https://search.scielo.org`     |
| **Cobertura** | 900K+ artigos, 1.800+ periódicos |
| **Idiomas**   | Português, Espanhol, Inglês     |

```bash
# Busca via interface (para abrir no navegador)
https://search.scielo.org/?q=inteligencia+artificial+educacao
    &lang=pt
    &filter[year_cluster][]=2023
    &filter[year_cluster][]=2024

# API SciELO (XML)
GET https://articlemeta.scielo.org/api/v1/article
    ?collection=scl
    &code=S0102-311X2023000100001

# Buscar periódicos
GET https://articlemeta.scielo.org/api/v1/journal
    ?collection=scl
    &issn=0102-311X
```

**Implementação:**

```javascript
// services/scielo.js

export function buildSciELOUrl(query, options = {}) {
  const { lang = 'pt', yearFrom = null, yearTo = null } = options;
  
  let url = `https://search.scielo.org/?q=${encodeURIComponent(query)}&lang=${lang}`;
  
  if (yearFrom) url += `&filter[year_cluster][]=${yearFrom}`;
  if (yearTo) url += `&filter[year_cluster][]=${yearTo}`;
  
  return url;
}

export function openSciELO(query, options) {
  window.open(buildSciELOUrl(query, options), '_blank');
}
```

---

### 5.2 SPELL (Scientific Periodicals Electronic Library)

> **Base brasileira focada em Administração, Contabilidade, Economia e Engenharia.**

| Info                | Detalhe                                 |
| ------------------- | --------------------------------------- |
| **URL**       | `https://www.spell.org.br`            |
| **API**       | ❌ Não possui API pública             |
| **Uso**       | Busca via interface web                 |
| **Cobertura** | 70K+ artigos de periódicos brasileiros |

```javascript
// services/spell.js

export function buildSpellUrl(query, options = {}) {
  const { yearFrom = null, yearTo = null, area = null } = options;
  
  let url = `https://www.spell.org.br/documentos/busca?termo=${encodeURIComponent(query)}`;
  
  if (yearFrom) url += `&ano_inicio=${yearFrom}`;
  if (yearTo) url += `&ano_fim=${yearTo}`;
  if (area) url += `&area=${encodeURIComponent(area)}`;
  
  return url;
}

export function openSpell(query, options) {
  window.open(buildSpellUrl(query, options), '_blank');
}
```

---

### 5.3 Portal de Periódicos CAPES

> **Maior portal de acesso a produção científica internacional no Brasil.**
> Acesso gratuito via IP de universidades públicas.

| Info             | Detalhe                                                             |
| ---------------- | ------------------------------------------------------------------- |
| **URL**    | `https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br` |
| **API**    | ❌ Não possui API pública                                         |
| **Acesso** | Via rede de universidades ou CAFe                                   |

```javascript
export function openCAPES(query) {
  const url = `https://www-periodicos-capes-gov-br.ezl.periodicos.capes.gov.br/index.php/acervo/buscador.html?q=${encodeURIComponent(query)}`;
  window.open(url, '_blank');
}
```

---

### 5.4 BDTD (Biblioteca Digital Brasileira de Teses e Dissertações)

> **Repositório nacional de teses e dissertações brasileiras.**

| Info                | Detalhe                      |
| ------------------- | ---------------------------- |
| **URL**       | `https://bdtd.ibict.br`    |
| **API**       | OAI-PMH                      |
| **Cobertura** | 800K+ teses e dissertações |

```bash
# OAI-PMH
GET https://bdtd.ibict.br/vufind/OAI/Server
    ?verb=ListRecords
    &metadataPrefix=oai_dc
    &set=bdtd

# Busca web
https://bdtd.ibict.br/vufind/Search/Results
    ?lookfor=inteligencia+artificial+educacao
    &type=AllFields
```

---

### 5.5 Catálogo de Teses e Dissertações CAPES

```javascript
export function openCatalogoCAPES(query) {
  const url = `https://catalogodeteses.capes.gov.br/catalogo-teses/#!/?q=${encodeURIComponent(query)}`;
  window.open(url, '_blank');
}
```

---

## 6. Pesquisa em Redes Sociais (APIs)

> **Para coletar falas, opiniões, tendências e percepções do público
> sobre o tema de pesquisa. Essencial para pesquisas qualitativas e
> estudos de percepção social.**

### 6.1 Twitter/X API

> **Ideal para capturar opiniões públicas, tendências e discurso social.**

| Info                     | Detalhe                                           |
| ------------------------ | ------------------------------------------------- |
| **URL Base**       | `https://api.twitter.com/2`                     |
| **Autenticação** | OAuth 2.0 (Bearer Token)                          |
| **Plano gratuito** | Free tier: apenas POST tweets + 1 regra de stream |
| **Plano Basic**    | $100/mês: 10K tweets GET/mês                    |
| **Documentação** | https://developer.twitter.com/en/docs             |

```bash
# Buscar tweets recentes (requer Basic plan ou Academic)
GET https://api.twitter.com/2/tweets/search/recent
    ?query=inteligencia artificial educacao -is:retweet lang:pt
    &max_results=100
    &tweet.fields=created_at,public_metrics,author_id,text
    &expansions=author_id
    &user.fields=name,username,verified
    Headers: Authorization: Bearer {BEARER_TOKEN}
```

**Operadores de busca úteis:**

```
"inteligência artificial" educação    → Busca exata + termo
lang:pt                               → Apenas português
-is:retweet                           → Excluir retweets
is:verified                           → Apenas verificados
has:links                             → Com links
from:usuario                          → De usuário específico
(IA OR "inteligência artificial")     → Operador OR
min_retweets:100                      → Mínimo de retweets
```

**Implementação:**

```javascript
// services/twitter.js

const BASE_URL = 'https://api.twitter.com/2';
const BEARER_TOKEN = process.env.TWITTER_BEARER_TOKEN;

export async function searchTweets(query, options = {}) {
  const { maxResults = 100, language = 'pt' } = options;
  
  const searchQuery = `${query} -is:retweet lang:${language}`;
  const url = `${BASE_URL}/tweets/search/recent?query=${encodeURIComponent(searchQuery)}&max_results=${maxResults}&tweet.fields=created_at,public_metrics,author_id,text&expansions=author_id&user.fields=name,username`;
  
  const response = await fetch(url, {
    headers: { 'Authorization': `Bearer ${BEARER_TOKEN}` }
  });
  return response.json();
}
```

**Alternativa gratuita — Nitter (frontend alternativo do Twitter):**

```javascript
export function openNitterSearch(query) {
  const url = `https://nitter.net/search?f=tweets&q=${encodeURIComponent(query)}&since=&until=&near=`;
  window.open(url, '_blank');
}
```

---

### 6.2 Reddit API

> **Excelente para discussões aprofundadas, opiniões e percepções em comunidades.**
> API gratuita com limites generosos.

| Info                     | Detalhe                                           |
| ------------------------ | ------------------------------------------------- |
| **URL Base**       | `https://oauth.reddit.com`                      |
| **Autenticação** | OAuth2 (app gratuito)                             |
| **Rate Limit**     | 60 requests/minuto                                |
| **Alternativa**    | Pushshift API (histórico), old.reddit.com/search |
| **Documentação** | https://www.reddit.com/dev/api/                   |

```bash
# Buscar posts (com OAuth)
GET https://oauth.reddit.com/search
    ?q=artificial intelligence education
    &sort=relevance
    &t=year
    &limit=25
    &type=link
    Headers: Authorization: Bearer {ACCESS_TOKEN}
             User-Agent: PaperBuilder/1.0

# Buscar em subreddit específico
GET https://oauth.reddit.com/r/MachineLearning/search
    ?q=education
    &restrict_sr=true
    &sort=relevance
    &t=year

# Sem autenticação (JSON trick)
GET https://www.reddit.com/search.json
    ?q=artificial+intelligence+education
    &sort=relevance
    &t=year
    &limit=25
```

**Implementação (sem OAuth, usando .json):**

```javascript
// services/reddit.js

export async function searchReddit(query, options = {}) {
  const { sort = 'relevance', time = 'year', limit = 25, subreddit = null } = options;
  
  let url;
  if (subreddit) {
    url = `https://www.reddit.com/r/${subreddit}/search.json?q=${encodeURIComponent(query)}&restrict_sr=true&sort=${sort}&t=${time}&limit=${limit}`;
  } else {
    url = `https://www.reddit.com/search.json?q=${encodeURIComponent(query)}&sort=${sort}&t=${time}&limit=${limit}`;
  }
  
  const response = await fetch(url, {
    headers: { 'User-Agent': 'PaperBuilder/1.0' }
  });
  const data = await response.json();
  
  return data.data.children.map(post => ({
    title: post.data.title,
    text: post.data.selftext,
    author: post.data.author,
    subreddit: post.data.subreddit,
    score: post.data.score,
    numComments: post.data.num_comments,
    url: `https://reddit.com${post.data.permalink}`,
    created: new Date(post.data.created_utc * 1000)
  }));
}

// Subreddits acadêmicos relevantes
const ACADEMIC_SUBREDDITS = [
  'MachineLearning',
  'ArtificialIntelligence',
  'science',
  'academia',
  'GradSchool',
  'datasets',
  'datascience',
  'education',
  'highereducation'
];
```

---

### 6.3 YouTube Data API

> **Para encontrar falas de especialistas, palestras, aulas e entrevistas.**

| Info                     | Detalhe                                    |
| ------------------------ | ------------------------------------------ |
| **URL Base**       | `https://www.googleapis.com/youtube/v3`  |
| **Autenticação** | Google API Key (gratuita)                  |
| **Quota**          | 10.000 unidades/dia (busca = 100 unidades) |
| **Documentação** | https://developers.google.com/youtube/v3   |

```bash
# Buscar vídeos
GET https://www.googleapis.com/youtube/v3/search
    ?part=snippet
    &q=inteligência artificial educação
    &type=video
    &maxResults=10
    &order=relevance
    &relevanceLanguage=pt
    &videoDuration=medium
    &key={YOUTUBE_API_KEY}

# Detalhes do vídeo (estatísticas)
GET https://www.googleapis.com/youtube/v3/videos
    ?part=snippet,statistics,contentDetails
    &id={VIDEO_ID}
    &key={YOUTUBE_API_KEY}

# Comentários de um vídeo
GET https://www.googleapis.com/youtube/v3/commentThreads
    ?part=snippet
    &videoId={VIDEO_ID}
    &maxResults=100
    &order=relevance
    &key={YOUTUBE_API_KEY}

# Legendas/Transcrições (via captions)
GET https://www.googleapis.com/youtube/v3/captions
    ?part=snippet
    &videoId={VIDEO_ID}
    &key={YOUTUBE_API_KEY}
```

**Implementação:**

```javascript
// services/youtube.js

const BASE_URL = 'https://www.googleapis.com/youtube/v3';
const API_KEY = process.env.YOUTUBE_API_KEY;

export async function searchVideos(query, options = {}) {
  const {
    maxResults = 10,
    language = 'pt',
    order = 'relevance',
    duration = 'any' // short, medium, long
  } = options;
  
  const url = `${BASE_URL}/search?part=snippet&q=${encodeURIComponent(query)}&type=video&maxResults=${maxResults}&order=${order}&relevanceLanguage=${language}&videoDuration=${duration}&key=${API_KEY}`;
  
  const response = await fetch(url);
  const data = await response.json();
  
  return data.items.map(item => ({
    videoId: item.id.videoId,
    title: item.snippet.title,
    description: item.snippet.description,
    channel: item.snippet.channelTitle,
    publishedAt: item.snippet.publishedAt,
    thumbnail: item.snippet.thumbnails.high.url,
    url: `https://www.youtube.com/watch?v=${item.id.videoId}`
  }));
}

export async function getVideoComments(videoId, maxResults = 100) {
  const url = `${BASE_URL}/commentThreads?part=snippet&videoId=${videoId}&maxResults=${maxResults}&order=relevance&key=${API_KEY}`;
  
  const response = await fetch(url);
  const data = await response.json();
  
  return data.items.map(item => ({
    author: item.snippet.topLevelComment.snippet.authorDisplayName,
    text: item.snippet.topLevelComment.snippet.textDisplay,
    likes: item.snippet.topLevelComment.snippet.likeCount,
    date: item.snippet.topLevelComment.snippet.publishedAt
  }));
}
```

---

### 6.4 Instagram / Meta API

> **Para capturar opiniões e conteúdo visual relacionado ao tema.**

| Info                     | Detalhe                                             |
| ------------------------ | --------------------------------------------------- |
| **URL Base**       | `https://graph.facebook.com/v18.0`                |
| **Autenticação** | Facebook App + Token                                |
| **Acesso**         | Limitado (apenas contas business/creator próprias) |
| **Alternativa**    | Busca manual por hashtags                           |

**Alternativa prática (abrir busca no navegador):**

```javascript
export function openInstagramSearch(hashtag) {
  const url = `https://www.instagram.com/explore/tags/${encodeURIComponent(hashtag)}/`;
  window.open(url, '_blank');
}

// Hashtags acadêmicas úteis
const ACADEMIC_HASHTAGS = [
  'inteligenciaartificial',
  'educacao',
  'pesquisaacademica',
  'ciencia',
  'universidade'
];
```

---

### 6.5 LinkedIn (Limitado)

> **Bom para capturar opiniões de profissionais e especialistas.**

| Info                  | Detalhe                                        |
| --------------------- | ---------------------------------------------- |
| **API**         | Muito restrita (apenas marketing partners)     |
| **Alternativa** | Google dork:`site:linkedin.com/pulse "tema"` |

```javascript
export function searchLinkedInArticles(query) {
  const googleUrl = `https://www.google.com/search?q=site:linkedin.com/pulse+${encodeURIComponent(query)}`;
  window.open(googleUrl, '_blank');
}
```

---

### 6.6 TikTok

> **Crescente como fonte de opiniões, especialmente de jovens.**

```javascript
export function openTikTokSearch(query) {
  const url = `https://www.tiktok.com/search?q=${encodeURIComponent(query)}`;
  window.open(url, '_blank');
}
```

---

## 7. Pesquisa em Sites de Notícias (APIs)

### 7.1 NewsAPI ⭐

> **Agrega notícias de 150K+ fontes no mundo todo.**

| Info                     | Detalhe                                     |
| ------------------------ | ------------------------------------------- |
| **URL Base**       | `https://newsapi.org/v2`                  |
| **Autenticação** | API Key gratuita (100 requests/dia no free) |
| **Plano Free**     | 100 requests/dia, últimos 30 dias          |
| **Cobertura**      | 150K+ fontes, 80+ países                   |
| **Registro**       | https://newsapi.org/register                |
| **Documentação** | https://newsapi.org/docs                    |

```bash
# Buscar tudo
GET https://newsapi.org/v2/everything
    ?q="inteligência artificial" AND educação
    &language=pt
    &sortBy=relevancy
    &from=2024-01-01
    &pageSize=20
    &apiKey={NEWS_API_KEY}

# Buscar headlines
GET https://newsapi.org/v2/top-headlines
    ?q=inteligência artificial
    &country=br
    &category=technology
    &apiKey={NEWS_API_KEY}

# Buscar por fonte específica
GET https://newsapi.org/v2/everything
    ?q=inteligência artificial educação
    &sources=globo,folha-de-sao-paulo
    &apiKey={NEWS_API_KEY}
```

**Implementação:**

```javascript
// services/newsApi.js

const BASE_URL = 'https://newsapi.org/v2';
const API_KEY = process.env.NEWS_API_KEY;

export async function searchNews(query, options = {}) {
  const {
    language = 'pt',
    sortBy = 'relevancy',
    from = null,
    to = null,
    pageSize = 20,
    page = 1
  } = options;
  
  let url = `${BASE_URL}/everything?q=${encodeURIComponent(query)}&language=${language}&sortBy=${sortBy}&pageSize=${pageSize}&page=${page}&apiKey=${API_KEY}`;
  
  if (from) url += `&from=${from}`;
  if (to) url += `&to=${to}`;
  
  const response = await fetch(url);
  const data = await response.json();
  
  return data.articles.map(article => ({
    title: article.title,
    description: article.description,
    content: article.content,
    source: article.source.name,
    author: article.author,
    url: article.url,
    imageUrl: article.urlToImage,
    publishedAt: article.publishedAt
  }));
}

export async function getHeadlines(options = {}) {
  const { country = 'br', category = 'technology', query = null } = options;
  
  let url = `${BASE_URL}/top-headlines?country=${country}&category=${category}&apiKey=${API_KEY}`;
  if (query) url += `&q=${encodeURIComponent(query)}`;
  
  const response = await fetch(url);
  return response.json();
}
```

---

### 7.2 GDELT Project

> **Monitora notícias do mundo todo em tempo real. Gratuito e sem limites.**

| Info                     | Detalhe                                                 |
| ------------------------ | ------------------------------------------------------- |
| **URL Base**       | `https://api.gdeltproject.org/api/v2`                 |
| **Autenticação** | Nenhuma                                                 |
| **Rate Limit**     | Sem limite específico                                  |
| **Cobertura**      | Bilhões de artigos, 100+ idiomas, desde 2015           |
| **Documentação** | https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ |

```bash
# Buscar artigos
GET https://api.gdeltproject.org/api/v2/doc/doc
    ?query=artificial intelligence education
    &mode=artlist
    &maxrecords=50
    &format=json
    &sourcelang=portuguese
    &startdatetime=20240101000000
    &enddatetime=20240630000000

# Buscar com análise de tom (sentimento)
GET https://api.gdeltproject.org/api/v2/doc/doc
    ?query=inteligencia artificial educacao
    &mode=tonechart
    &format=json

# Timeline de cobertura (quantas notícias por dia)
GET https://api.gdeltproject.org/api/v2/doc/doc
    ?query=inteligencia artificial educacao
    &mode=timelinevol
    &format=json
    &sourcelang=portuguese
```

**Implementação:**

```javascript
// services/gdelt.js

const BASE_URL = 'https://api.gdeltproject.org/api/v2/doc/doc';

export async function searchGDELT(query, options = {}) {
  const {
    language = 'portuguese',
    maxRecords = 50,
    startDate = null,
    endDate = null,
    mode = 'artlist'
  } = options;
  
  let url = `${BASE_URL}?query=${encodeURIComponent(query)}&mode=${mode}&maxrecords=${maxRecords}&format=json&sourcelang=${language}`;
  
  if (startDate) url += `&startdatetime=${startDate}`;
  if (endDate) url += `&enddatetime=${endDate}`;
  
  const response = await fetch(url);
  return response.json();
}

export async function getSentimentAnalysis(query, language = 'portuguese') {
  const url = `${BASE_URL}?query=${encodeURIComponent(query)}&mode=tonechart&format=json&sourcelang=${language}`;
  const response = await fetch(url);
  return response.json();
}

export async function getCoverageTimeline(query, language = 'portuguese') {
  const url = `${BASE_URL}?query=${encodeURIComponent(query)}&mode=timelinevol&format=json&sourcelang=${language}`;
  const response = await fetch(url);
  return response.json();
}
```

---

### 7.3 Google News (via RSS/Scraping)

> **Agregador de notícias do Google.**

```javascript
// services/googleNews.js

// Opção 1: Abrir no navegador
export function openGoogleNews(query, language = 'pt-BR') {
  const url = `https://news.google.com/search?q=${encodeURIComponent(query)}&hl=${language}`;
  window.open(url, '_blank');
}

// Opção 2: RSS Feed (pode ser parseado)
export function getGoogleNewsRSS(query) {
  return `https://news.google.com/rss/search?q=${encodeURIComponent(query)}&hl=pt-BR&gl=BR&ceid=BR:pt-419`;
}

// Opção 3: Via SerpAPI (paga)
// GET https://serpapi.com/search.json?engine=google_news&q=...&api_key=...
```

---

### 7.4 Media Cloud

> **Plataforma aberta para análise de mídia. Gratuita para pesquisadores.**

| Info                | Detalhe                                 |
| ------------------- | --------------------------------------- |
| **URL**       | `https://mediacloud.org`              |
| **API**       | REST API gratuita                       |
| **Registro**  | Gratuito para acadêmicos               |
| **Cobertura** | Milhões de fontes de notícias globais |

---

### 7.5 Wayback Machine (Internet Archive)

> **Para acessar versões históricas de páginas web (notícias antigas, etc.).**

```bash
# Verificar se uma URL foi arquivada
GET https://archive.org/wayback/available
    ?url=https://exemplo.com/noticia-ia-educacao

# Buscar snapshots
GET https://web.archive.org/cdx/search/cdx
    ?url=*.folha.uol.com.br/educacao/*inteligencia-artificial*
    &output=json
    &limit=50
```

---

## 8. Pesquisa Geral na Web (Google e Outros)

### 8.1 Google Custom Search API


```markdown
## 8. Pesquisa Geral na Web (Google e Outros)

### 8.1 Google Custom Search API

> **API oficial do Google para buscas programáticas.**

| Info | Detalhe |
|---|---|
| **URL Base** | `https://www.googleapis.com/customsearch/v1` |
| **Autenticação** | Google API Key + Custom Search Engine ID (CX) |
| **Plano gratuito** | 100 buscas/dia |
| **Plano pago** | $5 por 1.000 buscas extras |
| **Documentação** | https://developers.google.com/custom-search/v1 |
| **Setup** | https://programmablesearchengine.google.com/ |

**Como configurar:**

1. Criar um projeto no Google Cloud Console
2. Ativar a Custom Search API
3. Gerar uma API Key
4. Criar um Programmable Search Engine (CX)
5. Marcar "Search the entire web"

```bash
# Busca geral
GET https://www.googleapis.com/customsearch/v1
    ?key={GOOGLE_API_KEY}
    &cx={SEARCH_ENGINE_ID}
    &q=inteligência artificial educação superior brasil
    &num=10
    &start=1
    &lr=lang_pt
    &dateRestrict=y2
    &sort=date

# Busca com filtro de tipo
GET https://www.googleapis.com/customsearch/v1
    ?key={GOOGLE_API_KEY}
    &cx={SEARCH_ENGINE_ID}
    &q=inteligência artificial educação filetype:pdf
    &num=10

# Busca em site específico
GET https://www.googleapis.com/customsearch/v1
    ?key={GOOGLE_API_KEY}
    &cx={SEARCH_ENGINE_ID}
    &q=site:scielo.br inteligência artificial educação
    &num=10
```

**Parâmetros úteis:**

| Parâmetro       | Descrição                   | Exemplo                                            |
| ---------------- | ----------------------------- | -------------------------------------------------- |
| `q`            | Termo de busca                | `inteligência artificial educação`            |
| `num`          | Resultados por página (1-10) | `10`                                             |
| `start`        | Offset (paginação)          | `11` (segunda página)                           |
| `lr`           | Idioma dos resultados         | `lang_pt`, `lang_en`                           |
| `cr`           | País dos resultados          | `countryBR`                                      |
| `dateRestrict` | Período                      | `d7` (7 dias), `m6` (6 meses), `y2` (2 anos) |
| `sort`         | Ordenação                   | `date` (mais recente)                            |
| `fileType`     | Tipo de arquivo               | `pdf`, `doc`, `ppt`                          |
| `siteSearch`   | Restringir a um site          | `scielo.br`                                      |
| `exactTerms`   | Termos exatos obrigatórios   | `"inteligência artificial"`                     |
| `excludeTerms` | Termos a excluir              | `ensino médio`                                  |
| `rights`       | Licença                      | `cc_publicdomain`, `cc_attribute`              |

**Implementação completa:**

```javascript
// services/googleSearch.js

const BASE_URL = 'https://www.googleapis.com/customsearch/v1';
const API_KEY = process.env.GOOGLE_API_KEY;
const CX = process.env.GOOGLE_CX;

export async function searchGoogle(query, options = {}) {
  const {
    num = 10,
    start = 1,
    language = 'lang_pt',
    country = 'countryBR',
    dateRestrict = null,
    fileType = null,
    siteSearch = null,
    exactTerms = null,
    excludeTerms = null,
    sort = null
  } = options;

  let url = `${BASE_URL}?key=${API_KEY}&cx=${CX}&q=${encodeURIComponent(query)}&num=${num}&start=${start}`;

  if (language) url += `&lr=${language}`;
  if (country) url += `&cr=${country}`;
  if (dateRestrict) url += `&dateRestrict=${dateRestrict}`;
  if (fileType) url += `&fileType=${fileType}`;
  if (siteSearch) url += `&siteSearch=${siteSearch}`;
  if (exactTerms) url += `&exactTerms=${encodeURIComponent(exactTerms)}`;
  if (excludeTerms) url += `&excludeTerms=${encodeURIComponent(excludeTerms)}`;
  if (sort) url += `&sort=${sort}`;

  const response = await fetch(url);
  const data = await response.json();

  return {
    totalResults: data.searchInformation?.totalResults || 0,
    searchTime: data.searchInformation?.searchTime || 0,
    items: (data.items || []).map(item => ({
      title: item.title,
      link: item.link,
      snippet: item.snippet,
      displayLink: item.displayLink,
      fileFormat: item.fileFormat || null,
      datePublished: item.pagemap?.metatags?.[0]?.['article:published_time'] || null,
      image: item.pagemap?.cse_image?.[0]?.src || null
    }))
  };
}

// Buscar PDFs acadêmicos
export async function searchAcademicPDFs(query) {
  return searchGoogle(query, {
    fileType: 'pdf',
    dateRestrict: 'y5',
    num: 10
  });
}

// Buscar em sites acadêmicos específicos
export async function searchAcademicSites(query) {
  const sites = [
    'scielo.br',
    'scholar.google.com',
    'researchgate.net',
    'academia.edu',
    'periodicos.capes.gov.br'
  ];

  const results = [];
  for (const site of sites) {
    try {
      const data = await searchGoogle(query, { siteSearch: site, num: 5 });
      results.push(...data.items.map(item => ({ ...item, source: site })));
      await new Promise(r => setTimeout(r, 200)); // Rate limit
    } catch (e) {
      console.error(`Erro ao buscar em ${site}:`, e);
    }
  }
  return results;
}
```

---

### 8.2 Google Dorks para Pesquisa Acadêmica

> **Operadores avançados do Google para buscas precisas, sem necessidade de API.**
> Podem ser usados diretamente no navegador ou via Custom Search API.

**Dorks acadêmicos essenciais:**

```
# Buscar PDFs de artigos
"inteligência artificial" "educação superior" filetype:pdf

# Buscar em sites acadêmicos
"inteligência artificial" site:scielo.br OR site:researchgate.net

# Buscar teses e dissertações
"inteligência artificial" "educação" filetype:pdf site:*.edu.br

# Buscar apresentações
"inteligência artificial" "educação" filetype:ppt OR filetype:pptx

# Buscar dados/planilhas
"inteligência artificial" "educação" filetype:csv OR filetype:xlsx

# Buscar em repositórios institucionais
"inteligência artificial" site:repositorio.*.br

# Buscar apenas resultados recentes
"inteligência artificial" "educação" after:2023-01-01

# Buscar citações específicas
"segundo Silva" "inteligência artificial" "educação"

# Buscar revisões de literatura
"revisão sistemática" OR "systematic review" "artificial intelligence" "education"

# Buscar metodologia específica
"pesquisa quantitativa" "inteligência artificial" "educação" filetype:pdf

# Combinar múltiplos operadores
"inteligência artificial" AND "educação superior" AND "Brasil"
    site:scielo.br OR site:spell.org.br
    filetype:pdf
    after:2020-01-01
```

**Implementação de construtor de dorks:**

```javascript
// services/googleDorks.js

export function buildAcademicDork(options = {}) {
  const {
    terms = [],
    exactPhrases = [],
    excludeTerms = [],
    sites = [],
    fileTypes = [],
    dateAfter = null,
    dateBefore = null,
    inTitle = null,
    inUrl = null
  } = options;

  let dork = '';

  // Termos gerais
  if (terms.length > 0) {
    dork += terms.join(' ');
  }

  // Frases exatas
  exactPhrases.forEach(phrase => {
    dork += ` "${phrase}"`;
  });

  // Excluir termos
  excludeTerms.forEach(term => {
    dork += ` -${term}`;
  });

  // Sites
  if (sites.length > 0) {
    const siteQuery = sites.map(s => `site:${s}`).join(' OR ');
    dork += ` (${siteQuery})`;
  }

  // Tipos de arquivo
  if (fileTypes.length > 0) {
    const ftQuery = fileTypes.map(ft => `filetype:${ft}`).join(' OR ');
    dork += ` (${ftQuery})`;
  }

  // Datas
  if (dateAfter) dork += ` after:${dateAfter}`;
  if (dateBefore) dork += ` before:${dateBefore}`;

  // In title
  if (inTitle) dork += ` intitle:"${inTitle}"`;

  // In URL
  if (inUrl) dork += ` inurl:${inUrl}`;

  return dork.trim();
}

// Templates prontos de dorks acadêmicos
export const DORK_TEMPLATES = {
  artigosPDF: (tema) => buildAcademicDork({
    exactPhrases: [tema],
    fileTypes: ['pdf'],
    sites: ['scielo.br', 'researchgate.net', 'academia.edu'],
    dateAfter: '2020-01-01'
  }),

  tessesDissertacoes: (tema) => buildAcademicDork({
    exactPhrases: [tema],
    fileTypes: ['pdf'],
    sites: ['repositorio.ufsc.br', 'repositorio.usp.br', 'teses.usp.br'],
  }),

  revisaoSistematica: (tema) => buildAcademicDork({
    exactPhrases: ['revisão sistemática', tema],
    fileTypes: ['pdf'],
    dateAfter: '2020-01-01'
  }),

  dadosAbertos: (tema) => buildAcademicDork({
    exactPhrases: [tema],
    fileTypes: ['csv', 'xlsx', 'json'],
    sites: ['dados.gov.br', 'kaggle.com', 'data.world']
  }),

  noticiasRecentes: (tema) => buildAcademicDork({
    exactPhrases: [tema],
    sites: ['g1.globo.com', 'folha.uol.com.br', 'estadao.com.br', 'bbc.com'],
    dateAfter: '2024-01-01'
  })
};

// Abrir no Google
export function openGoogleDork(dork) {
  const url = `https://www.google.com/search?q=${encodeURIComponent(dork)}`;
  window.open(url, '_blank');
}
```

---

### 8.3 Bing Web Search API

> **Alternativa ao Google. Generoso plano gratuito.**

| Info                     | Detalhe                                             |
| ------------------------ | --------------------------------------------------- |
| **URL Base**       | `https://api.bing.microsoft.com/v7.0`             |
| **Autenticação** | API Key (Azure Cognitive Services)                  |
| **Plano gratuito** | 1.000 chamadas/mês                                 |
| **Documentação** | https://learn.microsoft.com/en-us/bing/search-apis/ |

```bash
GET https://api.bing.microsoft.com/v7.0/search
    ?q=inteligência artificial educação
    &count=10
    &offset=0
    &mkt=pt-BR
    &freshness=Month
    Headers: Ocp-Apim-Subscription-Key: {BING_API_KEY}

# Buscar notícias
GET https://api.bing.microsoft.com/v7.0/news/search
    ?q=inteligência artificial educação
    &count=10
    &mkt=pt-BR
    &freshness=Week
    Headers: Ocp-Apim-Subscription-Key: {BING_API_KEY}
```

**Implementação:**

```javascript
// services/bingSearch.js

const SEARCH_URL = 'https://api.bing.microsoft.com/v7.0/search';
const NEWS_URL = 'https://api.bing.microsoft.com/v7.0/news/search';
const API_KEY = process.env.BING_API_KEY;

export async function searchBing(query, options = {}) {
  const {
    count = 10,
    offset = 0,
    market = 'pt-BR',
    freshness = null // Day, Week, Month
  } = options;

  let url = `${SEARCH_URL}?q=${encodeURIComponent(query)}&count=${count}&offset=${offset}&mkt=${market}`;
  if (freshness) url += `&freshness=${freshness}`;

  const response = await fetch(url, {
    headers: { 'Ocp-Apim-Subscription-Key': API_KEY }
  });
  const data = await response.json();

  return {
    totalResults: data.webPages?.totalEstimatedMatches || 0,
    results: (data.webPages?.value || []).map(item => ({
      title: item.name,
      url: item.url,
      snippet: item.snippet,
      dateLastCrawled: item.dateLastCrawled
    }))
  };
}

export async function searchBingNews(query, options = {}) {
  const { count = 10, market = 'pt-BR', freshness = 'Month' } = options;

  const url = `${NEWS_URL}?q=${encodeURIComponent(query)}&count=${count}&mkt=${market}&freshness=${freshness}`;

  const response = await fetch(url, {
    headers: { 'Ocp-Apim-Subscription-Key': API_KEY }
  });
  const data = await response.json();

  return (data.value || []).map(item => ({
    title: item.name,
    url: item.url,
    description: item.description,
    source: item.provider?.[0]?.name || 'Desconhecido',
    datePublished: item.datePublished,
    image: item.image?.thumbnail?.contentUrl || null
  }));
}
```

---

### 8.4 DuckDuckGo Instant Answer API

> **Gratuita, sem autenticação, sem limites. Retorna respostas instantâneas.**

| Info                     | Detalhe                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| **URL Base**       | `https://api.duckduckgo.com/`                                      |
| **Autenticação** | Nenhuma                                                              |
| **Rate Limit**     | Sem limite oficial                                                   |
| **Limitação**    | Retorna apenas "instant answers", não resultados de busca completos |

```bash
GET https://api.duckduckgo.com/
    ?q=artificial+intelligence+education
    &format=json
    &no_html=1
    &skip_disambig=1
```

**Implementação:**

```javascript
// services/duckduckgo.js

export async function instantAnswer(query) {
  const url = `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json&no_html=1&skip_disambig=1`;

  const response = await fetch(url);
  const data = await response.json();

  return {
    abstract: data.Abstract || null,
    abstractSource: data.AbstractSource || null,
    abstractUrl: data.AbstractURL || null,
    definition: data.Definition || null,
    relatedTopics: (data.RelatedTopics || []).map(t => ({
      text: t.Text,
      url: t.FirstURL
    }))
  };
}

// Para busca completa, abrir no navegador
export function openDuckDuckGo(query) {
  const url = `https://duckduckgo.com/?q=${encodeURIComponent(query)}`;
  window.open(url, '_blank');
}
```

---

### 8.5 Brave Search API

> **Nova alternativa com foco em privacidade. API gratuita generosa.**

| Info                     | Detalhe                                 |
| ------------------------ | --------------------------------------- |
| **URL Base**       | `https://api.search.brave.com/res/v1` |
| **Autenticação** | API Key gratuita                        |
| **Plano gratuito** | 2.000 queries/mês                      |
| **Documentação** | https://brave.com/search/api/           |

```bash
GET https://api.search.brave.com/res/v1/web/search
    ?q=inteligência artificial educação
    &count=10
    &country=BR
    &search_lang=pt
    &freshness=py
    Headers: X-Subscription-Token: {BRAVE_API_KEY}
             Accept: application/json
```

**Implementação:**

```javascript
// services/braveSearch.js

const BASE_URL = 'https://api.search.brave.com/res/v1';
const API_KEY = process.env.BRAVE_API_KEY;

export async function searchBrave(query, options = {}) {
  const {
    count = 10,
    country = 'BR',
    language = 'pt',
    freshness = 'py' // pd=past day, pw=past week, pm=past month, py=past year
  } = options;

  const url = `${BASE_URL}/web/search?q=${encodeURIComponent(query)}&count=${count}&country=${country}&search_lang=${language}&freshness=${freshness}`;

  const response = await fetch(url, {
    headers: {
      'X-Subscription-Token': API_KEY,
      'Accept': 'application/json'
    }
  });
  const data = await response.json();

  return {
    results: (data.web?.results || []).map(item => ({
      title: item.title,
      url: item.url,
      description: item.description,
      age: item.age || null,
      language: item.language || null
    })),
    news: (data.news?.results || []).map(item => ({
      title: item.title,
      url: item.url,
      source: item.meta_url?.hostname || null,
      age: item.age || null
    }))
  };
}
```

---

## 9. Estratégias de Busca Avançada

### 9.1 Construção de Strings de Busca Acadêmica

> **Uma boa string de busca é a diferença entre encontrar 10 ou 10.000 resultados
> relevantes. A construção segue uma metodologia específica.**

#### Passo 1 — Definir os Conceitos-Chave

Partir do problema de pesquisa e extrair os conceitos principais:

```
Problema: "Como a IA generativa impacta o desempenho acadêmico
           de estudantes de graduação?"

Conceitos:
├── Conceito 1: Inteligência Artificial Generativa
├── Conceito 2: Desempenho Acadêmico
└── Conceito 3: Estudantes de Graduação / Ensino Superior
```

#### Passo 2 — Listar Sinônimos e Variações

```
Conceito 1 — IA Generativa:
├── "inteligência artificial generativa"
├── "generative artificial intelligence"
├── "generative AI"
├── "IA generativa"
├── "ChatGPT"
├── "large language models"
├── "LLM"
├── "GPT"
└── "modelos de linguagem"

Conceito 2 — Desempenho Acadêmico:
├── "desempenho acadêmico"
├── "academic performance"
├── "rendimento escolar"
├── "aproveitamento acadêmico"
├── "student achievement"
├── "learning outcomes"
└── "resultados de aprendizagem"

Conceito 3 — Ensino Superior:
├── "ensino superior"
├── "higher education"
├── "educação superior"
├── "graduação"
├── "undergraduate"
├── "universidade"
└── "university"
```

#### Passo 3 — Montar a String com Operadores Booleanos

```
Regra:
- OR entre sinônimos do MESMO conceito (amplia)
- AND entre conceitos DIFERENTES (restringe)
- Aspas ("") para termos compostos (exato)
- Parênteses () para agrupar
```

**String final:**

```
("inteligência artificial generativa" OR "generative AI" OR "ChatGPT"
 OR "large language models" OR "IA generativa" OR "LLM")
AND
("desempenho acadêmico" OR "academic performance" OR "rendimento escolar"
 OR "learning outcomes" OR "student achievement")
AND
("ensino superior" OR "higher education" OR "graduação"
 OR "undergraduate" OR "universidade")
```

#### Passo 4 — Adaptar para Cada Base

Cada base tem suas particularidades:

| Base                       | Adaptação                                                                                              |
| -------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Semantic Scholar** | Simplificar (não suporta booleanos complexos):`generative AI academic performance higher education`   |
| **OpenAlex**         | Usar o campo `default.search:` com termos simples                                                      |
| **PubMed**           | Usar MeSH terms + booleanos:`("Artificial Intelligence"[MeSH]) AND ("Educational Measurement"[MeSH])`  |
| **Google Scholar**   | Suporta booleanos mas simplificado:`"generative AI" AND "academic performance" AND "higher education"` |
| **Scopus**           | Suporta TITLE-ABS-KEY:`TITLE-ABS-KEY("generative AI" AND "academic performance")`                      |
| **Web of Science**   | Suporta TS (Topic Search):`TS=("generative AI" AND "academic performance")`                            |

**Implementação do construtor de strings:**

```javascript
// services/searchStringBuilder.js

export function buildSearchString(concepts) {
  // concepts = [
  //   { name: "IA Generativa", terms: ["generative AI", "ChatGPT", "LLM"] },
  //   { name: "Desempenho", terms: ["academic performance", "learning outcomes"] },
  //   { name: "Ensino Superior", terms: ["higher education", "university"] }
  // ]

  const groups = concepts.map(concept => {
    const quotedTerms = concept.terms.map(t => `"${t}"`);
    return `(${quotedTerms.join(' OR ')})`;
  });

  return groups.join(' AND ');
}

export function adaptForPlatform(concepts, platform) {
  switch (platform) {
    case 'semantic_scholar':
      // Pegar o primeiro termo de cada conceito
      return concepts.map(c => c.terms[0]).join(' ');

    case 'openalex':
      return concepts.map(c => c.terms[0]).join(' ');

    case 'pubmed':
      return concepts.map(concept => {
        const terms = concept.terms.map(t => `"${t}"`).join(' OR ');
        return `(${terms})`;
      }).join(' AND ');

    case 'google_scholar':
      return concepts.map(concept => {
        return `"${concept.terms[0]}"`;
      }).join(' AND ');

    case 'scopus':
      const scopusInner = concepts.map(concept => {
        const terms = concept.terms.map(t => `"${t}"`).join(' OR ');
        return `(${terms})`;
      }).join(' AND ');
      return `TITLE-ABS-KEY(${scopusInner})`;

    case 'web_of_science':
      const wosInner = concepts.map(concept => {
        const terms = concept.terms.map(t => `"${t}"`).join(' OR ');
        return `(${terms})`;
      }).join(' AND ');
      return `TS=(${wosInner})`;

    default:
      return buildSearchString(concepts);
  }
}
```

---

### 9.2 Protocolo PRISMA para Revisão Sistemática

> **Quando a pesquisa exige revisão sistemática, deve-se seguir o
> protocolo PRISMA (Preferred Reporting Items for Systematic Reviews).**

```
┌─────────────────────────────────────────────────────┐
│               IDENTIFICAÇÃO                          │
│                                                      │
│  Registros identificados nas bases:                  │
│  ├── Semantic Scholar: 342                           │
│  ├── OpenAlex: 512                                   │
│  ├── SciELO: 87                                      │
│  ├── PubMed: 156                                     │
│  └── Total: 1.097                                    │
│                                                      │
│  Duplicatas removidas: 234                           │
│  Registros após remoção: 863                         │
├─────────────────────────────────────────────────────┤
│               TRIAGEM                                │
│                                                      │
│  Registros triados (título + abstract): 863          │
│  Registros excluídos: 712                            │
│  Registros selecionados: 151                         │
├─────────────────────────────────────────────────────┤
│               ELEGIBILIDADE                          │
│                                                      │
│  Artigos lidos na íntegra: 151                       │
│  Artigos excluídos (com motivo): 108                 │
│  ├── Fora do escopo: 45                              │
│  ├── Metodologia inadequada: 28                      │
│  ├── Sem acesso ao texto completo: 20                │
│  └── Duplicatas não detectadas: 15                   │
├─────────────────────────────────────────────────────┤
│               INCLUSÃO                               │
│                                                      │
│  Estudos incluídos na revisão: 43                    │
│  ├── Quantitativos: 25                               │
│  ├── Qualitativos: 12                                │
│  └── Mistos: 6                                       │
└─────────────────────────────────────────────────────┘
```

**Implementação no App:**

```javascript
// services/prismaTracker.js

export function createPrismaRecord(paperId) {
  return {
    paperId,
    identification: {
      databases: {},
      totalIdentified: 0,
      duplicatesRemoved: 0,
      afterDuplicates: 0
    },
    screening: {
      totalScreened: 0,
      excluded: 0,
      selected: 0
    },
    eligibility: {
      fullTextAssessed: 0,
      excluded: 0,
      exclusionReasons: {},
      included: 0
    },
    inclusion: {
      totalIncluded: 0,
      byType: {}
    }
  };
}
```

---

### 9.3 Critérios de Inclusão e Exclusão

> **Definir ANTES de iniciar a busca para garantir rigor metodológico.**

```json
{
  "criterios_inclusao": [
    "Artigos publicados entre 2019 e 2024",
    "Artigos revisados por pares (peer-reviewed)",
    "Artigos em português, inglês ou espanhol",
    "Artigos que abordam IA no contexto educacional",
    "Artigos com metodologia clara e descrita",
    "Artigos disponíveis em texto completo"
  ],
  "criterios_exclusao": [
    "Artigos de opinião sem base empírica",
    "Resumos de conferências sem artigo completo",
    "Artigos duplicados",
    "Artigos fora do recorte temporal",
    "Artigos sem relação direta com o tema",
    "Teses e dissertações (apenas artigos de periódico)",
    "Artigos retratados (retracted)"
  ]
}
```

---

### 9.4 Snowball Technique (Técnica Bola de Neve)

> **Usar as referências de um artigo relevante para encontrar mais artigos.**

```
Paper Semente (artigo muito relevante)
│
├── Backward Snowball (Referências do paper)
│   ├── Referência 1 → Nova referência relevante ✅
│   ├── Referência 2 → Fora do escopo ❌
│   ├── Referência 3 → Nova referência relevante ✅
│   └── ... (analisar todas as referências)
│
└── Forward Snowball (Quem citou este paper)
    ├── Citação 1 → Nova referência relevante ✅
    ├── Citação 2 → Fora do escopo ❌
    ├── Citação 3 → Nova referência relevante ✅
    └── ... (analisar todas as citações)
```

**Implementação usando Semantic Scholar:**

```javascript
// services/snowball.js

import { getReferences, getCitations } from './semanticScholar.js';

export async function snowballSearch(seedPaperId, options = {}) {
  const {
    maxDepth = 2,           // Quantas camadas de snowball
    minCitations = 10,      // Filtrar por mínimo de citações
    yearFrom = 2019,        // Filtrar por ano
    maxPapers = 100         // Limite total
  } = options;

  const visited = new Set();
  const relevantPapers = [];

  async function explore(paperId, depth) {
    if (depth > maxDepth || visited.has(paperId) || relevantPapers.length >= maxPapers) {
      return;
    }

    visited.add(paperId);

    // Backward snowball
    const refs = await getReferences(paperId);
    for (const ref of refs.data || []) {
      const paper = ref.citedPaper;
      if (paper && paper.year >= yearFrom && paper.citationCount >= minCitations) {
        if (!visited.has(paper.paperId)) {
          relevantPapers.push({
            ...paper,
            foundVia: 'backward',
            fromPaper: paperId,
            depth
          });
          await explore(paper.paperId, depth + 1);
        }
      }
    }

    // Forward snowball
    const cites = await getCitations(paperId);
    for (const cite of cites.data || []) {
      const paper = cite.citingPaper;
      if (paper && paper.year >= yearFrom && paper.citationCount >= minCitations) {
        if (!visited.has(paper.paperId)) {
          relevantPapers.push({
            ...paper,
            foundVia: 'forward',
            fromPaper: paperId,
            depth
          });
          await explore(paper.paperId, depth + 1);
        }
      }
    }

    // Rate limiting
    await new Promise(r => setTimeout(r, 1100));
  }

  await explore(seedPaperId, 1);

  return {
    seed: seedPaperId,
    totalFound: relevantPapers.length,
    papers: relevantPapers,
    visited: visited.size
  };
}
```

---

## 10. Fluxo Completo de Pesquisa para o App

### 10.1 Fluxo Visual

```
[Usuário define tema e problema de pesquisa]
          │
          ▼
[Construir string de busca]
  ├── Definir conceitos-chave
  ├── Listar sinônimos (IA pode sugerir)
  └── Montar booleanos
          │
          ▼
[Busca simultânea em múltiplas fontes]
  ├── 🔬 Acadêmicas: Semantic Scholar + OpenAlex + CrossRef
  ├── 🇧🇷 Brasileiras: SciELO + SPELL + BDTD
  ├── 🔓 Open Access: CORE + Unpaywall + DOAJ
  ├── 🧠 IA: Consensus + Elicit
  └── 🌐 Web: Google + Bing + Brave
          │
          ▼
[Consolidar resultados]
  ├── Remover duplicatas (por DOI, título)
  ├── Ordenar por relevância / citações
  └── Aplicar critérios de inclusão/exclusão
          │
          ▼
[Análise dos resultados]
  ├── Preview de abstracts
  ├── IA resume cada paper
  ├── IA classifica relevância
  └── Usuário seleciona papers relevantes
          │
          ▼
[Download e armazenamento]
  ├── Buscar PDFs via Unpaywall / CORE
  ├── Salvar na pasta /01-referencias
  ├── Extrair texto dos PDFs
  └── IA gera resumos e citações
          │
          ▼
[Snowball Search (opcional)]
  ├── Backward (referências dos selecionados)
  └── Forward (quem citou os selecionados)
          │
          ▼
[Atualizar contexto.json]
  ├── Adicionar resumos das referências
  ├── Gerar citações formatadas
  └── Atualizar lista de fontes
          │
          ▼
[Pesquisa complementar (se necessário)]
  ├── 📰 Notícias: NewsAPI + GDELT
  ├── 🐦 Redes sociais: Twitter + Reddit + YouTube
  └── 📊 Dados: dados.gov.br + Kaggle
```

---

### 10.2 Serviço Unificado de Busca

```javascript
// services/unifiedSearch.js

import * as semanticScholar from './semanticScholar.js';
import * as openAlex from './openAlex.js';
import * as crossRef from './crossref.js';
import * as core from './core.js';
import * as unpaywall from './unpaywall.js';
import * as pubmed from './pubmed.js';
import * as arxiv from './arxiv.js';
import * as newsApi from './newsApi.js';
import * as gdelt from './gdelt.js';
import * as reddit from './reddit.js';
import * as youtube from './youtube.js';
import * as googleSearch from './googleSearch.js';
import * as bingSearch from './bingSearch.js';
import * as braveSearch from './braveSearch.js';

// ========================================
// BUSCA ACADÊMICA UNIFICADA
// ========================================

export async function searchAcademic(query, options = {}) {
  const {
    sources = ['semantic_scholar', 'openalex', 'crossref'],
    limit = 10,
    yearFrom = 2019,
    language = null,
    openAccessOnly = false
  } = options;

  const results = {};
  const errors = {};

  const searches = {
    semantic_scholar: () => semanticScholar.searchPapers(query, limit),
    openalex: () => openAlex.searchWorks(query, { perPage: limit, fromDate: `${yearFrom}-01-01`, openAccess: openAccessOnly }),
    crossref: () => crossRef.searchCrossRef(query, { rows: limit, fromDate: String(yearFrom) }),
    core: () => core.searchCore(query, { limit, yearFrom }),
    pubmed: () => pubmed.searchPubMed(query, limit),
    arxiv: () => arxiv.searchArxiv(query, limit)
  };

  // Executar buscas em paralelo
  const promises = sources
    .filter(s => searches[s])
    .map(async (source) => {
      try {
        results[source] = await searches[source]();
      } catch (e) {
        errors[source] = e.message;
      }
    });

  await Promise.all(promises);

  return { results, errors };
}

// ========================================
// BUSCA EM NOTÍCIAS UNIFICADA
// ========================================

export async function searchNews(query, options = {}) {
  const {
    sources = ['newsapi', 'gdelt'],
    limit = 20,
    language = 'pt'
  } = options;

  const results = {};
  const errors = {};

  if (sources.includes('newsapi')) {
    try {
      results.newsapi = await newsApi.searchNews(query, { language, pageSize: limit });
    } catch (e) {
      errors.newsapi = e.message;
    }
  }

  if (sources.includes('gdelt')) {
    try {
      results.gdelt = await gdelt.searchGDELT(query, { language: 'portuguese', maxRecords: limit });
    } catch (e) {
      errors.gdelt = e.message;
    }
  }

  return { results, errors };
}

// ========================================
// BUSCA EM REDES SOCIAIS UNIFICADA
// ========================================

export async function searchSocial(query, options = {}) {
  const {
    sources = ['reddit', 'youtube'],
    limit = 20
  } = options;

  const results = {};
  const errors = {};

  if (sources.includes('reddit')) {
    try {
      results.reddit = await reddit.searchReddit(query, { limit });
    } catch (e) {
      errors.reddit = e.message;
    }
  }

  if (sources.includes('youtube')) {
    try {
      results.youtube = await youtube.searchVideos(query, { maxResults: Math.min(limit, 50) });
    } catch (e) {
      errors.youtube = e.message;
    }
  }

  return { results, errors };
}

// ========================================
// BUSCA WEB UNIFICADA
// ========================================

export async function searchWeb(query, options = {}) {
  const {
    sources = ['google', 'bing', 'brave'],
    limit = 10
  } = options;

  const results = {};
  const errors = {};

  if (sources.includes('google')) {
    try {
      results.google = await googleSearch.searchGoogle(query, { num: limit });
    } catch (e) {
      errors.google = e.message;
    }
  }

  if (sources.includes('bing')) {
    try {
      results.bing = await bingSearch.searchBing(query, { count: limit });
    } catch (e) {
      errors.bing = e.message;
    }
  }

  if (sources.includes('brave')) {
    try {
      results.brave = await braveSearch.searchBrave(query, { count: limit });
    } catch (e) {
      errors.brave = e.message;
    }
  }

  return { results, errors };
}

// ========================================
// MEGA BUSCA (TUDO DE UMA VEZ)
// ========================================

export async function megaSearch(query, options = {}) {
  const {
    academic = true,
    news = false,
    social = false,
    web = false,
    academicSources = ['semantic_scholar', 'openalex'],
    newsSources = ['newsapi'],
    socialSources = ['reddit'],
    webSources = ['brave'],
    limit = 10
  } = options;

  const results = {};

  if (academic) {
    results.academic = await searchAcademic(query, {
      sources: academicSources,
      limit
    });
  }

  if (news) {
    results.news = await searchNews(query, {
      sources: newsSources,
      limit
    });
  }

  if (social) {
    results.social = await searchSocial(query, {
      sources: socialSources,
      limit
    });
  }

  if (web) {
    results.web = await searchWeb(query, {
      sources: webSources,
      limit
    });
  }

  return results;
}

// ========================================
// DEDUPLICAÇÃO DE RESULTADOS
// ========================================

export function deduplicateResults(allResults) {
  const seen = new Map();

  const normalized = allResults.map(result => {
    const key = result.doi
      || result.title?.toLowerCase().trim().replace(/\s+/g, ' ')
      || result.url;

    if (seen.has(key)) {
      // Mesclar fontes
      seen.get(key).sources.push(result.source);
      seen.get(key).totalSources++;
      return null;
    }

    const entry = {
      ...result,
      sources: [result.source],
      totalSources: 1
    };
    seen.set(key, entry);
    return entry;
  }).filter(Boolean);

  // Ordenar por quantidade de fontes (quanto mais fontes, mais relevante)
  return normalized.sort((a, b) => b.totalSources - a.totalSources);
}

// ========================================
// BUSCAR PDF GRATUITO
// ========================================

export async function findFreePDF(doi) {
  if (!doi) return null;

  // Tentar Unpaywall primeiro
  try {
    const unpResult = await unpaywall.findOpenAccess(doi);
    if (unpResult.pdfUrl) return unpResult.pdfUrl;
  } catch (e) {}

  // Tentar CORE
  try {
    const coreResult = await core.searchCore(doi, { limit: 1 });
    if (coreResult?.results?.[0]?.downloadUrl) {
      return coreResult.results[0].downloadUrl;
    }
  } catch (e) {}

  // Tentar Semantic Scholar
  try {
    const ssResult = await semanticScholar.getPaperDetails(doi);
    if (ssResult?.openAccessPdf?.url) {
      return ssResult.openAccessPdf.url;
    }
  } catch (e) {}

  return null;
}
```

---

## 11. Implementação no Paper Builder

### 11.1 Nova Tela — Central de Pesquisa

```
┌────────────────────────────────────────────────────────────────┐
│  🔍 CENTRAL DE PESQUISA — Impacto da IA na Educação            │
│────────────────────────────────────────────────────────────────│
│                                                                │
│  ── CONSTRUTOR DE BUSCA ──                                     │
│                                                                │
│  Conceito 1: [inteligência artificial generativa         ]     │
│  Sinônimos:  [generative AI, ChatGPT, LLM, GPT          ]     │
│  [+ Conceito]  [🤖 Sugerir sinônimos com IA]                   │
│                                                                │
│  Conceito 2: [desempenho acadêmico                       ]     │
│  Sinônimos:  [academic performance, learning outcomes    ]     │
│                                                                │
│  Conceito 3: [ensino superior                            ]     │
│  Sinônimos:  [higher education, university               ]     │
│                                                                │
│  String gerada:                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ("generative AI" OR "ChatGPT" OR "LLM") AND ("academic │  │
│  │  performance" OR "learning outcomes") AND ("higher      │  │
│  │  education" OR "university")                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│  [📋 Copiar]                                                   │
│                                                                │
│  ── FONTES ──                                                  │
│                                                                │
│  Acadêmicas:                                                   │
│  [v] Semantic Scholar  [v] OpenAlex  [ ] CrossRef              │
│  [ ] PubMed  [ ] arXiv  [ ] CORE  [ ] DOAJ                    │
│                                                                │
│  Brasileiras:                                                  │
│  [v] SciELO  [ ] SPELL  [ ] BDTD  [ ] CAPES                  │
│                                                                │
│  IA / Descoberta:                                              │
│  [ ] Consensus  [ ] Elicit  [ ] Connected Papers               │
│                                                                │
│  Notícias:                                                     │
│  [ ] NewsAPI  [ ] GDELT  [ ] Google News                       │
│                                                                │
│  Redes Sociais:                                                │
│  [ ] Reddit  [ ] YouTube  [ ] Twitter/X                        │
│                                                                │
│  Web:                                                          │
│  [ ] Google  [ ] Bing  [ ] Brave  [ ] DuckDuckGo              │
│                                                                │
│  ── FILTROS ──                                                 │
│                                                                │
│  Ano: [2019] até [2024]                                        │
│  Idioma: [v] Português  [v] Inglês  [ ] Espanhol              │
│  Apenas acesso aberto: [ ]                                     │
│  Mín. citações: [10]                                           │
│  Limite por fonte: [20]                                        │
│                                                                │
│  [🔍 PESQUISAR]                                                │
│                                                                │
│  ── RESULTADOS (156 encontrados, 98 únicos) ──                │
│                                                                │
│  [Todos] [Acadêmicos] [Notícias] [Social] [Web]               │
│  Ordenar: [Relevância ▼]  [Citações] [Data] [Fontes]          │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ⬜ Impact of Generative AI on Student Performance        │  │
│  │    Silva, J.C. et al. (2023) | Citações: 45             │  │
│  │    Fontes: Semantic Scholar, OpenAlex, CrossRef (3)      │  │
│  │    📄 PDF disponível (Open Access)                       │  │
│  │                                                          │  │
│  │    "This study examines the impact of generative AI      │  │
│  │    tools on academic performance in higher education..."  │  │
│  │                                                          │  │
│  │    [📥 Baixar PDF]  [🔍 Ver detalhes]  [🔗 Connected]    │  │
│  │    [📚 Adicionar às referências]                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ⬜ ChatGPT e o futuro da educação no Brasil              │  │
│  │    Oliveira, M.A. (2024) | Citações: 12                 │  │
│  │    Fontes: SciELO (1)                                    │  │
│  │    📄 PDF disponível                                     │  │
│  │                                                          │  │
│  │    [📥 Baixar PDF]  [📚 Adicionar às referências]         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                │
│  ── AÇÕES EM LOTE ──                                           │
│  [☑️ Selecionar todos]                                          │
│  [📚 Adicionar selecionados às referências]                    │
│  [📥 Baixar todos os PDFs disponíveis]                         │
│  [🤖 IA: Resumir todos os selecionados]                        │
│  [❄️ Snowball nos selecionados]                                │
│  [📊 Gerar PRISMA dos resultados]                              │
│                                                                │
│  [← Voltar ao Painel]                                          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

### 11.2 Novas Rotas da API

```
# Pesquisa
POST   /api/search/academic          → Busca em bases acadêmicas
POST   /api/search/news              → Busca em notícias
POST   /api/search/social            → Busca em redes sociais
POST   /api/search/web               → Busca na web
POST   /api/search/mega              → Busca em tudo
POST   /api/search/snowball          → Snowball search

# Utilitários de pesquisa
POST   /api/search/build-string      → Constrói string de busca
POST   /api/search/suggest-synonyms  → IA sugere sinônimos
POST   /api/search/deduplicate       → Remove duplicatas
POST   /api/search/find-pdf          → Busca PDF gratuito por DOI
POST   /api/search/batch-pdf         → Busca PDFs em lote

# PRISMA
GET    /api/papers/:id/prisma        → Dados PRISMA
PUT    /api/papers/:id/prisma        → Atualiza dados PRISMA

# Links externos (abrir no navegador)
GET    /api/search/external-url      → Gera URL para plataformas sem API
```

---

### 11.3 API Keys Necessárias (Todas Gratuitas)

```env
# .env

# === OBRIGATÓRIAS (100% gratuitas, sem cartão) ===
# Nenhuma API key necessária para:
# - OpenAlex (só email no header)
# - CrossRef (só email no header)
# - arXiv (sem auth)
# - DuckDuckGo (sem auth)
# - GDELT (sem auth)
# - Reddit JSON (sem auth para .json)
# - SciELO (sem auth)

# === GRATUITAS COM REGISTRO ===
SEMANTIC_SCHOLAR_API_KEY=       # Opcional, melhora rate limit
CORE_API_KEY=                   # Obrigatório para CORE
NEWS_API_KEY=                   # 100 requests/dia grátis
YOUTUBE_API_KEY=                # 10.000 unidades/dia grátis
GOOGLE_API_KEY=                 # Para Custom Search
GOOGLE_CX=                     # Search Engine ID
BING_API_KEY=                   # 1.000/mês grátis (Azure)
BRAVE_API_KEY=                  # 2.000/mês grátis

# === OPCIONAIS (podem requerer acesso institucional) ===
SCOPUS_API_KEY=                 # Elsevier Dev Portal (grátis para acadêmicos)
WOS_API_KEY=                    # Web of Science (institucional)
TWITTER_BEARER_TOKEN=           # Basic plan $100/mês
PUBMED_API_KEY=                 # Opcional, melhora rate limit

# === IAs do App ===
MINIMAX_API_KEY=                # Via OpenCode (free)
GEMINI_API_KEY=                 # Via Antigravity (free)
```

---

### 11.4 Prioridade de Implementação das APIs

| Prioridade     | API                  | Custo              | Dificuldade  | Valor               |
| -------------- | -------------------- | ------------------ | ------------ | ------------------- |
| 🔴**1**  | Semantic Scholar     | Grátis            | Fácil       | Altíssimo          |
| 🔴**2**  | OpenAlex             | Grátis            | Fácil       | Altíssimo          |
| 🔴**3**  | CrossRef             | Grátis            | Fácil       | Alto                |
| 🔴**4**  | Unpaywall            | Grátis            | Fácil       | Alto (PDFs grátis) |
| 🟡**5**  | CORE                 | Grátis (com key)  | Fácil       | Alto                |
| 🟡**6**  | GDELT                | Grátis            | Médio       | Médio              |
| 🟡**7**  | Reddit (.json)       | Grátis            | Fácil       | Médio              |
| 🟡**8**  | YouTube Data API     | Grátis            | Médio       | Médio              |
| 🟡**9**  | NewsAPI              | Grátis (limitado) | Fácil       | Médio              |
| 🟡**10** | Brave Search         | Grátis            | Fácil       | Médio              |
| 🟢**11** | Google Custom Search | Grátis (limitado) | Médio       | Médio              |
| 🟢**12** | Bing Search          | Grátis (limitado) | Médio       | Médio              |
| 🟢**13** | PubMed               | Grátis            | Médio       | Nicho (saúde)      |
| 🟢**14** | arXiv                | Grátis            | Médio (XML) | Nicho (exatas)      |
| 🟢**15** | DOAJ                 | Grátis            | Fácil       | Baixo               |
| ⚪**16** | Twitter/X            | $100/mês          | Difícil     | Depende             |
| ⚪**17** | Scopus               | Institucional      | Médio       | Alto (se tiver)     |
| ⚪**18** | Web of Science       | Institucional      | Médio       | Alto (se tiver)     |

### 11.5 Tabela Resumo — Todas as APIs

| API                        | Auth            | Free? | Rate Limit (Free) | Cobertura    | Melhor Para                    |
| -------------------------- | --------------- | ----- | ----------------- | ------------ | ------------------------------ |
| **Semantic Scholar** | Key opcional    | ✅    | 100/5min          | 200M+ papers | Busca geral, citações, TLDR  |
| **OpenAlex**         | Email header    | ✅    | 100K/dia          | 250M+ works  | Filtros avançados, analytics  |
| **CrossRef**         | Email header    | ✅    | 50/seg            | 130M+ DOIs   | Metadados, DOI lookup          |
| **Unpaywall**        | Email param     | ✅    | 100K/dia          | 30M+ OA      | Encontrar PDFs grátis         |
| **CORE**             | API Key         | ✅    | 10/seg            | 300M+        | Texto completo, download       |
| **PubMed**           | Key opcional    | ✅    | 3-10/seg          | 35M+         | Saúde, medicina               |
| **arXiv**            | Nenhuma         | ✅    | 1/3seg            | 2M+          | Exatas, computação           |
| **DOAJ**             | Nenhuma         | ✅    | —                | 9M+          | Periódicos OA verificados     |
| **SciELO**           | Nenhuma         | ✅    | —                | 900K+        | América Latina, português    |
| **Google Custom**    | API Key         | ✅*   | 100/dia           | Web toda     | Busca geral                    |
| **Bing**             | API Key         | ✅*   | 1K/mês           | Web toda     | Busca geral + notícias        |
| **Brave**            | API Key         | ✅*   | 2K/mês           | Web toda     | Privacidade, boa qualidade     |
| **DuckDuckGo**       | Nenhuma         | ✅    | —                | Web toda     | Instant answers                |
| **NewsAPI**          | API Key         | ✅*   | 100/dia           | 150K+ fontes | Notícias globais              |
| **GDELT**            | Nenhuma         | ✅    | —                | Bilhões     | Análise de mídia, sentimento |
| **YouTube**          | API Key         | ✅*   | 10K un/dia        | YouTube      | Vídeos, palestras, opiniões  |
| **Reddit**           | Nenhuma (.json) | ✅    | ~60/min           | Reddit       | Discussões, opiniões         |
| **Twitter/X**        | Bearer Token    | ❌    | —                | Twitter/X    | Opiniões públicas            |
| **Scopus**           | API Key         | 🟡    | —                | 91M+         | Acadêmica premium             |
| **Web of Science**   | API Key         | 🟡    | —                | 171M+        | Acadêmica premium             |

> ✅* = Gratuito com limites, sem necessidade de cartão de crédito
> 🟡 = Requer acesso institucional ou plano especial

---

> **Este documento serve como referência completa para implementar o módulo
> de pesquisa do Paper Builder. Comece pelas APIs de prioridade 1 (Semantic
> Scholar + OpenAlex + CrossRef + Unpaywall) e vá adicionando as demais
> conforme necessidade.**

```

---

Esse MD cobre todas as fontes de pesquisa, APIs e estratégias. Quer que eu comece a codar alguma parte específica do app agora?
```
