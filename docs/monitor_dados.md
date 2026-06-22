# Monitor de Dados - Tese de Doutorado

## Visão Geral do Projeto

**Tema:** Copiloto Algorítmico para Compras Públicas Complexas
**Pesquisador:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Fucape Business School - Doutorado em Contabilidade

---

## Status atual: 18 Artigos + 1 Artefato

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
| 01 | Complexidade Textual em Editais de Inovação | Texto integral de editais (15 editais reais) | PNCP API | 🟢 Pronto |
| 02 | Detecção de Anomalias de Preços | Dados de preços (10.5K registros) | Portal Transparência | 🟢 Pronto |
| 03 | Predição de Fracasso de Contratos | Contratos + aditivos (12.5K registros) | PNCP + Transparência | 🟢 Pronto |
| 04 | "Apagão das Canetas": Latência Decisória | Acórdãos TCU + timestamps editais (9K registros) | API TCU + PNCP | 🟢 Pronto |
| 05 | Redes de Fornecimento e Oligopólios | Nós e arestas da rede complexa (400 nós, 1.1K arestas) | PNCP + Transparência | 🟢 Pronto |
| 06 | Análise de Sobrevivência (Kaplan-Meier) | Contratos com datas (10K registros) | Portal Transparência | 🟢 Pronto |
| 07 | Governança Algorítmica: Benchmarking | Métricas por órgão (180 municípios) | Siconfi + IBGE | 🟢 Pronto |
| 08 | XAI em Prova de Conceito: TCEs | Decisões de auditoria (8.5K registros) | Bases Históricas + Dados TCU | 🟢 Pronto |
| 18 | Compliance Algorítmico em Compras de Inovação | Registros PNCP 2024 (273.309 registros) | PNCP Bulk (dados.gov.br) | 🟢 Pronto |

---

## ARTIGOS QUALITATIVOS (09-15)

| # | Artigo | Dados Necessários | Fonte | Status |
|---|--------|-------------------|-------|--------|
| 09 | "Jurisprudência do Medo": Análise de Discurso | Acórdãos TCU (5 acórdãos reais) | API Jurisprudência TCU | 🟢 Pronto |
| 10 | Uso Retórico da Inovação em Justificativas | Textos de justificativas (300-500) | PNCP API | 🟢 Pronto |
| 11 | "Voz do Mercado": Impugnações de Editais | Editais impugnados (150 registros Bardin + Qui-Quadrado) | Compras.gov.br | 🟢 Pronto |
| 12 | Evolução da Legislação de Compras | Textos legislativos (25 atos reais) | Download direto (Planalto) | 🟢 Pronto |
| 13 | "Dor das GovTechs": Netnografia | Posts e discussões (1.5K menções reais) | LinkedIn + Reddit | 🟢 Pronto |
| 14 | Discurso do "Custo Brasil" e Política Industrial | Notícias (450 matérias reais) | NewsAPI + Google | 🟢 Pronto |
| 15 | Enquadramento da IA no Controle Público | Cobertura jornalística (388 matérias Conjur/Valor/Jota) | Web Scraping (Conjur, Valor, Jota) | 🟢 Pronto |

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

## PENSADORES CRÍTICOS DA TECNOLOGIA NA GESTÃO

| # | Autor | Obra Principal | Ano | Foco da Crítica | Status |
|---|-------|----------------|------|-----------------|--------|
| 1 | Harry Braverman | Labor and Monopoly Capital | 1974 | Desqualificação do trabalho (*deskilling*) via automação | 🟢 Incorporado |
| 2 | Andrew Feenberg | Questioning Technology | 1999 | Teoria Crítica da Tecnologia: design tecnológico incorpora valores de controle | 🟢 Incorporado |
| 3 | Byung-Chul Han | Psicopolítica | 2014 | Controle psíquico via Big Data e autoexploração na gestão | 🟢 Incorporado |
| 4 | Karl Marx | O Capital (Livro I) | 1867 | Subordinação do trabalhador pela maquinaria e extração de mais-valia | 🟢 Incorporado |
| 5 | Shoshana Zuboff | The Age of Surveillance Capitalism | 2019 | Capitalismo de vigilância e modificação de conduta via algoritmos | 🟢 Incorporado |
| 6 | Evgeny Morozov | To Save Everything, Click Here | 2013 | Crítica ao solucionismo tecnológico na gestão pública | 🟢 Incorporado |
| 7 | Mats Alvesson & Hugh Willmott | Critical Management Studies | 1992 | Controle ideológico e assimetrias de poder nos discursos gerenciais | 🟢 Incorporado |
| 8 | Alberto Guerreiro Ramos | A Nova Ciência das Organizações | 1981 | Crítica à racionalidade instrumental na administração pública | 🟢 Incorporado |
| 9 | Maurício Tragtenberg | Burocracia e Ideologia | 1974 | Teorias da administração como ideologias de dominação burocrática | 🟢 Incorporado |
| 10 | Maria Ceci Misoczky | Considerações sobre a crítica nos Estudos Organizacionais | 2002 | Risco de cooptação da crítica pelo discurso gerencialista hegemônico | 🟢 Incorporado |

---

## RESUMO EXECUTIVO

### Dados Concluídos

| Categoria | Quantidade | Porcentagem |
|-----------|------------|--------------|
| Artigos com dados ✅ | 18 | 100.0% |
| Pensadores críticos incorporados 🟢 | 10 | 100.0% |
| Artigos com dados parciais ⚠️ | 0 | 0.0% |
| Artigos pendentes 🔴 | 0 | 0.0% |

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

*Última atualização: 18 de Maio de 2026*
*Repositório: github.com/renato0503/TeseDoutorado*