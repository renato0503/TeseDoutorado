"""
Cloud Function (Python 3.11) para o Copiloto Algoritmico.

Backend de ML real servido no Firebase (plano Blaze). Carrega os modelos
treinados (.pkl) uma unica vez no cold start e expoe um endpoint HTTP que
reproduz o pipeline do modulo de Avaliacao do Streamlit:

    texto -> clausulas (regex 16 padroes)
          -> lacunas contratuais
          -> score heuristico (0-100)
          -> Isolation Forest (TF-IDF) como feature adicional
          -> Random Forest (10 features, 100k contratos PNCP)
          -> SHAP TreeExplainer (explicabilidade + contrafactuais)

Autenticacao: requer token Firebase Auth valido (Authorization: Bearer <token>).

Deploy: firebase deploy --only functions
Entry point: funcao analisar_minuta (functions-framework, --target analisar_minuta)
"""

import json
import os
import sys
from pathlib import Path

# Garante que o diretorio 'models' seja importavel.
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Validacao opcional de Firebase Auth (desabilitada em dev local com SKIP_AUTH=1)
SKIP_AUTH = os.environ.get("SKIP_AUTH", "0") == "1"
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "publicopilot-aa662")
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS",
    "https://comprapublica.web.app,https://comprapublica.firebaseapp.com"
).split(",")

# Domínio principal para o cabeçalho CORS (backward compat).
PRIMARY_ORIGIN = ALLOWED_ORIGINS[0].strip() if ALLOWED_ORIGINS else "https://comprapublica.web.app"

import functions_framework  # noqa: E402

from models.risk_engine import analisar_risco_contratual, gerar_recomendacoes  # noqa: E402
from models.xai_explainer import gerar_explicacoes_clausulas  # noqa: E402


def _tratar_corpo(request):
    """Extrai texto e metadados do corpo da requisicao (JSON ou form)."""
    if request.content_type and "application/json" in request.content_type:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()
    texto = (data.get("texto") or data.get("minuta") or "").strip()
    try:
        valor = float(data.get("valor") or 0) or None
    except (TypeError, ValueError):
        valor = None
    try:
        vigencia_dias = int(data.get("vigencia_dias") or 0) or None
    except (TypeError, ValueError):
        vigencia_dias = None
    metadados = {}
    if valor is not None:
        metadados["valor"] = valor
    if vigencia_dias is not None:
        metadados["vigencia_dias"] = vigencia_dias
    return texto, metadados


def _validar_token_firebase(request):
    """Valida o token Firebase Auth (Authorization: Bearer <token>).

    Retorna (uid, email) se valido, ou (None, None) se SKIP_AUTH=1 (dev).
    Retorna (None, erro) se token invalido.
    """
    if SKIP_AUTH:
        return ("dev-user", "dev@local"), None

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, "Token de autenticacao ausente. Faca login primeiro."

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None, "Token vazio."

    # Validacao local sem chamar API (rapido e offline)
    try:
        import firebase_admin
        from firebase_admin import auth, credentials

        # Inicializacao lazy do SDK Admin
        if not firebase_admin._apps:
            try:
                # Tenta usar Application Default Credentials (funciona em Cloud Run/Functions)
                cred = credentials.ApplicationDefault()
            except Exception:
                cred = credentials.AnonymousProvider()
            firebase_admin.initialize_app(cred, {"projectId": FIREBASE_PROJECT_ID})

        decoded = auth.verify_id_token(token, check_revoked=False)
        return decoded.get("uid"), decoded.get("email")
    except ImportError:
        # firebase-admin nao instalado: faz validacao basica do JWT
        import base64
        import json as jsonlib
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None, "Token mal-formado."
            payload = parts[1]
            # Adiciona padding se necessario
            padding = 4 - (len(payload) % 4)
            if padding != 4:
                payload += "=" * padding
            decoded = jsonlib.loads(base64.urlsafe_b64decode(payload))
            if decoded.get("aud") == FIREBASE_PROJECT_ID and decoded.get("exp", 0) > 0:
                return decoded.get("user_id") or decoded.get("sub"), decoded.get("email")
            return None, "Token invalido (aud/exp)."
        except Exception as e:
            return None, f"Token invalido: {e}"
    except Exception as e:
        return None, f"Erro na verificacao do token: {e}"


