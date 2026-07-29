# Sprint de Melhorias — Artigo 10
## O Uso Retórico da "Inovação": Análise de Conteúdo das Justificativas de Contratação Pública no PNCP

**Status atual:** 7,0/10 — Dados reais (n=350, PNCP), conceito original (*innovation washing*), χ²=91,25 (p<0,001)
**Objetivo:** 9,0/10 — Submissão para EnANPAD 2027 / IRSPM 2027 / CONSAD
**Prazo estimado:** 5 dias (sprints de 1 dia cada)

---

## Sprint 1 — Correção de Autoplágio e Reestruturação (Dia 1)

### 1.1 Remover Autoplágio da Seção 6.1 (2h)
**Localização:** Seção "6.1 Implicações Práticas e Políticas Públicas" (3 parágrafos genéricos)

**O que fazer:**
- Apagar COMPLETAMENTE os 3 parágrafos atuais (Capacitação Contínua / Revisão de Marcos / Adoção de IA — textualmente iguais aos artigos 15 e 17)
- Escrever implicações EXCLUSIVAS DO ARTIGO 10, centradas em:
  - Mecanismos de auditoria semântica para identificar *innovation washing* em tempo real
  - Propostas de diretrizes objetivas para justificativas de inovação no PNCP
  - Indicadores de alerta precoce (Rhetorical Score > 0,7) para controle interno
  - Revisão dos critérios de enquadramento de "inovação" na Lei 14.133/2021

**Exemplo de novo texto (substituir integralmente):**

> Os achados deste artigo oferecem implicações diretas para o desenho de políticas públicas de compras e inovação.
>
> **1. Auditoria Semântica Preventiva:** O *Rhetorical Score* demonstrou capacidade de discriminar justificativas legítimas de retóricas (RS médio legítimo: 0,15 vs. retórico: 0,85). Recomenda-se a integração de mineração textual nos sistemas de controle interno (CGU, TCU) como triagem preliminar de processos de contratação direta. Editais com RS > 0,7 seriam automaticamente sinalizados para revisão aprofundada.
>
> **2. Diretrizes Objetivas para Justificativas de Inovação:** A ausência de parâmetros objetivos para o enquadramento legal de "inovação" (LC 182/2021) cria espaço para o isomorfismo de conveniência. Propõe-se que o PNCP adote um formulário estruturado de justificativa, exigindo: (a) especificação do problema técnico a ser resolvido; (b) evidência de inexistência de solução equivalente no mercado; (c) indicação do risco tecnológico envolvido; (d) prazo estimado de desenvolvimento.
>
> **3. Capacitação de Pregoeiros para Detecção de *Buzzwords*:** Programas de formação de agentes de contratação devem incluir módulos de detecção de *innovation washing*, capacitando gestores a identificar padrões retóricos como "blockchain descentralizado", "deep learning preditivo" e "solução disruptiva" quando usados sem fundamentação técnica.
>
> **4. Transparência Ativa das Justificativas:** A publicação padronizada das justificativas de contratação direta no PNCP, com metadados de classificação temática, permitiria à sociedade civil e ao mercado monitorar o uso da rubrica de inovação, criando accountability difusa.

### 1.2 Remover Viés do Copiloto na Seção 5.1 (1,5h)
**Localização:** Seção "5.1 Extensão Teórica e a Solução Sociotécnica (DSR)"

**O que fazer:**
- Apagar menções ao "Copiloto Algorítmico" como artefato
- Substituir por discussão sobre ferramentas de apoio à decisão baseadas em NLP
- Manter o conceito de "Latência Institucional Algorítmica" (é contribuição original)
- Reescrever o parágrafo final conectando os achados com a literatura de auditoria algorítmica (Coglianese & Lehr, 2019; Koshiyama et al., 2021)

### 1.3 Integrar a Nota de Validação ao Corpo do Texto (1h)
**Localização atual:** Box destacado entre seções 3 e 3.1
**Destino:** Nova subseção "3.2 Validação Externa do Instrumento" ou "4.3 Validação com Pregões do Espírito Santo"

