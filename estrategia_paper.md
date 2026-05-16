# Estratégia de Geração de Paper Acadêmico

## Visão Geral

Este documento descreve a estratégia completa para gerar papers acadêmicos seguindo rigorosamente o guia de escrita.md. O processo foi desenvolvido e validado com o paper "O Paradoxo da Produtividade da IA".

---

## Fase 1: Preparação do Ambiente

### 1.1 Arquivos de Referência Obrigatórios

Antes de iniciar, garanta que os seguintes arquivos existam:

- **escrita.md**: Guia completo de escrita acadêmica com regras deformatação, citações, linguagem e estrutura
- **pesquisa.md**: Diretrizes para pesquisa e coleta de dados
- **documentacao.md**: Documentação do projeto

### 1.2 Estrutura de Diretórios

```
ThePapperAI/
├── papers/
│   └── [nome-do-paper]/
│       ├── 01-pesquisa/
│       ├── 02-escrita/
│       ├── 03-revisao/
│       ├── 04-formatacao/
│       └── 05-documento/
│           ├── [nome].html
│           ├── [nome].docx
│           ├── tabelas.xlsx
│           └── assets/
├── escrita.md
├── pesquisa.md
└── estrategia_paper.md
```

---

## Fase 2: Pesquisa e Coleta de Dados

### 2.1 Definição do Tema

1. Identificar o tema do paper
2. Definir a pergunta de pesquisa
3. Estabelecer os objetivos (geral e específicos)

### 2.2 Revisão de Literatura

Seguir pesquisa.md para coletar referências de:
- Artigos acadêmicos (Google Scholar, SciELO, etc.)
- Livros e capítulos
- Relatórios e publicações corporativas
- Bases de dados especializadas

### 2.3 Categorias de Análise

Definir categorias analíticas baseadas no referencial teórico. Exemplos do paper:
- Natureza da justificativa
- Presença de dados operacionais concretos
- Contexto financeiro da empresa
- Existência de sobrecontratação prévia
- Investimentos simultâneos em IA
- Linguagem utilizada

---

## Fase 3: Escrita Seguindo escrita.md

### 3.1 Regras Obrigatórias de Idioma

- **Português do Brasil apenas**: Todo o texto em português brasileiro
- **Termos técnicos em inglês**: Manter em itálico na primeira ocorrência com tradução entre parênteses
- **Citações diretas em inglês**: Tradução livre entre parênteses

### 3.2 Estrutura do Paper (Formato APA)

1. **Título**
2. **Resumo** (150-300 palavras)
3. **Abstract** (mesmo conteúdo em inglês)
4. **Palavras-chave** / **Keywords**
5. **1. Introdução**
   - Contexto amplo
   - Problema específico
   - Justificativa
   - Objetivos
   - Estrutura do trabalho
6. **2. Revisão de Literatura**
   - Panorama geral
   - Frameworks teóricos
   - Estudos contemporâneos
   - Lacuna na literatura
7. **3. Metodologia**
   - Enquadramento metodológico
   - Delineamento
   - Procedimentos de coleta
   - Procedimentos de análise
   - Limitações
8. **4. Resultados**
   - Caracterização do corpus
   - Categorias de análise
   - Síntese
9. **5. Discussão**
   - Interpretação por categoria
   - Resposta à pergunta de pesquisa
   - Contribuições
10. **6. Conclusão**
    - Síntese dos achados
    - Implicações
    - Limitações
    - Sugestões futuras
11. **Referências**

### 3.3 Regras de Estilo

#### ❌ PROIBIDO
- Adjetivações valorativas: "excelente", "impressionante", "incrível"
- Expressões informais: "hoje em dia", "cada vez mais", "basicamente"
- Travessão (—)
- Palavras marcadoras de IA: "crucial", "inovador", "holístico", "delve", "landscape"
- Português de Portugal: "ao princípio", "de modo que"

#### ✅ OBRIGATÓRIO
- Conectivos após cada ponto (ver lista completa em escrita.md)
- Citações em toda afirmação que não seja resultado próprio
- Pessoa verbal: 3ª pessoa ou 1ª pessoa do plural
- Tempos verbais corretos por seção:
  - Revisão: presente ou pretérito
  - Metodologia: pretérito perfeito
  - Resultados: pretérito perfeito
  - Discussão: presente

### 3.4 Formatação APA 7ª Edição

| Elemento | Especificação |
|----------|----------------|
| Margens | 2.54 cm (1 polegada) |
| Fonte | Times New Roman 12 |
| Espaçamento | Duplo |
| Alinhamento | À esquerda |
| Recuo de parágrafo | 1.27 cm |
| Citações (até 40 palavras) | Aspas no texto |
| Citações (mais de 40 palavras) | Bloco recuado, fonte 10 |
| Referências | Recuo francês (hanging indent) |

---

## Fase 4: Criação das Tabelas

### 4.1 Processo de Criação