@functions_framework.http
def analisar_minuta(request):
    """Endpoint HTTP: POST com {texto, valor?, vigencia_dias?}.

    Requer token Firebase Auth (Authorization: Bearer <token>).
    Retorna JSON com score, lacunas, clausulas, explicacoes XAI,
    predicao do Random Forest e SHAP.
    """
    # Habilita CORS para origens autorizadas (whitelist).
    # Antes estava "*" (permissivo) — corrigido em 19/07/2026 para reduzir superficie de ataque.
    origin = request.headers.get("Origin", "").strip()
    if origin in [o.strip() for o in ALLOWED_ORIGINS]:
        cors_origin = origin
    else:
        cors_origin = PRIMARY_ORIGIN

    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": cors_origin,
            "Vary": "Origin",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {
        "Access-Control-Allow-Origin": cors_origin,
        "Vary": "Origin",
    }

    # === Validacao de autenticacao ===
    uid, erro_auth = _validar_token_firebase(request)
    if erro_auth:
        return (json.dumps({"erro": erro_auth, "code": "unauthorized"}), 401, headers)

    # === Processamento do corpo ===
    try:
        texto, metadados = _tratar_corpo(request)
    except Exception as exc:  # Corpo invalido
        return (json.dumps({"erro": f"Corpo da requisicao invalido: {exc}"}), 400, headers)

    if not texto:
        return (json.dumps({"erro": "Informe o texto da minuta (campo 'texto')."}), 400, headers)

    # === Execucao do pipeline ML ===
    try:
        resultado = analisar_risco_contratual(texto, metadados)
        recomendacoes = gerar_recomendacoes(
            resultado.get("lacunas", []),
            resultado.get("clausulas_encontradas", []),
            resultado.get("features_shap"),
        )
        explicacoes_clausulas = gerar_explicacoes_clausulas(
            resultado.get("clausulas_encontradas", [])
        )

        payload = {
            "score": resultado.get("score"),
            "classificacao": resultado.get("classificacao"),
            "clausulas_encontradas": resultado.get("clausulas_encontradas", []),
            "explicacoes_clausulas": explicacoes_clausulas,
            "lacunas": resultado.get("lacunas", []),
            "recomendacoes": recomendacoes,
            "rf_proba": resultado.get("rf_proba"),
            "rf_score": resultado.get("rf_score"),
            "risco_ml": resultado.get("risco_ml"),
            "features_shap": resultado.get("features_shap", []),
            "contrafactuais": resultado.get("contrafactuais", []),
            "modelo_treinado": resultado.get("modelo_treinado", False),
            "metricas_treino": resultado.get("metricas_treino", {}),
            "usuario_id": uid,
        }
        return (json.dumps(payload, ensure_ascii=False), 200, headers)
    except Exception as exc:  # Erro de inferencia
        return (json.dumps({"erro": f"Falha ao analisar minuta: {exc}"}), 500, headers)


@functions_framework.http
def set_admin_claim(request):
    """Endpoint HTTP: POST para definir custom claim 'admin' em um usuario.

    Body: { "uid": "...", "admin": true/false, "secret": "..." }

    A segurança é feita via SHARED_SECRET no env var. Apenas o proprietario
    do projeto pode definir custom claims atraves deste endpoint, usando
    o segredo que ele configurou.

    USO INICIAL (para criar o primeiro admin):
        1. Configure o env var ADMIN_SETUP_SECRET no Firebase Functions
        2. Faca POST com uid do admin e admin=true
        3. Apos a definicao, REMOVA o env var ADMIN_SETUP_SECRET por seguranca
    """
    # Habilita CORS
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return ("", 204, headers)

    headers = {"Access-Control-Allow-Origin": "*"}

    SHARED_SECRET = os.environ.get("ADMIN_SETUP_SECRET", "")
    if not SHARED_SECRET:
        return (json.dumps({"erro": "ADMIN_SETUP_SECRET nao configurado"}), 403, headers)

    try:
        data = request.get_json(silent=True) or {}
        if data.get("secret") != SHARED_SECRET:
            return (json.dumps({"erro": "Segredo invalido"}), 401, headers)

        uid = data.get("uid")
        admin = data.get("admin", True)

        if not uid:
            return (json.dumps({"erro": "uid obrigatorio"}), 400, headers)

        # Inicializar Firebase Admin SDK
        import firebase_admin
        from firebase_admin import auth, credentials

        if not firebase_admin._apps:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {"projectId": FIREBASE_PROJECT_ID})

        # Definir custom claim
        user = auth.set_custom_user_claims(uid, {"admin": bool(admin)})
        return (json.dumps({
            "sucesso": True,
            "uid": uid,
            "admin": bool(admin),
            "mensagem": f"Custom claim 'admin={admin}' definida para {uid}. Usuario deve fazer logout/login para o token ser atualizado."
        }), 200, headers)
    except Exception as exc:
        return (json.dumps({"erro": f"Falha: {exc}"}), 500, headers)

