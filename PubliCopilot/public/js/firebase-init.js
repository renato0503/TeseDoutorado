// PubliCopilot Firebase Integration
// ATENCAO: Credenciais sao carregadas via env (nao commitadas)

const ENV = {
  apiKey: "__FIREBASE_API_KEY__",
  authDomain: "publicopilot.firebaseapp.com",
  projectId: "publicopilot",
  storageBucket: "publicopilot.firebasestorage.app",
  messagingSenderId: "432118179013",
  appId: "1:432118179013:web:752294d08f504e1d2fbcac",
  measurementId: "G-Y2Q8770D9E"
};

// Inicializacao do Firebase (singleton)
let app, db, auth_instance;
let firebaseReady = false;
const firebaseReadyCallbacks = [];
let _initPromise = null;

function whenFirebaseReady() {
  return new Promise((resolve) => {
    if (firebaseReady) {
      resolve();
    } else {
      firebaseReadyCallbacks.push(resolve);
    }
  });
}

function initializeFirebase() {
  if (typeof firebase === 'undefined') {
    console.error('Firebase SDK nao carregado');
    return false;
  }

  // Singleton: so inicializa uma vez
  if (firebase.apps && firebase.apps.length > 0) {
    app = firebase.apps[0];
  } else {
    try {
      app = firebase.initializeApp(ENV);
    } catch (e) {
      console.error('Erro ao inicializar Firebase:', e);
      return false;
    }
  }

  try {
    db = firebase.firestore();
    auth_instance = firebase.auth();

    // Analytics e opcional e pode nao estar disponivel
    if (ENV.measurementId && typeof firebase.analytics === 'function' && window.location.hostname !== 'localhost') {
      try {
        firebase.analytics(app);
      } catch (e) {
        console.warn('Analytics nao disponivel (ignorado)');
      }
    }

    firebaseReady = true;

    // Resolver callbacks pendentes
    const cbs = firebaseReadyCallbacks.slice();
    firebaseReadyCallbacks.length = 0;
    cbs.forEach(cb => cb());

    // Expor helper global
    window.whenFirebaseReady = whenFirebaseReady;

    console.log('Firebase inicializado com sucesso');
    return true;
  } catch (e) {
    console.error('Erro ao inicializar Firebase:', e);
    return false;
  }
}

// =============================================================================
// PERSISTENCIA DE NEGOCIO
// =============================================================================

