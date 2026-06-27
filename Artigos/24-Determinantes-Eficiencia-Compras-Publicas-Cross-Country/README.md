# Artigo 24 - Determinantes da Eficiencia em Compras Cross-Country

## Status
- [x] Estrutura metodologica redigida (artigo_24.html)
- [x] Referencias verificadas
- [ ] Coleta Refinitiv Datastream
- [ ] Download WGI do World Bank (manual)
- [ ] Download UN E-Government Index (manual)
- [ ] Preenchimento da dummy de governanca algoritmica (manual)
- [ ] Resultados empiricos

## Como executar a coleta

1. Abra o Eikon Desktop
2. Execute:
   ```powershell
   $env:EIKON_APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
   python Scripts_Extracao/coletar_eikon.py
   ```

## Fontes manuais
- World Bank WGI: https://info.worldbank.org/governance/wgi/
- UN E-Government: https://publicadministration.un.org/en/intergovernmental-support/egdi
