# Sprint de Melhorias — Artigo 15
## O Enquadramento da IA no Controle Público na Mídia

**Status atual:** 8,0/10 — Estrutura sólida, dados reais, achados robustos (χ²=108,45; p<0,001)
**Objetivo:** 9,5/10 — Submissão para EGPA 2027 / ICEGOV 2027 / IRSPM 2027
**Prazo estimado:** 5 dias (sprints de 1 dia cada)

---

## Sprint 1 — Correções Estruturais e Autoplágio (Dia 1)

### 1.1 Renumerar Figuras (1h)
| Ação | Arquivo | Descrição |
|------|---------|-----------|
| Figura 1 | `artigo_15.html` | `figura1_enquadramentos_portal.svg` → "Distribuição dos Enquadramentos por Portal" |
| Figura 2 | `artigo_15.html` | `figura2_distribuicao_global.svg` → "Distribuição Global dos Enquadramentos" |
| Figura 3 | `artigo_15.html` | `artigo15_evolucao_midia.svg` → "Evolução Temporal do Enquadramento Midiático" |

**O que fazer:**
- No HTML, renomear todas as ocorrências de "Figura 1" e "Figura 2" para sequência única (Figura 1, 2, 3)
- Verificar se as tags `<img>` ou referências existem e apontam para os SVGs corretos
- Se não houver tags `<img>`, adicioná-las com `src` apontando para os arquivos na mesma pasta
- Adicionar legendas descritivas abaixo de cada figura

### 1.2 Remover Autoplágio da Seção 6.1 (2h)
**Localização:** Seção "6.1 Implicações Práticas e Políticas Públicas" (3 parágrafos)

**O que fazer:**
- Apagar COMPLETAMENTE os 3 parágrafos atuais (Capacitação Contínua / Revisão de Marcos / Adoção de IA)
- Escrever implicações EXCLUSIVAS do Artigo 15, centradas em:
  - Estratégias de comunicação para adoção de IA no setor público
  - Gestão da percepção pública e legitimidade social
  - Papel da mídia especializada na construção da confiança institucional
  - Recomendações para gestores: como navegar o ceticismo jurídico vs. pressão por eficiência

**Exemplo de novo texto (substituir integralmente):**

> Os achados de polarização discursiva entre a imprensa jurídica e econômica oferecem implicações diretas para a adoção de sistemas de IA no setor público brasileiro.
>
> **1. Estratégias de Comunicação Diferenciadas:** Órgãos públicos que implementam ferramentas algorítmicas devem calibrar sua comunicação institucional conforme o perfil do stakeholder. Para audiências jurídicas (tribunais de contas, ministério público), a ênfase deve recair sobre mecanismos de explicabilidade, rastreabilidade e conformidade legal. Para audiências econômicas (fornecedores, mercado), o discurso deve priorizar ganhos de eficiência, redução de custos de transação e previsibilidade decisória.
>
> **2. Transparência Algorítmica como Condição de Legitimidade:** O ceticismo jurídico identificado no Conjur (78,8% das matérias nos frames RVO + LCC) indica que a opacidade é o principal obstáculo à aceitação da IA no serviço público. Sistemas de apoio à decisão devem incorporar explicabilidade ex-ante (SHAP, contrafactuais normativos) como requisito funcional, não como acessório.
>
> **3. Monitoramento Contínuo da Percepção Midiática:** A valência de sentimento oscilou significativamente entre portais e ao longo do tempo (Conjur: -0,32; Valor: +0,58). Recomenda-se que órgãos de controle e inovação estabeleçam observatórios permanentes de enquadramento midiático para antecipar barreiras de aceitação pública.

### 1.3 Remover Viés do Copiloto na Seção 5.1 (1h)
**Localização:** Seção "5.1 Extensão Teórica e a Solução Sociotécnica (DSR)"

**O que fazer:**
- Apagar menções ao "Copiloto Algorítmico" como artefato específico
- Substituir por discussão genérica sobre "artefatos de apoio à decisão com XAI"
- Manter a contribuição teórica ("Latência Institucional Algorítmica") pois é original e bem articulada
- Conectar os achados de polarização com as condições de legitimidade social descritas na literatura (Suchman, 1995)

---

## Sprint 2 — Expansão do Referencial Teórico (Dia 2)

### 2.1 Inserir Seção 2.3 (3h)
Criar nova subseção "2.3 Aceitação Social de Algoritmos no Setor Público"

**Literatura a adicionar (5-7 referências):**

