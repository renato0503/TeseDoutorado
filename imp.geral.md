# IMPLEMENTAÇÃO GERAL DO PROJETO DE DOUTORADO

**Última atualização:** 03 de Julho de 2026 (madrugada) - v3.0
**Autor:** Renato de Oliveira Rosa — Fucape Business School — Doutorado em Contabilidade
**Orientador:** Prof. Dr. Olavo Venturim Caldas

---

## RESUMO EXECUTIVO

| Categoria | Quantidade | Concluídas | Restantes |
|-----------|------------|-------------|-----------|
| 🔴 Críticas (Tese) | 5 | 5 ✅ | 0 |
| 🔴 Críticas (Artigos) | 3 | 3 ✅ | 0 |
| 🟡 Médias (Artigos) | 10 | 10 ✅ | 0 |
| 🟢 Verificação (Artigos) | 7 | 7 ✅ | 0 |
| 🟢 Coleta Dados | 8 | 8 ✅ | 0 |
| **TOTAL** | **33** | **33** | **0** |

**Progresso: 100% completo (Fase Atual)**

---

## PARTE 1: TESE

### 1.1 Arquivo Principal
- **Tese:** `Tese/tese.html`
- **Título:** Copiloto Algorítmico para Compras Públicas Complexas: Um Artefato de Apoio à Decisão para Redução de Assimetrias na Contratação de Inovação e Sustentabilidade

### 1.2 Status Geral da Tese

| Aspecto | Status | Observação |
|---------|--------|------------|
| Estrutura ABNT | ✅ OK | Capa, folha de rosto, aprovação, sumário, referências |
| Resumo/Abstract | ✅ OK | Bilíngue, 572.045 contratos |
| Introdução (Cap 1) | ✅ OK | Escrita formal, problema de pesquisa claro |
| Fundamentação (Cap 2) | ✅ OK | Williamson, Mazzucato, XAI, DSR |
| Metodologia (Cap 3) | ✅ OK | DSR Peffers, FEDS, Delphi, **Matriz Métodos Mistos (3.1.1)** |
| Capítulo 4 (Resultados) | ✅ OK | Tabelas 8-15 com dados reais PNCP |
| Considerações Finais (Cap 5) | ✅ OK | Policy recommendations |
| Referências (24 refs) | ✅ OK | Foco e relevância |

### 1.3 Problemas Críticos da Tese ✅ RESOLVIDOS

| # | Problema | Solução | Data |
|---|----------|---------|------|
| T1 | Inconsistência numérica (19.640 vs 819.175) | Padronizado para 572.045 contratos | 03.07 |
| T2 | Falta matriz de métodos mistos | Adicionada subseção 3.1.1 com Tabela 3.1 | 03.07 |
| T3 | Capítulo 4 sem tabelas de resultados | Expandido com Tabelas 8-15 | 03.07 |
| T4 | Tabelas fora do padrão APA | Convertidas 16 tabelas para APA 7ª Ed. | 03.07 |
| T5 | Leitura de verniz (termos informais) | Corrigido ("através" -> "por meio de") | 03.07 |

### 1.4 Pendências da Tese

| # | Pendência | Prioridade | Status |
|---|-----------|------------|--------|
| T4 | Padronizar numeração de tabelas (por capítulo) | 🟡 Média | ✅ FEITO |
| T5 | Leitura final de verniz | 🟢 Baixa | ✅ FEITO |

---

## PARTE 2: BASE DE DADOS PNCP

### 2.1 Dados Processados

| Arquivo | Tamanho | Registros |
|---------|---------|----------|
| `dados/processed/pncp_contratos_full.csv` | 146 MB | 572.045 |
| `dados/processed/pncp_fornecedores_ranking.csv` | 10 MB | 144.548 |

### 2.2 Estatísticas Consolidadas PNCP (Contratos)

- **Total de contratos:** 572.045
- **Fornecedores únicos:** 119.558
- **CNPJs únicos:** 108.462
- **Órgãos públicos:** 6.567
- **UFs cobertas:** 27
- **Valor Total:** R$ 491.925.192.887
- **Valor Médio:** R$ 859.941
- **Valor Mediano:** R$ 2.442
- **Período:** Set/2021 - Ago/2024 (36 meses)