// Salvar analise no Firestore (colecao analises/{uid}/historico)
async function salvarAnalise(uid, dados) {
  if (!db) {
    console.warn('Firestore nao disponivel');
    return null;
  }
  try {
    const docRef = await db.collection('analises').doc(uid).collection('historico').add({
      ...dados,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp()
    });
    console.log('Analise salva:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('Erro ao salvar analise:', error);
    return null;
  }
}

// Salvar edital gerado no Firestore (colecao editais/)
// Agora com metadados de orgao/origem para a fase de testes multi-orgao.
async function salvarGeracao(dados) {
  if (!db) {
    console.warn('Firestore nao disponivel');
    return null;
  }
  try {
    const usuario = firebase.auth().currentUser;
    let orgaoId = null;
    let orgaoNome = null;
    if (usuario) {
      try {
        const token = await usuario.getIdTokenResult();
        orgaoId = (token.claims && token.claims.orgaoId) || null;
      } catch (e) { /* ignora */ }
      try {
        const doc = await db.collection('usuarios').doc(usuario.uid).get();
        if (doc.exists) {
          const dd = doc.data() || {};
          orgaoId = orgaoId || dd.orgaoId || null;
          orgaoNome = dd.orgaoNome || null;
        }
      } catch (e) { /* ignora */ }
    }
    const docRef = await db.collection('editais').add({
      ...dados,
      orgaoId,
      orgaoNome,
      usuarioId: usuario ? usuario.uid : null,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp()
    });
    console.log('Edital salvo:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('Erro ao salvar edital:', error);
    return null;
  }
}

// Salvar edital gerado no Firestore (legacy alias para salvarGeracao)
async function salvarEdital(dados) {
  return salvarGeracao(dados);
}

// =============================================================================
// AUDIT LOG (telemetria completa para a fase de testes)
// =============================================================================

// Tipos validos de evento (nao bloqueante: tipos desconhecidos sao aceitos)
const TIPOS_EVENTO_VALIDOS = new Set([
  // Auth
  'login_sucesso', 'login_erro', 'login_anonimo',
  'logout', 'cadastro_sucesso', 'cadastro_erro',
  'perfil_atualizado', 'primeiro_acesso',
  // Navegacao
  'page_view',
  // Avaliacao
  'avaliar_click', 'avaliar_inicio', 'avaliar_sucesso', 'avaliar_erro',
  'exemplo_selecionado',
  // Geracao
  'gerar_click', 'gerar_inicio', 'gerar_sucesso', 'gerar_erro',
  'carregar_exemplo',
  // Sistema
  'erro_js', 'api_timeout',
]);

/**
 * Registra um evento de telemetria na colecao `logs/`.
 *
 * @param {string} tipo  - Nome do evento (ver TIPOS_EVENTO_VALIDOS).
 * @param {object} dados - Campos extras a anexar. NAO inclua PII sensivel
 *                         (cpf, senha, etc.). O uid/email sao auto-anexados.
 *
 * @returns {Promise<void>}
 *
 * Nunca lanca excecao — telemetria eh best-effort e nao pode quebrar a app.
 */
async function registrarEvento(tipo, dados = {}) {
  if (!db || !tipo) return;
  if (!TIPOS_EVENTO_VALIDOS.has(tipo)) {
    // Em dev, avisa. Em prod, segue silenciosamente para nao gerar ruido.
    if (window.console && window.console.warn) {
      console.warn('[registrarEvento] tipo nao canonico:', tipo);
    }
  }
  try {
    const usuario = firebase.auth().currentUser;
    let orgaoId = null;
    let claims = null;
    if (usuario) {
      try {
        const tokenResult = await usuario.getIdTokenResult(false);
        claims = tokenResult.claims || {};
        orgaoId = claims.orgaoId || null;
      } catch (e) { /* segue sem claims */ }
    }
    const payload = {
      tipo,
      uid: usuario ? usuario.uid : null,
      email: usuario ? usuario.email : null,
      orgaoId,
      claims,
      path: window.location.pathname,
      query: window.location.search || '',
      referrer: document.referrer || '',
      userAgent: navigator.userAgent,
      tsLocal: new Date().toISOString(),
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
      ...sanitizeForLog(dados),
    };
    // Limpa campos que nao devem ir ao log
    if (payload.claims && payload.claims.admin === undefined) {
      // claims sem admin -> ok, so para reduzir tamanho
    }
    delete payload.senha;
    delete payload.password;
    delete payload.senhaTemp;
    delete payload.captcha;
    // Trunca payloads muito grandes para evitar 1MB doc-limit
    const str = JSON.stringify(payload);
    if (str.length > 900_000) {
      payload.userAgent = '[truncado]';
      payload.referrer = '[truncado]';
    }
    await db.collection('logs').add(payload);
  } catch (error) {
    console.error('[registrarEvento] erro:', error, { tipo });
  }
}

/**
 * Remove campos sensiveis/circulares antes de enviar para o log.
 */
function sanitizeForLog(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  const safe = {};
  const BLOCK = new Set(['senha', 'password', 'senhaTemp', 'token', 'idToken',
                         'captcha', 'authorization', 'cookie']);
  for (const k of Object.keys(obj)) {
    if (BLOCK.has(k.toLowerCase())) {
      safe[k] = '[REDACTED]';
    } else if (typeof obj[k] === 'object' && obj[k] !== null && !Array.isArray(obj[k])) {
      // Trunca profundidade >2
      try {
        safe[k] = sanitizeForLog(obj[k]);
      } catch (e) {
        safe[k] = '[objeto]';
      }
    } else {
      safe[k] = obj[k];
    }
  }
  return safe;
}

// Manter compat: alias historico
async function registrarLog(tipo, dados) {
  return registrarEvento(tipo, dados);
}

// =============================================================================
// LEITURA DE HISTORICO
// =============================================================================

// Carregar historico do usuario (paginacao simples, ordem desc por dataCriacao)
async function carregarHistorico(tipo, limite = 10, filtros = {}) {
  if (!db) return [];
  try {
    let ref;
    if (tipo.startsWith('editais')) {
      ref = db.collection('editais').orderBy('dataCriacao', 'desc').limit(limite);
    } else if (tipo.startsWith('analises')) {
      ref = db.collection('analises').orderBy('dataCriacao', 'desc').limit(limite);
    } else {
      ref = db.collection(tipo).orderBy('dataCriacao', 'desc').limit(limite);
    }
    if (filtros.orgaoId) {
      ref = ref.where('orgaoId', '==', filtros.orgaoId);
    }
    if (filtros.uid) {
      ref = ref.where('uid', '==', filtros.uid);
    }
    if (filtros.tipo) {
      ref = ref.where('tipo', '==', filtros.tipo);
    }
    const snapshot = await ref.get();
    return snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
  } catch (error) {
    console.error('Erro ao carregar historico:', error);
    return [];
  }
}

// Inicializar IMEDIATAMENTE (sincrono) - o script e carregado sem defer
try {
  initializeFirebase();
} catch (e) {
  console.error('Falha na inicializacao:', e);
}
