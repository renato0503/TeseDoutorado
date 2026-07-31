# Sprint de Melhorias — Artigo 17
## Design Science Research na Contabilidade Pública: Mapeamento de Artefatos, Tipologias de Contribuição e Lacunas para a Governança Algorítmica

**Status atual:** 7,0/10 — PRISMA-ScR, 42 artigos, matriz Gregor & Hevner, lacunas identificadas
**Fragilidades críticas:** Sem abstract em inglês; corpus pequeno (42); sem fluxograma PRISMA; sem conferências; autoplágio na seção 6.1
**Objetivo:** 8,5/10 — Submissão para ICEGOV 2027 / DESRIST 2027 / EGOV 2027
**Prazo estimado:** 6 dias (sprints de 1 dia cada)

---

## Sprint 1 — Correções Estruturais Críticas (Dia 1)

### 1.1 Adicionar Abstract em Inglês (1h)
**Localização:** Após o resumo em português

**O que escrever:**

> **ABSTRACT**
>
> Design Science Research has consolidated as a methodological paradigm for research that aims to build artifacts to solve practical problems in the applied social sciences. This article investigates the typologies of artifacts and evaluation methods employed in DSR studies applied to public accounting and administration. A scoping review was conducted following the PRISMA-ScR protocol, operationalized through an automated search via the OpenAlex API. The final corpus comprises 42 articles (2004–2026), totaling 4,456 citations. Results indicate that 35.7% of artifacts are e-government information systems, 28.6% are conceptual frameworks, and 19.0% are artificial intelligence applications. The Gregor and Hevner (2013) knowledge matrix reveals that 61.9% of studies classify as improvement. A scarcity of artifacts focused on public procurement planning is identified, along with a predominance of artificialist over naturalist evaluations. These findings support a research agenda for developing AI artifacts to mitigate informational asymmetries in innovation procurement.
>
> **Keywords:** Design Science Research; Public Accounting; Artifacts; Scoping Review; Algorithmic Governance.

### 1.2 Remover Autoplágio da Seção 6.1 (2h)
**Localização:** Seção "6.1 Implicações Práticas e Políticas Públicas" (3 parágrafos genéricos)

**O que fazer:**
- Apagar COMPLETAMENTE os 3 parágrafos atuais (Capacitação em DSR / Colaboração Academia-Gestão / Adoção de IA em Compras — genéricos)
- Escrever implicações EXCLUSIVAS DO ARTIGO 17, centradas em:

**Exemplo de novo texto:**

> Os achados deste scoping review oferecem implicações para três públicos distintos.
>
> **1. Para Pesquisadores em DSR:** A predominância do quadrante *improvement* (61,9%) sobre *invention* (23,8%) indica que a área tem priorizado soluções incrementais para problemas conhecidos. Pesquisadores interessados em contribuições originais devem explorar o quadrante *invention*, especialmente no desenvolvimento de artefatos para planejamento de contratações públicas — área com cobertura de apenas 7,1% do corpus. A escassez de artefatos de IA para compras governamentais representa oportunidade concreta de contribuição teórica e prática.
>
> **2. Para Avaliadores de Periódicos e Programas:** A concentração de artefatos em sistemas e-government (35,7%) e frameworks (28,6%) sugere que a DSR na contabilidade pública tem privilegiado contribuições de baixa a média complexidade técnica. Avaliadores devem incentivar a submissão de artefatos que incorporem técnicas avançadas de IA (NLP, sistemas multi-agente, XAI), atualmente restritas a 19% do corpus. O baixo percentual de avaliações naturalistas (31,7%) é preocupante e deve ser tratado como critério de qualidade em futuras avaliações.
>
> **3. Para Gestores e Formuladores de Políticas:** A baixa proporção de artefatos voltados ao planejamento de compras (7,1%) contrasta com a relevância econômica do tema (compras públicas = 15% do PIB). Recomenda-se que agências de fomento (CAPES, CNPq, FAPs) priorizem chamadas para desenvolvimento de artefatos tecnológicos aplicados à gestão de contratações públicas, com exigência de validação naturalista em contextos operacionais reais.

### 1.3 Remover Viés do Copiloto na Conclusão (1h)
**Localização:** Seções 5 e 6 — menções genéricas a "copilotos de apoio à decisão"

**O que fazer:**
- Substituir "copilotos de apoio à decisão" por "artefatos de apoio à decisão baseados em IA"
- Manter o foco nas lacunas mapeadas, não em uma solução específica
- O artigo 17 é uma revisão — não precisa propor solução; apenas mapear e identificar oportunidades

---

## Sprint 2 — Expansão do Corpus e Refinamento da Busca (Dia 2)

### 2.1 Refazer Estratégia de Busca (3h)
**Localização:** Seção 3 — Metodologia

