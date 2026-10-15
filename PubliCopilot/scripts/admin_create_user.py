# -*- coding: utf-8 -*-
"""
admin_create_user.py — Provisionamento manual de usuários para a fase de testes
do PubliCopilot com SESP, Politec, TJPR e TJRN.

Uso individual:
    python admin_create_user.py ^
        --email maria.silva@sesp.mt.gov.br ^
        --nome "Maria Silva" ^
        --orgao SESP-MT ^
        --perfil pregoeiro ^
        --whatsapp "(65) 99999-0001"

Uso em lote (via JSON):
    python admin_create_user.py --arquivo usuarios_teste.json

O script usa o Firebase Admin SDK e exige credenciais com privilégios elevados:
- Opção A (recomendada): defina a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS
  apontando para o JSON da service account do projeto publicopilot.
- Opção B: passe --credentials /caminho/para/serviceAccount.json

Saída:
    Para cada usuário criado, imprime um bloco com:
        - email
        - senha temporária (exibida UMA VEZ — guarde agora)
        - UID no Firebase Auth
        - orgaoId associado

Segurança:
    - As senhas temporárias são gravadas também em `usuarios/{uid}.senhaTemporariaHash`
      (NUNCA a senha em texto puro) e o usuário é forçado a redefinir no primeiro
      acesso via flag `primeiroAcesso: true`.
    - Cada usuário recebe automaticamente o claim `orgaoId` (custom claim) que pode
      ser usado em regras do Firestore para isolamento por órgão.

Orgaos pré-configurados:
    SESP-MT, POLITEC-MT, TJPR, TJRN
"""

import argparse
import json
import os
import random
import string
import sys
from datetime import datetime, timezone

try:
    import firebase_admin
    from firebase_admin import auth, credentials, firestore
except ImportError:
    print("ERRO: firebase-admin nao instalado. Rode: pip install firebase-admin", file=sys.stderr)
    sys.exit(1)


ORGAOS = {
    "SESP-MT": {
        "nome": "Secretaria de Estado de Seguranca Publica de Mato Grosso",
        "sigla": "SESP-MT",
        "estado": "MT",
        "contato_email": "compras@sesp.mt.gov.br",
        "ativo": True,
    },
    "POLITEC-MT": {
        "nome": "Pericia Oficial e Identificacao Tecnica do Estado de Mato Grosso",
        "sigla": "POLITEC-MT",
        "estado": "MT",
        "contato_email": "licitacao@politec.mt.gov.br",
        "ativo": True,
    },
    "TJPR": {
        "nome": "Tribunal de Justica do Estado do Parana",
        "sigla": "TJPR",
        "estado": "PR",
        "contato_email": "copel@tjpr.jus.br",
        "ativo": True,
    },
    "TJRN": {
        "nome": "Tribunal de Justica do Estado do Rio Grande do Norte",
        "sigla": "TJRN",
        "estado": "RN",
        "contato_email": "compras@tjrn.jus.br",
        "ativo": True,
    },
}


PERFIS_VALIDOS = {"servidor", "pregoeiro", "gestor", "agente_compras",
                  "assessor_juridico", "autoridade_competente",
                  "pesquisador", "fornecedor", "cidadao", "outro"}


def _init_firebase(credentials_path=None):
    """Inicializa o SDK Admin com credenciais."""
    if firebase_admin._apps:
        return

    if credentials_path:
        cred = credentials.Certificate(credentials_path)
    else:
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred, {"projectId": "publicopilot"})


def _gerar_senha_temporaria(tamanho=14):
    """Gera senha aleatória que atende às regras do frontend (>=8, 1 maiusc, 1 min, 1 num)."""
    if tamanho < 8:
        tamanho = 8
    alfabeto_minusculo = string.ascii_lowercase
    alfabeto_maiusculo = string.ascii_uppercase
    digitos = string.digits

    senha = [
        random.choice(alfabeto_maiusculo),
        random.choice(alfabeto_minusculo),
        random.choice(digitos),
    ]
    restante = tamanho - len(senha)
    pool_completo = alfabeto_maiusculo + alfabeto_minusculo + digitos + "!@#$%&*"
    for _ in range(restante):
        senha.append(random.choice(pool_completo))
    random.shuffle(senha)
    return "".join(senha)


