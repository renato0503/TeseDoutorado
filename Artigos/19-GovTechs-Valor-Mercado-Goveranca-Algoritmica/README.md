# Artigo 19 - GovTechs e Valor de Mercado

## Status
- [x] Estrutura metodologica redigida (artigo_19.html)
- [x] Referencias verificadas
- [ ] Coleta de dados Refinitiv Eikon (requer Eikon Desktop rodando)
- [ ] Identificacao de eventos de certificacao (preenchimento manual)
- [ ] Resultados empiricos

## Como executar a coleta

1. Abra o Eikon Desktop na sua maquina
2. Em outro terminal:
   ```powershell
   $env:EIKON_APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
   python Scripts_Extracao/coletar_eikon.py
   ```
3. Verifique os CSVs em `Raw_Data/`

## Proximos passos
- Cruzar lista de empresas com receita publica > 5% (usar formularios de referencia B3)
- Buscar eventos de certificacao em comunicados ao mercado e na midia especializada
- Rodar estudo de eventos (CAR) e regressao em painel