**Problema atual:** Apenas OpenAlex; 42 artigos; período 2004-2024 (desatualizado)

**O que fazer:**

**a) Expandir para múltiplas bases:**
- **Web of Science (WoS):** Coleção Principal
- **Scopus:** TITLE-ABS-KEY
- **OpenAlex:** manter como base complementar
- **Google Scholar:** para verificação de cobertura

**b) Reformular string de busca:**

```
("design science research" OR "DSR" OR "design science")
AND
("public accounting" OR "public sector" OR "government" OR "public administration" OR "public management")
AND
("artifact" OR "artefact" OR "system" OR "framework" OR "method" OR "instantiation")
```

**c) Expandir fontes para incluir conferências:**
- DESRIST Proceedings (Design Science Research in Information Systems)
- ICIS Proceedings (International Conference on Information Systems)
- AMCIS Proceedings (Americas Conference on Information Systems)
- EGOV Conference Proceedings

**d) Atualizar período:** 2004–2026 (incluir 2025 e 2026)

**e) Meta de corpus:** 60-80 artigos (vs. 42 atuais)

### 2.2 Incluir Fluxograma PRISMA (1,5h)
Criar o fluxograma de triagem (obrigatório para PRISMA-ScR):

```
Registros identificados (n = ~1.400)
        ↓
Após remoção de duplicatas (n = ~1.100)
        ↓
Triagem por título e resumo (n = ~1.100)
        ↓
Artigos excluídos (n = ~950) — fora do escopo
        ↓
Artigos para leitura integral (n = ~150)
        ↓
Artigos excluídos após leitura (n = ~70-90)
        ↓
Artigos incluídos na revisão (n = 60-80)
```

**O que fazer:**
- Criar o fluxograma em PNG/SVG
- Salvar como `figura0_fluxograma_prisma.png`
- Inserir no início da Seção 4

### 2.3 Justificar Exclusão de Conferências Anterior (30 min)
Se decidir manter apenas periódicos, justificar formalmente:

> A decisão de excluir anais de conferências baseou-se em três critérios: (a) artigos de conferências frequentemente não passam pelo mesmo nível de revisão por pares de periódicos; (b) muitos proceedings são posteriormente publicados em periódicos, gerando duplicidade; (c) a padronização metadadal de conferências na OpenAlex é heterogênea, comprometendo a replicabilidade. Contudo, reconhece-se que esta exclusão pode ter omitido artefatos relevantes apresentados no DESRIST, principal conferência de DSR.

**Alternativa — recomendo incluir conferências para fortalecer o corpus.** Nesse caso, remover esta justificativa e documentar a inclusão.

---

## Sprint 3 — Aprofundamento da Análise e Figuras (Dia 3)

### 3.1 Incorporar Figuras no HTML (2h)
**Arquivos existentes na pasta:**
- `figura1_tipos_artefatos.png` — adicionar como Figura 1
- `figura2_metodos_avaliacao.png` — adicionar como Figura 2
- `figura3_evolucao_temporal.png` — adicionar como Figura 3
- `figura4_distribuicao_geografica.png` — adicionar como Figura 4
- `figura5_matriz_gregor_hevner.png` — adicionar como Figura 5
- `artigo17_distribuicao_artefatos.svg` — pode ser Figura 6 ou substituir Figura 1

**O que fazer:**
- Verificar se cada figura tem tag `<figure>` com `<img>` e `<figcaption>` no HTML
- Se não existirem, adicionar com caminhos relativos corretos
- Garantir que todas as figuras sejam referenciadas no texto
- Se alguma figura estiver faltando, recriar com Python (`gerar_graficos.py` existente)

### 3.2 Análise Qualitativa por Quadrante (2h)
**Localização:** Seção 4.4 (após Tabela 3)

**O que fazer — criar subseções para cada quadrante:**

> **4.4.1 Quadrante Improvement (61,9% — 26 artigos)**
>
> Os 26 artigos classificados como *improvement* concentram-se em melhorias incrementais em sistemas de e-government (12 artigos) e frameworks conceituais (8 artigos). Exemplos representativos incluem: [Artigo A] que propõe um sistema de monitoramento de transferências fiscais com dashboard em tempo real; [Artigo B] que desenvolve um framework de maturidade para governo digital. O padrão dominante é a introdução de soluções novas para problemas já documentados, como transparência fiscal e eficiência de gastos. A inovação reside no *design* do artefato, não no problema endereçado.
>
> **4.4.2 Quadrante Invention (23,8% — 10 artigos)**
>
> Os 10 artigos de *invention* propõem soluções para problemas não endereçados anteriormente pela literatura. Destacam-se: [Artigo C] — sistema de detecção de fraudes em licitações usando redes neurais; [Artigo D] — plataforma de participação cidadã baseada em blockchain para orçamento participativo. Estes estudos representam contribuições originais tanto no problema quanto na solução.
>
> **4.4.3 Quadrantes Exaptation (9,5%) e Routine Design (4,8%)**
>
> Os quadrantes minoritários indicam que a área ainda explora pouco a transferência de soluções entre domínios (*exaptation*) e que o *routine design* é residual, sugerindo baixa incidência de pesquisas sem contribuição original.

