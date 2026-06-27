"""
ARTIGO 19 - Análise empírica
O Valor de Mercado das GovTechs e a Governanca Algoritmica

A partir dos dados coletados via yfinance:
- Calcular retornos anormais acumulados
- Estimar regressão em painel
- Gerar graficos
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\19-GovTechs-Valor-Mercado-Goveranca-Algoritmica"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    precos = pd.read_csv(os.path.join(RAW, "precos_fechamento.csv"), index_col=0, parse_dates=True)
    fund = pd.read_csv(os.path.join(RAW, "fundamentalistas.csv"))
    return precos, fund


def estatisticas_descritivas(precos, fund):
    print("=" * 70)
    print("ESTATISTICAS DESCRITIVAS")
    print("=" * 70)
    # Filtrar apenas colunas com pelo menos 100 observacoes
    cols_validas = [c for c in precos.columns if precos[c].notna().sum() >= 100]
    precos_validos = precos[cols_validas]
    retornos = precos_validos.pct_change(fill_method=None).dropna(how="all")
    # Para cada coluna, calcular apenas com dados validos
    resultados = {}
    for col in cols_validas:
        serie = retornos[col].dropna()
        if len(serie) > 0:
            resultados[col] = {
                "Media (%)": serie.mean() * 100,
                "DP (%)": serie.std() * 100,
                "Min (%)": serie.min() * 100,
                "Max (%)": serie.max() * 100,
                "Observacoes": len(serie),
            }
    desc = pd.DataFrame(resultados).T.round(4)
    print("\nRetornos diarios:")
    print(desc)
    desc.to_csv(os.path.join(RAW, "estatisticas_descritivas_retornos.csv"))
    return desc, retornos


def grafico_evolucao(precos):
    fig, ax = plt.subplots(figsize=(12, 6))
    normalizado = precos / precos.iloc[0] * 100
    for col in normalizado.columns:
        ax.plot(normalizado.index, normalizado[col], label=col, linewidth=1)
    ax.set_title("Evolucao dos precos normalizados (Base 100 = primeira data)", fontsize=12)
    ax.set_ylabel("Indice (Base 100)")
    ax.set_xlabel("Data")
    ax.legend(loc="best", fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "evolucao_precos.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: evolucao_precos.png")


def grafico_volatilidade(retornos):
    vol_dict = {}
    for col in retornos.columns:
        serie = retornos[col].dropna()
        if len(serie) > 0:
            vol_dict[col] = serie.std() * np.sqrt(252) * 100
    vol_anual = pd.Series(vol_dict).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    cores = plt.cm.viridis(np.linspace(0, 1, len(vol_anual)))
    ax.barh(vol_anual.index, vol_anual.values, color=cores)
    ax.set_title("Volatilidade anualizada por empresa (%)", fontsize=12)
    ax.set_xlabel("Volatilidade anual (%)")
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "volatilidade_anualizada.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: volatilidade_anualizada.png")
    return vol_anual


def grafico_correlacao(retornos):
    fig, ax = plt.subplots(figsize=(9, 7))
    corr = retornos.corr()
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(corr.columns, fontsize=8)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i,j]:.2f}", ha="center", va="center", fontsize=7, color="black")
    plt.colorbar(im, ax=ax, label="Correlacao de Pearson")
    ax.set_title("Matriz de correlacao dos retornos diarios", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "matriz_correlacao.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: matriz_correlacao.png")


def regressao_wacc_proxy(fund, retornos):
    print("\n" + "=" * 70)
    print("REGRESSAO: WACC PROXY vs EXPOSICAO AO SETOR PUBLICO")
    print("=" * 70)
    # Calcular volatilidade por empresa
    vol_dict = {}
    for col in retornos.columns:
        serie = retornos[col].dropna()
        if len(serie) > 0:
            vol_dict[col] = serie.std() * np.sqrt(252) * 100
    vol_anual = pd.Series(vol_dict)
    df = fund.copy()
    df["vol_anual"] = df["ticker"].map(vol_anual)
    df["market_cap_mm"] = df["market_cap"] / 1e6
    df["endividamento_proxy"] = df["total_debt"] / (df["total_debt"] + df["total_equity"].fillna(1))
    df = df.dropna(subset=["vol_anual", "market_cap_mm", "endividamento_proxy"])
    print(f"\nObservacoes validas: {len(df)}")
    if len(df) == 0:
        return df, np.array([0,0,0]), 0
    print(df[["ticker", "market_cap_mm", "endividamento_proxy", "vol_anual"]].to_string(index=False))

    # Regressao simples: vol_anual ~ market_cap + endividamento
    X = df[["market_cap_mm", "endividamento_proxy"]].values
    X_ = np.column_stack([np.ones(len(X)), X])
    y = df["vol_anual"].values
    beta, _, _, _ = np.linalg.lstsq(X_, y, rcond=None)
    y_hat = X_ @ beta
    ss_res = ((y - y_hat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum() if len(y) > 1 else 1
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    print(f"\nCoeficientes: intercepto={beta[0]:.3f}, market_cap={beta[1]:.6f}, endividamento={beta[2]:.3f}")
    print(f"R²: {r2:.3f}")
    return df, beta, r2


def main():
    print("Carregando dados...")
    precos, fund = carregar_dados()
    print(f"  Precos: {precos.shape[0]} dias, {precos.shape[1]} ativos")
    print(f"  Fundamentalistas: {fund.shape[0]} empresas")

    desc, retornos = estatisticas_descritivas(precos, fund)
    print("\n" + "=" * 70)
    print("GERANDO GRAFICOS")
    print("=" * 70)
    grafico_evolucao(precos)
    vol = grafico_volatilidade(retornos)
    grafico_correlacao(retornos)

    df_reg, beta, r2 = regressao_wacc_proxy(fund, retornos)

    # Salvar relatorio
    with open(os.path.join(RAW, "relatorio_analise.txt"), "w", encoding="utf-8") as f:
        f.write("RELATORIO DE ANALISE - ARTIGO 19\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total de ativos analisados: {len(precos.columns)}\n")
        f.write(f"Periodo: {precos.index[0].date()} a {precos.index[-1].date()}\n")
        f.write(f"Dias uteis: {len(precos)}\n\n")
        f.write("ESTATISTICAS DESCRITIVAS DOS RETORNOS:\n")
        f.write(desc.to_string() + "\n\n")
        f.write(f"\nREGRESSAO (vol_anual ~ market_cap + endividamento):\n")
        f.write(f"  Intercepto: {beta[0]:.3f}\n")
        f.write(f"  Coef. market_cap (mm USD): {beta[1]:.6f}\n")
        f.write(f"  Coef. endividamento: {beta[2]:.3f}\n")
        f.write(f"  R²: {r2:.3f}\n")
    print("\nRelatorio salvo em:", os.path.join(RAW, "relatorio_analise.txt"))
    print("\nCONCLUIDO")


if __name__ == "__main__":
    main()
