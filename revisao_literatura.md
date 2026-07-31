# REVISAO DA LITERATURA — BANCO DE FICHAMENTO DOS ARTIGOS DE CONGRESSO

**Ultima atualizacao:** 31/07/2026

## 1. OBJETIVO

Construir um banco de fichamento bibliografico que embase teoricamente os **4 artigos de congresso** do projeto:

| # | Artigo | Pasta |
|---|--------|-------|
| 02 | Copiloto Algoritmico (Artigo Tecnologico) | `artigos_congressos/BTCongress/Artigo-Tecnologico-Copiloto/` |
| 10 | Uso Retorico da "Inovacao" (innovation washing) | `artigos_congressos/Enbra/Artigo10-Uso-Retorico-Inovacao/` |
| 15 | Enquadramento da IA no Controle Publico na Midia | `artigos_congressos/Enbra/Artigo15-Enquadramento-IA-Midia/` |
| 17 | DSR na Contabilidade Publica (Scoping Review) | `artigos_congressos/BTCongress/Artigo17-DSR-Contabilidade-Publica/` |

## 2. METAS

- **15 temas** organizados em 4 blocos teoricos.
- **Pelo menos 25 fichamentos por tema** → total alvo: **≥ 375 registros**.
- Proporcao por tema: **70% artigos recentes** (2018-2026) + **30% classicos/seminais**.
- Para cada tema: cobrir tanto os **autores classicos** (fundadores do constructo) quanto o **estado-da-arte recente**.

## 3. CRITERIOS DE INCLUSAO / EXCLUSAO

### Inclusao
- Artigos, revisoes sistematicas, meta-analises, capitulos de livro e working papers publicados em fontes revisadas por pares ou repositórios academicos reconhecidos (SSRN, NBER, arXiv para IA).
- Relevancia direta ao constructo teorico do tema e ao congresso-alvo.
- Portugues ou ingles.
- Recuperados em pelo menos uma base e com metadados completos (DOI ou identificador confiavel).

### Exclusao
- Noticias, blogs, materiais de divulgacao sem revisao.
- Duplicados (deduplicacao obrigatoria por DOI/DOI-normalizado ou titulo).
- Artigos fora do escopo tematico apos leitura do resumo.

## 4. BASES DE BUSCA

| Base | Tipo de acesso | Prioridade | Uso |
|------|----------------|-----------|-----|
| **OpenAlex** | API gratuita (já usada no projeto) | ★★★★★ | Busca automatizada, metadados, citacoes |
| **Scopus** | Assinatura | ★★★★★ | Qualidade + citacoes + filtros |
| **Web of Science** | Assinatura | ★★★★★ | Qualidade + citacoes |
| **Google Scholar** | Gratuito | ★★★★ | Cobertura ampla, citacoes |
| **Semantic Scholar** | API gratuita | ★★★★ | IA/CS, resumos |
| **Lens.org** | Gratuito/API | ★★★ | Patentes + artigos |
| **IEEE Xplore / ACM DL** | Assinatura | ★★★ | XAI, NLP, sistemas |
| **SSRN** | Gratuito | ★★ | Preprints financas/direito |
| **Periódicos CAPES** | Institucional | ★★★ | Acesso texto completo PT-BR |

## 5. QUERIES DE BUSCA (TEMPLATE GERAL)

Padrao por tema (em ingles e portugues):

```
<construct core> AND <dominio> AND <modificador>
```

Exemplo (TCE + compras):
```
("transaction cost" OR "transaction cost economics") AND ("public procurement" OR "public contracting" OR "government procurement")
```

Estrategia por bloco:
- **Clássicos**: buscar sem filtro de ano, ordenar por `cited_by_count` desc, selecionar os 3-5 seminais.
- **Recentes**: filtrar `publication_year >= 2018`, ordenar por relevancia/citacoes recentes, selecionar 15-20.
- Combinar tambem a estrategia de **bola de neve** (snowballing) a partir das referencias dos 4 artigos e dos classicos encontrados.

## 6. TEMAS E SPRINTS DE BUSCA

Cada sprint corresponde a um tema e deve gerar **≥ 25 registros** no `fichamento_congressos.csv`.

### BLOCO A — FUNDACOES ECONOMICAS E INSTITUCIONAIS (Sprints 1-7)

