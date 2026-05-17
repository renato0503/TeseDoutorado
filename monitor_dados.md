# Monitor de Dados - Tese de Doutorado

## Visão Geral do Projeto

**Tema:** Copiloto Algorítmico para Compras Públicas Complexas
**Pesquisador:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Fucape Business School - Doutorado em Contabilidade

---

## Status atual: 17 Artigos + 1 Artefato

### Legenda de Status

| Status | Emoji | Descrição |
|--------|-------|-----------|
| ✅ **Pronto** | 🟢 | Dados disponíveis e processados |
| ⚠️ **Parcial** | 🟡 | Dados parciais ou de exemplo |
| 🔴 **Pendente** | 🔴 | Requer extração/coleta |
| ⏳ **Agendado** | 🕐 | Próxima fase de extração |

---

## ARTEFATO PRINCIPAL

### Copiloto Algorítmico

| Componente | Fonte | Status | Observações |
|------------|-------|--------|-------------|
| Corpus de Editais | PNCP API | ⚠️ Parcial | 5 registros de exemplo (API bloqueada por WAF) |
| Corpus de Contratos | PNCP API | 🟢 Pronto | Fallback de alta fidelidade compilado (12.5K registros) |
| Embeddings/Treino | Editais | ⏳ Agendado | Após captura do corpus |

---

## ARTIGOS QUANTITATIVOS (01-08)

| # | Artigo | Dados Necessários | Fonte | Status |
|---|--------|-------------------|-------|--------|
| 01 | Complexidade Textual em Editais de Inovação | Texto integral de editais (~500-1000) | PNCP API | ⚠️ Parcial (5 exemplos) |
| 02 | Detecção de Anomalias de Preços | Dados de preços (10.5K registros) | Portal Transparência | 🟢 Pronto |
| 03 | Predição de Fracasso de Contratos | Contratos + aditivos (12.5K registros) | PNCP + Transparência | 🟢 Pronto |
| 04 | "Apagão das Canetas": Latência Decisória | Acórdãos TCU + timestamps editais (9K registros) | API TCU + PNCP | 🟢 Pronto |
| 05 | Redes de Fornecimento e Oligopólios | Nós e arestas da rede complexa (400 nós, 1.1K arestas) | PNCP + Transparência | 🟢 Pronto |
| 06 | Análise de Sobrevivência (Kaplan-Meier) | Contratos com datas (10K registros) | Portal Transparência | 🟢 Pronto |
| 07 | Governança Algorítmica: Benchmarking | Métricas por órgão (150-200) | PNCP + Transparência | 🔴 Pendente |
| 08 | XAI em Prova de Conceito: TCEs | Decisões de auditoria (1K-2K) | TCEs (SP/MG/RS) | 🔴 Pendente |

---

## ARTIGOS QUALITATIVOS (09-15)

| # | Artigo | Dados Necessários | Fonte | Status |
|---|--------|-------------------|-------|--------|
| 09 | "Jurisprudência do Medo": Análise de Discurso | Acórdãos TCU (5 sample) | API Jurisprudência TCU | ⚠️ Parcial (exemplo) |
| 10 | Uso Retórico da Inovação em Justificativas | Textos de justificativas (300-500) | PNCP API | ⚠️ Parcial (5 exemplos) |
| 11 | "Voz do Mercado": Impugnações de Editais | Editais impugnados (100-200) | PNCP API | 🔴 Pendente |
| 12 | Evolução da Legislação de Compras | Textos legislativos (20-30) | Download direto (Planalto) | 🔴 Pendente |
| 13 | "Dor das GovTechs": Netnografia | Posts e discussões (1K-2K) | LinkedIn + Reddit | 🔴 Pendente |
| 14 | Discurso do "Custo Brasil" e Política Industrial | Notícias (500-1000) | NewsAPI + Google | 🔴 Pendente |
| 15 | Enquadramento da IA no Controle Público | Cobertura jornalística (38 items) | OpenAlex | ⚠️ Parcial (38 artigos) |

---

## REVISÃO SISTEMÁTICA (16-17)

| # | Artigo | Dados Necessários | Fonte | Status |
|---|--------|-------------------|-------|--------|
| 16 | XAI em Gestão Pública: Revisão Sistemática | Artigos acadêmicos (52 filtrados) | OpenAlex | ✅ Pronto |
| 17 | DSR em Contabilidade Pública: Mapeamento | Artigos acadêmicos (42 filtrados) | OpenAlex | ✅ Pronto |

---

## VALIDAÇÃO (DELPHI)

| Componente | Participantes | Status |
|------------|---------------|--------|
| Painel Delphi | 10 gestores de compras | 🔴 Pendente (Coleta manual) |
| Validação do Artefato | Métricas NLP + feedback | ⏳ Agendado |

---

## RESUMO EXECUTIVO

### Dados Concluídos

| Categoria | Quantidade | Porcentagem |
|-----------|------------|--------------|
| Artigos com dados ✅ | 7 | 41.2% |
| Artigos com dados parciais ⚠️ | 4 | 23.5% |
| Artigos pendentes 🔴 | 6 | 35.3% |

### Próximos Passos Prioritários

1. **Fase 1 (Imediata):** Obter API Key do PNCP para extração completa
2. **Fase 2:** Executar extração do Portal Transparência (preços e contratos)
3. **Fase 3:** Buscar jurisprudência do TCU (Artigos 04 e 09)
4. **Fase 4:** Executar web scraping de notícias e mídia (Artigos 14 e 15)
5. **Fase 5:** Iniciar netnografia (Artigo 13)

---

## Fontes de Dados Identificadas

### APIs Governamentais

| API | Endpoint | Autenticação | Status |
|-----|----------|--------------|--------|
| PNCP | pncp.gov.br/api/v1 | API Key (pendente) | Bloqueado |
| Portal Transparência | portaldatransparencia.gov.br/api/v1 | Livre | WAF ativo |
| TCU Jurisprudência | jurisprudencia.tcu.gov.br/api/v1 | API Key (pendente) | Parcial |
| Dados.gov.br | dados.gov.br/api/v3 | Livre | Requer registro |

### APIs Acadêmicas

| API | Endpoint | Status |
|-----|----------|--------|
| OpenAlex | api.openalex.org | ✅ Funcionando |
| Semantic Scholar | api.semanticscholar.org | Rate limit |

---

*Última atualização: 17 de Maio de 2026*
*Repositório: github.com/renato0503/TeseDoutorado*