### 3.3 Adicionar Tabela de Periódicos com Maior Contribuição (1h)
Criar nova tabela:

| Periódico | Nº Artigos | % | Fator de Impacto (JCR) | Especialidade |
|-----------|-----------|--|----------------------|--------------|
| Government Information Quarterly | 4 | 9,5% | 8,4 | Governo Digital |
| Journal of Information Systems | 4 | 9,5% | 2,1 | SI em Contabilidade |
| Int. J. of Accounting Inf. Systems | 3 | 7,1% | 3,5 | SI Contábeis |
| [demais periódicos] | ... | ... | ... | ... |

---

## Sprint 4 — Refinamento Teórico e Diálogo com Literatura (Dia 4)

### 4.1 Inserir Seção 2.4 — DSR no Contexto Brasileiro (2h)
**Localização:** Após 2.3 (aplicações de DSR na contabilidade pública)

**O que escrever:**
- Contexto brasileiro de compras públicas e inovação
- Relevância da DSR para problemas públicos brasileiros
- Por que o Brasil é um caso relevante para estudo (15% do PIB em compras, alta burocracia, "apagão das canetas")
- Conexão com a literatura de Estado Empreendedor (Mazzucato) aplicada a países em desenvolvimento

### 4.2 Expandir Seção 2.3 — Aplicações de DSR (1h)
Adicionar exemplos específicos de artefatos DSR na contabilidade pública internacional:
- Sistemas de auditoria contínua (Kuhn & Sutton, 2010)
- Frameworks de transparência fiscal (Lourenço et al., 2019)
- Plataformas de orçamento participativo digital (Sampaio et al., 2021)
- modelos preditivos para gestão de contratos públicos

### 4.3 Expandir Referências para 30-35 (1h)
Adicionar:
- Hevner et al. (2004) — já incluso
- Peffers et al. (2007) — já incluso
- Gregor & Hevner (2013) — já incluso
- Tricco et al. (2018) — já incluso
- **Novas:**
  - Sampaio et al. (2021). *Government Information Quarterly*
  - Kuhn & Sutton (2010). *International Journal of Accounting Information Systems*
  - Lourenço et al. (2019). *Transparency and Governance*
  - Venable et al. (2016). *Journal of the Association for Information Systems*
  - Baskerville et al. (2018). *European Journal of Information Systems*
  - Iivari (2015). *Communications of the Association for Information Systems*
  - Dresch et al. (2015). *Design Science Research: A Method for Science and Technology Advancement*

---

## Sprint 5 — Consolidação de Lacunas e Agenda de Pesquisa (Dia 5)

### 5.1 Detalhar e Priorizar Lacunas (2h)
**Localização:** Seção 5.1

**O que fazer:**
Transformar as 3 lacunas atuais em uma matriz priorizada:

| Lacuna | Evidência no Corpus | Impacto | Urgência | Prioridade |
|--------|---------------------|---------|----------|------------|
| Escassez de artefatos para compras públicas | Apenas 3 artigos (7,1%) abordam compras | Alto (15% do PIB) | Alta | **1** |
| Predomínio de avaliações artificialistas (68,3%) | 28 de 42 artigos não testam em ambiente real | Alto (validade externa) | Alta | **2** |
| Baixa aplicação de técnicas avançadas de IA | Apenas 8 artigos (19%) com IA; nenhum com NLP ou multi-agente | Médio (oportunidade) | Média | **3** |
| Concentração em e-government (35,7%) sem foco em complexidade | 15 artigos em sistemas genéricos | Médio | Média | **4** |

Para cada lacuna, adicionar parágrafo com:
- Por que essa lacuna existe (explicação institucional/incentivos)
- Consequências de não preenchê-la
- Como poderia ser endereçada (exemplo de agenda de pesquisa)

### 5.2 Criar Agenda de Pesquisa Prioritária (1,5h)
**Localização:** Final da Seção 5

**Tabela de agenda:**

| Prioridade | Tópico de Pesquisa | Método Sugerido | Artefato Esperado |
|------------|-------------------|-----------------|-------------------|
| 1 | Desenvolvimento de copiloto algorítmico para compras públicas | DSR (ciclos iterativos) | Sistema de avaliação e geração de editais com XAI |
| 2 | Avaliação naturalista de artefatos DSR em órgãos públicos | Estudo de caso múltiplo + TAM | Validação em 3 órgãos federais |
| 3 | NLP para auditoria semântica de justificativas de contratação | DSR + Deep Learning | Classificador de *innovation washing* |
| 4 | Framework de transparência algorítmica para o setor público | DSR (design principle) | Conjunto de princípios de design (PDs) |
| 5 | Sistema multi-agente para gestão de riscos contratuais | DSR + Simulação | Protótipo integrado ao PNCP |