#### Sprint 1 — Compras Publicas Complexas
- **Artigos fonte:** 10, 17
- **Autores classicos-alvo:** Thai (2001), Erridge & McMurray (2005), Jackson (2012), Caldwell et al. (2009), Georghiou et al. (2013)
- **Autores recentes-alvo:** Ntompras et al. (2024), Knight et al. (2023), Uyarra et al. (2022), Grandia & Voncken (2019)
- **Queries:**
  - EN: `("complex public procurement" OR "procurement complexity" OR "complex contracting") AND (government OR public sector)`
  - EN: `("public procurement" AND "complexity") AND (typology OR framework OR definition)`
  - PT: `"compras publicas complexas" OR "complexidade em compras publicas"`

#### Sprint 2 — Public Procurement of Innovation (PPI)
- **Artigos fonte:** 10, 17
- **Autores classicos-alvo:** Edler & Georghiou (2007), Georghiou et al. (2013), Uyarra & Flanagan (2010), Rolfstam (2012), Lember et al. (2014)
- **Autores recentes-alvo:** Dinlersoz et al. (2023), Obenaus et al. (2024), Palte et al. (2024), Zirpoli & Becker (2021)
- **Queries:**
  - EN: `"public procurement of innovation" AND (policy OR demand-side OR instruments)`
  - EN: `("procurement" AND "innovation") AND (mission-oriented OR pre-commercial OR PCP)`
  - PT: `"compras publicas de inovacao"`

#### Sprint 3 — Estado Empreendedor e Políticas Mission-Oriented (Mazzucato)
- **Artigos fonte:** 02, 10, 17
- **Autores classicos-alvo:** Mazzucato (2013, 2018), Edler & Georghiou (2007)
- **Autores recentes-alvo:** Rodrik (2024), Cirera & Lage (2023), Kattel et al. (2023), Foray et al. (2022), Jacobsson & Vasa (2024)
- **Queries:**
  - EN: `("entrepreneurial state" OR "mission-oriented innovation" OR "mission economy") AND (public OR state OR government)`
  - EN: `"public procurement" AND ("market creation" OR "demand-side innovation policy")`
  - PT: `"estado empreendedor" OR "politicas mission-oriented"`

#### Sprint 4 — Economia dos Custos de Transacao (TCE / Williamson-Coase)
- **Artigos fonte:** 02, 10, 17
- **Autores classicos-alvo:** Coase (1937), Williamson (1979, 1981, 1985, 2010), Shelanski & Klein (1995), Rindfleisch & Heide (1997)
- **Autores recentes-alvo:** Masten (2022), Ménard (2017, 2022), Johnsen (2023), Braidford et al. (2024), Tadelis (2012)
- **Queries:**
  - EN: `("transaction cost economics" OR "transaction cost") AND ("public procurement" OR "government contracting")`
  - EN: `(Williamson OR Coase) AND (contract OR governance OR asset specificity)`
  - PT: `"custos de transacao" AND "compras publicas"`

#### Sprint 5 — Teoria da Agencia em Compras Publicas
- **Artigos fonte:** 02
- **Autores classicos-alvo:** Jensen & Meckling (1976), Eisenhardt (1989), Moe (1984), Pratt & Zeckhauser (1985)
- **Autores recentes-alvo:** Brey & Briggle (2022), Torbat et al. (2023), Khi et al. (2024), Gonzalez-Benito (2021)
- **Queries:**
  - EN: `("agency theory" OR "principal-agent") AND ("public procurement" OR "public contracting" OR outsourcing)`
  - EN: `"agency costs" AND (government OR public sector) AND (contract OR outsourcing)`
  - PT: `"teoria da agencia" AND "licitacao"`

#### Sprint 6 — Isomorfismo Institucional e Teoria Institucional
- **Artigos fonte:** 10
- **Autores classicos-alvo:** DiMaggio & Powell (1983), Meyer & Rowan (1977), Scott (2001)
- **Autores recentes-alvo:** (buscar aplicacoes recentes de isomorfismo em organizacoes publicas)
- **Queries:**
  - EN: `("institutional isomorphism" OR "mimetic isomorphism" OR "new institutionalism") AND (public OR government OR organization)`
  - EN: `"institutional theory" AND ("public procurement" OR "public administration")`
  - PT: `"isomorfismo institucional"`

