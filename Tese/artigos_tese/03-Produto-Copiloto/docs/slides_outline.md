# Estrutura dos Slides de Defesa

**Tese:** Copiloto Algoritmico para Compras Publicas Complexas
**Autor:** Renato de Oliveira Rosa
**Orientador:** Prof. Dr. Olavo Venturim Caldas
**Programa:** Doutorado em Contabilidade - Fucape Business School
**Tempo estimado:** 20-25 minutos

---

## Slide 1: Capa
- Titulo da tese
- Nome do autor
- Orientador
- Fucape Business School
- Data da defesa

## Slide 2: Agenda
1. Problema de pesquisa
2. Objetivos
3. Fundamentacao teorica
4. Metodo (Design Science Research)
5. Entregavel 1: Diagnostico Empirico (PNCP)
6. Entregavel 2: Artigo Tecnologico (DSR)
7. Entregavel 3: O Produto (Copiloto) **[DEMO AO VIVO]**
8. Contribuicoes e limitacoes

## Slide 3: O Problema
- **Lacuna pratica:** Gestores publicos enfrentam assimetria informacional ao redigir editais de compras complexas (TI, inovacao, sustentabilidade)
- **Consequencia:** Editais direcionados, impugnacoes, punicoes do TCU, "apagao das canetas"
- **Lacuna teorica:** Ausencia de ferramentas XAI aplicadas a contratacoes publicas no Brasil
- **Questao de pesquisa:** Como reduzir a assimetria informacional em compras publicas complexas usando IA Explicavel?

## Slide 4: Objetivos
- **Geral:** Desenvolver um artefato (Copiloto Algoritmico) baseado em XAI para mitigar assimetria informacional em compras complexas
- **Especificos:**
  1. Diagnosticar compras complexas no PNCP (5.687 de 572k)
  2. Construir motor de ML (Isolation Forest + Random Forest + SHAP)
  3. Desenvolver produto funcional com modelo Freemium

## Slide 5: Fundamentacao Teorica
- **Economia dos Custos de Transacao** (Williamson, 1985): assimetria, oportunismo, racionalidade limitada
- **Teoria da Agencia** (Jensen & Meckling, 1976): conflito agente-principal
- **Selecao Adversa** (Akerlof, 1970): mercado de limoes nas compras publicas
- **XAI / SHAP** (Lundberg & Lee, 2017): explicabilidade algoritmica
- **Design Science Research** (Peffers et al., 2007): metodo de construcao de artefatos

## Slide 6: Metodo - Design Science Research
- Framework de 6 etapas de Peffers et al. (2007)
- **Ciclo 1:** Diagnostico empirico (PNCP) -> identificacao do problema
- **Ciclo 2:** Construcao do artefato (DSR) -> desenvolvimento do Copiloto
- **Ciclo 3:** Validacao -> metricas de ML + demonstracao funcional

## Slide 7: Entregavel 1 - Diagnostico Empirico
- **Base:** 572.045 contratos PNCP (Set/2021 - Ago/2024)
- **Metodo:** Filtro semantico NLP (dicionario Inovacao + Sustentabilidade)
- **Resultado:** 5.687 compras complexas (0.99%)
  - 3.098 fornecedores unicos
  - 1.622 orgaos unicos
  - R$ 491,9 bi em valor total
- **Proxies:** Porte do orgao (orcamento PNCP), Capital Social (BrasilAPI)

## Slide 8: Entregavel 2 - Artigo Tecnologico
- **Arquitetura do Copiloto:**
  1. TF-IDF (500 features) sobre objetos de contratos
  2. Isolation Forest (100 arvores) -> deteccao de anomalias
  3. Random Forest (100 arvores) -> predicao de risco (99.13% acc)
  4. SHAP TreeExplainer -> explicabilidade
- **Features:** valor_log (80.5%), complexidade_lexica (8.6%), score_tecnico (4.5%)
- **XAI:** Graficos SHAP provam que nao e "caixa preta"

## Slide 9: Entregavel 3 - O Produto
- **Stack:** Firebase + Scikit-Learn + SHAP
- **2 Modulos:**
  1. Avaliacao de Minutas (ML real)
  2. Geracao de Editais (XAI)
- **Modelo Freemium:** 3 analises gratuitas, Premium com reescrita
- **Consultoria:** Esteira para Consultoria Renato Rosa
- **Deploy:** Firebase (Hosting + Cloud Functions)

## Slide 10: DEMO AO VIVO (3-5 min)
- Abrir `firebase deploy`
- Home: metricas PNCP, status modelos
- Modulo 1: Carregar exemplo, analisar, mostrar SHAP
- Modulo 2: Gerar edital com clausulas XAI
- Premium: sugestoes de reescrita

## Slide 11: Contribuicoes
- **Teorica:** Aplicacao de XAI (SHAP) a contratacoes publicas brasileiras
- **Metodologica:** DSR aplicada a Contabilidade Publica
- **Pratica:** Ferramenta funcional para gestores publicos
- **Social:** Reducao da assimetria informacional, accountability, transparencia

## Slide 12: Limitacoes e Agenda Futura
- **Limitacoes:**
  - Target sintetico (nao ha label real de "fracasso" no PNCP)
  - Amostra de treino: 50k de 572k contratos
  - Dependencia da qualidade dos dados do PNCP
- **Agenda futura:**
  - Treinar com labels reais (impugnacoes, acordaos TCU)
  - Integrar LLM para reescrita avancada (GPT/LLaMA)
  - Expansao para estados e municipios

## Slide 13: Publicacoes e Produtos
- Artigo Cientifico 1: Diagnostico Empirico (submissao: RAC/RAUSP)
- Artigo Tecnologico 2: Copiloto DSR (submissao: JISTEM)
- Repositorio GitHub: github.com/renato0503/TeseDoutorado
- Produto: Copiloto Algoritmico (Firebase)
- Versao estatica: comprapublica.web.app (Firebase)

## Slide 14: Agradecimentos
- Orientador: Prof. Dr. Olavo Venturim Caldas
- Banca examinadora
- Fucape Business School
- Colegas e familia

---

**Dicas para apresentacao:**
- Ensaie a demo ao vivo 2-3 vezes antes da defesa
- Tenha uma versao offline (local) como backup
- Prepare prints das telas principais caso a internet falhe
- Cronometre cada slide para nao estourar o tempo
