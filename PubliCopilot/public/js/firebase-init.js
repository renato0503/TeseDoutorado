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

// Salvar analise no Firestore (colecao analises/{uid}/)
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

// Salvar edital gerado no Firestore
async function salvarEdital(dados) {
  if (!db) {
    console.warn('Firestore nao disponivel');
    return null;
  }
  try {
    const docRef = await db.collection('editais').add({
      ...dados,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp()
    });
    console.log('Edital salvo:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('Erro ao salvar:', error);
    return null;
  }
}

// Registrar log de uso
async function registrarLog(tipo, dados) {
  if (!db) return;

  try {
    await db.collection('logs').add({
      tipo,
      ...dados,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
      userAgent: navigator.userAgent
    });
  } catch (error) {
    console.error('Erro ao registrar log:', error);
  }
}

// Carregar historico do usuario
async function carregarHistorico(tipo, limite = 10) {
  if (!db) return [];

  try {
    const snapshot = await db.collection(tipo)
      .orderBy('dataCriacao', 'desc')
      .limit(limite)
      .get();

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
