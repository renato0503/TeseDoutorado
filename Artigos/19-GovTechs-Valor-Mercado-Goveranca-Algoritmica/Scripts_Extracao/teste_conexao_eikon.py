"""
Teste de conexão com Refinitiv Eikon Data API
Uso: python teste_conexao_eikon.py
"""
import os
import sys

APP_KEY = os.environ.get("EIKON_APP_KEY", "")
if not APP_KEY:
    print("ERRO: defina a variavel de ambiente EIKON_APP_KEY antes de executar.")
    print("Exemplo (PowerShell): $env:EIKON_APP_KEY = 'sua_app_key'")
    sys.exit(1)

try:
    import eikon as ek
    ek.set_app_key(APP_KEY)

    df = ek.get_timeseries(
        rics=["PETR4.SA"],
        fields="CLOSE",
        start_date="2024-01-01",
        end_date="2024-01-10",
    )
    print("Conexao OK. Amostra PETR4.SA:")
    print(df.head())
except Exception as e:
    print(f"Falha na conexao: {e}")
    sys.exit(1)
