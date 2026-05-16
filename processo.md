# Processo de Desenvolvimento - Doutorado

---

## Fases do Doutorado

### Fase 1: Pesquisa e Revisão de Literatura
- Coleta de referências via APIs acadêmicas
- Revisão sistemática (PRISMA)
- Mapeamento bibliométrico (VOSviewer)
- Scoping Review

### Fase 2: Desenvolvimento do Artefato
- Extração de editais via API PNCP
- Construção da biblioteca de dados
- Desenvolvimento do copiloto algorítmico
- Implementação de módulos (avaliação + geração)

### Fase 3: Validação Técnica
- Métricas de NLP (legibilidade, similaridade)
- Testes de detecção de anomalias
- Avaliação de explicabilidade (SHAP)

### Fase 4: Pesquisa Empirical (Delphi)
- Seleção do painel (10 gestores)
- Construção do roteiro
- Rodadas de entrevista
- Análise de consenso

### Fase 5: Escrita e Publicação
- Redação dos artigos
- Formatação APA
- Submissão aos periódicos

---

## Stack Tecnológico

### Coleta de Dados
- Python (requests, BeautifulSoup)
- APIs: PNCP, Portal Transparência, TCU
- Jupyter Notebook para análises

### Processamento
- spaCy / NLTK (NLP)
- scikit-learn (ML)
- NetworkX (grafos)
- lifelines (análise sobrevivência)

### Análise Qualitativa
- IRaMuTeQ (análise textual)
- Python (análise discurso)

### Escrita
- Markdown → HTML (formatação APA)
- GitHub Pages (visualização)

---

## Git e Controle de Versão

### Estrutura de Branches

```
main        → Versão estável dos artigos
develop     → Desenvolvimento dos artigos
artigo-XX   → Branch específica por artigo
```

### Comandos

```bash
# Criar branch para artigo específico
git checkout -b artigo-01-opacidade

# Commit com mensagem descritiva
git commit -m "Adiciona seção metodologia artigo 1"

# Merge para develop
git merge develop

# Push para origin
git push origin main
```

---

## Padrões de Código

### Python para Coleta

```python
import requests
from typing import List, Dict

class PNCPClient:
    BASE_URL = "https://pncp.gov.br/api/v1"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def buscar_editais(self, palavra_chave: str, data_inicial: str) -> List[Dict]:
        url = f"{self.BASE_URL}/contratacoes"
        params = {"palavraChave": palavra_chave, "dataInicial": data_inicial}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
```

### Análise de Legibilidade

```python
import spacy
from textstat import flesch_kincaid_grade

def calcular_complexidade(texto: str) -> dict:
    nlp = spacy.load("pt_core_news_lg")
    doc = nlp(texto)
    
    return {
        "flesch_kincaid": flesch_kincaid_grade(texto),
        "num_tokens": len(doc),
        "num_sentencas": len(list(doc.sents)),
        "palavras_complexas": sum(1 for token in doc if len(token.text) > 10)
    }
```

---

## Checklists

### Coleta de Dados
- [ ] Registar credenciais APIs
- [ ] Testar endpoint de cada API
- [ ] Documentar estrutura de resposta
- [ ] Criar scripts de extração
- [ ] Validar dados coletados

### Análise Quantitativa
- [ ] Limpar dados (missing, outliers)
- [ ] Executar análise descritiva
- [ ] Aplicar método estatístico
- [ ] Interpretar resultados
- [ ] Criar visualizações

### Escrita
- [ ] Revisar conforme escrita.md
- [ ] Verificar citações APA
- [ ] Validar estrutura do artigo
- [ ] Testar render HTML
- [ ] Revisão ortográfica

---

## Repositório

**URL:** https://github.com/renato0503/TeseDoutorado

**Organização:**
- `Tese/` - Arquivos da tese
- `Artigos/` - 17 artigos em desenvolvimento
- `scripts/` - Scripts Python de análise
- `dados/` - Dados brutos e processados

---

## Referências

- Consultar `pesquisa.md` para APIs disponíveis
- Consultar `escrita.md` para normas de formatação
- Consultar `estrategia_paper.md` para estratégia de publicação