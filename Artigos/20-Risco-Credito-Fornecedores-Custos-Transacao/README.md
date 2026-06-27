# Artigo 20 - Score de Risco de Credito de Fornecedores Publicos

## Status
- [x] Estrutura metodologica redigida (artigo_20.html)
- [x] Referencias verificadas
- [ ] Coleta de dados Refinitiv CreditView
- [ ] Cruzamento CNPJ <-> RIC
- [ ] Extracao de aditivos/rescisoes do PNCP
- [ ] Resultados empiricos

## Como executar a coleta

1. Abra o Eikon Desktop
2. Execute:
   ```powershell
   $env:EIKON_APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
   python Scripts_Extracao/coletar_eikon.py
   ```

## Proximos passos
- Carregar lista de CNPJs do PNCP (Base_de_Dados_e_APIs/Raw_Data/...)
- Cruzar CNPJ <-> RIC para identificar fornecedores publicos efetivos
- Extrair dados de aditivos/rescisoes dos contratos
- Rodar regressao logistica + Cox