### 5.3 Reforçar a Conexão com Governança Algorítmica (30 min)
Em vez de mencionar governança algorítmica apenas na introdução e conclusão, distribuir referências ao longo do texto:
- Na seção 2.4 (governança algorítmica e lacunas)
- Na seção 5.1 (lacuna de artefatos para governança algorítmica)
- Na seção 5.2 (agenda de pesquisa em governança algorítmica)
- Na conclusão

---

## Sprint 6 — Finalização e Preparação para Submissão (Dia 6)

### 6.1 Adicionar Limitações Específicas (1h)

> **6.2 Limitações do Estudo**
>
> Este scoping review apresenta limitações que devem ser consideradas na interpretação dos achados. Primeiro, a restrição à base OpenAlex pode ter omitido artigos indexados exclusivamente em Scopus, Web of Science ou SciELO. Embora a OpenAlex agregue múltiplas fontes, a cobertura não é exaustiva. Segundo, a decisão de excluir artigos de conferências (DESRIST, ICIS, EGOV) pode ter sub-representado artefatos em estágio inicial de desenvolvimento, comum em comunidades de DSR. Terceiro, a análise baseou-se predominantemente nos metadados disponíveis na base, sem verificação sistemática do texto completo de todos os 42 artigos — o que pode ter introduzido erros de classificação. Quarto, o corpus de 42 artigos é reduzido para um scoping review; revisões futuras com corpus expandido podem revelar padrões adicionais. Quinto, a classificação na matriz de Gregor e Hevner (2013) envolve julgamento subjetivo do pesquisador; a não realização de dupla codificação independente (Kappa) para esta classificação é uma limitação metodológica.

### 6.2 Verificar e Padronizar a Estrutura do Artigo (1h)
- Confirmar que todas as seções seguem numeração sequencial
- Incluir seção "Referências" padronizada em APA 7a
- Verificar que figuras e tabelas são numeradas sequencialmente
- Incluir notas de tabelas com "Fonte: Elaboração própria (2026)"

### 6.3 Revisão de Escrita e Formatação (1,5h)
- Substituir linguagem rebuscada por termos precisos
- Verificar consistência terminológica (ex.: "artefato" vs. "ferramenta")
- Revisar ortografia e gramática
- Ajustar formatação HTML para impressão

### 6.4 Checklist de Submissão (30 min)

| Item | OK? |
|------|-----|
| Abstract em português ≤ 250 palavras | |
| Abstract em inglês (CRIAR) | |
| Palavras-chave (4-6) | |
| Fluxograma PRISMA (CRIAR) | |
| Corpus expandido para 60-80 artigos | |
| Figuras 1-5 embutidas no HTML | |
| Seção 6.1 original (sem autoplágio) | |
| Seção 2.4 (contexto brasileiro) | |
| Matriz de lacunas priorizadas | |
| Agenda de pesquisa (5 tópicos) | |
| Limitações detalhadas | |
| 30-35 referências | |

---

## Resumo do Escopo

| Sprint | Atividade | Horas | Entregável |
|--------|-----------|-------|------------|
| 1 | Abstract EN, autoplágio, remoção viés Copiloto | 4,5h | Seções 5.1, 6.1 reescritas; abstract EN |
| 2 | Expansão corpus (WoS+Scopus+conf) + fluxograma PRISMA | 5h | Corpus 60-80 artigos; figura PRISMA |
| 3 | Figuras, análise qualitativa por quadrante, tabela periódicos | 5h | 6 figuras; seções 4.4.1-4.4.3 |
| 4 | Contexto brasileiro, referencial expandido | 4h | Seção 2.4; +7 referências |
| 5 | Matriz de lacunas, agenda de pesquisa | 4h | Seções 5.1-5.2 detalhadas |
| 6 | Limitações, revisão final, checklist | 3h | Artigo finalizado |
| **Total** | | **25,5h** | |

---

## Próximos Passos Após Sprint 6

1. Submeter para **ICEGOV 2027** (International Conference on Theory and Practice of Electronic Governance)
2. Ou para **DESRIST 2027** (Design Science Research in Information Systems)
3. Ou para **EGOV 2027** (IFIP EGOV-CeDEM-ePart)
4. Versão estendida para *Government Information Quarterly* (como "Research Note")
5. Considerar transformar em capítulo de handbook sobre DSR no setor público

---

*Criado em: 29/07/2026*