**O que fazer:**
- Remover o box visual solto
- Criar subseção formal: "3.2 Validação do Instrumento de Análise"
- Descrever o teste piloto com 126 processos do ES, RS=0,0079
- Explicar por que a validação externa fortalece a generalizabilidade dos achados
- Incluir breve tabela comparativa:

| Amostra | n | RS médio | % Retórica | Fonte |
|---------|---|----------|------------|-------|
| Principal (nacional) | 350 | 0,68 | 89,11% | API PNCP (2021-2026) |
| Validação (ES Pregão) | 126 | 0,0079 | 0,79% | API PNCP (Jan/2024) |

---

## Sprint 2 — Abertura da Caixa-Preta Metodológica (Dia 2)

### 2.1 Detalhar o Algoritmo do Rhetorical Score (3h)
**Localização:** Seção 3 (Metodologia)

**O que fazer:**
Inserir subseção detalhada "3.3 Cálculo do Intensity Rhetorical Score (RS)" contendo:

**a) Dicionário de Termos Retóricos:** Lista exaustiva dos termos utilizados como indicadores de retórica. Exemplos:

| Categoria | Termos | Peso |
|-----------|--------|------|
| Buzzwords tecnológicas | blockchain, deep learning, I.A., machine learning, big data, indústria 4.0, transformação digital, metaverso, criptografia, descentralizado | 0,3 cada |
| Superlativos | disruptivo, revolucionário, inovador, vanguarda, _state-of-the-art_, único, sem precedentes | 0,2 cada |
| Termos de conveniência | inexigibilidade, urgência, excepcionalidade, complexidade, singularidade, inviabilidade de competição | 0,15 cada |
| Jargão administrativo | otimização, sinergia, governança, compliance, accountability, resiliência, sustentabilidade | 0,1 cada |

**b) Fórmula de Cálculo:**

$$RS = \frac{\sum_{i=1}^{n} (f_i \cdot p_i)}{t}$$

Onde:
- $f_i$ = frequência do termo $i$ na justificativa
- $p_i$ = peso associado ao termo $i$
- $t$ = número total de palavras da justificativa (normalização)

**c) Thresholds de Classificação:**
- RS ≤ 0,20: Inovação Legítima
- 0,20 < RS ≤ 0,50: Misto (revisão manual)
- RS > 0,50: Retórico (alta probabilidade de *innovation washing*)

**d) Exemplos Concretos:**
Incluir 3 exemplos reais (anônimos) de justificativas com seus RS:

> **Exemplo 1 (RS=0,88 — Mimetismo Tecnológico):** "A presente contratação visa a aquisição de solução disruptiva de deep learning e blockchain descentralizado para otimização sinérgica dos processos de governança digital, utilizando inteligência artificial de última geração para transformação digital da administração..."
> *(Objeto real: 5 licenças de Microsoft Office 365)*

> **Exemplo 2 (RS=0,12 — Inovação Legítima):** "Contratação de empresa especializada para desenvolvimento de sistema de rastreamento de vacinas com tecnologia blockchain, conforme especificações técnicas do anexo I, incluindo prototipação concorrente e validação em ambiente controlado por 90 dias..."
> *(Objeto real: software inédito de logística farmacêutica)*

### 2.2 Justificar a Escolha de Bardin vs. Outras Abordagens (1h)
Adicionar parágrafo em 3.1:

> A Análise de Conteúdo de Bardin (2016) foi selecionada em detrimento de abordagens automatizadas (ex.: LDA, BERTopic) por três razões: (a) a sutileza semântica das justificativas demanda interpretação contextual que modelos de tópicos não capturam; (b) a necessidade de validação por pares (Kappa > 0,85) para garantir robustez; (c) a possibilidade de categorias emergirem indutivamente do corpus, em vez de serem impostas por um modelo pré-treinado.

---

## Sprint 3 — Criação de Figuras e Visualização (Dia 3)

### 3.1 Criar Figura 1 — Distribuição das Categorias (1,5h)
**Ferramenta:** Python (matplotlib/seaborn) ou Excel
**Dados:** `dados/dataset_analisado.csv`

