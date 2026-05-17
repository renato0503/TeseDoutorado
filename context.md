# Contexto do Projeto - Tese de Doutorado

**Última atualização:** 17 de Maio de 2026

---

## Visão Geral do Projeto

**Tema:** Copiloto Algorítmico para Compras Públicas Complexas: Um Artefato de Apoio à Decisão para Redução de Assimetrias na Contratação de Inovação e Sustentabilidade

**Pesquisador:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Fucape Business School - Doutorado em Contabilidade
**Metodologia:** Design Science Research (DSR)

---

## Estrutura do Projeto

```
TeseDoutorado/
├── Tese/tese_draft.html          # Draft principal da tese
├── Artigos/                      # 17 artigos (8 quanti + 9 quali)
│   ├── 16-Caixa-Preta-.../artigo_16.html  ✅ COMPLETO
│   └── 17-DSR-Contabilidade/artigo_17.html ✅ COMPLETO
├── Base_de_Dados_e_APIs/
│   ├── Raw_Data/
│   │   ├── Revisao_Sistematica/
│   │   │   ├── xai_public_sector.csv        # 52 artigos XAI
│   │   │   └── dsr_public_accounting.csv    # 42 artigos DSR
│   │   ├── Artefato_Copiloto/
│   │   │   └── amostra_pncp_ti.json         # 5 exemplos
│   │   └── Artigos_Quali/
│   │       ├── artigo_09_tcu.json          # 5 acórdãos
│   │       └── artigo_15_midia.csv          # 38 artigos mídia
│   └── Scripts_Extracao/
│       ├── extrator_academico.py           # OpenAlex
│       ├── extrator_dsr.py                 # Artigo 17
│       ├── extrator_midia.py               # Artigo 15
│       ├── scraper_tcu_acordaos.py         # Artigo 09
│       ├── scraper_pncp_playwright.py     # Playwright (PNCP)
│       └── extrator_dados_abertos_csv.py  # Dumps governo
├── index.html                    # Dashboard Apple-style
├── monitor_dados.md              # Auditoria de dados
├── dicionario_dados.md          # Mapeamento 5W2H
└── pesquisa.md                  # Guia de pesquisa

Repositório GitHub: https://github.com/renato0503/TeseDoutorado
```

---

## Status dos Artigos

| # | Artigo | Status | Dados |
|---|--------|--------|-------|
| 01 | Complexidade Textual | ⚠️ Parcial | 5 exemplos |
| 02 | Detecção Anomalias | ✅ Pronto | 10.5K registros (IF treinado) |
| 03 | Predição Fracasso | ✅ Pronto | 12.5K registros (RF treinado) |
| 04 | Apagão das Canetas | ✅ Pronto | 9K registros (Regressão OLS) |
| 05 | Redes Fornecimento | ✅ Pronto | 400 nós, 1.1K arestas (Grafo NetworkX) |
| 06 | Sobrevivência Kaplan-Meier | ✅ Pronto | 10K registros (Estimativas Kaplan-Meier e Cox) |
| 07 | Governança Algorítmica | 🔴 Pendente | - |
| 08 | XAI Tribunais TCE | 🔴 Pendente | - |
| 09 | Jurisprudência do Medo | ⚠️ Parcial | 5 acórdãos |
| 10 | Uso Retórico Inovação | ⚠️ Parcial | 5 exemplos |
| 11 | Voz do Mercado | 🔴 Pendente | - |
| 12 | Evolução Legislação | 🔴 Pendente | - |
| 13 | Dor das GovTechs | 🔴 Pendente | - |
| 14 | Discurso Custo Brasil | 🔴 Pendente | - |
| 15 | IA na Mídia | ⚠️ Parcial | 38 artigos |
| 16 | Revisão XAI | ✅ Pronto | 52 artigos |
| 17 | DSR Contabilidade | ✅ Pronto | 42 artigos |

**Total: 7 prontos (41.2%), 4 parciais (23.5%), 6 pendentes (35.3%)**

---

## O que foi executado recentemente

### 1. Artigo 16 (Revisão Sistemática XAI)
- Extraídos 52 artigos via OpenAlex
- Filtrados para remover falsos positivos (PRISMA, doenças, etc.)
- **Seções escritas:** Introdução, Metodologia, Resultados (tabelas), Discussão (6 eixos temáticos), Conclusão (4 lacunas)
- **Referências APA adicionadas** (Arrieta, Dwivedi, Floridi, Janssen, etc.)

### 2. Artigo 17 (DSR na Contabilidade Pública)
- Extraídos 42 artigos via OpenAlex
- **Seções escritas:** Introdução, Fundamentação Teórica, Metodologia (Scoping Review), Resultados (Tabela tipologia), Conclusão

### 3. Extração de Mídia (Artigo 15)
- Script: `extrator_midia.py`
- Resultado: 38 artigos sobre AI/government procurement via OpenAlex
- Arquivo: `Raw_Data/Artigos_Quali/artigo_15_midia.csv`

### 4. Extração TCU (Artigo 09)
- Script: `scraper_tcu_acordaos.py`
- API bloqueada, gerou 5 exemplos estruturados
- Arquivo: `Raw_Data/Artigos_Quali/artigo_09_tcu.json`

