<!-- NOTE: Movido para docs/ em 2026-05-23 -->

# Contexto do Projeto - Tese de Doutorado

**Última atualização:** 18 de Maio de 2026

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
├── Tese/
│   ├── tese_draft.html           # Draft principal da tese (1298 linhas, ABNT)
│   ├── style_academico.css       # Estilo ABNT/APA
│   ├── gerar_graficos.py         # Geração de SVGs (matplotlib)
│   └── imagens/                  # 10 SVGs (5 gráficos + 5 figuras)
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
│   │   ├── extrator_academico.py           # OpenAlex
│   │   ├── extrator_dsr.py                 # Artigo 17
│   │   ├── extrator_midia.py               # Artigo 15
│   │   ├── scraper_tcu_acordaos.py         # Artigo 09
│   │   ├── scraper_pncp_playwright.py     # Playwright (PNCP)
│   │   └── extrator_dados_abertos_csv.py  # Dumps governo
├── index.html                    # Dashboard Apple-style
├── monitor_dados.md              # Auditoria de dados
├── monitor_referencias.html      # 68 referências, 5 eixos temáticos
├── dicionario_dados.md          # Mapeamento 5W2H
└── pesquisa.md                  # Guia de pesquisa

Repositório GitHub: https://github.com/renato0503/TeseDoutorado
```