**# Padrões de Engenharia: Paradigma de Geração Determinística com LLMs (v5.0)

Resumo Executivo (Abstract): O presente documento estabelece um framework metodológico para o desenvolvimento de software assistido por agentes de Inteligência Artificial (LLMs). O objetivo central é mitigar a geração estocástica de código (coloquialmente referida como "vibe coding") — uma antiprática caracterizada por alta entropia, forte acoplamento e ausência de modelagem arquitetural. Ao impor invariantes arquiteturais e limitar o raio de impacto (blast radius) da inferência do modelo, asseguramos manutenibilidade, segurança e coesão sistêmica.

Postulado Fundamental: O LLM opera exclusivamente como um motor heurístico de execução algorítmica. O determinismo lógico, a definição da topologia arquitetural e a validação de corretude (correctness) permanecem sob a jurisdição inalienável da engenharia humana.

---

### 📋 Síntese Operacional do Pipeline (Workflow Checklist)

Para fins de execução expedita e ancoragem cognitiva do agente, o ciclo de vida do desenvolvimento reduz-se ao cumprimento estrito dos seguintes trâmites e primitivas de comando:

* /spec: Formulação da especificação estrutural (Mapeamento rigoroso de pages, behaviors e components).
* /break: Decomposição da especificação em issues menores e linearmente independentes.
* /plan: Varredura de contexto e elaboração do plano de execução antes de qualquer implementação.
* Agentes e Skills Especializadas: Execução descentralizada através de instâncias de IA restritas por camadas sistêmicas (e.g., especialização em frontend vs. database).
* Governança Baseada em Documentos (MD): Imposição contínua de regras inegociáveis de arquitetura e design através do diretório de referências.

---

### Fase 0: Inicialização Axiomática (A Infraestrutura /references)

A ausência de contexto de domínio em LLMs resulta em regressão à média estatística dos dados de treinamento. Para evitar a injeção de padrões arquiteturais heterogêneos e obsoletos, deve-se inicializar o ambiente de trabalho com axiomas fundamentais.

* Diretriz: Instancie o diretório /references na raiz do repositório como o espaço de inicialização (prompt priming) obrigatório do agente.
* Os 4 Pilares da Governança Estática:
  1. workflow.md (Controle de Processo): Define o autômato finito do ciclo de desenvolvimento (Spec $\rightarrow$ Break $\rightarrow$ Plan $\rightarrow$ Execute). Interdita modificações não mapeadas em grafos de dependência e bancos de dados.
  2. architecture.md (Topologia de Sistemas): Documenta as invariantes topológicas, como o paradigma Thin Client / Fat Server e a separação por Domínios Bounded (Feature Modules), suprimindo o acoplamento do padrão MVC genérico.
  3. DESIGN.md (Contrato Visual e UI): Restringe o espaço de busca da IA na geração de CSS e componentes, impondo o uso estrito do Design System homologado, prevenindo a inflação do Abstract Syntax Tree (AST) com código de interface redundante.
  4. specification.md (Ontologia do Produto): Fornece o escopo de domínio. Permite que o agente infira a macroestrutura lógica (Big Picture) durante a manipulação algorítmica de micro-estados.

---

### Fase 1: Mapeamento Ontológico (Discovery & Design)

A formulação do escopo mitiga a alucinação estrutural. O agente requer uma taxonomia clara antes da geração de código.

* Ação: Invocação do comando /spec para sintetizar a Especificação Mestra.
* Requisitos do Contrato Ontológico:
  * Topologia de Roteamento: Grafo direcionado de todas as rotas e endpoints da aplicação.
  * Árvore de Composição: Hierarquia estrita dos componentes de User Interface (UI).
  * Máquinas de Estado (Comportamento): Descrição das transições de estado causadas por interações do usuário (e.g., triggers, mutações de estado, tratamento de concorrência e latency).

---

### Fase 2: Desacoplamento Contextual (Feature Slicing)

A degradação do mecanismo de atenção (attention mechanism) em Transformers correla-se diretamente com o tamanho da janela de contexto. A minimização do escopo de inferência é imperativa.