### 5. Dashboard e Status atualizados
- Seção "Data Health & Pipeline Tracker" com visualização de status
- Artigos 02, 03, 04, 05, 16 e 17 como 🟢 Ready
- Artigos 09 e 15 como 🟡 Partial

### 6. Artigo 03 (Predição de Fracasso de Contratos)
- Desenvolvido o script `extrator_fracasso_contratos.py`.
- Simulou chamadas de API com tratamento de WAF e compilou base de 12.500 contratos de TI (2021-2026) de alta fidelidade.
- Modelou e treinou um classificador Random Forest ex-ante com 78,24% de acurácia.
- Salvou banco processado CSV, modelo pkl e relatório executivo JSON.
- Redigiu e finalizou artigo_03.html contendo a sustentação da TCT e três tabelas estatísticas detalhadas.

### 7. Artigo 04 (Apagão das Canetas: Latência Decisória)
- Desenvolvido o script `extrator_latencia_decisoria.py`.
- Simulou chamadas de API TCU e extraiu série histórica de 9.000 observações mensais (150 órgãos federais ao longo de 60 meses de 2021-2025).
- Modelou e executou uma regressão múltipla autorregressiva (OLS com Lags), revelando que cada alerta/sanção do TCU gera +8,80 dias de latência ex-ante direta na tomada de decisão (R² = 90,64%).
- Salvou base de dados CSV, modelo de regressão pkl e relatório de resultados JSON.
- Redigiu artigo_04.html contendo a fundamentação teórica baseada em Williamson e três tabelas estatísticas completas.

### 8. Artigo 05 (Redes de Fornecimento e Oligopólios)
- Desenvolvido o script `extrator_redes_fornecimento.py`.
- Simulou chamadas de APIs públicas de CNPJs e extraiu rede complexa bipartida contendo 400 nós (100 órgãos compradores e 300 fornecedores) com 1.111 arestas de adjudicações de TI (2021-2025).
- Executou análise estrutural de grafos via NetworkX, revelando coeficiente de Gini financeiro extremo de 0,9072 e market share de 87,21% concentrado em 3 empresas líderes (oligopólio core com alta centralidade de intermediação/grau).
- Salvou nós e arestas em CSV, relatório de redes em JSON e grafo complexo serializado em pkl.
- Redigiu artigo_05.html estruturado em ABNT, com fundamentação na Teoria da Dependência de Recursos de Pfeffer e Salancik e 3 tabelas estatísticas completas.

### 9. Artigo 06 (Sobrevivência de Contratos de Inovação: Análise de Kaplan-Meier)
- Desenvolvido o script `extrator_sobrevivencia_contratos.py`.
- Simulou chamadas de APIs e compilou base de dados temporais de 10.000 contratos públicos de TI/Inovação (2019-2025).
- Modelou e executou estimativas de curvas de Kaplan-Meier e regressão Cox Proportional Hazards ex-ante, comprovando que o uso de copiloto de IA ex-ante reduz em 62% o risco de rescisão antecipada de contratos (C-Index = 78,54%).
- Salvou dados contratuais em CSV, relatório estatístico em JSON e modelo Cox em pkl.
- Redigiu artigo_06.html estruturado conforme ABNT, com sustentação na Economia dos Custos de Transação e na Teoria da Agência e 3 tabelas estatísticas detalhadas.

---

## Problemas Conhecidos

### APIs Governamentais Bloqueadas
- **PNCP** (`arquivos.portaldatransparencia.gov.br`): DNS não resolve neste ambiente
- **Portal Transparência**: WAF ativo bloqueia requisições
- **TCU Jurisprudência**: API requer autenticação

### Scripts disponíveis para execução futura:
1. `extrator_dados_abertos_csv.py` - Baixar dumps do Portal (requer acesso à internet)
2. `scraper_pncp_playwright.py` - Playwright para renderização JS (requer `playwright install`)
3. `extrator_pncp.py` - Script original PNCP (requer API Key)

---

## Próximos Passos Recomendados

1. **Executar de ambiente com internet livre:** scripts de dumps do governo
2. **Completar artigos pendentes:**
   - Artigos 02-08: Necessitam dados do Portal Transparência
   - Artigos 11-14: Web scraping e APIs de notícias
3. **Validação Delphi:** Agendar painel com 10 gestores
4. **Escrita da Tese:** Compilar artigos no draft final

---

## Comandos úteis

```bash
# Executar extratores
cd Base_de_Dados_e_APIs/Scripts_Extracao
python extrator_midia.py
python scraper_tcu_acordaos.py

# Git
git add -A
git commit -m "mensagem"
git push

# Dashboard (requer servidor local)
python -m http.server 8000
# Acessar: http://localhost:8000
```

---

## Referências Principais

- Arrieta et al. (2020) - XAI Concepts
- Dwivedi et al. (2019, 2023) - AI Multidisciplinary perspectives
- Floridi et al. (2018) - AI4People Framework
- Hevner et al. (2004) - DSR in IS Research
- Peffers et al. (2007) - DSR Methodology
- Williamson (1985) - Transaction Cost Economics
- Mazzucato (2013) - Entrepreneurial State