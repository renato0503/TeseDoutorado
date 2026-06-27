# Artigo 21 - Reacao do Mercado a Fiscalizacao do TCU

## Status
- [x] Estrutura metodologica redigida (artigo_21.html)
- [x] Referencias verificadas
- [ ] Coleta de retornos Eikon
- [ ] Identificacao de acordaos do TCU (preenchimento manual)
- [ ] Calculo de CAR e contagio setorial
- [ ] Resultados empiricos

## Como executar a coleta

1. Abra o Eikon Desktop
2. Execute:
   ```powershell
   $env:EIKON_APP_KEY = "7d2c324b20fd439fa46ebefeb82dcbf5e837b5e5"
   python Scripts_Extracao/coletar_eikon.py
   ```

## Fontes para identificacao de acordaos
- Portal de jurisprudencia TCU: https://pesquisa.apps.tcu.gov.br/
- Diario Oficial da Uniao
- Midia especializada (Conjur, Valor, Jota)
