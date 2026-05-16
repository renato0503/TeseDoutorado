# Contexto do Projeto - Tese de Doutorado

**Última atualização:** 16 de Maio de 2026

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
| 02 | Detecção Anomalias | 🔴 Pendente | - |
| 03 | Predição Fracasso | 🔴 Pendente | - |
| 04 | Apagão das Canetas | 🔴 Pendente | - |
| 05 | Redes Fornecimento | 🔴 Pendente | - |
| 06 | Sobrevivência Kaplan-Meier | 🔴 Pendente | - |
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

**Total: 4 prontos (23.5%), 4 parciais (23.5%), 9 pendentes (52.9%)**

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

### 5. Dashboard atualizado
- Seção "Data Health & Pipeline Tracker" com visualização de status
- Artigos 16 e 17 como 🟢 Ready
- Artigos 09 e 15 como 🟡 Partial

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