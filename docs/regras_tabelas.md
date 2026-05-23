# Regras para Formatação de Tabelas Acadêmicas (APA 7ª Edição)

## Visão Geral

Este documento estabelece as regras de formatação de tabelas seguindo o padrão da American Psychological Association (APA) 7ª edição, adotado como padrão unificado para todos os artigos da tese.

---

## Estrutura Geral das Tabelas

### Elementos Obrigatórios

1. **Número da Tabela**: Negrito, acima da tabela, seguido do título
2. **Título (Caption)**: Em itálico, posicionado acima da tabela
3. **Cabeçalho**: Com bordas superior e inferior, texto centralizado
4. **Corpo**: Células com alinhamento especificado
5. **Linha final**: Borda inferior apenas na última linha de dados
6. **Nota (Fonte)**: Abaixo da tabela, sem itálico

### Marges e Espaçamentos

- Tabelas centralizadas na página
- Espaçamento simples dentro das células
- Font size: 10pt
- Margens: superior e inferior de 0,5cm

---

## Cabeçalhos de Tabela (APA)

### Alinhamento

| Tipo de Dados | Alinhamento |
|---------------|-------------|
| Texto | Alinhado à esquerda |
| Números | Alinhado à direita ou centro |
| Cabeçalho de coluna | Sempre centralizado |

### Estrutura de Linhas

```
┌─────────────────────────────────────────────┐
│ Tabela 1                                     │
│ Título da Tabela em Itálico                  │
├─────────────────────────────────────────────┤
│ Coluna 1  │  Coluna 2  │  Coluna 3         │  ← Bordas superior/in inferior
├───────────┼─────────────┼───────────────────┤
│ Dados     │    123      │    456            │
│ Dados     │    789      │    012            │
├───────────┼─────────────┼───────────────────┤
│ dados     │    345      │    678            │  ← Única linha com borda inferior
└───────────┴─────────────┴───────────────────┘
   Fonte: Elaboração própria.
```

---

## Título (Caption) - APA

### Formato Padrão

**Tabela X**  
*Título descritivo em itálico*

### Exemplos

**Correto (APA):**  
**Tabela 1**  
* Métricas Gerais do Benchmarking de Eficiência Administrativa*

**Incorreto (ABNT):**  
Tabela 1: Métricas Gerais do Benchmarking de Eficiência Administrativa

### Observações

- Número da tabela em **negrito**
- Título em *itálico*
- Não usar dois-pontos entre número e título
- Título deve ser conciso mas descritivo

---

## Células de Dados

### Alinhamento por Tipo

```html
<td class="left">   <!-- Texto: esquerda -->
<td class="right">  <!-- Números: direita -->
<td class="center"> <!-- Centralizado -->
```

### Números

- Separador decimal: vírgula (formato brasileiro)
- Separador de milhar: ponto
- Exemplos: 1.234,56 | 87,5 | 0,38

### Valores Monetários

- **NUNCA** incluir símbolo de moeda (R$, $, €) no cabeçalho
- Incluir informação na nota de fonte: "Fonte: Elaboração própria. Valores em reais (R$)."

### Casas Decimais

- Manter consistência dentro da coluna
- Arredondar para 2 casas decimais quando apropriado
- Não usar zeros à esquerda: 0,38 não 0,38

---

## Notas de Tabela (APA)

### Tipos de Nota

1. **Nota geral**: Explanations about the table
2. **Nota de probabilidade**: Significant results (p < .001)
3. **Nota de fonte**: Origem dos dados

### Ordem de Precedência

1. Nota geral (se houver)
2. Nota de probabilidade (se houver)
3. Nota de fonte (sempre)

### Formato

```
Nota. [Nota geral explicativa se houver]
* p < .05. ** p < .01. *** p < .001.
Fonte: [descrição da origem].
```

---

## Tabelas em HTML (Estrutura CSS)

### Classe ABNT-Table (Padrão)

```css
table.abnt-table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.6cm 0;
    font-size: 10pt;
    line-height: 1.2;
}

table.abnt-table th {
    border-top: 1.5px solid black;
    border-bottom: 1.5px solid black;
    padding: 6px;
    font-weight: bold;
    text-align: center;
}

table.abnt-table td {
    padding: 5px;
    text-align: center;
}

table.abnt-table td.left {
    text-align: left;
}

table.abnt-table td.right {
    text-align: right;
}

table.abnt-table tr.last-row td {
    border-bottom: 1.5px solid black;
}
```

### Elementos de Estilo

```css
.table-note {
    text-indent: 0 !important;
    font-size: 10pt;
    margin-top: 0.1cm;
    margin-bottom: 0.3cm;
    line-height: 1.2;
}

.table-caption {
    font-weight: bold;
    text-align: left;
    margin-bottom: 0.2cm;
}
```

---

## Checklist de Revisão

- [ ] Número da tabela em negrito
- [ ] Título em itálico
- [ ] Sem dois-pontos após o número
- [ ] Cabeçalho com bordas superior e inferior
- [ ] Última linha com borda inferior
- [ ] Valores monetários apenas na nota de fonte
- [ ] Números com vírgula decimal e ponto de milhar
- [ ] Alinhamento correto por tipo de dado
- [ ] Nota de fonte em formato APA
- [ ] Sem linhas verticais

---

## Exemplo Completo (APA)

```
**Tabela 1**
*Métricas Gerais do Benchmarking de Eficiência Administrativa*

| Métrica                    | Valor     |
|----------------------------|-----------|
| Tempo Médio (horas/edital) | 45,66     |
| Ganho Relativo             | 88,74%    |
| Teste T pareado             | p < .001  |

Nota. Métricas obtidas a partir de simulação com 180 municípios.
* p < .05. ** p < .01. *** p < .001.
Fonte: Elaboração própria.
```

---

*Última atualização: Maio 2026*
*Documento de referência para padronização APA em todos os artigos da tese*