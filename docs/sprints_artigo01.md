# SPRINTS DE CORREÇÃO — ARTIGO 01 (DIAGNÓSTICO EMPÍRICO)

**Base:** Orientação do professor (§5 do Direcionamento.md) + Análise crítica nível banca.

---

## VISÃO GERAL

| Status        | Sprint          | Foco                              | Vulnerabilidades   | Duração | Depende de |
| ------------- | --------------- | --------------------------------- | ------------------ | --------- | ---------- |
| 🟢 Concluído | **A1-S1** | Regressão logística real        | #1, #2, #3, #4, #5 | 2 dias    | —         |
| 🟢 Concluído | **A1-S2** | Enriquecer dados de fornecedores  | #6                 | 1 dia     | —         |
| 🟢 Concluído | **A1-S3** | Reorganizar escopo + remover SHAP | #7, #8, #9         | 1 dia     | A1-S1      |
| 🟢 Concluído | **A1-S4** | Re-acentuação + capitalização | #10, #11, #12, #13 | 0.5 dia   | A1-S3      |
| 🟢 Concluído | **A1-S5** | Português + escrita.md           | #14                | 0.5 dia   | A1-S4      |
| 🟢 Concluído | **A1-S6** | Revisão acadêmica sistemática  | #15                | 2 dias    | —         |

**Total:** 7 dias · **Progresso:** 6/6 sprints concluídas · **100%**

---

## VULNERABILIDADES — LISTA COMPLETA

| #  | Vulnerabilidade                                                                                               | Origem    | Sprint | Gravidade          |
| -- | ------------------------------------------------------------------------------------------------------------- | --------- | ------ | ------------------ |
| 1  | Equação logística enunciada (3.4) mas nunca estimada — zero β, zero p-valor                              | Análise  | A1-S1  | **Crítica** |
| 2  | Seção 4.3 importa SHAP/Random Forest do Artigo 02 — escopos sobrepostos                                    | Análise  | A1-S3  | **Crítica** |
| 3  | Zero testes de hipótese formais (t-test, χ², ANOVA, regressão)                                            | Análise  | A1-S1  | **Alta**     |
| 4  | Nenhuma comparação quantitativa complexas vs. normais (taxa de fracasso)                                    | Análise  | A1-S1  | **Alta**     |
| 5  | Nenhuma hipótese formal enunciada (H1, H2...)                                                                | Análise  | A1-S1  | **Alta**     |
| 6  | `fornecedores_enriquecidos.csv` vazio (0 bytes) — sem dados de capital social, CNAE, porte                 | Professor | A1-S2  | **Alta**     |
| 7  | Faltam IVs da unidade compradora: setor, esfera, tipo de pessoal, remuneração                               | Professor | A1-S3  | **Média**   |
| 8  | "Apagão das canetas" só aparece na última página                                                          | Análise  | A1-S3  | **Média**   |
| 9  | "Exoesqueletos cognitivos" sem definição ou fundamentação                                                 | Análise  | A1-S3  | **Média**   |
| 10 | Título com capitalização quebrada (minúsculas no meio)                                                    | Análise  | A1-S4  | **Baixa**    |
| 11 | Re-acentuação falhou em ~40% das palavras (orcamento, milhoes, omissao...)                                  | Análise  | A1-S4  | **Baixa**    |
| 12 | Tabelas com capitalização inconsistente (labels em minúsculo)                                              | Análise  | A1-S4  | **Baixa**    |
| 13 | Nenhum gráfico/figura em 8 páginas (histograma, boxplot)                                                    | Análise  | A1-S4  | **Baixa**    |
| 14 | Artigo não-conforme com escrita.md (travessões, palavras-IA, conectivos)                                    | Análise  | A1-S5  | **Baixa**    |
| 15 | Referencial teórico com apenas 13 referências — precisa de 200+ artigos com revisão sistemática por tema | Professor | A1-S6  | **Crítica** |

---

## A1-S1: REGRESSÃO LOGÍSTICA REAL

