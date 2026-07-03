# PubliCopilot

**Copiloto Algorítmico para Compras Públicas**

Plataforma de apoio à decisão para avaliação de editais e geração de cláusulas para compras públicas complexas.

## Arquitetura

```
PubliCopilot/
├── public/                 # Arquivos estáticos para Firebase Hosting
│   ├── index.html         # Landing page
│   ├── modulo_avaliacao/  # Módulo de avaliação de minutas
│   ├── modulo_geracao/    # Módulo de geração de editais
│   └── js/
│       └── firebase-init.js
├── functions/             # Cloud Functions (se necessário)
├── env/                   # Configurações Firebase (NÃO COMMITAR)
│   └── firebase-config.env
├── firestore.rules        # Regras do Firestore
├── firestore.indexes.json # Índices do Firestore
├── firebase.json          # Configuração do Firebase
└── .firebaserc           # Aponta para o projeto
```

## Configuração

### 1. Variáveis de Ambiente

As credenciais do Firebase estão em `env/firebase-config.env`.
Este arquivo está no `.gitignore` e NUNCA deve ser commitado.

### 2. Instalar Firebase CLI

```bash
npm install -g firebase-tools
firebase login
```

### 3. Deploy

```bash
cd PubliCopilot
firebase deploy
```

## Módulos

### Módulo de Avaliação
- Análise de minutas de editais
- Detecção de lacunas contratuais
- Classificação de cláusulas com NLP
- Relatório de conformidade legal

### Módulo de Geração
- Geração de cláusulas para editais
- Base de conhecimento PNCP (19.640 editais)
- Similaridade semântica
- Justificativas XAI

## Firebase (Plano Spark)

Este projeto usa apenas módulos gratuitos:

- **Hosting**: 10GB armazenamento, 360MB/dia transferência
- **Firestore**: 1GB armazenamento, 50K leituras, 20K escritas/dia

## Estrutura Firestore

```
/avaliacoes/{id}
  - textoOriginal: string
  - score: number
  - lacunas: array
  - recomendacoes: array
  - dataCriacao: timestamp
  - usuarioId: string

/editais/{id}
  - dadosEntrada: object
  - clausulasGeradas: array
  - dataCriacao: timestamp
  - usuarioId: string

/logs/{id}
  - tipo: string
  - dados: object
  - dataCriacao: timestamp
```

## URL de Produção

https://comprapublica.web.app

## Desenvolvimento Local

```bash
# Servir localmente
firebase serve

# Ou usar um servidor HTTP simples
cd public
python -m http.server 8080
```

## Segurança

- Regras de Firestore configuradas para permitir apenas operações autenticadas
- Credenciais em arquivo separado (env/)
- Logs de auditoria para todas as operações
