# PIPELINE DE RETREINAMENTO PERIODICO
# Sprint 5.20: Script para atualizar modelos com novos dados do PNCP.
#
# Uso: python scripts/retrain_pipeline.py
#
# Periodicidade sugerida: trimestral (a cada nova leva de dados do PNCP).

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PIPELINE DE RETREINAMENTO DO COPILOTO ALGORITMICO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scripts = @(
    @{Path="scripts/construir_target_real.py"; Desc="S1.1: Construir target_real observavel"},
    @{Path="scripts/train_all_models.py"; Desc="S1.2-S2: Treinar modelos + baselines + SHAP + contrafactuais"}
)

foreach ($script in $scripts) {
    Write-Host "[EXECUTANDO] $($script.Desc)..." -ForegroundColor Yellow
    $result = & python3 $script.Path 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERRO] $($script.Path) falhou com codigo $LASTEXITCODE" -ForegroundColor Red
        Write-Host $result
        exit 1
    }
    Write-Host "[OK] $($script.Path) concluido." -ForegroundColor Green
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "RETREINAMENTO CONCLUIDO COM SUCESSO" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Verifique os arquivos atualizados em:" -ForegroundColor White
Write-Host "  Tese/03-Produto-Copiloto/models/saved/" -ForegroundColor Gray
Write-Host "  dados/processed/" -ForegroundColor Gray

# Validacao pos-retreinamento
Write-Host ""
Write-Host "[VALIDACAO] Executando testes unitarios..." -ForegroundColor Yellow
$testResult = & python3 -m pytest Tese/03-Produto-Copiloto/tests/test_models.py -v --tb=short 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Todos os testes passaram." -ForegroundColor Green
} else {
    Write-Host "[AVISO] Alguns testes falharam. Verifique o log acima." -ForegroundColor Red
}