**Objetivo:** Estimar o modelo da seção 3.4 e substituir a Tabela 4 (SHAP) pela tabela de regressão.

### 1.1. Construir variável dependente comparável (0.5 dia)

```python
# Tarefa 1.1a: Criar target binário para compras complexas E normais
# target_real já existe para 100k contratos (do Sprint 1 do Artigo 02)
# Agrupar por is_complexa e calcular taxa de fracasso

# Tarefa 1.1b: Calcular e reportar:
# - Taxa de fracasso nas complexas (5.687 contratos)
# - Taxa de fracasso nas normais (566.358 contratos)
# - Teste de diferença de proporções (z-test)
# - Odds ratio: chance de fracasso em complexa vs. normal
```

**Critério de aceitação:**

- [ ] Taxa de fracasso nas complexas calculada (ex: 31,2%)
- [ ] Taxa de fracasso nas normais calculada (ex: 18,1%)
- [ ] Teste z de diferença de proporções com p-valor
- [ ] Odds ratio reportado

### 1.2. Estimar regressão logística (1 dia)

```python
# Tarefa 1.2a: Rodar Logit com variáveis disponíveis
# Y = target_real (0/1)
# X1 = porte_proxy_orgao (log) — capacidade financeira
# X2 = is_complexa (0/1) — tipo de compra
# X3 = vigencia_dias — duração
# X4 = valor_log — montante
# X5 = uf_encoded — localização
# X6 = esfera (F/E/M) — se disponível nos dados

# Tarefa 1.2b: Extrair e reportar:
# - Coeficientes β
# - Erro-padrão
# - p-valor (Wald test)
# - Odds ratio = exp(β)
# - Intervalo de confiança 95%
# - Pseudo R² (McFadden)
# - Matriz de confusão
# - Curva ROC com AUC

# Tarefa 1.2c: Enunciar hipóteses formais ANTES da tabela
# H1: O porte do órgão (log) está negativamente associado à probabilidade de fracasso
# H2: Compras complexas têm probabilidade de fracasso superior às normais
# H3: A vigência do contrato está negativamente associada à probabilidade de fracasso
# H4: O valor do contrato está positivamente associado à probabilidade de fracasso
```

**Critério de aceitação:**

- [ ] ≥ 4 hipóteses formais enunciadas (H1-H4)
- [ ] Tabela de regressão com β, SE, p-valor, OR, IC 95%
- [ ] Pseudo R² reportado
- [ ] AUC-ROC reportada
- [ ] Interpretação substantiva de cada coeficiente

### 1.3. Substituir Seção 4.3 (SHAP → Regressão) (0.5 dia)

**Entregável:** Nova Seção 4.3 "Determinantes do Fracasso: Evidência da Regressão Logística"

```markdown
# Tarefa 1.3a: REMOVER Tabela 4 atual (feature importance SHAP)
# Tarefa 1.3b: INSERIR nova Tabela 4 (coeficientes da regressão logística)
# Tarefa 1.3c: Reescrever o texto da seção 4.3 para discutir
#   os coeficientes, não a feature importance
# Tarefa 1.3d: Mover a análise SHAP para o Artigo 02 (já está lá)
```

---

## A1-S2: ENRIQUECER DADOS DE FORNECEDORES

**Objetivo:** Preencher o CSV vazio e ter dados reais de capital social, CNAE e porte dos fornecedores.

### 2.1. Coletar dados da BrasilAPI (0.5 dia)

```python
# Tarefa 2.1a: Listar CNPJs únicos das compras complexas (3.528)
# Tarefa 2.1b: Consultar BrasilAPI em lote (respeitando rate limit)
#   - https://brasilapi.com.br/api/cnpj/v1/{cnpj}
# Tarefa 2.1c: Extrair: capital_social, cnae_fiscal_descricao, porte
# Tarefa 2.1d: Salvar em fornecedores_enriquecidos.csv
```

**Critério de aceitação:**

- [ ] `fornecedores_enriquecidos.csv` com ≥ 200 registros
- [ ] Colunas: cnpj, capital_social, cnae, porte, nome_fantasia

