"""
limpar_modelos.py — Remove arquivos .pkl duplicados/redundantes do PubliCopilot.

Estrategia: manter apenas arquivos REFERENCIADOS pelo codigo em producao
(main.py, model_loader.py, risk_engine.py, xai_explainer.py).

Arquivos a MANTER (11 total):
  - random_forest.pkl
  - isolation_forest.pkl
  - tfidf_vectorizer.pkl
  - scaler.pkl
  - shap_explainer.pkl
  - shap_background.pkl
  - metricas.json
  - feature_columns.pkl          (necessario p/ listar colunas do RF)
  - label_encoder_uf.pkl         (necessario p/ encoding UF)
  - label_encoder_tipo.pkl       (necessario p/ encoding tipo contrato)
  - counterfactual_templates.json (necessario p/ explicacoes XAI)

Arquivos a DELETAR (4 total — espurios/duplicados):
  - random_forest_sem_vigencia.pkl     (12,4 MB) - modelo antigo nao usado
  - scaler_sem_vigencia.pkl            (0,9 KB)  - scaler redundante
  - feature_columns_sem_vigencia.pkl   (0,2 KB)  - lista de colunas antiga
  - shap_values_sample.pkl             (51,7 KB) - sample nao usado em runtime

Economia estimada: ~12,5 MB (reducao de 30% no tamanho do package de deploy).

Uso:
    python limpar_modelos.py            # dry-run (mostra o que faria)
    python limpar_modelos.py --aplicar  # executa a limpeza de fato
"""

import os
import sys
from pathlib import Path

SAVED_DIR = Path(r"C:\Users\Renato\Documents\Doutorado\PubliCopilot\functions\models\saved")

# Lista de arquivos ESSENCIAIS (referenciados pelo codigo em runtime)
KEEP = {
    "random_forest.pkl",
    "isolation_forest.pkl",
    "tfidf_vectorizer.pkl",
    "scaler.pkl",
    "shap_explainer.pkl",
    "shap_background.pkl",
    "metricas.json",
    "feature_columns.pkl",          # usado por get_feature_columns()
    "label_encoder_uf.pkl",         # usado por get_label_encoder_uf()
    "label_encoder_tipo.pkl",       # usado por get_label_encoder_tipo()
    "counterfactual_templates.json",  # usado por xai_explainer.py
}

# Lista de arquivos a DELETAR (espurios/duplicados)
DELETE = {
    "random_forest_sem_vigencia.pkl",
    "scaler_sem_vigencia.pkl",
    "feature_columns_sem_vigencia.pkl",
    "shap_values_sample.pkl",
}

def main():
    aplicar = "--aplicar" in sys.argv
    modo = "EXECUCAO REAL" if aplicar else "DRY-RUN (use --aplicar para executar)"

    print("=" * 60)
    print(f"LIMPEZA DE MODELOS DUPLICADOS — {modo}")
    print("=" * 60)
    print(f"Diretorio: {SAVED_DIR}")
    print()

    if not SAVED_DIR.exists():
        print(f"ERRO: Diretorio nao encontrado: {SAVED_DIR}")
        sys.exit(1)

    # Listar arquivos atuais
    all_files = sorted([f.name for f in SAVED_DIR.iterdir() if f.is_file()])

    print(f"Total de arquivos atuais: {len(all_files)}")
    for f in all_files:
        marker = "[MANTER]" if f in KEEP else ("[DELETAR]" if f in DELETE else "[?]")
        size_kb = (SAVED_DIR / f).stat().st_size / 1024
        print(f"  {marker:<10} {f:<45} ({size_kb:>8.1f} KB)")

    # Calcular economia
    economia_bytes = sum((SAVED_DIR / f).stat().st_size for f in DELETE if (SAVED_DIR / f).exists())
    economia_kb = economia_bytes / 1024
    economia_mb = economia_kb / 1024

    print()
    print(f"Arquivos a deletar: {len(DELETE)}")
    print(f"Espaco a liberar:   {economia_mb:.2f} MB ({economia_kb:.1f} KB)")

    if not aplicar:
        print()
        print("[DRY-RUN] Nenhuma alteracao foi feita.")
        print("Para executar a limpeza de fato, rode: python limpar_modelos.py --aplicar")
        return

    # Execucao real
    print()
    print("Executando limpeza...")
    deletados = 0
    erros = 0
    for filename in DELETE:
        filepath = SAVED_DIR / filename
        if not filepath.exists():
            print(f"  [SKIP] {filename} (nao existe)")
            continue
        try:
            size_mb = filepath.stat().st_size / (1024 * 1024)
            filepath.unlink()
            print(f"  [OK]   {filename} deletado ({size_mb:.2f} MB liberados)")
            deletados += 1
        except Exception as e:
            print(f"  [ERRO] {filename}: {e}")
            erros += 1

    print()
    print("=" * 60)
    print(f"Limpeza concluida: {deletados} deletados, {erros} erros")
    print(f"Espaco liberado: {economia_mb:.2f} MB")
    print("=" * 60)
    print()
    print("Proximos passos:")
    print("  1. cd C:\\Users\\Renato\\Documents\\Doutorado\\PubliCopilot")
    print("  2. firebase deploy --only functions --project publicopilot")
    print("  3. Validar que a Cloud Function carrega modelos corretamente")

if __name__ == "__main__":
    main()