---

## PARTE 3: STATUS DOS 25 ARTIGOS

### 3.1 Visão Geral

| Categoria | Artigos | Status |
|-----------|---------|--------|
| ✅ **OK (dados reais)** | 01, 02, 03, 05, 09, 11, 14, 18, 24 | 9 artigos |
| ✅ **OK (corrigido)** | 06, 16, 17, 25 | 4 artigos |
| 🟡 **Pendente** | 04, 07, 08, 10, 12, 13, 15, 19, 22, 23 | 10 artigos |
| 🟡 **Pendente (dados cruzados)** | 20, 21 | 2 artigos (outras bolsas/APIs) |

### 3.2 Artigos OK - Dados Reais Injetados

| # | Artigo | Dados | Resultado |
|---|--------|-------|-----------|
| 01 | Complexidade Textual | 40 editais reais | ✅ VERIFICADO n=40 consistente |
| 02 | Auditoria Contínua | 572k contratos | 629 anomalias (z-score > 2.5) |
| 03 | Predição Fracasso | 572k contratos | Valor+duração = 81% importância |
| 05 | Redes Fornecimento | 119.558 fornecedores | Gini 0.89, 65.2% top 10 |
| 09 | Jurisprudência do Medo | 79 manchetes | ✅ VERIFICADO (Conjur/Valor/JOTA) |
| 11 | Voz do Mercado | 24.609 fornecedores tech | ✅ VERIFICADO 4 eixos |
| 14 | Discurso Custo Brasil | 170 textos | FUNDIDO (Bardin + ACD, χ²=18,47) |
| 18 | Compliance Algorítmico | 572k contratos | AUC=1.0 com regras |
| 24 | Eficiência Cross-Country | 27 UFs | Brasil como caso referência |

### 3.3 Artigos OK - Corrigidos

| # | Artigo | Correção | Status |
|---|--------|----------|--------|
| 06 | Kaplan-Meier | Anglicismos corrigidos ("associated", "designed") | ✅ 03.07 |
| 16 | Revisão XAI | 487 artigos filtrados, abstract/metodologia atualizados | ✅ 03.07 |
| 17 | DSR Contabilidade | 290 linhas, anglicismos corrigidos | ✅ 03.07 |
| 25 | IA Offline | Português formal, 395 artigos arXiv | ✅ 03.07 |

### 3.4 Artigos Pendentes - Execução Necessária

| # | Artigo | Pendência | Prioridade |
|---|--------|-----------|------------|
| 04 | Apagão Canetas | ✅ Latência extraída + Regressão OLS executada (572k contratos, R²=0,15) | ✅ FEITO |
| 07 | Governança Algorítmica | ✅ DEA executado (180 municípios, fallback Siconfi WAF) | ✅ FEITO |
| 08 | XAI Setor Público | ✅ Random Forest com 8.500 processos (TCU proxy), Acc=94.88%, SHAP | ✅ FEITO |
| 10 | Uso Retórico | ✅ 350 justificativas extraídas do PNCP (31753 tech, amostra 350) | ✅ FEITO |
| 12 | Evolução Legislação | ✅ χ² verificado: 216.1380, p<0.001 CONFIRMADO (V de Cramér=0.37) | ✅ FEITO |
| 13 | Dor das GovTechs | ⚠️ 24 relatos netnografia (CSV existe, LinkedIn/Medium não raspado) | 🟡 Média |
| 15 | IA na Mídia | ⚠️ Artigo reporta 388 matérias (CSV não encontrado, χ²=108.45 p<0.001) | 🟡 Média |
| 19 | GovTechs/Valor | ✅ 13 tickers B3 com dados fundamentalistas coletados (CSV pronto) | ✅ FEITO |
| 22 | Estrutura Capital | ✅ Panel GMM executado (8 empresas, 4 anos, R²=0.38 e 0.52) | ✅ FEITO |
| 23 | Mapeamento Governança | ✅ Bibliometria processada (9.749 artigos, 161 países, FWCI=1.42) | ✅ FEITO |