def _garantir_orgaos(db):
    """Cria/atualiza docs da coleção orgaos/ para os 4 orgaos de teste.

    Idempotente: se ja existir, nao sobrescreve. Use --force-orgaos se quiser.
    """
    orgaos_ref = db.collection("orgaos")
    criadas = 0
    atualizadas = 0
    for orgao_id, orgao_meta in ORGAOS.items():
        doc_ref = orgaos_ref.document(orgao_id)
        snap = doc_ref.get()
        payload = {
            **orgao_meta,
            "orgaoId": orgao_id,
            "atualizadoEm": firestore.SERVER_TIMESTAMP,
        }
        if snap.exists:
            doc_ref.set(payload, merge=True)
            atualizadas += 1
        else:
            payload["criadoEm"] = firestore.SERVER_TIMESTAMP
            doc_ref.set(payload)
            criadas += 1
    print(f"[orgaos] {criadas} criados, {atualizadas} atualizados. Total configurados: {len(ORGAOS)}")


def _criar_ou_atualizar_usuario(db, args, senha_temp):
    """Cria usuario no Firebase Auth + doc Firestore.

    Estrategia:
        1. create_user() (ou get_user_by_email se ja existe).
        2. set_custom_user_claims({orgaoId, perfil, admin:False}).
        3. set/update doc usuarios/{uid}.
        4. Retorna (uid, novo_flag).
    """
    user_record = None
    ja_existia = False
    try:
        user_record = auth.get_user_by_email(args.email)
        ja_existia = True
        print(f"  [auth] Usuario ja existia (uid={user_record.uid}). Atualizando claims/doc.")
    except auth.UserNotFoundError:
        user_record = auth.create_user(
            email=args.email,
            password=senha_temp,
            display_name=args.nome,
            phone_number=None,
            email_verified=False,
            disabled=False,
        )
        print(f"  [auth] Criado (uid={user_record.uid}).")

    if not args.preserve_claims:
        claims = {
            "orgaoId": args.orgao,
            "perfil": args.perfil,
            "admin": False,
            "senhaTemporaria": True,
            "cadastradoPorAdmin": True,
        }
        auth.set_custom_user_claims(user_record.uid, claims)
        print(f"  [claims] Definidas: orgaoId={args.orgao}, perfil={args.perfil}, senhaTemporaria=True.")

    usuario_doc = {
        "nome": args.nome,
        "email": args.email,
        "whatsapp": args.whatsapp or "",
        "instituicao": ORGAOS.get(args.orgao, {}).get("nome", ""),
        "orgaoId": args.orgao,
        "orgaoNome": ORGAOS.get(args.orgao, {}).get("nome", ""),
        "perfil": args.perfil,
        "papel": "usuario",
        "ativo": True,
        "totalAnalises": 0,
        "totalGeracoes": 0,
        "provedor": "password",
        "dataCriacao": firestore.SERVER_TIMESTAMP,
        "dataAtualizacao": firestore.SERVER_TIMESTAMP,
        "ultimoAcesso": None,
        "primeiroAcesso": True,
        "cadastradoPorAdmin": True,
        "senhaTemporaria": True,
    }

    usuarios_ref = db.collection("usuarios").document(user_record.uid)
    existing = usuarios_ref.get()
    if existing.exists and args.preserve_doc:
        print(f"  [firestore] Doc ja existia. Mantido (use --overwrite-doc para sobrescrever campos gerenciais).")
    else:
        usuarios_ref.set(usuario_doc, merge=(existing.exists and args.preserve_doc))
        acao = "Atualizado" if existing.exists else "Criado"
        print(f"  [firestore] {acao} doc usuarios/{user_record.uid}.")

    return user_record.uid, ja_existia


def _processar_um(db, args):
    senha_temp = args.senha if args.senha else _gerar_senha_temporaria()
    uid, ja_existia = _criar_ou_atualizar_usuario(db, args, senha_temp)

    print("")
    print("=" * 72)
    print(f"  USUARIO PROCESSADO")
    print("=" * 72)
    print(f"  Email        : {args.email}")
    print(f"  Nome         : {args.nome}")
    print(f"  Orgao        : {args.orgao} ({ORGAOS[args.orgao]['nome']})")
    print(f"  Perfil       : {args.perfil}")
    print(f"  WhatsApp     : {args.whatsapp or '(nao informado)'}")
    print(f"  UID          : {uid}")
    print(f"  Ja existia   : {'Sim' if ja_existia else 'Nao (novo)'}")
    print(f"  Senha temp.  : {senha_temp if not ja_existia else '(manter senha anterior; usuario ja existia)'}")
    print("=" * 72)
    if not ja_existia and not args.senha:
        print(f"  >> ANOTE A SENHA TEMPORARIA ACIMA. Ela NAO sera exibida novamente. <<")
    print("")
    return uid