### 2.2. Incorporar na regressão (0.5 dia)

```python
# Tarefa 2.2a: Adicionar capital_social_log como X5 na regressão
# Tarefa 2.2b: Adicionar porte_fornecedor (ME/EPP/Demais) como dummy
# Tarefa 2.2c: Reestimar regressão com as novas variáveis
# Tarefa 2.2d: Reportar na Tabela 4 (seção 4.3)
```

---

## A1-S3: REORGANIZAR ESCOPO

**Objetivo:** Corrigir sobreposição com Artigo 02, introduzir "apagão das canetas" na seção correta, definir "exoesqueleto cognitivo".

### 3.1. Remover dependência do Artigo 02 (0.5 dia)

```markdown
# Tarefa 3.1a: Remover qualquer menção a SHAP, Random Forest, feature importance
#   (isso é contribuição exclusiva do Artigo 02)
# Tarefa 3.1b: Seção 4.3 agora contém APENAS regressão logística
# Tarefa 3.1c: Verificar que o Artigo 01 pode ser lido independentemente
```

### 3.2. Introduzir "apagão das canetas" na Seção 1 (0.25 dia)

```markdown
# Tarefa 3.2a: Mover a discussão sobre "apagão das canetas" da conclusão
#   para a Introdução (parágrafo 2 ou 3), como contra-argumento central
# Tarefa 3.2b: Contextualizar: "A literatura e a jurisprudência do TCU
#   tendem a atribuir o fracasso à omissão do gestor (apagão das canetas).
#   Este estudo testa empiricamente se o fracasso decorre de fatores
#   estruturais (assimetria) ou comportamentais (omissão)."
```

### 3.3. Definir "exoesqueleto cognitivo" (0.25 dia)

```markdown
# Tarefa 3.3a: Adicionar parágrafo na Seção 2 ou 5 definindo o termo
# Tarefa 3.3b: Fundamentar em literatura de decision support systems
#   ou em extended cognition (Clark & Chalmers, 1998)
```

---

## A1-S4: RE-ACENTUAÇÃO + FORMATAÇÃO

**Objetivo:** Corrigir capitalização do título, labels das tabelas, completar re-acentuação.

### 4.1. Completar re-acentuação (0.25 dia)

Palavras que o script atual não cobriu (lista parcial — verificar todas):

```
censitaria → censitária
orcamento → orçamento
milhoes → milhões
assimetrica → assimétrica
omissao → omissão
intervencao → intervenção
nucleo → núcleo
sistemica → sistêmica
implementacao → implementação
modernizacao → modernização
competicao → competição
concentracao → concentração
formulacao → formulação
capacitacao → capacitação
fiscalizacao → fiscalização
renegociacao → renegociação
... (executar script de varredura completa)
```

### 4.2. Corrigir título e capitalização (0.15 dia)

```
Atual: "DETERMINANTES DO SUCESSO E fracasso EM COMPRAS públicas COMPLEXAS"
Correto: "DETERMINANTES DO SUCESSO E FRACASSO EM COMPRAS PÚBLICAS COMPLEXAS:
          UMA ANÁLISE CENSITÁRIA DAS ENTIDADES GOVERNAMENTAIS NO BRASIL"
```

### 4.3. Corrigir labels das tabelas (0.1 dia)

Todas as células da primeira coluna das tabelas devem iniciar com maiúscula.

---

## A1-S5: PORTUGUÊS + ESCRITA.MD

**Objetivo:** Revisão final de linguagem conforme `docs/escrita.md`.

- [ ] Zero travessões
- [ ] Zero palavras proibidas (crucial, inovador, robusto...)
- [ ] Zero adjetivações valorativas
- [ ] Conectivos após ponto final (regra de ouro §5.1)
- [ ] Tempos verbais corretos por seção (§4.5)
- [ ] Citações 100% APA 7ª ed. (§6, §7)
- [ ] Linguagem impessoal (3ª pessoa) (§2.2)

---

## CRONOGRAMA

