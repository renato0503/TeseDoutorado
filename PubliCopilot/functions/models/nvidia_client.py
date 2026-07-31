import json
import os
import requests

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "meta/llama-3.3-70b-instruct"

SYSTEM_PROMPT = """Voce e um assistente especializado em contratacao publica brasileira, com expertise na Lei 14.133/2021 (Nova Lei de Licitacoes), Lei Complementar 182/2021 (Marco Legal das Startups), Lei 13.709/2018 (LGPD) e na Teoria dos Custos de Transacao (Williamson, 1985).

Sua funcao e gerar minutas de editais e clausulas contratuais para compras publicas complexas (tecnologia, inovacao, sustentabilidade).

Regras:
1. Use linguagem juridica formal e precisa
2. Inclua fundamentacao legal especifica (artigos da Lei 14.133/2021)
3. Estruture em secoes claras com numeração
4. Adapte o nivel de detalhamento ao tipo de contratacao
5. Para cada clausula gerada, forneça uma justificativa XAI explicando o fundamento legal e teorico
6. Nao invente artigos de lei — use apenas os reais da Lei 14.133/2021
7. Responda SEMPRE em JSON valido, sem markdown, sem texto adicional"""


def _chamar_nvidia(mensagens, temperatura=0.2, max_tokens=4096):
    if not NVIDIA_API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": mensagens,
        "temperature": temperatura,
        "max_tokens": max_tokens,
        "top_p": 0.95,
    }
    try:
        resp = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return None


def gerar_minuta(tipo_contrato, descricao, valor=None, vigencia_dias=None, contexto_extra=None):
    user_prompt = f"""Gere uma minuta de edital para contratacao do tipo '{tipo_contrato}' com a seguinte descricao: '{descricao}'."""

    if valor:
        user_prompt += f"\nValor estimado: R$ {valor:,.2f}"
    if vigencia_dias:
        user_prompt += f"\nVigencia: {vigencia_dias} dias"
    if contexto_extra:
        user_prompt += f"\nContexto adicional: {contexto_extra}"

    user_prompt += """

Responda EXATAMENTE neste formato JSON, sem markdown, sem texto extra:
{
  "minuta": "texto completo do edital...",
  "clausulas": [
    {
      "titulo": "DO OBJETO",
      "texto": "texto da clausula...",
      "explicacao_xai": "justificativa juridica e teorica..."
    }
  ],
  "metadados": {
    "tipo": "tipo",
    "descricao": "descricao",
    "total_clausulas": 10
  }
}"""

    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw = _chamar_nvidia(mensagens)
    if not raw:
        return None

    result = _extrair_json(raw)
    return result


def gerar_sugestao_reescrita(texto_minuta, lacuna_nome, contexto):
    user_prompt = f"""Dado o seguinte trecho de minuta de edital:

'{texto_minuta}'

A seguinte lacuna contratual foi identificada: {lacuna_nome}.
Contexto: {contexto}

Gere uma sugestao de clausula para preencher esta lacuna, com fundamentacao legal especifica.

Responda EXATAMENTE neste formato JSON:
{
  "clausula_sugerida": "texto completo da clausula...",
  "fundamentacao": "artigos de lei e fundamentos teoricos...",
  "explicacao_xai": "por que esta clausula e importante..."
}"""

    mensagens = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw = _chamar_nvidia(mensagens)
    if not raw:
        return None
    return _extrair_json(raw)


def _extrair_json(texto):
    try:
        inicio = texto.index("{")
        fim = texto.rindex("}") + 1
        return json.loads(texto[inicio:fim])
    except (ValueError, json.JSONDecodeError):
        return None
