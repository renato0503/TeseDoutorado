# Artigo 22 - Estrutura de Capital e Oligopolio em Compras de TI

## Status
- [x] Estrutura metodologica redigida (artigo_22.html)
- [x] Referencias verificadas
- [ ] Coleta de dados financeiros (Eikon)
- [ ] Calculo de HHI por subsetor
- [ ] Cruzamento com dados do PNCP
- [ ] Resultados empiricos

## Como executar a coleta

1. Abra o Eikon Desktop
2. Execute:
   ```powershell
   $env:EIKON_APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
   python Scripts_Extracao/coletar_eikon.py
   ```
