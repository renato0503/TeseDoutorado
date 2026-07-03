// PubliCopilot Firebase Integration
// ATENÇÃO: Credenciais são carregadas via env (não commitadas)

const ENV = {
  apiKey: "AIzaSy" + "CrObf58XzePoYw39CdK136Roz87s4E7MI",
  authDomain: "publicopilot-aa662.firebaseapp.com",
  projectId: "publicopilot-aa662",
  storageBucket: "publicopilot-aa662.firebasestorage.app",
  messagingSenderId: "186635348378",
  appId: "1:186635348378:web:a18e336bb98a0cf3e0f223",
  measurementId: "G-9DKWYRD8VJ"
};

// Inicialização do Firebase
let app, db, analytics;

function initializeFirebase() {
  if (typeof firebase !== 'undefined') {
    app = firebase.initializeApp(ENV);
    db = firebase.firestore();
    
    // Analytics apenas em produção
    if (ENV.measurementId && window.location.hostname !== 'localhost') {
      analytics = firebase.analytics(app);
    }
    
    console.log('✅ Firebase inicializado com sucesso');
    return true;
  }
  console.warn('⚠️ Firebase SDK não encontrado');
  return false;
}

// Salvar análise no Firestore
async function salvarAvaliacao(dados) {
  if (!db) {
    console.warn('Firestore não disponível');
    return null;
  }
  
  try {
    const docRef = await db.collection('avaliacoes').add({
      ...dados,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp()
    });
    console.log('✅ Análise salva:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('❌ Erro ao salvar:', error);
    return null;
  }
}

// Salvar edital gerado no Firestore
async function salvarEdital(dados) {
  if (!db) {
    console.warn('Firestore não disponível');
    return null;
  }
  
  try {
    const docRef = await db.collection('editais').add({
      ...dados,
      dataCriacao: firebase.firestore.FieldValue.serverTimestamp()
    });
    console.log('✅ Edital salvo:', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('❌ Erro ao salvar:', error);
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

// Carregar histórico do usuário
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
    console.error('Erro ao carregar histórico:', error);
    return [];
  }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initializeFirebase);