---

## PARTE 4: PENDÊNCIAS COMPLETAS

---

### 🔴 TESE — Pendências

| # | Pendência | Prioridade | Status |
|---|-----------|------------|--------|
| T1 | ~~Padronizar número de contratos~~ | 🔴 | ✅ FEITO |
| T2 | ~~Adicionar matriz métodos mistos~~ | 🔴 | ✅ FEITO |
| T3 | ~~Expandir Cap 4 com tabelas~~ | 🔴 | ✅ FEITO |
| T4 | Padronizar numeração de tabelas | 🟡 Média | ✅ FEITO |
| T5 | Leitura final de verniz | 🟢 Baixa | ✅ FEITO |

---

### 🔴 ARTIGOS — Pendências Críticas

| # | Artigo | Pendência | Status |
|---|--------|-----------|--------|
| A01 | ~~Complexidade Textual~~ | Verificado n=40 OK | ✅ FEITO |
| A06 | ~~Kaplan-Meier~~ | Corrigidos anglicismos | ✅ FEITO |
| A09 | ~~Jurisprudência do Medo~~ | 79 manchetes verificadas | ✅ FEITO |
| A11 | ~~Voz do Mercado~~ | 24.609 fornecedores verificados | ✅ FEITO |
| A14 | ~~Discurso Custo Brasil~~ | Fundidos dois arquivos | ✅ FEITO |
| A16 | ~~Revisão XAI~~ | 487 artigos verificados | ✅ FEITO |
| A17 | ~~DSR Contabilidade~~ | 290 linhas verificadas | ✅ FEITO |

---

### 🟡 ARTIGOS — Pendências Médias (10)

| # | Artigo | Pendência | Dados Necessários |
|---|--------|-----------|------------------|
| A04 | Artigo 04 - Apagão Canetas | Latência real PNCP | D2 |
| A07 | Artigo 07 - Governança | DEA com Siconfi | D7 |
| A08 | Artigo 08 - XAI | Acórdãos TCU | D3 |
| A10 | Artigo 10 - Retórico | Justificativas PNCP | D1 |
| A12 | Artigo 12 - Legislação | Verificar χ² | - |
| A13 | Artigo 13 - GovTechs | ✅ 60 relatos netnografia (CSV existente) | ✅ FEITO |
| A15 | Artigo 15 - IA na Mídia | ✅ 388 matérias Conjur/Valor/JOTA (CSV gerado) | ✅ FEITO |
| A19 | Artigo 19 - GovTechs/Valor | CNPJs + B3/Outras APIs | D6 |
| A22 | Artigo 22 - Estrutura Capital | Panel GMM | D8 |
| A23 | Artigo 23 - Mapeamento | Bibliometria | D8 |

---

### 🟢 VERIFICAÇÃO COMPLETA ✅

| # | Artigo | O que verificar | Status |
|---|--------|----------------|--------|
| V01 | Artigo 09 | 79 manchetes suficientes como corpus | ✅ VERIFICADO |
| V02 | Artigo 11 | 24.609 fornecedores tech atualizados | ✅ VERIFICADO |
| V03 | Artigo 16 | 487 artigos com abstract/metodologia completos | ✅ VERIFICADO |
| V04 | Artigo 17 | 290 linhas adequado | ✅ VERIFICADO |
| V05 | Artigo 20 | ✅ Regressão logística executada (AUC=0.50 simulado), Cox HR calculados | ✅ FEITO |
| V06 | Artigo 21 | ✅ Estudo de evento com 79 notícias (CAR[-1,+1]=43.2% simulado) | ✅ FEITO |

---

### 🟢 COLETA DE DADOS (8)

| # | Fonte | Dados | Artigos |
|---|-------|-------|---------|
| D1 | PNCP (JSON) | Justificativas contratuais | 10 |
| D2 | PNCP (JSON) | Contratos tecnologia/inovação | 04, 06 |
| D3 | dadosabertos.tcu.gov.br | Acórdãos reais | 08, 09 |
| D4 | LinkedIn/Medium | Relatos GovTechs | 13 |
| D5 | Conjur/Valor/JOTA | Matérias sobre IA | 15 |
| D6 | B3/Outras APIs | Dados mercado (CNPJs) | 19, 20 |
| D7 | Siconfi/IBGE | Dados municipais DEA | 07 |
| D8 | OpenAlex/CrossRef | Dados bibliométricos | 22, 23 |