def _processar_arquivo(db, arquivo):
    """Processa varios usuarios a partir de um JSON."""
    with open(arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    if not isinstance(dados, list):
        dados = [dados]

    sucessos = 0
    falhas = 0
    for i, item in enumerate(dados, 1):
        try:
            from_args = argparse.Namespace(**item)
            _processar_um(db, from_args)
            sucessos += 1
        except KeyError as e:
            print(f"[ERRO item {i}] Campo obrigatorio faltando: {e}", file=sys.stderr)
            falhas += 1
        except Exception as e:
            print(f"[ERRO item {i}] {type(e).__name__}: {e}", file=sys.stderr)
            falhas += 1

    print(f"\n[resumo] {sucessos} processados com sucesso, {falhas} falhas.")
    sys.exit(0 if falhas == 0 else 1)


def _validar_args(args):
    if args.modo != "arquivo" and not args.orgao:
        print("ERRO: --orgao obrigatorio (SESP-MT | POLITEC-MT | TJPR | TJRN).", file=sys.stderr)
        sys.exit(2)
    if args.modo != "arquivo" and args.orgao not in ORGAOS:
        print(f"ERRO: orgao '{args.orgao}' nao reconhecido. Validos: {list(ORGAOS.keys())}", file=sys.stderr)
        sys.exit(2)
    if args.modo != "arquivo" and not args.email:
        print("ERRO: --email obrigatorio.", file=sys.stderr)
        sys.exit(2)
    if args.modo != "arquivo" and not args.nome:
        print("ERRO: --nome obrigatorio.", file=sys.stderr)
        sys.exit(2)
    if args.modo != "arquivo" and args.perfil not in PERFIS_VALIDOS:
        print(f"ERRO: perfil '{args.perfil}' invalido. Validos: {sorted(PERFIS_VALIDOS)}", file=sys.stderr)
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description="Provisiona usuarios manualmente para a fase de testes multi-orgao.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    sub = parser.add_mutually_exclusive_group(required=True)
    sub.add_argument("--modo", choices=["unico", "arquivo", "seed-orgaos"],
                     help="unico = cria 1 usuario; arquivo = batch via JSON; seed-orgaos = so cria os 4 orgaos.")
    sub.add_argument("--arquivo", help="Caminho para JSON com lista de usuarios (modo=arquivo).")

    parser.add_argument("--email", help="Email do usuario.")
    parser.add_argument("--nome", help="Nome completo.")
    parser.add_argument("--orgao", choices=list(ORGAOS.keys()),
                        help="Orgao (SESP-MT | POLITEC-MT | TJPR | TJRN).")
    parser.add_argument("--perfil", choices=sorted(PERFIS_VALIDOS), default="servidor",
                        help="Peril/role do servidor.")
    parser.add_argument("--whatsapp", default="",
                        help="WhatsApp com DDD (opcional).")
    parser.add_argument("--senha", default="",
                        help="Senha fixa (opcional). Se omitido, gera aleatoria.")

    parser.add_argument("--credentials", default=None,
                        help="Caminho para JSON da service account (ou use GOOGLE_APPLICATION_CREDENTIALS).")

    parser.add_argument("--preserve-claims", action="store_true",
                        help="Nao sobrescreve custom claims (cuidado: pode deixar claims inconsistentes).")
    parser.add_argument("--preserve-doc", action="store_true",
                        help="Nao sobrescreve campos do doc Firestore se ja existir.")

    args = parser.parse_args()

    _validar_args(args)

    _init_firebase(args.credentials)
    db = firestore.client()

    if args.modo == "seed-orgaos":
        _garantir_orgaos(db)
        sys.exit(0)
    elif args.modo == "arquivo":
        _processar_arquivo(db, args.arquivo)
    else:
        _garantir_orgaos(db)
        _processar_um(db, args)


if __name__ == "__main__":
    main()
