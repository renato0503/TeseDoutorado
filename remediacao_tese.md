# PLANO DE REMEDIACAO — PASTA `Tese/` (Artigo 1 + Artigo 2 + Produto + Scripts)

**Ultima atualizacao:** 31/07/2026
**Objetivo:** corrigir inconsistencias criticas, metodologicas e de layout dos entregaveis da pasta `Tese/`, tornando-os publicaveis e defensaveis perante a banca.
**Fonte canonica de numeros:** `dados/processed/*.csv`, `resultados_reais.json`, `stats_compras_complexas.json`, `target_distribution.json`.

---

## NUMEROS CANONICOS (verificados nos dados reais)

| Metrica | Valor canonico | Fonte |
|---------|---------------|-------|
| Populacao PNCP | 572.045 contratos (Set/2021-Ago/2024) | resumo_pncp_contratos.json |
| Complexas identificadas por NLP (populacao) | **5.687** (0,99%) | stats_compras_complexas.json |
| Fornecedores unicos complexas | 3.098 | stats_compras_complexas.json |
| Orgaos unicos complexas | 1.622 | stats_compras_complexas.json |
| Amostra inferencial (pos-filtro vigencia≥30) | **73.201** | resultados_reais.json |
| Complexas na amostra | **19.245** (26,3%) | resultados_reais.json (n_complexas) |
| Normais na amostra | **53.956** | resultados_reais.json |
| Taxa base eventos | 2,6% | resultados_reais.json |
| Taxa complexas / normais | 4,48% / 1,93% (OR bruto 2,38; z=19,08) | resultados_reais.json tabela_7 |
| Pseudo R² (Modelo 1) | **0,062** (nao 0,153) | resultados_reais.json tabela_4_mod1 |
| AUC-ROC (Modelo 1) | **0,697** (nao 0,813) | resultados_reais.json tabela_4_mod1 |
| OR is_complexa | **1,708** [1,550-1,882] | resultados_reais.json tabela_4_mod1 |
| OR vigencia_log | **1,482** [1,399-1,571] | resultados_reais.json tabela_4_mod1 |
| OR valor_log | **1,201** [1,180-1,223] | resultados_reais.json tabela_4_mod1 |
| Modelo 2 | is_complexa 1,668; vigencia 1,471; valor 1,196; R² 0,0647 | resultados_reais.json tabela_5 |
| Modelo 3 | is_complexa **12,389**; vigencia 1,552; valor 1,217; R² 0,0797 | resultados_reais.json tabela_5 |
| Interacao is_complexa×maturidade | OR = **0,855** (p<0,001) | resultados_reais.json tabela_5 |
| LR test 1-2 | χ²=55,10 (p<0,001) | resultados_reais.json tabela_5 |
| LR test 2-3 | χ²=265,51 (p<0,001) | resultados_reais.json tabela_5 |
| PSM ATT | **+0,90 pp** (nao +4,2) | resultados_reais.json tabela_6_psm |
| Cox HR is_complexa | **1,85** | resultados_reais.json figura_4_cox |
| PSM balanceamento | p≈4,9e-10 (rejeita — mal interpretado no texto) | resultados_reais.json tabela_6_psm |
| target_real (amostra 100k) | 18.787 positivos (18,79%) | target_distribution/analise real |
| Total fornecedores | 119.558 CNPJs / 144.548 fornecedores | resumo_pncp_contratos.json |

**Nota sobre o paradoxo 5.687 vs 19.245:** 5.687 = complexas identificadas pelo NLP na POPULACAO (0,99%). 19.245 = complexas na AMOSTRA INFERENCIAL pos-filtro (26,3% de 73.201). A definicao de "complexa" usada nos modelos (is_complexa) e mais ampla que a identificacao NLP; o artigo deve explicitar essa distincao em vez de usar os numeros indistintamente.

---

## CAUSA-RAIZ DO LAYOUT (R8)

Os artigos 1 e 2 da Tese possuem `<base href="https://raw.githubusercontent.com/...">`, que faz o navegador resolver `../../../css/style_academico.css` contra o GitHub raw. Ao abrir localmente, se o repo nao tiver o CSS nesse caminho (ou estiver offline), o artigo renderiza **sem estilo**. O Produto (`produto_tecnologico.html`) nao possui `<base>`, por isso funciona.
**Correcao:** trocar `<base href>` para `<base href="./">` nos artigos 1 e 2 da Tese.

---

## SPRINTS

### R1 — Alertas criticos do Artigo 1 (obrigatorio imediato)
| # | Acao | Arquivo/Linha |
|---|------|--------------|
| R1.1 | Remover citacao fantasma "Hacked & Alsheikh (2024)" do texto (L80) e das referencias (L348); substituir no texto por Zuiderwijk et al. (2021) | artigo_01_diagnostico.html |
| R1.2 | Padronizar numeros: Resumo "19.245 complexos (26,3% da amostra pos-filtro)" em vez de "25,6%"; clarificar que 5.687 = NLP na populacao | Resumo L32, Metodologia L124 |
| R1.3 | Titulo: remover "ANALISE CENSITARIA" → "UMA ANALISE EMPIRICA EM LARGA ESCALA"; alinhar L108 (populacao de referencia) e L46 | L26, L108, L46 |
| R1.4 | Corrigir T1 (1.320/1,32%) e Figura 7 para usar contagem canonica (19.245 complexas pos-filtro; 5.687 NLP populacao) | T1 L117, Fig7 L296-300 |