| Tema | Referência | Contribuição para o artigo |
|------|------------|---------------------------|
| Algorithm Aversion | Dietvorst, Simmons & Massey (2015, *JEP: General*) | Explica por que profissionais rejeitam algoritmos mesmo quando superam humanos |
| Algorithm Appreciation | Logg, Minson & Moore (2019, *JMP*) | Contraponto: em algumas tarefas, pessoas preferem algoritmos |
| Trust in AI in Government | Wirtz, Weyerer & Sturm (2020, *Public Management Review*) | Fatores de confiança em IA no setor público |
| Public Sector AI Acceptance | Zuiderwijk, Chen & Salem (2021, *Government Information Quarterly*) | Modelo de aceitação de IA em governos |
| Social Construction of Technology | Pinch & Bijker (1984, *Social Studies of Science*) | Base teórica: a tecnologia é moldada socialmente |
| Algorithimic Legitimacy | Kaur et al. (2022, *AI & Society*) | Como algoritmos ganham ou perdem legitimidade |

**O que fazer:**
- Escrever 2-3 parágrafos articulando essas referências com o objeto do artigo
- Concluir com: "a aceitação da IA no setor público não depende apenas da acurácia técnica, mas da congruência entre o enquadramento midiático e as expectativas normativas dos diferentes públicos"

### 2.2 Expandir Seção 2.2 com Enquadramentos Específicos (1h)
Adicionar parágrafo sobre:
- Esquemas de enquadramento de tecnologia na mídia (Scheufele & Tewksbury, 2007)
- Como frames de "eficiência" vs. "risco" competem na cobertura de inovação governamental

### 2.3 Adicionar Referências (30 min)
Inserir todas as novas referências no final do artigo, em ordem alfabética. Garantir formatação APA 7a.

---

## Sprint 3 — Metodologia e Transparência (Dia 3)

### 3.1 Detalhar Codificação da Valência (2h)
**Localização:** Seção "3.1 Confiabilidade e Rigor Metodológico"

**O que fazer:**
Adicionar parágrafo detalhando o cálculo da valência:

> A valência de sentimento foi codificada em escala contínua de -1,0 a +1,0, adaptada de Semetko & Valkenburg (2000). Cada matéria recebeu um escore baseado na proporção de parágrafos com tom positivo vs. negativo em relação ao uso de IA no controle público. Parágrafos neutros ou descritivos (ex.: "o tribunal adquiriu um sistema de IA para auditoria") não pontuaram. Parágrafos com tom positivo (ex.: "a ferramenta reduziu em 40% o tempo de análise") contribuíram positivamente; parágrafos com tom negativo (ex.: "o modelo apresentou vieses raciais") contribuíram negativamente. O escore final de cada matéria é a média simples dos escores de seus parágrafos. Exemplos:
>
> - Matéria Valora 42 (RS=+0,92): 11 parágrafos positivos, 1 neutro, 0 negativos
> - Matéria Conjur 87 (RS=-0,73): 2 parágrafos positivos, 3 neutros, 8 negativos

### 3.2 Descrever Critérios de Elegibilidade do Corpus (1h)
Adicionar subseção "3.2 Critérios de Seleção do Corpus":

> Foram incluídas matérias que (a) mencionassem explicitamente o uso de IA, algoritmos ou aprendizado de máquina no contexto da administração pública brasileira; (b) fossem publicadas entre jan/2021 e mar/2026; (c) estivessem disponíveis integralmente nos portais Conjur, Valor Econômico ou Jota. Foram excluídas (a) notas curtas (< 3 parágrafos); (b) editoriais de opinião de terceiros; (c) matérias duplicadas entre os portais; (d) conteúdo pago/publicitário identificado.

### 3.3 Incluir Tabela de Exemplos de Codificação (1h)
Criar pequena tabela com 4-5 exemplos de matérias codificadas:

| Portal | Título Resumido | Frame | Valência | Justificativa |
|--------|----------------|-------|----------|---------------|
| Valor | "IA reduz custos de auditoria do TCU" | MET | +0,85 | Foco em eficiência e ganhos |
| Conjur | "Algoritmo opaco ameaça direito de defesa" | RVO | -0,91 | Foco em riscos processuais |

---

## Sprint 4 — Resultados e Visualização (Dia 4)

### 4.1 Embutir Figuras no HTML (2h)
Garantir que as 3 figuras estejam visíveis no HTML:
- Verificar/consertar caminhos das imagens SVG
- Adicionar tags `<figure>` com `<img src="...">` e `<figcaption>`
- Garantir que o `alt text` esteja preenchido

