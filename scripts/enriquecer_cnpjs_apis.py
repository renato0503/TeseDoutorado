import pandas as pd
import requests
import time
import json
import os

COMPLEX_FILE = 'dados/processed/pncp_compras_complexas.csv'
FULL_FILE = 'dados/processed/pncp_contratos_full.csv'
OUTPUT_FORNECEDORES = 'Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/fornecedores_enriquecidos.csv'
OUTPUT_ORGAOS = 'Tese/artigos_tese/01-Artigo-Cientifico-Diagnostico/dados/orgaos_proxies.csv'

print("Carregando compras complexas...")
df_complex = pd.read_csv(COMPLEX_FILE)

# 1. FORNECEDORES (VENDEDORES) - Bater na BrasilAPI
fornecedores_cnpj = df_complex['fornecedor_cnpj'].dropna().astype(str).unique()
# Pega apenas uma amostra de 100 para fins de teste no momento (se quisermos rodar todos, demora horas)
# Vamos processar no máximo 200 para prova de conceito deste diagnóstico
fornecedores_cnpj = fornecedores_cnpj[:200] 

print(f"Buscando dados na BrasilAPI para {len(fornecedores_cnpj)} fornecedores (Amostra para prova de conceito)...")

resultados_fornecedores = []
for i, cnpj in enumerate(fornecedores_cnpj):
    # Limpa formatação do CNPJ
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj_clean) == 14:
        try:
            url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_clean}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                resultados_fornecedores.append({
                    'cnpj': cnpj_clean,
                    'razao_social': data.get('razao_social', ''),
                    'porte': data.get('porte', ''),
                    'capital_social': data.get('capital_social', 0),
                    'cnae_principal': data.get('cnae_fiscal_descricao', ''),
                    'natureza_juridica': data.get('natureza_juridica', '')
                })
            # Pausa para não estourar rate limit da API pública
            time.sleep(0.4)
            if (i+1) % 50 == 0:
                print(f"Progresso: {i+1}/{len(fornecedores_cnpj)}")
        except Exception as e:
            pass

df_fornecedores = pd.DataFrame(resultados_fornecedores)
os.makedirs(os.path.dirname(OUTPUT_FORNECEDORES), exist_ok=True)
df_fornecedores.to_csv(OUTPUT_FORNECEDORES, index=False)
print(f"Fornecedores enriquecidos salvos em: {OUTPUT_FORNECEDORES}")


# 2. ÓRGÃOS COMPRADORES - Criar proxies internamente a partir da população de 572k
print("\nGerando proxies de Porte para os Órgãos Compradores...")
# Não temos o CNPJ do órgão, então vamos usar a população total para calcular:
# - Orçamento Total (soma do valor global transacionado em todos os contratos do PNCP)
# - Número de contratos fechados
# - Média de valor por contrato

print("Carregando banco full...")
df_full = pd.read_csv(FULL_FILE)

# Órgãos que fizeram compras complexas
orgaos_alvo = df_complex['orgao'].dropna().unique()

print(f"Calculando proxies de orçamento para {len(orgaos_alvo)} órgãos...")
# Filtra o dataset total para os órgãos que nos interessam e agrega
df_full_alvo = df_full[df_full['orgao'].isin(orgaos_alvo)]
orgaos_stats = df_full_alvo.groupby('orgao').agg(
    orcamento_proxy_pncp=('valor_global', 'sum'),
    total_contratos_pncp=('valor_global', 'count'),
    media_valor_contrato=('valor_global', 'mean')
).reset_index()

orgaos_stats.to_csv(OUTPUT_ORGAOS, index=False)
print(f"Proxies dos órgãos salvas em: {OUTPUT_ORGAOS}")
print("Processo concluído!")
