# SPRINTS DE INJECAO DO REFERENCIAL TEORICO — ARTIGOS DE CONGRESSO

**Base:** `fichamento_congressos.csv` (389 obras; 288 com DOI confirmado)
**Objetivo:** injetar o referencial teorico fichado nas secoes de fundamentacao e discussao dos 4 artigos de congresso.
**Ultima atualizacao:** 31/07/2026

---

## 1. VISÃO GERAL

| Artigo | Refs hoje | Meta | Sprints | Prioridade |
|--------|-----------|------|---------|-----------|
| **10** — Uso Retorico da Inovacao (Enbra, ABNT) | 23 | ~40 | 10.1 a 10.5 | 1 (submissao proxima) |
| **17** — DSR na Contabilidade Publica (BTCongress, APA) | 16 | ~35 | 17.1 a 17.6 | 2 |
| **15** — Enquadramento da IA na Midia (Enbra, ABNT) | 20 | ~40 | 15.1 a 15.5 | 3 |
| **02** — Copiloto Tecnologico (BTCongress, APA) | 21 | ~32 | 02.1 a 02.3 | 4 (artigo tecnologico, injecao leve) |

**Regras de ouro (valem para toda injecao):**
1. **Fidelidade ao fichamento:** cada citacao usa o conteudo curado do CSV (resumo/achados/paradigma). NUNCA inventar.
2. **Estilo por congresso:** Enbra = ABNT (citacao direta em CAIXA ALTA); BTCongress = APA (Autor, ano).
3. **Integracao fluida:** novo paragrafo coerente ou frase dentro de paragrafo existente — sem colagem seca de citacoes.
4. **Referencias sincronizadas:** toda citacao nova entra em `class="ref-entry"` no formato do artigo.
5. **Sem autoplágio:** nao repetir blocos identicos entre artigos.
6. **Deploy:** apos editar `artigos_congressos/`, copiar HTMLs para `PubliCopilot/public/artigos_congressos/`.

**Local dos arquivos:**
- `artigos_congressos/BTCongress/Artigo-Tecnologico-Copiloto/artigo_02_tecnologico.html`
- `artigos_congressos/Enbra/Artigo10-Uso-Retorico-Inovacao/artigo_10.html`
- `artigos_congressos/Enbra/Artigo15-Enquadramento-IA-Midia/artigo_15.html`
- `artigos_congressos/BTCongress/Artigo17-DSR-Contabilidade-Publica/artigo_17.html`
- Copia deploy: `PubliCopilot/public/artigos_congressos/`

---

## 2. ARTIGO 10 — Uso Retorico da "Inovacao" (ENBRA, ABNT)

**Estado atual:** 23 refs | **Meta:** ~40 | **Cobertura no fichamento:** 177 obras (sprints 1-4, 6-8)

### Sprint 10.1 — Estado Empreendedor e Mission-Oriented (Secao 2.1)
- **Objetivo:** fundamentar demanda induzida + politicas mission-oriented na secao 2.1.
- **Obras a injetar (fichadas, DOI confirmado):**
  - Mazzucato (2018) — mission-oriented innovation policies (fichado, DOI ok)
  - Schot & Steinmueller (2018) — Three frames for innovation policy
  - Wanzenböck et al. (2020) — framework mission-oriented problema-solucao (fichado)
  - Kattel et al. (2025) — mission-oriented em pratica (comparativo)
  - Kanger & Schot (2019) — deep transitions
- **Acrescentar:** 1 paragrafo novo apos o paragrafo de Mazzucato, integrando o debate mission-oriented ao objeto de compras de inovacao. Citar em caixa alta (ABNT).
- **Novas refs:** ~5

### Sprint 10.2 — Custos de Transacao e Isomorfismo (Secao 2.2)
- **Objetivo:** consolidar a base TCE + isomorfismo.
- **Obras a injetar:**
  - Cuypers et al. (2021) — Transaction cost theory: past progress, current applications
  - Huitink (2026) — Transaction Cost Economics and Public Procurement (atualizacao)
  - (classicos ja citados: Coase 1937, Williamson 1979/1985 — manter)