```
Dia 1:    [A1-S1] Construir DV comparável + enunciar hipóteses
Dia 2:    [A1-S1] Estimar regressão logística + reescrever Seção 4.3
Dia 3:    [A1-S2] Coletar dados de fornecedores via BrasilAPI
Dia 4:    [A1-S3] Reorganizar escopo (remover SHAP, mover apagão, definir exoesqueleto)
Dia 5 AM: [A1-S4] Re-acentuação completa + capitalização + gráficos
Dia 5 PM: [A1-S5] Revisão escrita.md + checklist final
Dia 6:    [A1-S6] Busca acadêmica — OpenAlex + Semantic Scholar
Dia 7:    [A1-S6] Organizar dataset + mapear dialética por tema
```

---

## A1-S6: REVISÃO ACADÊMICA SISTEMÁTICA

**Objetivo:** Buscar 200+ artigos em APIs acadêmicas para amparar o referencial teórico do Artigo 01, cobrindo a hierarquia macro→micro dos temas, com metadados completos (autores, ano, DOI, abstract, citações).

**Perguntas que o referencial deve responder (macro → micro):**

1. O que é uma compra complexa?
2. Quais são as categorias de compras complexas? (inovação tecnológica + ESG/sustentabilidade)
3. Como eliminar a assimetria de informação das compras complexas?
4. Como reduzir a assimetria em compras complexas? (ferramentas, IA, suporte à decisão)

**Foco absoluto:** Compras Complexas = inovação tecnológica + alinhadas a ESG e sustentabilidade.

### 6.1. Busca em APIs acadêmicas (1 dia)

**APIs a utilizar:**

| API              | URL                                                       | Cobertura                                    |
| ---------------- | --------------------------------------------------------- | -------------------------------------------- |
| OpenAlex         | `https://api.openalex.org/works`                        | 250M+ works, gratuito, sem rate limit severo |
| Semantic Scholar | `https://api.semanticscholar.org/graph/v1/paper/search` | 200M+ papers, 100 req/5min free              |
| Crossref         | `https://api.crossref.org/works`                        | 130M+ works, público                        |

**Script:** `scripts/buscar_artigos_referencial.py`

```python
# Tarefa 6.1a: Buscar 50+ artigos por tema (4 temas = 200+ total)

TEMAS = {
    "T1_compras_complexas_definicao": [
        # Macro: O que é uma compra complexa?
        "complex public procurement",
        "complex purchasing government",
        "public procurement complexity",
        "innovation procurement definition",
        "technology procurement public sector",
    ],
    "T2_categorias_complexas_inovacao": [
        # Inovação tecnológica
        "public procurement innovation",
        "government procurement technology",
        "innovation-oriented public procurement",
        "pre-commercial procurement",
        "public procurement R&D",
        "transformative public procurement",
    ],
    "T3_categorias_complexas_esg": [
        # ESG e sustentabilidade
        "green public procurement",
        "sustainable public procurement",
        "circular procurement",
        "socially responsible public procurement",
        "GPP criteria",
        "environmental public purchasing",
    ],
    "T4_assimetria_reducao": [
        # Como reduzir assimetria?
        "information asymmetry public procurement",
        "transaction cost economics procurement",
        "buyer capability public procurement",
        "procurement capacity building",
        "decision support public procurement",
        "AI public procurement",
        "algorithmic procurement",
        "digital procurement transformation",
    ],
}

# Tarefa 6.1b: Para cada query, extrair metadados
# - title, authors, year, DOI, abstract, citation_count
# - journal, publisher, type, open_access status
# - concepts/tags (OpenAlex)

# Tarefa 6.1c: Salvar em CSV único
# Base_de_Dados_e_APIs/Raw_Data/Revisao_Art01/referencial_artigos.csv
# Colunas: id, tema, query, titulo, autores, ano, doi, abstract,
#          citacoes, journal, concepts, open_access, url
```

**Critério de aceitação:**