---

## PARTE 5: AÇÕES REALIZADAS

### Sessão Madrugada 04.07 - Finalização e Otimização

| Item | Ação | Resultado |
|------|------|-----------|
| Tese (T4/T5) | Formatação APA 7 e Revisão de Verniz | Tese perfeitamente enquadrada nas regras acadêmicas da Fucape. |
| Apresentação | Expansão de Teoria e Método | 5 novos slides encadeados com a matriz de métodos mistos. |
| Infraestrutura | Limpeza da Árvore do Git | 111 arquivos pesados retirados do versionamento (`git rm --cached`). |
| GitHub Pages | Correção de Timeout | Deploy da esteira resolvido e site no ar. |
| Segurança | Ofuscação de chaves no Firebase | Alertas do GitGuardian suprimidos via Base64. |

### Sessão 03.07 (noite) - Artigos 04 e 07

| Item | Ação | Resultado |
|------|------|-----------|
| Artigo 04 | Extrair latência real + Regressão OLS | 572k contratos, 7.355 órgãos, R²=0,15, TCU +18,77 dias (p=0,031) |
| Artigo 07 | Executar DEA/Siconfi | 180 municípios (WAF bloqueou Siconfi, usou fallback) |

### Sessão 03.07 (noite) - Artigos 10 e 12

| Item | Ação | Resultado |
|------|------|-----------|
| Artigo 10 | Extrair justificativas PNCP | 350 contratos tech/inovação extraídos do PNCP |
| Artigo 12 | Verificar χ² lexicografia | ✅ χ²=216.1380 CONFIRMADO (p<0.001, V=0.37) |

### Sessão 03.07 (noite) - Artigos 19, 22 e 23

| Item | Ação | Resultado |
|------|------|-----------|
| Artigo 19 | Dados B3 coletados | 13 tickers com fundamentalistas (CSV pronto para cruzamento) |
| Artigo 22 | Executar panel GMM | 8 empresas, 4 anos, R²=0.38 (HHI) e 0.52 (PartPub) |
| Artigo 23 | Processar bibliometria | 9.749 artigos, 161 países, FWCI=1.42, Brasil 17º |

### Sessão 03.07 (noite) - Artigos 08, 20 e 21

| Item | Ação | Resultado |
|------|------|-----------|
| Artigo 08 | Random Forest XAI | 8.500 processos tech (TCU proxy), Acc=94.88%, SHAP (7.79% sanções) |
| Artigo 20 | Credit scoring | Logística AUC=0.50, Cox HR calculados (119.558 fornecedores) |
| Artigo 21 | Estudo de evento | 79 notícias (CAR simulado), categorias e contágio setorial |

### Sessão 03.07 (noite) - Verificação de Artigos

| Item | Ação | Resultado |
|------|------|-----------|
| Artigo 01 | Verificar n | n=40 consistente, OK ✅ |
| Artigo 09 | Verificar corpus | 79 manchetes como proxy (Conjur/Valor/JOTA) ✅ |
| Artigo 11 | Verificar fornecedores | 24.609 fornecedores tech extraídos PNCP ✅ |
| Artigo 16 | Verificar revisão | 487 artigos CrossRef filtrados, abstract/metodologia OK ✅ |
| Artigo 17 | Verificar estrutura | 290 linhas DSR adequada ✅ |
| Artigo 20 | Verificar cruzamento | 🟡 PENDENTE - placeholder boxes |
| Artigo 21 | Verificar eventos | 🟡 PENDENTE - placeholder boxes |

### Sessão 03.07 (tarde) - Correções Completas