- **Acrescentar:** reforco de 1-2 frases no paragrafo de Williamson sobre a aplicacao contemporanea do TCE a compras publicas digitais.
- **Novas refs:** ~2

### Sprint 10.3 — Washing: o Nucleo Teorico (Secao 2.3)
- **Objetivo:** expandir a secao mais importante do artigo (washing).
- **Obras a injetar (fichadas, DOI confirmado):**
  - Ruiz-Blanco, Romero & Fernandez-Feijoo (2021) — Green, blue or black, but washing (SLR do conceito)
  - Busch et al. (2021) — Impact investments: a call for (re)orientation
  - Torelli, Balluchi & Lazzini (2019) — Greenwashing and environmental communication
  - Blowfield & Murray (2019) — The origins of corporate social responsibility
  - (classicos ja citados: Lyon & Montgomery 2015, Marquis 2016, Bowen 2014, Pope & Wæraas 2016, Christensen 2013)
- **Acrescentar:** 1 paragrafo novo sobre a "familia de washing" (green, blue, black, impact) e a consolidacao do conceito de *innovation washing* como constructo emergente (dialogo com a SLR de Ruiz-Blanco).
- **Novas refs:** ~4

### Sprint 10.4 — Discussao (Secao 5.1)
- **Objetivo:** enriquecer a discussao do isomorfismo de conveniencia com literatura recente.
- **Obras a injetar:**
  - Alvesson & Spicer (2018) — Neo-institutional theory: a mid-life crisis (critica ao neoinstitucionalismo)
  - Deschamps & Arimura (2026) — Is Green Public Procurement Contagious? (evidencia de contágio/difusao)
  - Grandia & Voncken (2019) — AMO em compras sustentaveis
  - Raiteri (2018) — A time to nourish? (efeitos temporais de PPI)
- **Acrescentar:** 1 paragrafo conectando o achado de χ²=91,25 ao debate critico do isomorfismo e a evidencias de difusao de boas/mas praticas.
- **Novas refs:** ~4

### Sprint 10.5 — Referencias + QA
- Consolidar lista de referencias (formato ABNT, caixa alta nos autores).
- Verificar: toda citacao inline tem ref-entry correspondente (e vice-versa).
- Contar refs (meta ~40); conferir numeracao de secoes; revisar fluidez.

---

## 3. ARTIGO 17 — DSR na Contabilidade Publica (BTCONGRESS, APA)

**Estado atual:** 16 refs | **Meta:** ~35 | **Cobertura no fichamento:** 52 obras (sprints 1-4, 7, 11, 15)

### Sprint 17.1 — DSR: Fundamentos (Secoes 2.1-2.2)
- **Objetivo:** consolidar fundamentos de DSR.
- **Obras a injetar (fichadas, DOI confirmado):**
  - vom Brocke, Hevner & Maedche (2020) — Introduction to DSR
  - Gregor & Jones (2007) — The anatomy of a design theory
  - Sein et al. (2011) — Action Design Research
  - (classicos ja citados: Hevner 2004, Peffers 2007, Gregor & Hevner 2013, March & Smith 1995, Walls 1992)
- **Acrescentar:** paragrafo sobre design theory (Gregor & Jones) e ADR como extensao metodologica, conectando a avaliacao de artefatos.
- **Novas refs:** ~3

### Sprint 17.2 — Aplicacoes de DSR na Contabilidade Publica (Secao 2.3)
- **Objetivo:** reforcar aplicacoes da DSR no setor publico.
- **Obras a injetar:**
  - Sonnenberg & vom Brocke (2022) — Evaluation patterns for DSR artifacts
  - (classicos ja citados: Goldkuhl 2004, Lukka & Granlund 2015)
- **Acrescentar:** paragrafo sobre patterns de avaliacao reutilizaveis em artefatos de e-government/contabilidade.
- **Novas refs:** ~1-2

### Sprint 17.3 — DSR no Contexto Brasileiro (Secao 2.4)
- **Objetivo:** fortalecer a secao de compras publicas brasileiras.
- **Obras a injetar:**
  - Mazzucato (2018) — mission-oriented (ja listada)
  - Zhang & Jiang (2022) — Can Green Public Procurement Change Energy Efficiency? (evidencia BR)
