import os
import sys
import calendar
from datetime import datetime, timedelta
from extrator_contratacoes import extrair as extrair_contratacoes
from extrator_contratos import extrair as extrair_contratos

# Força o flush dos prints para podermos acompanhar no log em tempo real
sys.stdout.reconfigure(line_buffering=True)

DIR_DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "dados", "pncp_raw")

def gerar_meses(ano_inicio, mes_inicio, ano_fim, mes_fim):
    """Gera pares de datas de início e fim para cada mês no intervalo."""
    atual_ano, atual_mes = ano_inicio, mes_inicio
    meses = []
    
    while (atual_ano < ano_fim) or (atual_ano == ano_fim and atual_mes <= mes_fim):
        _, ultimo_dia = calendar.monthrange(atual_ano, atual_mes)
        data_inicial = f"{atual_ano}{atual_mes:02d}01"
        data_final = f"{atual_ano}{atual_mes:02d}{ultimo_dia}"
        
        meses.append((data_inicial, data_final))
        
        atual_mes += 1
        if atual_mes > 12:
            atual_mes = 1
            atual_ano += 1
            
    return meses

def orquestrar(ano_inicio=2021, mes_inicio=1, ano_fim=2024, mes_fim=12):
    meses = gerar_meses(ano_inicio, mes_inicio, ano_fim, mes_fim)
    
    for (inicio, fim) in meses:
        print(f"\n=======================================================")
        print(f"--- Iniciando coleta para o período: {inicio} a {fim} ---")
        print(f"=======================================================\n")
        
        # 1. Contratações
        print(f"[{inicio}-{fim}] Coletando Contratações...")
        try:
            extrair_contratacoes(inicio, fim, DIR_DADOS)
        except Exception as e:
            print(f"Erro ao extrair contratações para {inicio}-{fim}: {e}")
        
        # 2. Contratos
        print(f"[{inicio}-{fim}] Coletando Contratos...")
        try:
            extrair_contratos(inicio, fim, DIR_DADOS)
        except Exception as e:
            print(f"Erro ao extrair contratos para {inicio}-{fim}: {e}")
            
    print("\nOrquestração finalizada! Todos os dados de 2021 a 2024 foram baixados.")

if __name__ == "__main__":
    # Inicia a extração oficial (2021 a 2024 completo)
    orquestrar(ano_inicio=2021, mes_inicio=1, ano_fim=2024, mes_fim=12)