**Tipo:** Gráfico de barras horizontais com as 4 categorias

```
Mero Mimetismo Tecnológico  ███████████████████████ 33,43%
Inovação Legítima           █████████████████████   31,43%
Urgência Retórica           ████████████            17,71%
Redundância Instrumental    ████████████            17,43%
```

**O que fazer:**
- Salvar como `figura1_categorias_retoricas.png` na pasta do artigo
- Referenciar no HTML como Figura 1

### 3.2 Criar Figura 2 — RS Competitivo vs. Contratação Direta (1h)
**Tipo:** Gráfico de barras comparativo ou boxplot

| Modalidade | RS Médio |
|------------|----------|
| Certames Competitivos | 0,43 |
| Contratações Diretas | 0,76 |

**Dados complementares:**
- Incluir barras de erro (desvio padrão)
- Adicionar linha de threshold (RS=0,50) para referência visual

**O que fazer:**
- Salvar como `figura2_rs_por_modalidade.png`
- Referenciar no HTML como Figura 2

### 3.3 Criar Figura 3 — Exemplos de Justificativas (1h)
**Tipo:** Nuvem de palavras (*word cloud*) com os termos mais frequentes nas categorias retóricas

**O que fazer:**
- Gerar com Python (biblioteca wordcloud)
- Salvar como `figura3_wordcloud_retorica.png`
- Incluir breve análise: "os termos 'inovação', 'tecnologia' e 'digital' aparecem em 89% das justificativas retóricas, mas em apenas 34% das legítimas"

### 3.4 Embutir Figuras no HTML (30 min)
- Adicionar tags `<figure>` com `<img src="...">` e `<figcaption>`
- Inserir na Seção 4 (Resultados)

---

## Sprint 4 — Expansão Teórica e Consistência (Dia 4)

### 4.1 Inserir Diálogo com Literatura de *Washing* (2h)
**Localização:** Seção 2 (após 2.2)

**Nova subseção 2.3 — Inovação vs. Maquiagem: O Fenômeno do *Washing***

Adicionar diálogo com literaturas análogas:

| Fenômeno | Referência Base | Paralelo com *Innovation Washing* |
|----------|----------------|-----------------------------------|
| Greenwashing | Lyon & Montgomery (2015, *Annual Review of Environment and Resources*) | Empresas simulam responsabilidade ambiental; gestores simulam inovação |
| Impact Washing | Busch et al. (2021, *Nature Sustainability*) | Superestimação de impacto social positivo |
| CSR Washing | Pope & Wæraas (2016, *Business & Society*) | Adoção superficial de discurso de responsabilidade social |
| Academic Washing | Biagioli & Lippman (2020, *Nature*) | Uso retórico de termos acadêmicos sem substância |

Escrever 2-3 parágrafos:
- Definir *innovation washing* como subtipo de isomorfismo institucional
- Mostrar que o fenômeno não é exclusivo do Brasil (citar evidências internacionais)
- Diferenciar *innovation washing* no setor público (incentivos diferentes: punição vs. competição)

### 4.2 Aprofundar a Conexão com Isomorfismo Institucional (1h)
- Retomar DiMaggio & Powell (1983) com mais profundidade
- Discutir especificamente o isomorfismo mimético em compras públicas
- Conectar com a literatura de *institutional logics* (Thornton & Ocasio, 1999)

### 4.3 Expandir Referências para 20-25 (1h)
Adicionar:
- Busch et al. (2021). *Nature Sustainability*
- Coglianese & Lehr (2019). *University of Pennsylvania Law Review*
- Koshiyama et al. (2021). *AI and Society*
- Lyon & Montgomery (2015). *Annual Review of Environment and Resources*
- Pope & Wæraas (2016). *Business & Society*
- Suchman (1995). *Academy of Management Review*
- Thornton & Ocasio (1999). *American Journal of Sociology*

---

## Sprint 5 — Conclusão, Limitações e Preparação (Dia 5)