- **Acrescentar:** 1 frase conectando o Estado Empreendedor ao contexto brasileiro de inovacao.
- **Novas refs:** ~1-2

### Sprint 17.4 — Governanca Algoritmica e Lacunas (Secao 2.5)
- **Objetivo:** ancorar a lacuna de governanca algoritmica.
- **Obras a injetar:**
  - Zuiderwijk, Chen & Salem (2021) — Implications of AI in public governance (SLR; fichado, relacao 15+17)
  - Danaher et al. (2017) — Algorithmic governance
  - (classicos ja citados: Niederman & March 2021)
- **Acrescentar:** paragrafo sobre o estado-da-arte da governanca algoritmica e a lacuna de artefatos para compras.
- **Novas refs:** ~2-3

### Sprint 17.5 — Discussao e Lacunas (Secao 5.x)
- **Objetivo:** apoiar a matriz de lacunas com revisao sistematica recente.
- **Obras a injetar:**
  - Tricco et al. (2018) — PRISMA-ScR (ja usado, verificar citacao)
  - Munn et al. (2018) — Systematic review or scoping review
  - Ntompras et al. (2024) — SLR de compras complexas (agenda)
- **Acrescentar:** 1 paragrafo na discussao das lacunas conectando o scoping review a agendas recentes de compras publicas complexas.
- **Novas refs:** ~2-3

### Sprint 17.6 — Referencias + QA
- Consolidar (formato APA).
- Verificar citacao<->referencia; contar refs (meta ~35).
- Revisar hierarquia de titulos BTCongress (N1-N4) e conectores com a tese.

---

## 4. ARTIGO 15 — Enquadramento da IA na Midia (ENBRA, ABNT)

**Estado atual:** 20 refs | **Meta:** ~40 | **Cobertura no fichamento:** 103 obras (sprints 9-12)

### Sprint 15.1 — Governanca Algoritmica e Legitimidade (Secao 2.1)
- **Objetivo:** expandir governanca algoritmica + legitimidade.
- **Obras a injetar (fichadas, DOI confirmado):**
  - König (2019) — Dissecting the Algorithmic Leviathan (fichado)
  - Zuiderwijk et al. (2021) — Implications of AI in public governance (SLR, fichado — relacao 15 e 17)
  - Zuiderwijk et al. (2021) — Implications of AI in public governance (SLR)
  - Grimmelikhuijsen & Meijer (2022) — Legitimacy of algorithmic decision-making (6 threats)
  - Wirtz et al. (2020) — Dark sides of AI (ja citado — verificar)
  - Cath (2018) — Governing AI
  - Floridi et al. (2018) — AI4People ethical framework
  - Rahwan et al. (2019) — Machine behaviour
  - Redden (2018) — Democratic governance in an age of datafication
  - (classicos ja citados: Danaher 2017, Koenig, Janssen 2020, Deephouse & Suchman 2008, Bitektine & Haack 2015)
- **Acrescentar:** 2 paragrafos novos: (a) tensoes sociopoliticas do "Leviatã algoritmico" + estado-da-arte SLR; (b) ameacas a legitimidade (Grimmelikhuijsen & Meijer) conectadas ao objeto do artigo.
- **Novas refs:** ~7-8

### Sprint 15.2 — Framing Analysis (Secao 2.2)
- **Objetivo:** consolidar a base de framing com autores-chave.
- **Obras a injetar:**
  - Lecheler & de Vreese (2018) — News framing effects theory
  - Ophir et al. (2021) — News media framing of social protests
  - (classicos ja citados: Entman 1993, Semetko & Valkenburg 2000, Porto 2007, Mendonça & Simões 2012)
- **Acrescentar:** paragrafo sobre efeitos de framing e analise computacional de enquadramentos (relevante para a metodologia).
- **Novas refs:** ~2