* Ação: Utilização do comando /break para particionar a Especificação em grafos de tarefas (Issues) linearmente independentes.
* Corolários da Decomposição:
  * Complexidade $O(1)$ por Tarefa: Cada mutação de estado ou renderização de página configura uma Issue atômica. Isso reduz o ruído informacional e previne regressões topológicas.
  * Desenvolvimento Shift-Left (Prototipagem Estática): A interface deve ser compilada e homologada independentemente da lógica de negócios.
  * Mock-Driven Development (MDD): A injeção de dependência via Mock Service Workers (MSW) ou esquemas JSON é obrigatória. O acoplamento precoce a APIs subjacentes é estritamente proibido, garantindo a validação da Teoria dos Contratos.

---

### Fase 3: Heurística de Planejamento e Prevenção de Entropia

A fase de design arquitetural amarra as predições do LLM a um plano de execução determinístico.

* Ação: Execução do comando /plan para formulação do vetor de ataque da Issue.
* Diretrizes de Varredura (RAG Interno):
  1. Maximização do DRY (Don't Repeat Yourself): O agente deve computar a interseção entre o escopo da tarefa e a base de código existente, isolando componentes reutilizáveis.
  2. Adesão a RFCs Oficiais: Consulta mandatória às documentações das bibliotecas em uso.
* Outputs Críticos do Planejamento:

1. Resolução formal de Happy Paths e ramificações de exceção (Edge Cases).
2. TDD (Test-Driven Development): Estruturação prévia da suíte de testes (unitários e de integração).
3. Invariância de Dados (Migrations): Esquemas de banco de dados exigem scripts transacionais rigorosos (UP / DOWN). Bloqueio Crítico: Exclusões estruturais (operações destrutivas como Drop Column) requerem aprovação explícita do engenheiro líder.
4. Mapeamento de cardinalidade: Relatório exato e imutável das mutações de arquivo esperadas (Matriz Diff).

---

### Fase 4: Execução Modular Injetada

A síntese de código é realizada mediante o plano estritamente validado.

* Ação: Invocação do comando de execução (/execute) sob supervisão humana.
* Padrões de Engenharia Exigidos:
  * Domain-Driven Design (DDD) no Frontend: Arquitetura baseada em Feature Modules (coesão comportamental). O acoplamento transversal entre domínios é tratado como code smell crítico.
  * Execução Multi-Agente: Delegação hierárquica baseada em competências. O agente encarregado da Persistência de Dados não deve manipular a camada de Visualização, mitigando o risco de sobreposição de papéis lógicos.

---

### Fase 5: Análise Estática e Verificação Automatizada (Self-Review)

O LLM deve executar algoritmos de verificação antes da submissão para Code Review humano, estabelecendo um ciclo de auto-correção iterativo.

* Ação: Execução de rotina de inspeção intrínseca (/review).
* Critérios de Aceitação da Verificação Automática:
  * Segurança de Tipos (Type Safety): Rejeição taxativa de tipagem genérica não documentada (e.g., inibição de pragmas any em TypeScript).
  * Higiene Cibernética (Clean Code): Depuração de artefatos de diagnóstico (console.log), purga de referências órfãs (dead code/imports) e encapsulamento de constantes literais (Magic Numbers).
  * Cobertura de Testes: A computação só é finalizada se a árvore de testes gerada na Fase 3 alcançar status de sucesso (pass).

---

### Fase 6: Arquitetura Zero-Trust e Blindagem Operacional

O modelo mental de segurança pressupõe que o ambiente de front-end operará em contexto perpetuamente hostil.

* Ação: Consulta cíclica ao diretório axiomático /references.
* Limites Categóricos:
  * Assimetria Computacional (Thin Client / Fat Server):
    * Frontend: Atua estritamente como autômato de renderização isomórfica e captura de I/O. É desprovido de estado de negócios seguro.
    * Backend: Detém o monopólio da validação semântica, controle de acesso baseado em funções (RBAC), transações atômicas e criptografia.
  * Injeção de Ambiente: É categoricamente vetado o hardcoding de identificadores de rede (e.g., localhost) ou tokens de autorização. O acoplamento a variáveis de ambiente (.env) é estruturalmente obrigatório.

---

### Fase 7: Redução Contínua de Entropia (Refactoring Loop)

Sistemas complexos sob a influência contínua de agentes de IA sofrem acúmulo latente de débito técnico por divergência assintótica.

* Ação: Agendamento periódico do comando de otimização (/refactor).
* Heurística do Refatoramento: O agente rastreia e compara árvores sintáticas para identificar blocos com alta correlação estrutural. Ação resolutiva: Promove a extração das primitivas duplicadas para módulos de utilidade global (/shared/utils), validando a estabilidade do sistema pós-unificação através da execução redundante da suíte de testes automatizados.

**