### 5.1 Reescrever Conclusão (2h)
**O que fazer:**
- Manter os achados quantitativos (já são o ponto forte)
- Adicionar agenda de pesquisa específica:
  - Correlacionar RS com execução financeira ex-post (aditivos, cancelamentos)
  - Validar o dicionário de termos retóricos com análise de decisões do TCU
  - Expandir para compras de sustentabilidade (testar *greenwashing*)
  - Desenvolver modelo preditivo de *innovation washing* usando BERT
- Remover qualquer menção ao "Copiloto Algorítmico"

### 5.2 Adicionar Limitações Específicas (1h)
Adicionar seção de limitações honesta:

> **5.2 Limitações do Estudo**
>
> Este estudo apresenta limitações que qualificam seus achados. Primeiro, a análise concentrou-se no texto das justificativas sem cruzamento com dados de execução contratual (aditivos, prazos, cancelamentos), o que permitiria verificar se justificativas retóricas de fato resultam em piores desfechos contratuais. Segundo, o *Rhetorical Score*, embora replicável, é uma métrica ad-hoc que requer validação psicométrica formal (análise fatorial, consistência interna). Terceiro, a amostra de 350 justificativas, embora adequada para os testes estatísticos realizados, pode não capturar a heterogeneidade regional das práticas de contratação no Brasil. Quarto, a validação externa com 126 processos do Espírito Santo (Seção 3.2) é geograficamente limitada. Pesquisas futuras podem expandir a validação para múltiplos estados e incluir análise longitudinal.

### 5.3 Revisão de Escrita e Formatação (1h)
- Verificar consistência da numeração de seções (3.1, 3.2, 3.3)
- Padronizar citações APA 7a
- Incluir sobrenomes completos nas primeiras ocorrências
- Revisar ortografia e gramática

### 5.4 Gerar Versão em Inglês (1,5h)
Preparar tradução completa do artigo para submissão internacional:

| Elemento | Status atual | Ação |
|----------|-------------|------|
| Abstract | OK | Já existe versão em inglês |
| Título | "O Uso Retórico..." | Criar versão: *"The Rhetorical Use of 'Innovation': Content Analysis of Public Procurement Justifications in the Brazilian PNCP"* |
| Corpo do texto | Português | Criar versão `artigo_10_en.html` |
| Figuras | Manter originais | Legendas em inglês |

### 5.5 Checklist de Submissão (30 min)

| Item | OK? |
|------|-----|
| Título ≤ 15 palavras | |
| Abstract ≤ 250 palavras | |
| Palavras-chave (4-6) | |
| Algoritmo RS documentado (transparente) | |
| 3 figuras criadas | |
| Nota de validação integrada | |
| Seção 6.1 original (sem autoplágio) | |
| Seção 5.1 sem menção ao Copiloto | |
| Kappa > 0,85 reportado | |
| Limitações explícitas | |
| 20-25 referências | |

---

## Resumo do Escopo

| Sprint | Atividade | Horas | Entregável |
|--------|-----------|-------|------------|
| 1 | Autoplágio, integração validação, reestruturação | 4,5h | Seções 5.1, 6.1 reescritas; validação integrada |
| 2 | Transparência do RS (dicionário, fórmula, exemplos) | 4h | Seção 3.3 completa |
| 3 | Criação de 3 figuras + embedding | 4h | 3 figuras; HTML atualizado |
| 4 | Expansão teórica (washing, isomorfismo) | 4h | Seção 2.3 nova; referências expandidas |
| 5 | Conclusão, limitações, versão inglês | 5h | Artigo finalizado; versão EN |
| **Total** | | **21,5h** | |

---

## Próximos Passos Após Sprint 5

1. Submeter para **EnANPAD 2027** (deadline típica: maio) — Divisão APB (Administração Pública)
2. Ou para **IRSPM 2027** — painel de Public Procurement and Innovation
3. Versão em inglês para *Government Information Quarterly* ou *Public Management Review*
4. Validar RS com especialistas em compras públicas

---

*Criado em: 29/07/2026*