#### Sprint 7 — Paralisia Decisoria / "Apagao das Canetas" / Direito Administrativo do Medo
- **Artigos fonte:** 10, 17
- **Autores classicos-alvo:** Valgas dos Santos (2020), Sundfeld (2014)
- **Autores recentes-alvo:** Wanderer & Knappe (2023), Rauch & Wulff (2021), Baldwin & Black (2023), Bovens & Yesilkagit (2024), Daouk & Bryde (2024), Husted & Shapiro (2023)
- **Queries:**
  - EN: `("bureaucratic paralysis" OR "decision paralysis" OR "fear of accountability") AND (public OR government OR procurement)`
  - EN: `("chilling effect" OR "fear of blame" OR "risk aversion") AND ("public manager" OR "public procurement")`
  - PT: `"apagao das canetas" OR "direito administrativo do medo" OR "medo de responsabilizacao"`

### BLOCO B — DISCURSO, LEGITIMIDADE E MIDIA (Sprints 8-10)

#### Sprint 8 — Washing: Greenwashing, CSR-Washing, Impact-Washing e Innovation-Washing
- **Artigos fonte:** 10
- **Autores classicos-alvo:** Lyon & Montgomery (2015), Marquis et al. (2016), Bowen (2014), Pope & Wæraas (2016), Christensen et al. (2013)
- **Autores recentes-alvo:** Busch et al. (2021) + buscar inovacoes recentes no constructo (washing em inovacao, tech-washing)
- **Queries:**
  - EN: `("greenwashing" OR "csr-washing" OR "impact washing" OR "innovation washing") AND (institutional OR legitimacy OR rhetoric)`
  - EN: `"washing" AND ("public procurement" OR government OR "public sector")`
  - PT: `"maquiagem de inovacao" OR "innovation washing"`

#### Sprint 9 — Framing Analysis e Cobertura MidiaTica
- **Artigos fonte:** 15
- **Autores classicos-alvo:** Entman (1993), Semetko & Valkenburg (2000), Porto (2007), Mendonça & Simões (2012)
- **Autores recentes-alvo:** (aplicacoes recentes de framing em tecnologia, IA e politicas publicas)
- **Queries:**
  - EN: `("framing theory" OR "media framing") AND (technology OR algorithms OR "artificial intelligence")`
  - EN: `"agenda-setting" AND ("public sector" OR government OR policy)`
  - PT: `"analise de enquadramento" AND (midia OR jornalismo OR politica)`

#### Sprint 10 — Legitimidade Organizacional e Sociotecnica
- **Artigos fonte:** 15
- **Autores classicos-alvo:** Suchman (1995), Deephouse & Suchman (2008), Bitektine & Haack (2015)
- **Autores recentes-alvo:** (legitimidade de IA/algoritmos em instituicoes)
- **Queries:**
  - EN: `("organizational legitimacy" OR "legitimacy theory") AND ("artificial intelligence" OR algorithm OR automation)`
  - EN: `"legitimacy" AND ("public administration" OR government) AND (technology OR digital)`
  - PT: `"legitimidade organizacional"`

### BLOCO C — ALGORITMOS, IA E XAI (Sprints 11-14)

#### Sprint 11 — Governanca Algoritmica
- **Artigos fonte:** 15, 17
- **Autores classicos-alvo:** Danaher et al. (2017), Koenig (2019), Janssen et al. (2020), Passotti et al. (2022)
- **Autores recentes-alvo:** Zuiderwijk et al. (2021), Wirtz et al. (2020) + buscar estado-da-arte 2023-2026
- **Queries:**
  - EN: `("algorithmic governance" OR "algorithmic accountability") AND (government OR "public sector" OR "public administration")`
  - EN: `("governance of algorithms" OR "AI governance") AND (public OR state)`
  - PT: `"governanca algoritmica"`

#### Sprint 12 — Aceitacao de Algoritmos: Aversao e Apreciacao
- **Artigos fonte:** 15
- **Autores classicos-alvo:** Dietvorst et al. (2015), Logg et al. (2019)
- **Autores recentes-alvo:** (algorithm acceptance, AI acceptance no setor publico 2020-2026)
- **Queries:**
  - EN: `("algorithm aversion" OR "algorithm appreciation") AND (decision OR public OR government)`
  - EN: `("acceptance of AI" OR "trust in algorithms") AND ("public sector" OR government)`
  - PT: `"avaliacao de algoritmos" OR "aceitacao de IA"`

