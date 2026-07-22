"""
SPRINT 6.1: Re-acentuacao do artigo — ASCII para portugues brasileiro.

Este script le o arquivo HTML do artigo (escrito sem acentos para
evitar problemas de encoding) e aplica substituicoes sistematicas
para converter para portugues brasileiro com acentuacao completa.

ATENCAO: Abstract em ingles NAO deve ser re-acentuado.
As secoes em ingles (ABSTRACT) sao preservadas.

Uso: python scripts/reacentuar_artigo.py
"""

import re
from pathlib import Path

ARTIGO_PATH = Path(
    r"C:\Users\Renato\Documents\Doutorado\Tese\artigos_tese"
    r"\02-Artigo-Tecnologico-Copiloto\artigo_02_tecnologico.html"
)

MAPA_ACENTOS = {
    # A
    "adocao": "adoção",
    "agencia": "agência",
    "analise": "análise",
    "aplicacao": "aplicação",
    "area": "área",
    "arvores": "árvores",
    "ate": "até",
    "atipico": "atípico",
    "atipicos": "atípicos",
    "automaticamente": "automaticamente",
    # C
    "caixa-preta": "caixa-preta",
    "caracteristicas": "características",
    "cibernetica": "cibernética",
    "cientifico": "científico",
    "cientifica": "científica",
    "cientificos": "científicos",
    "codigo": "código",
    "codigo-fonte": "código-fonte",
    "computacionais": "computacionais",
    "conclusao": "conclusão",
    "conclusoes": "conclusões",
    "conformidade": "conformidade",
    "confianca": "confiança",
    "conhecimento": "conhecimento",
    "conjunto": "conjunto",
    "constitucional": "constitucional",
    "construto": "construto",
    "construtos": "construtos",
    "contratacao": "contratação",
    "contratacoes": "contratações",
    "contratuais": "contratuais",
    "construcao": "construção",
    "contribuicao": "contribuição",
    "contribuicoes": "contribuições",
    "concepcao": "concepção",
    "correcao": "correção",
    "correcoes": "correções",
    "criterios": "critérios",
    # D
    "deficit": "déficit",
    "definicao": "definição",
    "demonstracao": "demonstração",
    "desempenho": "desempenho",
    "descricao": "descrição",
    "descricoes": "descrições",
    "deteccao": "detecção",
    "deterministico": "determinístico",
    "deterministica": "determinística",
    "disponivel": "disponível",
    "disponiveis": "disponíveis",
    "distribuicao": "distribuição",
    "duracao": "duração",
    "decada": "década",
    "decisao": "decisão",
    "decisoes": "decisões",
    "diagnostico": "diagnóstico",
    "dinamicas": "dinâmicas",
    "dinamicos": "dinâmicos",
    "disseminacao": "disseminação",
    "distancia": "distância",
    # E
    "eficiencia": "eficiência",
    "emergentes": "emergentes",
    "empirica": "empírica",
    "empirico": "empírico",
    "empiricos": "empíricos",
    "epistemologia": "epistemologia",
    "epistemica": "epistêmica",
    "especifico": "específico",
    "especifica": "específica",
    "especificos": "específicos",
    "especificidade": "especificidade",
    "estagio": "estágio",
    "estagios": "estágios",
    "estrategia": "estratégia",
    "evidencia": "evidência",
    "exigencia": "exigência",
    "explicacao": "explicação",
    "explicacoes": "explicações",
    "explicavel": "explicável",
    "explicaveis": "explicáveis",
    "extracao": "extração",
    # F
    "facil": "fácil",
    "fracasso": "fracasso",
    "funcao": "função",
    "fundamentacao": "fundamentação",
    # G
    "generico": "genérico",
    "genericos": "genéricos",
    "gestao": "gestão",
    "governanca": "governança",
    # H
    "heuristica": "heurística",
    "heuristicas": "heurísticas",
    "heuristico": "heurístico",
    # I
    "identificacao": "identificação",
    "impugnacao": "impugnação",
    "impugnacoes": "impugnações",
    "indicacao": "indicação",
    "ineficiencia": "ineficiência",
    "inegociavel": "inegociável",
    "inflacionada": "inflacionada",
    "inflacionadas": "inflacionadas",
    "informacao": "informação",
    "informacoes": "informações",
    "ingestao": "ingestão",
    "inovacao": "inovação",
    "insuficiente": "insuficiente",
    "integracao": "integração",
    "inteligencia": "inteligência",
    "interpretaveis": "interpretáveis",
    "intrinseco": "intrínseco",
    "intrinseca": "intrínseca",
    "introducao": "introdução",
    "investigacao": "investigação",
    "iteracao": "iteração",
    "iteracoes": "iterações",
    # J
    "juridico": "jurídico",
    "juridica": "jurídica",
    "juridicos": "jurídicos",
    "juridicas": "jurídicas",
    "jurisprudencia": "jurisprudência",
    # L
    "licitacao": "licitação",
    "licitacoes": "licitações",
    "licitatorio": "licitatório",
    "licitatoria": "licitatória",
    "limitacao": "limitação",
    "limitacoes": "limitações",
    "linguistica": "linguística",
    "linguistico": "linguístico",
    "logica": "lógica",
    # M
    "maquina": "máquina",
    "maxima": "máxima",
    "maximo": "máximo",
    "media": "média",
    "medio": "médio",
    "mercadologica": "mercadológica",
    "mercadologicas": "mercadológicas",
    "metricas": "métricas",
    "metodo": "método",
    "metodos": "métodos",
    "metodologia": "metodologia",
    "metodologico": "metodológico",
    "minima": "mínima",
    "minimo": "mínimo",
    "modulo": "módulo",
    "modulos": "módulos",
    "multiplas": "múltiplas",
    "multiplos": "múltiplos",
    "municipio": "município",
    "motivacao": "motivação",
    # N
    "nao": "não",
    "nivel": "nível",
    "niveis": "níveis",
    "numerica": "numérica",
    "numericas": "numéricas",
    "numerico": "numérico",
    "numericos": "numéricos",
    "numero": "número",
    "numeros": "números",
    # O
    "observacao": "observação",
    "observacoes": "observações",
    "observavel": "observável",
    "observaveis": "observáveis",
    "operacao": "operação",
    "operacionalizacao": "operacionalização",
    "orgao": "órgão",
    "orgaos": "órgãos",
    # P
    "pagina": "página",
    "paginas": "páginas",
    "padrao": "padrão",
    "padroes": "padrões",
    "paradigma": "paradigma",
    "particionavel": "particionável",
    "periodo": "período",
    "periodos": "períodos",
    "porem": "porém",
    "pragmatica": "pragmática",
    "predicao": "predição",
    "predicoes": "predições",
    "preditivo": "preditivo",
    "preditivos": "preditivos",
    "pre-processamento": "pré-processamento",
    "probabilidade": "probabilidade",
    "processamento": "processamento",
    "proporcao": "proporção",
    "proposito": "propósito",
    "protecao": "proteção",
    "prototipos": "protótipos",
    "publica": "pública",
    "publicas": "públicas",
    "publico": "público",
    "publicos": "públicos",
    "publicacao": "publicação",
    # Q
    "quantitativa": "quantitativa",
    # R
    "razao": "razão",
    "reducao": "redução",
    "relacao": "relação",
    "restricao": "restrição",
    "restricoes": "restrições",
    "rescisao": "rescisão",
    "rescisoes": "rescisões",
    "retificacao": "retificação",
    "retificacoes": "retificações",
    "revisao": "revisão",
    # S
    "sessao": "sessão",
    "sessoes": "sessões",
    "sintese": "síntese",
    "sintetico": "sintético",
    "sinteticos": "sintéticos",
    "solucao": "solução",
    "solucoes": "soluções",
    "substituicao": "substituição",
    "subsecao": "subseção",
    "sugestao": "sugestão",
    "sugestoes": "sugestões",
    "supervisionado": "supervisionado",
    # T
    "tambem": "também",
    "tecnica": "técnica",
    "tecnicas": "técnicas",
    "tecnico": "técnico",
    "tecnicos": "técnicos",
    "tecnologia": "tecnologia",
    "tecnologias": "tecnologias",
    "tecnologica": "tecnológica",
    "tecnologicas": "tecnológicas",
    "tecnologico": "tecnológico",
    "tecnologicos": "tecnológicos",
    "teoria": "teoria",
    "teorias": "teorias",
    "teorica": "teórica",
    "teoricas": "teóricas",
    "teorico": "teórico",
    "teoricos": "teóricos",
    "transparencia": "transparência",
    "traducao": "tradução",
    # U
    "urgencia": "urgência",
    "unica": "única",
    "unicas": "únicas",
    "unico": "único",
    "unicos": "únicos",
    "usuario": "usuário",
    "usuarios": "usuários",
    "util": "útil",
    "uteis": "úteis",
    # V
    "validacao": "validação",
    "variavel": "variável",
    "variaveis": "variáveis",
    "versao": "versão",
    "vetorizacao": "vetorização",
    "viavel": "viável",
    "viaveis": "viáveis",
    "vigencia": "vigência",
    "violacao": "violação",
    "visualizacao": "visualização",
    # Words needing specific handling
    "esta intrinsecamente": "está intrinsecamente",
    "esta ligado": "está ligado",
    "esta representado": "está representado",
    "equalizacao de forcas": "equalização de forças",
    "adocao de": "adoção de",
    "prestacao de contas": "prestação de contas",
    "aplicacao web": "aplicação web",
    "licenca MIT": "licença MIT",
    "repositorio aberto": "repositório aberto",
    "implantacao do": "implantação do",
    "concentracao de": "concentração de",
    "explicacao contrafactual": "explicação contrafactual",
    "explicacoes contrafactuais": "explicações contrafactuais",
    "sugestao de reescrita": "sugestão de reescrita",
    "serie temporal": "série temporal",
    "compras governamentais": "compras governamentais",
    "unidades compradoras": "unidades compradoras",
    "gestores publicos": "gestores públicos",
    "gestor publico": "gestor público",
    "agentes publicos": "agentes públicos",
    "politica de privacidade": "política de privacidade",
    "titularidade do codigo": "titularidade do código",
    "capacidade institucional": "capacidade institucional",
    "seguranca juridica": "segurança jurídica",
    "seguranca cibernetica": "segurança cibernética",
    "maquina de aprender": "máquina de aprender",
    "controlada pelo gestor": "controlada pelo gestor",
    "custos de transacao": "custos de transação",
    "discricionariedade do agente publico": "discricionariedade do agente público",
    "autonomia do gestor": "autonomia do gestor",
}

with open(ARTIGO_PATH, "r", encoding="utf-8") as f:
    content = f.read()

inside_abstract_en = False
lines = content.split("\n")
new_lines = []

for line in lines:
    if "<h2>ABSTRACT</h2>" in line:
        inside_abstract_en = True
    if "</div>" in line and inside_abstract_en:
        if "Palavras-chave" not in line and "Keywords" not in line:
            inside_abstract_en = False

    if inside_abstract_en:
        new_lines.append(line)
        continue

    for ascii_word, accented_word in MAPA_ACENTOS.items():
        pattern = re.compile(r"\b" + re.escape(ascii_word) + r"\b", re.IGNORECASE)
        line = pattern.sub(accented_word, line)

    new_lines.append(line)

result = "\n".join(new_lines)

with open(ARTIGO_PATH, "w", encoding="utf-8") as f:
    f.write(result)

print(f"Re-acentuacao concluida: {ARTIGO_PATH.name}")
print(f"Total de substituicoes no dicionario: {len(MAPA_ACENTOS)}")