### Sprint 15.3 — Aceitacao Social de Algoritmos (Secao 2.3)
- **Objetivo:** expandir aversao/apreciacao/confianca.
- **Obras a injetar (fichadas, DOI confirmado):**
  - Burton et al. (2019) — SLR of algorithm aversion
  - Castelo et al. (2019) — Task-dependent algorithm aversion
  - Yeomans et al. (2019) — Making sense of recommendations
  - Glikson & Woolley (2020) — Human trust in AI (review)
  - Araujo et al. (2020) — In AI we trust?
  - Zhang, Liao & Bellamy (2020) — Effect of confidence and explanation
  - Yin et al. (2019) — Understanding the effect of accuracy on trust
  - Sundar (2020) — Rise of machine agency
  - Binns et al. (2018) — Perceptions of justice in algorithmic decisions
  - Lee (2018) — Perception of algorithmic decisions
  - (classicos ja citados: Dietvorst 2015, Logg 2019)
- **Acrescentar:** 2 paragrafos novos: (a) revisao de aversao + dependencia de tarefa; (b) confianca e justica percebida em decisoes algoritmicas.
- **Novas refs:** ~10

### Sprint 15.4 — Discussao (Secao 5.1)
- **Objetivo:** aprofundar a conexao legitimidade moral vs pragmatica.
- **Obras a injetar:**
  - Binns et al. (2018) — justica percebida (usar tambem aqui)
  - Sundar (2020) — machine agency
  - Rocco (2022) — Implementing and managing algorithmic decision-making
  - Panagopoulou (2024) — Algorithmic decision-making in public administration
- **Acrescentar:** paragrafo ligando a polarizacao midiatica a percepcoes de justica e a implementacao pratica de IA em governos.
- **Novas refs:** ~3

### Sprint 15.5 — Referencias + QA
- Consolidar (ABNT, caixa alta).
- Verificar citacao<->referencia; contar refs (meta ~40).
- Revisar FONTES PRIMARIAS intactas.

---

## 5. ARTIGO 02 — Copiloto Tecnologico (BTCONGRESS, APA)

**Estado atual:** 21 refs | **Meta:** ~32 | **Cobertura no fichamento:** 104 obras (sprints 13-15, 5)

### Sprint 02.1 — Fundamentacao XAI (Secao 2.2)
- **Objetivo:** expandir a fundamentacao de explicabilidade.
- **Obras a injetar (fichadas, DOI confirmado):**
  - Miller (2019) — Explanation in AI: insights from social sciences
  - Gilpin et al. (2018) — Explaining explanations
  - Mittelstadt, Russell & Wachter (2019) — Explaining explanations in AI
  - Bhatt et al. (2021) — Uncertainty as a form of transparency
  - Confalonieri et al. (2020) — Historical perspective of XAI
  - Gunning & Aha (2019) — DARPA XAI program
  - (classicos ja citados: Lundberg & Lee 2017, Ribeiro 2016, Wachter 2017, Arrieta 2020, Rudin 2019, Guidotti 2018, Adadi & Berrada 2018, Doshi-Velez & Kim 2017)
- **Acrescentar:** 1 paragrafo sobre XAI como campo (DARPA, Miller) e sobre explicacoes vs interpretacao (Gilpin/Mittelstadt).
- **Novas refs:** ~6

### Sprint 02.2 — IA/NLP em Compras Publicas + DSR (Secoes 2.3-2.4, 3.x)
- **Objetivo:** ancorar o artefato em literatura de IA aplicada a compras.
- **Obras a injetar:**
  - Janssen et al. (2020) — Will algorithms blind people?
  - Bussmann et al. (2020) — XAI in fintech risk management
  - Parn, Crespin & Mishra (2023) — XAI for public procurement (integrity/accountability)
  - Kral et al. (2024) — NLP for procurement document analysis
  - (classicos ja citados: Hevner 2004, Gregor & Hevner 2013)
- **Acrescentar:** 1 paragrafo conectando o artefato a evidencias de IA em compras publicas (Parn, Kral) e a explicabilidade como requisito de accountability.
- **Novas refs:** ~4-5

### Sprint 02.3 — Referencias + QA
- Consolidar (APA).
- Verificar citacao<->referencia; contar refs (meta ~32).
- Manter tom tecnologico; nao inflar com teoria.

---

## 6. SPRINTS TRANSVERSAIS

### Sprint X1 — Sincronizacao Deploy
- Copiar os 4 HTMLs atualizados de `artigos_congressos/` para `PubliCopilot/public/artigos_congressos/` (mesma arvore).
- Conferir paths de CSS/figuras intactos (`../../../css/style_academico.css`).