#### Sprint 13 — XAI: Explicabilidade, SHAP, LIME, Contrafactuais
- **Artigos fonte:** 02, 15
- **Autores classicos-alvo:** Lundberg & Lee (2017), Ribeiro et al. (2016), Wachter et al. (2017), Doshi-Velez & Kim (2017), Arrieta et al. (2020), Rudin (2019)
- **Autores recentes-alvo:** (XAI no setor publico, explicações contrafactuais, avaliação de explicabilidade)
- **Queries:**
  - EN: `("explainable AI" OR XAI) AND (government OR "public sector" OR "public administration")`
  - EN: `(SHAP OR LIME OR "counterfactual explanations") AND (decision support OR accountability)`
  - PT: `"inteligencia artificial explicavel"`

#### Sprint 14 — IA e NLP em Compras Publicas
- **Artigos fonte:** 02
- **Autores classicos-alvo:** Vaidya et al. (2006) (e-procurement)
- **Autores recentes-alvo:** Hacked & Alsheikh (2024), Soltes et al. (2023), Kral et al. (2024), Parn et al. (2023)
- **Queries:**
  - EN: `("artificial intelligence" OR "machine learning" OR NLP) AND ("public procurement")`
  - EN: `("e-procurement" OR "procurement automation") AND (AI OR algorithm OR text mining)`
  - PT: `"inteligencia artificial" AND "licitacao" OR "compras publicas"`

### BLOCO D — METODOLOGIA (Sprint 15)

#### Sprint 15 — Design Science Research (DSR)
- **Artigos fonte:** 02, 17
- **Autores classicos-alvo:** Hevner et al. (2004), Peffers et al. (2007), Gregor & Hevner (2013), March & Smith (1995), Walls et al. (2021), Kuechler & Vaishnavi (2012)
- **Autores recentes-alvo:** vom Brocke et al. (2020), Baskerville et al. (2019), Venable et al. (2012/2016), Sonnenberg & vom Brocke (2022), Niederman & March (2021)
- **Queries:**
  - EN: `("design science research" OR DSR) AND (methodology OR evaluation OR artifacts)`
  - EN: `"design science" AND ("public administration" OR "public accounting" OR "public sector")`
  - EN: `("FEDS" OR "Gregor and Hevner" OR "design principles") AND evaluation`
  - PT: `"pesquisa em design science" OR "design science research"`

## 7. FLUXO DE TRABALHO POR SPRINT

```
1. RODAR QUERIES nas bases (OpenAlex automatizado; Scopus/WoS/GS manual ou API)
2. DEDUPLICAR por DOI normalizado (e titulo quando sem DOI)
3. TRIAGEM: ler titulo+resumo; aplicar criterios de inclusao/exclusao
4. CLASSIFICAR: categoria (classico=30% / recente=70%) por tema
5. FICHAR: preencher todas as colunas do fichamento_congressos.csv
6. QA: verificar metadados completos, DOI valido, coerencia da relacao_artigo
7. ATUALIZAR status para "fichado"
```

## 8. SCHEMA DO BANCO — `fichamento_congressos.csv`

Delimitador: `;` | Encoding: UTF-8 | Linha de cabecalho com os campos abaixo.

| Campo | Descricao |
|-------|-----------|
| `id` | Identificador unico (tema+numero) |
| `tema` | Nome do tema (Sprint 1-15) |
| `autores` | Autores completos (ABNT: SOBRENOME, N. et al.) |
| `ano` | Ano de publicacao |
| `titulo` | Titulo completo |
| `journal` | Periodico/fonte |
| `doi` | DOI ou identificador confiavel |
| `base_dados` | Base onde foi recuperado (OpenAlex, Scopus, WoS...) |
| `citacoes` | Numero de citacoes |
| `categoria` | `classico` ou `recente` (derivado do ano real: >=2018 = recente) |
| `palavras_chave` | Palavras-chave do artigo |
| `resumo` | Resumo/abstract |
| `objetivos` | Objetivos declarados |
| `metodologia` | Metodo, amostra, coleta, analise |
| `resultados` | Principais resultados |
| `posicao_academica` | Posicao no debate (fundador, consolidador, critico, aplicador, estado-da-arte) |
| `paradigma` | Positivista, interpretativista, pragmatista, design science, critico, pos-positivista |
| `principais_achados` | Achados-chave sintetizados |
| `relacao_artigo` | Artigo do congresso que usa o fichamento (02, 10, 15, 17) |
| `status` | `pendente` (apenas cabecalho) → `fichado` |

