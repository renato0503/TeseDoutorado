(function () {
  'use strict';

  const AdminSeed = {
    db: null, auth: null,
    async init() {
      if (typeof firebase === 'undefined' || !firebase.apps || !firebase.apps.length) return;
      this.db = firebase.firestore();
      this.auth = firebase.auth();
      this.auth.onAuthStateChanged(async (user) => {
        if (user) await this.verificarESemear(user);
      });
    },
    async verificarESemear(user) {
      try {
        await user.getIdToken(true);
        const tokenResult = await user.getIdTokenResult();
        const hasClaim = tokenResult.claims.admin === true;
        const doc = await this.db.collection('usuarios').doc(user.uid).get();
        const isAdminDoc = doc.exists && doc.data().papel === 'admin';
        if (!hasClaim && !isAdminDoc) return;
        if (doc.exists) {
          const data = doc.data();
          if (data.papel !== 'admin' || !data.ativo) {
            await docRef.update({ papel: 'admin', ativo: true, dataAtualizacao: firebase.firestore.FieldValue.serverTimestamp() });
          }
        } else {
          await this.db.collection('usuarios').doc(user.uid).set({
            nome: user.displayName || user.email || 'Admin',
            email: user.email || '',
            papel: 'admin', ativo: true,
            primeiroAcesso: false,
            dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
            provedor: user.providerData[0]?.providerId || 'firebase',
          });
        }
      } catch (e) { console.error('AdminSeed:', e); }
    },
  };

  function bootstrap() {
    if (typeof firebase === 'undefined' || !firebase.apps || !firebase.apps.length) { setTimeout(bootstrap, 200); return; }
    AdminSeed.init();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bootstrap);
  else bootstrap();
  window.AdminSeed = AdminSeed;
})();