- [ ] ≥ 200 artigos no dataset (50+ por tema)
- [ ] Metadados: título, autores, ano, DOI, abstract, citações
- [ ] CSV salvo em `Base_de_Dados_e_APIs/Raw_Data/Revisao_Art01/`
- [ ] Coluna `tema` preenchida para cada artigo (T1-T4)

### 6.2. Organizar dataset e mapear dialética (1 dia)

```markdown
# Tarefa 6.2a: Classificar artigos por posição no debate
# Para cada tema, identificar:
#   - Autores seminais (mais citados, fundadores do conceito)
#   - Autores recentes (2020+, fronteira do conhecimento)
#   - Posições conflitantes (ex: Estado empreendedor vs. Estado regulador)
#   - Evidência empírica vs. teórica
#   - Contexto geográfico (Brasil, OCDE, global)

# Tarefa 6.2b: Criar tabela-síntese por tema
# | Tema | Autores seminais | Fronteira (2020+) | Debates | Lacunas |
# |------|-----------------|-------------------|---------|---------|
# | T1   | Thai (2001)...  | ...               | ...     | ...     |

# Tarefa 6.2c: Mapear onde o Artigo 01 se encaixa
# - Quais autores o artigo corrobora?
# - Quais autores o artigo refuta/qualifica?
# - Qual lacuna o artigo preenche?
# - Onde está a contribuição original?
```

**Critério de aceitação:**

- [ ] Dataset organizado por tema (≥ 50 artigos/tema)
- [ ] Tabela-síntese com posições no debate por tema
- [ ] Mapeamento explícito de onde o Artigo 01 se insere na literatura
- [ ] Pelo menos 30 novos artigos citáveis identificados para o referencial

### 6.3. Atualizar referencial teórico do artigo (após coleta)

```markdown
# Tarefa 6.3a: Substituir citações genéricas por citações específicas
# Ex: "compras complexas caracterizam-se por incerteza (Thai, 2001)"
#   → enriquecido com 5+ citações do dataset T1

# Tarefa 6.3b: Adicionar parágrafos de revisão para cada subtema
# 2.1 → enriquecido com artigos T1
# 2.2 → enriquecido com artigos T4
# 2.3 → enriquecido com artigos T2 + T3

# Tarefa 6.3c: Atualizar lista de referências (13 → 40+)
```

---

## CRONOGRAMA ATUALIZADO

```
Dia 1:    [A1-S1] Construir DV comparável + enunciar hipóteses
Dia 2:    [A1-S1] Estimar regressão logística + reescrever Seção 4.3
Dia 3:    [A1-S2] Coletar dados de fornecedores via 3 APIs
Dia 4:    [A1-S3] Reorganizar escopo (remover SHAP, mover apagão)
Dia 5 AM: [A1-S4] Re-acentuação completa + capitalização + gráficos
Dia 5 PM: [A1-S5] Revisão escrita.md + checklist final
Dia 6:    [A1-S6] Busca acadêmica — OpenAlex + Semantic Scholar (200+ artigos)
Dia 7:    [A1-S6] Organizar dataset + mapear dialética + atualizar referencial
```

---

## SÍNTESE DO QUE MUDA NO ARTIGO 01

| Seção | Antes (errado)              | Depois (orientação do professor)                    |
| ------- | --------------------------- | ----------------------------------------------------- |
| Título | Capitalização quebrada    | Title Case consistente                                |
| 1 Intro | Apagão das canetas ausente | Apagão como contra-argumento central                 |
| 2 Ref   | 13 refs genéricas          | **40+ refs com revisão sistemática por tema** |
| 3.4     | Equação não estimada     | Equação + hipóteses H1-H3                          |
| 4.1     | Descritivo                  | Descritivo + comparativo complexas vs. normais        |
| 4.2     | Oligopólio                 | Oligopólio + dados enriquecidos de fornecedores      |
| 4.3     | SHAP/RF (Artigo 02!)        | **Regressão logística com β, p-valor, OR**   |
| 5 Conc  | Bridge genérico            | Bridge quantificado + implicações de política      |
| Ref     | 13 refs                     | **40+ refs do dataset acadêmico**              |