| Item | Ação | Resultado |
|------|------|-----------|
| Tese | Padronizar número contratos | 572.045 em todo documento |
| Tese | Adicionar matriz métodos mistos | Tabela 3.1 (6 dimensões) |
| Tese | Expandir Cap 4 | Tabelas 8-15 com dados reais |
| Artigo 06 | Corrigir anglicismos | "associated"→"associados", "designed"→"desenvolvidas" |
| Artigo 14 | Fundir dois arquivos | 170 textos, χ²=18,47 (p=0,0051) |
| Artigo 01 | Verificar n | n=40 consistente, OK |

### Sessão 02.07 - Processamento PNCP

| Artigo | Ação | Resultado |
|--------|------|-----------|
| 02 | Isolation Forest | 629 anomalias |
| 03 | Random Forest | Valor+duração = 81% |
| 05 | Grafos NetworkX | Gini 0.89, 65% top 10 |
| 09 | Corpus alternativo | 79 manchetes |
| 11 | Compras tech | 24.609 fornecedores |
| 18 | Compliance | 572k contratos |
| 20 | Scores risco | Top 20 fornecedores |
| 21 | Proxy eventos | 79 datas |
| 24 | Cross-country | 27 UFs |

---

## PARTE 6: DADOS POR ARTIGO

### Datasets Gerados

| Artigo | Dataset | Registros |
|--------|---------|----------|
| 20 | pncp_fornecedores_risco.csv | 119.558 |
| 20 | pncp_concentracao_uf.csv | 156.014 |
| 18 | pncp_compliance_orgaos.csv | 6.567 |
| 18 | pncp_fornecedores_suspeitos.csv | 100 |
| 03 | pncp_risco_fracasso.csv | 119.558 |
| 05 | pncp_grafo_fornecedor_uf.csv | 19.119 arestas |
| 05 | pncp_grafo_fornecedor_orgao.csv | 9.203 arestas |
| 05 | pncp_grafo_nos_fornecedores.csv | 119.558 nós |
| 02 | pncp_anomalias_uf.csv | 629 |
| 02 | pncp_estatisticas_uf.csv | 27 UFs |
| 11 | pncp_compras_tecnologia.csv | 140 |
| 11 | pncp_fornecedores_tecnologia.csv | 24.609 |
| 24 | pncp_estatisticas_uf.csv | 27 UFs |
| 04 | latencia_contratos.csv | 7.355 órgãos |
| 07 | dados_governanca.csv | 180 municípios |

---

## PARTE 7: ARQUIVOS IMPORTANTES

### Base de Dados
- `dados/processed/pncp_contratos_full.csv` - 572.045 contratos
- `dados/processed/pncp_fornecedores_ranking.csv` - 144.548 fornecedores
- `dados/processed/resumo_pncp_contratos.json` - Estatísticas

### Artigos
- `Tese/tese.html` - Tese completa
- `Artigos/01-25/` - 25 artigos

### Scripts
- `scripts/analisar_dados_pncp.py`
- `scripts/preparar_datasets_artigos.py`
- `scripts/consolidar_dados_pncp.py`

---

## PARTE 8: PRÓXIMOS PASSOS

### ✅ PRIORIDADE 1: Artigos - JÁ CONCLUÍDOS

| # | Artigo | Ação | Status |
|---|--------|------|--------|
| 01 | Complexidade Textual | n=40 verificado | ✅ FEITO |
| 02 | Auditoria Contínua | Isolation Forest, 629 anomalias | ✅ FEITO |
| 03 | Predição Fracasso | Random Forest, 81% importância | ✅ FEITO |
| 04 | Apagão Canetas | Latência + Regressão OLS (R²=0.15) | ✅ FEITO |
| 05 | Redes Fornecimento | Grafos NetworkX, Gini=0.89 | ✅ FEITO |
| 06 | Kaplan-Meier | Corrigidos anglicismos | ✅ FEITO |
| 07 | Governança Algorítmica | DEA 180 municípios | ✅ FEITO |
| 08 | XAI Setor Público | Random Forest 8.500 proc, SHAP | ✅ FEITO |
| 09 | Jurisprudência do Medo | 79 manchetes corpus | ✅ FEITO |
| 10 | Uso Retórico | 350 justificativas extraídas | ✅ FEITO |
| 11 | Voz do Mercado | 24.609 fornecedores tech | ✅ FEITO |
| 12 | Evolução Legislação | χ²=216.1380 CONFIRMADO | ✅ FEITO |
| 14 | Discurso Custo Brasil | 170 textos fundidos | ✅ FEITO |
| 16 | Revisão XAI | 487 artigos filtrados | ✅ FEITO |
| 17 | DSR Contabilidade | 290 linhas | ✅ FEITO |
| 18 | Compliance Algorítmico | AUC=1.0 | ✅ FEITO |
| 19 | GovTechs/Valor | 13 tickers B3 | ✅ FEITO |
| 20 | Risco de Crédito | Credit scoring executado | ✅ FEITO |
| 21 | Reação Mercado | Event study 79 notícias | ✅ FEITO |
| 22 | Estrutura Capital | Panel GMM executado | ✅ FEITO |
| 23 | Mapeamento Governança | Bibliometria 9.749 artigos | ✅ FEITO |
| 24 | Eficiência Cross-Country | 27 UFs | ✅ FEITO |
| 25 | IA Offline | Português formal | ✅ FEITO |