## 8b. EXECUCAO CURADA (31/07/2026) — LISTA-MESTRA + VALIDACAO

A execucao abandonou a busca generica (Crossref/OpenAlex com ruido) e adotou a
**metodologia da lista-mestra curada** (mesma do projeto Itau):

1. **Curadoria manual** de obras REAIS por tema em `curadoria/bloco_*.json`:
   - Classicos seminais conhecidos da literatura de cada tema;
   - Recentes de alto impacto (2018-2026) conhecidos / referenciados nos 4 artigos.
2. **Validacao no Crossref por CORRESPONDENCIA DE TITULO**:
   - `builder_fichamento_curado.py` consulta o DOI fornecido; so aceita se o
     titulo retornado bater com o curado (ratio >= 0.62).
   - Se o DOI fornecido for invalido, tenta `query.bibliographic` pelo titulo e
     adota o melhor candidato que bata no titulo.
   - Se nada bater, preserva os metadados CURADOS e marca `base_dados =
     'Referencia (sem DOI confirmado)'`.
3. **Campos analiticos** (resumo, objetivos, metodologia, resultados, posicao
   academica, paradigma, achados, relacao_artigo) curados por sintese fiel do
   conteudo real de cada obra.

**Resultado (389 obras):**
- **288 obras com DOI confirmado** no Crossref (74%).
- **101 obras como referencia** (sem DOI confirmado — preserva metadados curados).
- Proporcao por ano real: **41% recentes (2018+) / 59% classicos** no total.
  Temas IA/XAI atingem a meta (S13: 75%, S14: 84%); temas de fundacao teorica
  (TCE, Isomorfismo, Framing, Legitimidade) permanecem classicos por natureza.
  O refinamento da proporcao 70/30 por tema fica como sprint futuro (busca
  Scopus/WoS para ampliar recentes nesses temas).

**Scripts criados:**
| Script | Funcao |
|--------|--------|
| `Scripts_Extracao/builder_fichamento_curado.py` | Valida DOIs no Crossref por titulo + gera CSV |
| `Scripts_Extracao/adicionar_recentes.py` | Enriquece blocos com recentes reais |
| `Scripts_Extracao/consolidar_blocos.py` | Deduplica e reagrupa por tema/bloco |

## 9. CRONOGRAMA

| Fase | Sprints | Previsao |
|------|---------|----------|
| Fase 1 — Bloco A | Sprints 1-7 (fundacoes economicas) | Semana 1 |
| Fase 2 — Bloco B | Sprints 8-10 (discurso/legitimidade) | Semana 2 |
| Fase 3 — Bloco C | Sprints 11-14 (IA/XAI) | Semana 2-3 |
| Fase 4 — Bloco D | Sprint 15 (DSR) | Semana 3 |
| Fase 5 — QA | Revisao cruzada, completude, dedup final | Semana 4 |

## 10. FERRAMENTAS

- **Busca automatizada:** adaptar `Base_de_Dados_e_APIs/Scripts_Extracao/extrator_fichamento_openalex.py` para receber a lista de temas/queries e gravar direto no `fichamento_congressos.csv`.
- **Exportacao Scopus/WoS:** exportar CSV e merge manual (ou script de merge por DOI).
- **Snowballing:** extrair referencias dos classicos e dos 4 artigos para completar lacunas.

### Nota operacional (31/07/2026)

A API do OpenAlex opera com **orçamento diário gratuito** que reseta à meia-noite UTC. Ao executar o extrator e obter `429 Rate limit exceeded`, o orçamento do dia esgotou — **repetir no dia seguinte** ou usar as bases de assinatura (Scopus/WoS) como fallback. O script já implementa backoff exponencial (até 5 tentativas por requisição).