### 4.2 Adicionar Análise Longitudinal (2h)
**Localização:** Seção 4 (após Tabela 3)

> **4.4 Evolução Temporal dos Enquadramentos (2021-2026)**
>
> A Figura 3 apresenta a evolução dos enquadramentos ao longo do período analisado. Observa-se que o frame MET (Modernização e Eficiência) cresceu de 28,1% em 2021 para 45,2% em 2025, possivelmente impulsionado por políticas governamentais de digitalização (Estratégia Brasileira de IA, 2024). O frame RVO (Riscos e Opacidade) atingiu pico em 2023 (34,7%), ano de decisões controversas do STF sobre reconhecimento facial. Após 2024, os frames convergem para um equilíbrio instável, sugerindo que o debate público sobre IA no controle ainda não consolidou um enquadramento dominante.

### 4.3 Criar Tabela de Testes Estatísticos Adicionais (1h)
Incluir análise post-hoc para identificar quais pares de portais diferem significativamente:

> Testes de comparação post-hoc (Bonferroni ajustado) confirmaram que a diferença entre Conjur e Valor Econômico é altamente significativa (χ² = 74,23; p < 0,001), enquanto Conjur vs. Jota (χ² = 12,18; p = 0,058) e Valor vs. Jota (χ² = 9,87; p = 0,096) não atingiram significância ao nível de 5%, sugerindo que o Jota ocupa posição intermediária entre os dois polos.

---

## Sprint 5 — Conclusão e Preparação para Submissão (Dia 5)

### 5.1 Reescrever Conclusão (2h)
**O que fazer:**
- Manter os achados principais (já estão bons)
- Remover referências ao Copiloto na conclusão
- Adicionar parágrafo sobre agenda de pesquisa:
  - Ampliar corpus para mídias sociais (Twitter/X, LinkedIn)
  - Análise comparativa com outros países do BRICS
  - Efeito da cobertura midiática sobre decisões reais de investimento em IA governamental
  - Relação entre enquadramento midiático e alocação orçamentária em tecnologia pública

### 5.2 Revisão de Limitações (1h)
Adicionar limitações específicas e honestas:

> Além das limitações já mencionadas (três portais, recorte temporal 2021-2026), este estudo não estabelece relação causal entre o enquadramento midiático e decisões de policy. A análise de valência, embora replicável, captura apenas o tom explícito do texto, não nuances implícitas ou ironia. A codificação manual, embora com Kappa > 0,85, está sujeita a vieses de interpretação cultural dos codificadores. Pesquisas futuras podem empregar análise de sentimentos automatizada (BERT, RoBERTa) para validação externa.

### 5.3 Revisão de Escrita e Formatação (2h)
- Padronizar citações conforme APA 7a
- Verificar numeração consistente de seções e subseções
- Revisar ortografia e gramática
- Verificar se o abstract em inglês reflete o conteúdo final
- Ajustar formatação HTML para impressão limpa (CSS print)

### 5.4 Checklist de Submissão (30 min)

| Item | OK? |
|------|-----|
| Título claro e informativo | |
| Abstract ≤ 250 palavras | |
| Palavras-chave (4-6) | |
| Figuras numeradas e legendadas | |
| Tabelas numeradas e com fontes | |
| Referências 25-35 | |
| Seção 6.1 original (sem autoplágio) | |
| Seção 5.1 sem menção ao Copiloto | |
| Metodologia replicável | |
| Limitações explícitas | |

---

## Resumo do Escopo

| Sprint | Atividade | Horas | Entregável |
|--------|-----------|-------|------------|
| 1 | Correções estruturais e autoplágio | 4h | `artigo_15.html` reescrito (seções 5.1, 6.1) |
| 2 | Expansão referencial teórico | 4,5h | Nova seção 2.3, +7 referências |
| 3 | Metodologia e transparência | 4h | Seção 3 detalhada, tabela de exemplos |
| 4 | Resultados e visualização | 5h | Figuras embutidas, análise longitudinal |
| 5 | Conclusão e preparação | 5,5h | Artigo finalizado, checklist de submissão |
| **Total** | | **23h** | |

---

## Próximos Passos Após Sprint 5

1. Submeter para EGPA 2027 (deadline típica: abril/2027) ou ICEGOV
2. Considerar versão em inglês para periódico: *Government Information Quarterly*
3. Preparar apresentação (slides 15 min + pôster)

---

*Criado em: 29/07/2026*