### R2 — Metodologia do Artigo 1
| # | Acao |
|---|------|
| R2.1 | Documentar mean-centering no Modelo 3 e explicar OR=12,389 (multicolinearidade com interacao) |
| R2.2 | Corrigir interpretacao H2/Figura 7: OR vigencia positivo (1,482) = risco cumulativo, NAO "concentracao em baixa vigencia" (L296) |
| R2.3 | Validadcao NLP: substituir "em fase de execucao" por resultados de validacao piloto real OU marcar como limitacao explicita |
| R2.4 | n=26 fornecedores: reformular como proxy defensavel (CNPJs truncados como identificador de fornecedor) |

### R3 — Coerencia interna do Artigo 1
| # | Item | Valor canonico |
|---|------|---------------|
| R3.1 | Pseudo R² 0,153 (L216) → 0,062 | resultados_reais.json |
| R3.2 | AUC 0,813 (L216) → 0,697 | resultados_reais.json |
| R3.3 | OR intervalo [0,58;0,61] (L217) → [1,399-1,571] | resultados_reais.json |
| R3.4 | LR test "p>0,10" (L217) → χ²=55,10*** (rejeita) | resultados_reais.json |
| R3.5 | PSM +4,2 pp (L261) → +0,90 pp; ATE→ATT | resultados_reais.json |
| R3.6 | GLMM placeholder (T5) → rotular como estimacao distinta ou recalcular |
| R3.7 | "teste de balanceamento p=0,000" (T6) → interpretar como rejeicao de balanceamento |
| R3.8 | Frase duplicada L108-109 → remover |
| R3.9 | Figuras sem acentuacao → padronizar |
| R3.10 | Siglas: VD, PLN/NLP, GLMM, OR, AUC, HR, IC, CNAE → expandir 1a mencao |
| R3.11 | Erros: atuarou, ejecutou-se, aggravada, L310 → corrigir |
| R3.12 | Refs orfas (Husted & Shapiro; Pärn et al.) → citar ou remover |
| R3.13 | Intervalos de pagina truncados → corrigir |
| R3.14 | Conclusao L312/L317 contradiz T4/T7 → reconciliar |

### R4 — Produto: riscos criticos
| # | Acao |
|---|------|
| R4.1 | SHAP vigencia_log 76,11% → 14,40% (Tabela 5, Figura 6, L271/352/368) |
| R4.2 | Matriz de confusao 98,89% (L346) → alinhar a Tabela 6 (93,36%) |
| R4.3 | Identidade Firebase: padronizar para projeto real `publicopilot` / `publicopilot.web.app` |
| R4.4 | Remover fragmento orfao `product_tecnologico.html` (381B) |

### R5 — Produto: versao, features, docs
| # | Acao |
|---|------|
| R5.1 | Atualizar para v2.1 (NVIDIA llama-3.3, rate limiting, OrdinalEncoder, XSS, dashboard admin) |
| R5.2 | Corrigir features (remover sla_presenca, dotacao_presenca, escore_if; sincronizar com Modelo B 11 features) |
| R5.3 | Reconciliar metricas academicas (93,36/90,83/26,39) vs producao (90,96/91,05/22,67) |
| R5.4 | Corpus "19.640 editais" → alinhar com numero canonico |
| R5.5 | Docs de apoio: remover narrativa Streamlit Cloud → Firebase |
| R5.6 | Artefatos de edicao ("硬", "recomendarecomenda", etc.) → corrigir |
| R5.7 | Refs listadas sem citacao → citar ou remover |

### R6 — Scripts geradores e rascunhos
| # | Acao |
|---|------|
| R6.1 | `scripts/montar_tese.py` / `reconstruir_tese_v2.py`: substituir metricas viciadas (98,27/98,97/95,22) e narrativa Streamlit |
| R6.2 | `artigo_cientifico_diagnostico.md`: atualizar esqueleto |
| R6.3 | `artigo_tecnologico_copiloto.md`: corrigir 94,88% → 93,36% |

### R7 — QA final
- Validacao numerica cruzada (todas as mencoes de n, OR, AUC, R², PSM, SHAP batendo entre Resumo/Corpo/Tabelas)
- Ausencia total de "Hacked", "comprapublica" (quando devia ser publicopilot), "Streamlit Cloud", "em fase de execucao"
- HTML integro, refs em ordem alfabetica, siglas expandidas

### R8 — LAYOUT HTML (artigos 1 e 2 da Tese)
| # | Acao |
|---|------|
| R8.1 | Artigo 1: trocar `<base href="https://raw.githubusercontent.com/...">` → `<base href="./">` |
| R8.2 | Artigo 2: idem |
| R8.3 | Validar renderizacao local (CSS + figuras carregam) |

---

## ORDEM DE EXECUCAO
R8 (layout, baixo risco) → R1 (criticos) → R2 (metodologia) → R3 (coerencia) → R4/R5 (produto) → R6 (scripts) → R7 (QA).

## CRITERIOS DE ACEITE
- Todos os numeros batem com os JSONs canonicos.
- Zero ocorrencias de "Hacked", "CENSITARIA" (titulo), "25,6%", "0,153", "0,813", "+4,2", "98,89%", "76,11%", "Streamlit Cloud".
- Artigos 1 e 2 da Tese renderizam com estilo ao abrir localmente.