1. **Identificar todas as tabelas do paper**: Listar todas as tabelas mencionadas no texto
2. **Criar estrutura em CSV**: Formatarp dados em formato CSV
3. **Converter para Excel (XLSX)**: Usar openpyxl para criar arquivo com cada tabela em sheet separada

### 4.2 Exemplo de Script Python

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Nome da Tabela"

# Escrever dados
# Aplicar estilos...

wb.save("tabelas.xlsx")
```

### 4.3 Estrutura do Arquivo XLSX

Cada sheet deve conter:
- Cabeçalho em negrito com fundo cinza
- Bordas em todas as células
- Texto justificado com quebra de linha

---

## Fase 5: Validação e Revisão

### 5.1 Checklist de Revisão (segundo escrita.md)

#### Estrutura
- [ ] Texto segue lógica macro → micro em todas as seções
- [ ] Cada seção cumpre sua função sem repetir conteúdo
- [ ] Introdução apresenta: contexto, problema, justificativa, objetivo
- [ ] Revisão da literatura é analítica
- [ ] Metodologia detalhada o suficiente para replicação
- [ ] Resultados apresentam dados sem interpretação
- [ ] Discussão interpreta resultados à luz da literatura
- [ ] Conclusão sintetiza sem introduzir informação nova

#### Linguagem
- [ ] Sem adjetivações valorativas
- [ ] Sem expressões informais ou coloquiais
- [ ] Sem uso de travessão
- [ ] Sem palavras marcadoras de IA
- [ ] Pessoa verbal correta (3ª pessoa / 1ª plural)
- [ ] Tempos verbais corretos por seção
- [ ] Frases com no máximo 4 linhas

#### Coesão e Fluidez
- [ ] Toda frase após ponto final começa com conectivo
- [ ] Parágrafos conectados entre si
- [ ] Não há dois parágrafos consecutivos com mesmo conectivo

#### Citações
- [ ] Toda afirmação que não é resultado próprio tem citação
- [ ] Citações no formato APA correto
- [ ] Variedade nas formas de integrar citações
- [ ] Todas as referências citadas no texto
- [ ] Referências atualizadas (predominantemente últimos 5-10 anos)

---

## Fase 6: Geração de Documentos Finais

### 6.1 Arquivos de Saída

1. **HTML**: Versão para GitHub Pages
2. **DOCX**: Versão para download/edição
3. **XLSX**: Tabelas formatadas para Excel

### 6.2 Configuração do GitHub Pages

1. Ativar GitHub Pages em Settings → Pages
2. Selecionar branch main
3. O site será disponível em: `https://[usuario].github.io/[repositorio]/`

### 6.3 Arquivo Index

Criar index.html na raiz com menu de papers:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>ThePapperAI - Papéis Acadêmicos</title>
</head>
<body>
    <h1>ThePapperAI</h1>
    <p>Papers Acadêmicos Gerados com IA</p>
    
    <div class="papers-grid">
        <!-- Cards para cada paper -->
    </div>
</body>
</html>
```

---

## Fase 7: Git e Deploy

### 7.1 Comandos Git

```bash
# Adicionar arquivos (forçar se ignorados pelo .gitignore)
git add -f arquivo.html arquivo.docx arquivo.xlsx

# Commitar
git commit -m "Descrição das alterações"

# Push
git push
```

### 7.2 Atualização do .gitignore

Para permitir arquivos específicos:

```gitignore
# Allow specific files
!papers/[pasta]/05-documento/[arquivo].html
!papers/[pasta]/05-documento/[arquivo].docx
!index.html
!tabelas.xlsx
```

---

## Checklist Final de Execução

- [ ] Tema definido e pergunta de pesquisa formulada
- [ ] Referências coletadas e organizadas
- [ ] Estrutura do paper definida
- [ ] Draft completo seguindo escrita.md
- [ ] Todas as tabelas criadas em XLSX
- [ ] Revisãoconforme checklist
- [ ] Arquivos HTML e DOCX gerados
- [ ] GitHub Pages ativado
- [ ] Index.html criado com menu
- [ ] Arquivos commitados e pushados

---

## Notas Adicionais

### Diferenças ABNT vs APA

| Aspecto | ABNT | APA |
|---------|------|-----|
| Sobrenome entre parênteses | MAIÚSCULO | Normal |
| Separador de autores | ponto e vírgula | & |
| Espaçamento | 1,5 | Duplo |
| Alinhamento | Justificado | À esquerda |

### Conectivos Acadêmicos (exemplos)

**Adição**: Além disso, Ademais, Nesse sentido, De forma complementar
**Contraste**: Contudo, Entretanto, No entanto, Por outro lado
**Causa**: Em razão disso, Devido a esse fato, Em consequência
**Consequência**: Dessa forma, Assim sendo, Por conseguinte
**Conclusão**: Portanto, Logo, Em síntese, Diante do exposto

---

*Documento gerado automaticamente para fins de documentação do processo.*