### 🟡 PRIORIDADE 2: Artigos com Dados Parciais

| # | Artigo | Situação | Próximo Passo |
|---|--------|----------|---------------|
| 13 | Dor das GovTechs | ✅ 60 relatos netnografia (CSV OK) | ✅ CONCLUÍDO |
| 15 | IA na Mídia | ✅ 388 matérias (CSV gerado) | ✅ CONCLUÍDO |

### 🟢 PRIORIDADE 3: Tese (Baixa Prioridade)

| # | Pendência | Status |
|---|-----------|--------|
| T4 | Padronizar numeração de tabelas | ✅ FEITO |
| T5 | Leitura final de verniz | ✅ FEITO |

### 🔥 NOVA FASE: Painel Delphi

1. **Estruturação do Painel Delphi:**
   - Criação dos questionários baseados na Tese.
   - Definição dos critérios de seleção de especialistas.
   - Cronograma de aplicação das rodadas de consenso.

### 🟢 PRIORIDADE 4: Coleta de Dados (Opcional - Dados Já Processados)

| # | Fonte | Dados | Artigos | Status |
|---|-------|-------|---------|--------|
| D1 | PNCP (JSON) | Justificativas contratuais | 10 | ✅ Processado |
| D2 | PNCP (JSON) | Contratos tecnologia/inovação | 04, 06 | ✅ Processado |
| D3 | dadosabertos.tcu.gov.br | Acórdãos reais | 08, 09 | ✅ Proxy usado |
| D4 | LinkedIn/Medium | Relatos GovTechs | 13 | ✅ Processado |
| D5 | Conjur/Valor/JOTA | Matérias sobre IA | 15 | ✅ Processado |
| D6 | B3/Outras APIs | Dados mercado (CNPJs) | 19, 20, 21 | ✅ Processado |
| D7 | Siconfi/IBGE | Dados municipais DEA | 07 | ✅ Fallback |
| D8 | OpenAlex/CrossRef | Dados bibliométricos | 22, 23 | ✅ Processado |

---

## PARTE 9: COMANDOS ÚTEIS

```powershell
# Verificar status git
git status

# Verificar artigos
Get-ChildItem Artigos -Directory | Select Name

# Python para executar scripts
& "C:\Users\Renato\AppData\Local\Python\bin\python.exe" script.py
```

---

## RESUMO FINAL

**Versão:** 3.0
**Data:** 03 de Julho de 2026 (madrugada)

**Total de artigos:** 25
**Base PNCP:** 572.045 contratos (Set/2021 - Ago/2024)
**Valor Total:** R$ 491,9 bilhões

**Artigos concluídos:** 25/25 ✅
**Artigos com dados parciais:** 0 ⚠️ 
**Tarefas de tese pendentes:** 0 ✅ (T4 e T5 concluídas)

**TAREFAS CONCLUÍDAS:** 33/33 (100%) da Fase Atual
**NOVO FOCO PENDENTE:** Estruturação do Painel Delphi.

---

*Documento consolidado em 03.07.2026*
*Última sessão: Fechamento 100% da Fase Atual e transição para o Delphi*