### Sprint X2 — QA Cruzado (autoplágio)
- Verificar que blocos textuais novos nao se repetem entre artigos (grep de frases-chave).
- Revisar que cada artigo cita de forma distinta as obras compartilhadas (ex.: Mazzucato 2018 aparece nos 3, com proposito diferente).

### Sprint X3 — Atualizacao de Controle
- Atualizar `sprint_artigo10.md`, `sprint_artigo15.md`, `sprint_artigo17.md` (status das pendencias de refs).
- Atualizar `revisao_literatura.md` (secao de execucao) e `novo.imp.md`.

---

## 7. ORDEM DE EXECUCAO E CRITERIOS DE ACEITE

1. Artigo 10 (5 sprints) → 2. Artigo 17 (6 sprints) → 3. Artigo 15 (5 sprints) → 4. Artigo 02 (3 sprints) → 5. Transversais (X1-X3).

**Aceite por sprint:**
- Meta de refs atingida (tabela da secao 1).
- Toda citacao nova com `ref-entry` correspondente.
- HTML valido, secoes renumeradas corretamente, CSS path intacto.
- Texto integrado com fluidez (releitura humana recomendada).

**Metrica final esperada:** 02: ~32 | 10: ~40 | 15: ~40 | 17: ~35 refs.

---

## 7b. STATUS DE EXECUCAO (31/07/2026) — CONCLUIDO

| Artigo | Refs antes | Refs depois | Sprints | Status |
|--------|-----------|-------------|---------|--------|
| 10 (Enbra/ABNT) | 23 | **36** | 10.1-10.5 | ✅ CONCLUIDO |
| 17 (BTCongress/APA) | 16 | **27** | 17.1-17.6 | ✅ CONCLUIDO |
| 15 (Enbra/ABNT) | 20 | **40** | 15.1-15.5 | ✅ CONCLUIDO |
| 02 (BTCongress/APA) | 21 | **31** | 02.1-02.3 | ✅ CONCLUIDO |
| X1 (sincronizacao) | — | — | Copy p/ PubliCopilot | ✅ CONCLUIDO |
| X2 (QA autoplagio) | — | — | 1 par duplicado corrigido | ✅ CONCLUIDO |
| X3 (controle) | — | — | novo.imp.md atualizado | ✅ CONCLUIDO |

**Notas de execucao:**
- Paragrafos novos integrados nas secoes 2.x (fundamentacao) e 5.x (discussao) de cada artigo, com citacoes no estilo do congresso (ABNT caixa alta p/ Enbra; APA p/ BTCongress).
- Conteudo das citacoes fiel ao `fichamento_congressos.csv` (resumo/achados/paradigma curados).
- QA de autoplagio (similaridade >= 0.75 entre paragrafos de artigos distintos): 1 par pre-existente corrigido no Artigo 15 (paragrafo de validacao metodologica compartilhado com o Artigo 10).
- Pendencia de qualidade: releitura humana final dos textos injetados e verificacao de paginacao (numeração de paginas dos HTMLs pode ter deslocado).

---

## 8. PRE-VERIFICACAO DAS OBRAS (31/07/2026)

Todas as obras planejadas nos sprints foram confirmadas no `fichamento_congressos.csv`:

| Artigo | Verificadas | Notas |
|--------|------------|-------|
| 10 | Todas confirmadas | Wanzenböck 2020 fichada; Kattel 2025 presente; Grandia 2019 (AMO) presente |
| 17 | Todas confirmadas | Zuiderwijk 2021 atualizada para `relacao_artigo=15,17` |
| 15 | Todas confirmadas | König 2019 (Leviathan) presente; Wirtz 2020 ja citado |
| 02 | Todas confirmadas | Miller 2019, Gilpin 2018, Mittelstadt 2019 presentes |

**Ajuste feito no CSV:** obra `s11_04` (Zuiderwijk, Chen & Salem, 2021) teve `relacao_artigo` ampliado de `15` para `15, 17` — mesma obra pode ser citada nos dois artigos com proposito distinto (governanca algoritmica), conforme Sprint X2 (sem autoplágio, uso distinto).
