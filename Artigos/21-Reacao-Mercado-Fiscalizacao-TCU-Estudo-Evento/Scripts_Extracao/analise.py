"""
ARTIGO 21 - Análise empírica
Reacao do Mercado a Fiscalizacao do TCU
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ART_DIR = r"C:\Users\Renato\Documents\Doutorado\Artigos\21-Reacao-Mercado-Fiscalizacao-TCU-Estudo-Evento"
RAW = os.path.join(ART_DIR, "Raw_Data")
IMG = os.path.join(ART_DIR, "imagens")
os.makedirs(IMG, exist_ok=True)


def carregar_dados():
    precos = pd.read_csv(os.path.join(RAW, "precos_fechamento.csv"), index_col=0, parse_dates=True)
    retornos = pd.read_csv(os.path.join(RAW, "retornos_diarios.csv"), index_col=0, parse_dates=True)
    return precos, retornos


def estatisticas_descritivas(retornos):
    print("=" * 70)
    print("ESTATISTICAS DESCRITIVAS DOS RETORNOS")
    print("=" * 70)
    cols_validas = [c for c in retornos.columns if retornos[c].notna().sum() >= 100]
    res = {}
    for c in cols_validas:
        s = retornos[c].dropna()
        res[c] = {
            "Media (%)": s.mean() * 100,
            "DP (%)": s.std() * 100,
            "Sharpe (anual)": (s.mean() / s.std()) * np.sqrt(252) if s.std() > 0 else 0,
            "Obs.": len(s),
        }
    desc = pd.DataFrame(res).T.round(4)
    print(desc)
    desc.to_csv(os.path.join(RAW, "estatisticas_retornos_tcu.csv"))
    return desc


def grafico_evolucao_normalizada(precos):
    fig, ax = plt.subplots(figsize=(12, 6))
    df_norm = precos / precos.iloc[0] * 100
    for col in df_norm.columns:
        if col == "^BVSP":
            ax.plot(df_norm.index, df_norm[col], label=col, linewidth=2, color="black", linestyle="--")
        else:
            ax.plot(df_norm.index, df_norm[col], label=col, linewidth=1, alpha=0.7)
    ax.set_title("Evolucao normalizada dos precos (Base 100 = 2015-01-01)", fontsize=12)
    ax.set_ylabel("Indice (Base 100)")
    ax.set_xlabel("Data")
    ax.legend(loc="best", fontsize=8, ncol=3)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "evolucao_normalizada.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: evolucao_normalizada.png")


def analise_evento_sintetico(retornos, precos):
    """
    Simula estudo de eventos: seleciona datas aleatorias
    e calcula retornos anormais em janelas curtas
    """
    print("\n" + "=" * 70)
    print("ESTUDO DE EVENTO SIMULADO (prova de conceito metodologica)")
    print("=" * 70)
    np.random.seed(42)
    if "^BVSP" not in retornos.columns:
        return

    ibov = retornos["^BVSP"]
    empresas = [c for c in retornos.columns if c != "^BVSP" and retornos[c].notna().sum() > 200]

    # Calcular beta de mercado para cada empresa (empirico)
    betas = {}
    for emp in empresas:
        df = pd.concat([retornos[emp], ibov], axis=1).dropna()
        df.columns = ["empresa", "mercado"]
        if len(df) > 50:
            cov = df["empresa"].cov(df["mercado"])
            var = df["mercado"].var()
            if var > 0:
                betas[emp] = cov / var

    # Datas de evento simuladas: seleciona N datas aleatorias
    datas_evento = np.random.choice(ibov.dropna().index[100:-100], size=10, replace=False)

    cars = []
    for data_evento in datas_evento:
        idx = ibov.index.get_loc(data_evento)
        for emp in empresas:
            if emp not in betas:
                continue
            # Janela de estimativa: 100 dias antes
            janela_est = retornos.iloc[max(0, idx-100):idx]
            if len(janela_est) < 50:
                continue
            # Retornos esperados: R*E = Rf + Beta * (Rm - Rf)
            re = janela_est[emp].mean()
            rm = janela_est["^BVSP"].mean()
            beta = betas[emp]
            # Janela de evento: [-3, +3]
            for offset in range(-3, 4):
                if idx + offset >= len(retornos):
                    continue
                ret_obs = retornos[emp].iloc[idx + offset]
                ret_esp = re + beta * (retornos["^BVSP"].iloc[idx + offset] - rm)
                ar = ret_obs - ret_esp
                cars.append({
                    "data": data_evento,
                    "empresa": emp,
                    "offset": offset,
                    "retorno_anormal": ar,
                })
    df_car = pd.DataFrame(cars)
    if df_car.empty:
        print("Dados insuficientes para estudo de evento.")
        return
    # CAR medio por offset
    car_medio = df_car.groupby("offset")["retorno_anormal"].mean() * 100
    print("\nRetorno Anormal Medio por offset (em %):")
    print(car_medio.round(4))
    car_medio.to_csv(os.path.join(RAW, "car_medio_por_offset.csv"))

    # Grafico
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(car_medio.index, car_medio.values, color=["red" if v < 0 else "green" for v in car_medio.values])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Retorno Anormal Medio em Janela de Evento [-3, +3]", fontsize=12)
    ax.set_xlabel("Dias desde o evento")
    ax.set_ylabel("Retorno Anormal Medio (%)")
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "estudo_evento_car.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: estudo_evento_car.png")


def correlacao_empresas_ibov(retornos):
    if "^BVSP" not in retornos.columns:
        return
    ibov = retornos["^BVSP"]
    empresas = [c for c in retornos.columns if c != "^BVSP" and retornos[c].notna().sum() > 100]
    cors = []
    for emp in empresas:
        df = pd.concat([retornos[emp], ibov], axis=1).dropna()
        if len(df) > 50:
            cor = df.corr().iloc[0, 1]
            cors.append({"empresa": emp, "correlacao_ibov": cor})
    df_cor = pd.DataFrame(cors).sort_values("correlacao_ibov", ascending=False)
    print("\nCorrelacao com IBOV:")
    print(df_cor.to_string(index=False))
    df_cor.to_csv(os.path.join(RAW, "correlacao_ibov.csv"))

    fig, ax = plt.subplots(figsize=(10, 5))
    cores = ["#2ecc71" if v > 0.5 else "#f39c12" if v > 0.3 else "#e74c3c" for v in df_cor["correlacao_ibov"]]
    ax.barh(df_cor["empresa"], df_cor["correlacao_ibov"], color=cores)
    ax.set_xlabel("Correlacao de Pearson com IBOVESPA")
    ax.set_title("Exposicao das Empresas ao Mercado", fontsize=12)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.grid(True, alpha=0.3, axis="x")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG, "correlacao_ibov.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("  -> Salvo: correlacao_ibov.png")


def main():
    precos, retornos = carregar_dados()
    print(f"Periodo: {precos.index[0].date()} a {precos.index[-1].date()}")
    print(f"Ativos: {precos.shape[1]}")

    estatisticas_descritivas(retornos)
    grafico_evolucao_normalizada(precos)
    correlacao_empresas_ibov(retornos)
    analise_evento_sintetico(retornos, precos)
    print("\nConcluido")


if __name__ == "__main__":
    main()
