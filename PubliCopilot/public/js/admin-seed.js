// PubliCopilot - Seed automatico do Admin
// Este arquivo e executado automaticamente apos o login do admin.
// Cria o documento no Firestore com papel: 'admin' se ainda nao existir.

(function() {
  'use strict';

  const ADMIN_UID = '0RezM8WDtqVp4Od3TMYNMKESPye2';
  const ADMIN_EMAIL = 'gestor.renatorosa@gmail.com';
  const ADMIN_NOME = 'Renato de Oliveira Rosa';
  const ADMIN_WHATSAPP = '(27) 99999-0001';

  const AdminSeed = {
    db: null,
    auth: null,

    async init() {
      if (typeof firebase === 'undefined') {
        console.warn('AdminSeed: Firebase nao disponivel');
        return;
      }
      if (!firebase.apps || firebase.apps.length === 0) {
        console.warn('AdminSeed: Firebase nao inicializado');
        return;
      }

      this.db = firebase.firestore();
      this.auth = firebase.auth();

      // Listener de autenticacao
      this.auth.onAuthStateChanged(async (user) => {
        if (user) {
          await this.verificarESemear(user);
        }
      });
    },

    async verificarESemear(user) {
      // So aplica o seed se for o UID/email do admin
      const isAdmin = user.uid === ADMIN_UID || user.email === ADMIN_EMAIL;
      if (!isAdmin) return;

      try {
        // Forçar refresh do token para pegar custom claims atualizadas
        await user.getIdToken(true);
        const tokenResult = await user.getIdTokenResult();
        const hasAdminClaim = tokenResult.claims.admin === true;

        if (!hasAdminClaim) {
          console.warn('AdminSeed: Custom claim "admin" nao definido para este usuario.');
          console.warn('AdminSeed: Acesse o Console do Firebase > Authentication > usuario UID ' + user.uid);
          console.warn('AdminSeed: Ou use a Cloud Function setAdminClaim (requer deploy).');
          // Mesmo sem a custom claim, ainda tenta criar o documento (que serve como fallback de papel)
        }

        const docRef = this.db.collection('usuarios').doc(ADMIN_UID);
        const doc = await docRef.get();

        if (!doc.exists) {
          console.log('AdminSeed: Criando documento do admin...');
          await docRef.set({
            nome: ADMIN_NOME,
            whatsapp: ADMIN_WHATSAPP,
            email: ADMIN_EMAIL,
            papel: 'admin',
            ativo: true,
            primeiroAcesso: false,
            dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
            dataSeed: firebase.firestore.FieldValue.serverTimestamp(),
            observacao: 'Admin principal - seed automatico em 19/07/2026',
            provedor: user.providerData[0]?.providerId || 'firebase'
          });
          console.log('AdminSeed OK Documento criado em /usuarios/' + ADMIN_UID);
        } else {
          // Atualiza papel para admin se necessario
          const data = doc.data();
          if (data.papel !== 'admin' || !data.ativo) {
            console.log('AdminSeed: Atualizando papel para admin...');
            await docRef.update({
              papel: 'admin',
              ativo: true,
              dataAtualizacao: firebase.firestore.FieldValue.serverTimestamp()
            });
            console.log('AdminSeed OK Documento atualizado para papel: admin');
          } else {
            console.log('AdminSeed: Documento do admin ja existe e esta correto.');
          }
        }
      } catch (e) {
        console.error('AdminSeed: Erro ao semear admin:', e);
      }
    }
  };

  // Inicializar quando DOM e Firebase estiverem prontos
  function bootstrap() {
    if (typeof firebase === 'undefined' || !firebase.apps || firebase.apps.length === 0) {
      setTimeout(bootstrap, 200);
      return;
    }
    AdminSeed.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }

  // Expor helper para o console do navegador
  window.AdminSeed = AdminSeed;

  // Helper: setar custom claim admin via Cloud Function
  window.setAdminClaim = async function(uid, adminFlag, secret) {
    adminFlag = adminFlag !== false;
    if (!uid) {
      const user = firebase.auth().currentUser;
      if (!user) {
        console.error('Nenhum usuario logado. Faca login primeiro.');
        return;
      }
      uid = user.uid;
    }
    secret = secret || prompt('Digite o ADMIN_SETUP_SECRET (env var da Cloud Function):');
    if (!secret) {
      console.error('Segredo nao fornecido');
      return;
    }
    try {
      const resp = await fetch('https://us-central1-publicopilot-aa662.cloudfunctions.net/set_admin_claim', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, admin: adminFlag, secret })
      });
      const data = await resp.json();
      if (resp.ok) {
        console.log('[OK] Custom claim definida:', data);
        console.log('IMPORTANTE: O usuario deve fazer logout/login para o token ser atualizado.');
      } else {
        console.error('[ERRO]', data);
      }
    } catch (e) {
      console.error('Falha:', e);
    }
  };

  window.seedAdmin = async function() {
    if (typeof firebase === 'undefined' || !firebase.apps || firebase.apps.length === 0) {
      console.error('Firebase nao inicializado');
      return;
    }
    const auth = firebase.auth();
    const db = firebase.firestore();
    const user = auth.currentUser;
    if (!user) {
      console.error('Nenhum usuario logado. Faca login primeiro.');
      return;
    }
    console.log('Usuario logado:', user.email, 'UID:', user.uid);
    const docRef = db.collection('usuarios').doc(ADMIN_UID);
    const doc = await docRef.get();
    if (!doc.exists) {
      await docRef.set({
        nome: ADMIN_NOME,
        whatsapp: ADMIN_WHATSAPP,
        email: ADMIN_EMAIL,
        papel: 'admin',
        ativo: true,
        primeiroAcesso: false,
        dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
        dataSeed: firebase.firestore.FieldValue.serverTimestamp(),
        observacao: 'Admin principal - seed manual via console em 19/07/2026',
        provedor: user.providerData[0]?.providerId || 'firebase'
      });
      console.log('[OK] Documento do admin criado em /usuarios/' + ADMIN_UID);
    } else {
      await docRef.update({
        papel: 'admin',
        ativo: true,
        dataAtualizacao: firebase.firestore.FieldValue.serverTimestamp()
      });
      console.log('[OK] Documento do admin atualizado em /usuarios/' + ADMIN_UID);
    }
    console.log('Verifique em: https://console.firebase.google.com/project/publicopilot-aa662/firestore/data/~2Fusuarios~2F' + ADMIN_UID);
  };

  // Auto-seed tambem tenta executar quando a URL contiver ?seed=admin
  if (window.location.search.includes('seed=admin')) {
    setTimeout(() => {
      console.log('[AdminSeed] URL com ?seed=admin detectada, executando seed apos login...');
      const waitAuth = setInterval(() => {
        if (firebase.auth && firebase.auth().currentUser) {
          clearInterval(waitAuth);
          window.seedAdmin();
        }
      }, 500);
    }, 1000);
  }
})();
