// PubliCopilot - Sistema de Autenticação Completo
// Suporta: Login, Cadastro, Logout, Google Auth, CAPTCHA matemático

(function() {
  'use strict';

  // ===========================================================
  // CAPTCHA MATEMÁTICO (anti-bot, sem dependências externas)
  // ===========================================================
  const Captcha = {
    challenge: null,
    expected: null,

    gerar() {
      const a = Math.floor(Math.random() * 9) + 1;
      const b = Math.floor(Math.random() * 9) + 1;
      const ops = ['+', '-', '*'];
      const op = ops[Math.floor(Math.random() * ops.length)];
      let answer;
      let display = `${a} ${op} ${b}`;
      switch (op) {
        case '+': answer = a + b; break;
        case '-': answer = a - b; break;
        case '*': answer = a * b; break;
      }
      this.challenge = display;
      this.expected = answer;
      return { display, answer };
    },

    validar(input) {
      if (this.expected === null) return false;
      return parseInt(input, 10) === this.expected;
    },

    novo() {
      const c = this.gerar();
      const el = document.getElementById('captcha-question');
      if (el) el.textContent = c.display;
      const inp = document.getElementById('captcha-input');
      if (inp) inp.value = '';
    }
  };

  // ===========================================================
  // MÁSCARAS DE ENTRADA
  // ===========================================================
  const Masks = {
    whatsapp(value) {
      value = value.replace(/\D/g, '');
      if (value.length > 11) value = value.slice(0, 11);
      if (value.length > 6) return `(${value.slice(0,2)}) ${value.slice(2,7)}-${value.slice(7)}`;
      if (value.length > 2) return `(${value.slice(0,2)}) ${value.slice(2)}`;
      if (value.length > 0) return `(${value.slice(0,2)}`;
      return '';
    }
  };

  // ===========================================================
  // VALIDAÇÕES
  // ===========================================================
  const Validators = {
    nome(nome) {
      nome = (nome || '').trim();
      if (nome.length < 3) return 'Nome deve ter ao menos 3 caracteres.';
      if (nome.length > 100) return 'Nome muito longo (max 100 caracteres).';
      if (!/^[A-Za-zÀ-ÿ\s'-]+$/.test(nome)) return 'Nome contém caracteres inválidos.';
      return null;
    },
    whatsapp(tel) {
      const digits = (tel || '').replace(/\D/g, '');
      if (digits.length < 10) return 'WhatsApp inválido (mínimo 10 dígitos com DDD).';
      if (digits.length > 11) return 'WhatsApp inválido (máximo 11 dígitos).';
      return null;
    },
    email(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!email) return 'E-mail obrigatório.';
      if (!re.test(email)) return 'E-mail inválido.';
      if (email.length > 120) return 'E-mail muito longo.';
      return null;
    },
    senha(senha) {
      if (!senha) return 'Senha obrigatória.';
      if (senha.length < 8) return 'Senha deve ter ao menos 8 caracteres.';
      if (senha.length > 128) return 'Senha muito longa.';
      if (!/[A-Z]/.test(senha)) return 'Senha deve ter ao menos 1 letra maiúscula.';
      if (!/[a-z]/.test(senha)) return 'Senha deve ter ao menos 1 letra minúscula.';
      if (!/\d/.test(senha)) return 'Senha deve ter ao menos 1 número.';
      return null;
    },
    confirmarSenha(senha, confirmar) {
      if (senha !== confirmar) return 'As senhas não coincidem.';
      return null;
    }
  };

  // ===========================================================
  // SISTEMA DE AUTENTICAÇÃO
  // ===========================================================
  const Auth = {
    user: null,
    db: null,
    auth: null,
    initialized: false,
    _readyCallbacks: [],

    _whenReady() {
      return new Promise((resolve) => {
        if (this.initialized) {
          resolve();
        } else {
          this._readyCallbacks.push(resolve);
        }
      });
    },

    async init() {
      if (this.initialized) return;

      // Esperar Firebase SDK carregar
      let tries = 0;
      while (typeof firebase === 'undefined' || typeof firebase.initializeApp !== 'function') {
        if (tries > 100) {
          console.warn('Firebase SDK nao carregou apos 10s');
          return;
        }
        await new Promise(r => setTimeout(r, 100));
        tries++;
      }

      // Esperar firebase-init.js inicializar (singleton)
      if (typeof window.whenFirebaseReady === 'function') {
        await window.whenFirebaseReady();
      } else {
        tries = 0;
        while (!firebase.apps || firebase.apps.length === 0) {
          if (tries > 100) {
            console.warn('firebase-init.js nao inicializou o app apos 10s');
            break;
          }
          await new Promise(r => setTimeout(r, 100));
          tries++;
        }
      }

      if (!firebase.apps || firebase.apps.length === 0) {
        console.error('Firebase nao inicializado. Verifique firebase-init.js');
        return;
      }

      try {
        this.auth = firebase.auth();
        this.db = firebase.firestore();
        this.initialized = true;

        // Resolver callbacks pendentes
        this._readyCallbacks.forEach(cb => cb());
        this._readyCallbacks = [];

        // Listener de estado de autenticacao (persiste entre paginas via localStorage)
        this.auth.onAuthStateChanged(async (user) => {
          this.user = user;
          await this.atualizarUI();
        });

        // Forcar atualizacao inicial (caso onAuthStateChanged nao dispare rapido)
        setTimeout(() => {
          if (!this.user && this.auth.currentUser) {
            this.user = this.auth.currentUser;
            this.atualizarUI();
          }
        }, 500);

        console.log('Auth inicializado');
      } catch (e) {
        console.error('Erro ao inicializar Auth:', e);
      }
    },

    async cadastrar(dados) {
      // Validações
      const erros = [];
      for (const campo of ['nome', 'whatsapp', 'email', 'senha', 'confirmarSenha']) {
        if (campo === 'senha') {
          const e = Validators.senha(dados.senha);
          if (e) erros.push(e);
        } else if (campo === 'confirmarSenha') {
          const e = Validators.confirmarSenha(dados.senha, dados.confirmarSenha);
          if (e) erros.push(e);
        } else {
          const e = Validators[campo](dados[campo]);
          if (e) erros.push(e);
        }
      }
      if (!Captcha.validar(dados.captcha)) {
        erros.push('CAPTCHA incorreto. Tente novamente.');
      }
      if (erros.length > 0) {
        throw new Error(erros.join('\n'));
      }

      // Criar usuário no Firebase Auth
      const cred = await this.auth.createUserWithEmailAndPassword(dados.email, dados.senha);
      const user = cred.user;
      await user.updateProfile({ displayName: dados.nome });

      // Salvar perfil estendido no Firestore
      await this.db.collection('usuarios').doc(user.uid).set({
        nome: dados.nome,
        whatsapp: dados.whatsapp,
        email: dados.email,
        papel: 'usuario',
        ativo: true,
        dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
        primeiroAcesso: true
      });

      return user;
    },

    async login(email, senha) {
      const cred = await this.auth.signInWithEmailAndPassword(email, senha);
      return cred.user;
    },

    async loginGoogle() {
      const provider = new firebase.auth.GoogleAuthProvider();
      const cred = await this.auth.signInWithPopup(provider);
      const user = cred.user;

      // Verificar se já existe perfil, senão criar
      const docRef = this.db.collection('usuarios').doc(user.uid);
      const doc = await docRef.get();
      if (!doc.exists) {
        await docRef.set({
          nome: user.displayName || '',
          whatsapp: user.phoneNumber || '',
          email: user.email,
          papel: 'usuario',
          ativo: true,
          dataCriacao: firebase.firestore.FieldValue.serverTimestamp(),
          primeiroAcesso: true,
          provedor: 'google.com'
        });
      }
      return user;
    },

    async logout() {
      await this.auth.signOut();
    },

    async getIdToken() {
      if (!this.user) return null;
      return await this.user.getIdToken(true);
    },

    async isAdmin() {
      if (!this.user) return false;
      try {
        const doc = await this.db.collection('usuarios').doc(this.user.uid).get();
        if (!doc.exists) return false;
        return doc.data().papel === 'admin';
      } catch (e) {
        return false;
      }
    },

    async atualizarUI() {
      const loginBtn = document.getElementById('btn-login');
      const signupBtn = document.getElementById('btn-signup');
      const userMenu = document.getElementById('user-menu');
      const userName = document.getElementById('user-name');
      const userEmail = document.getElementById('user-email');
      const userInitial = document.getElementById('user-initial');
      const btnLogout = document.getElementById('btn-logout');

      if (this.user) {
        if (loginBtn) loginBtn.style.display = 'none';
        if (signupBtn) signupBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'flex';
        if (userName) userName.textContent = this.user.displayName || this.user.email.split('@')[0];
        if (userEmail) userEmail.textContent = this.user.email;
        if (userInitial) userInitial.textContent = (this.user.displayName || this.user.email)[0].toUpperCase();
        if (btnLogout) btnLogout.onclick = () => this.logout();
      } else {
        if (loginBtn) loginBtn.style.display = '';
        if (signupBtn) signupBtn.style.display = '';
        if (userMenu) userMenu.style.display = 'none';
      }
    }
  };

  // ===========================================================
  // MODAL DE AUTENTICAÇÃO
  // ===========================================================
  const Modal = {
    overlay: null,
    mode: 'login', // 'login' ou 'signup'

    init() {
      this.criar();
    },

    criar() {
      if (document.getElementById('auth-overlay')) return;

      const overlay = document.createElement('div');
      overlay.id = 'auth-overlay';
      overlay.className = 'auth-overlay';
      overlay.innerHTML = `
        <div class="auth-modal">
          <button class="auth-close" id="auth-close" aria-label="Fechar">×</button>
          <div class="auth-header">
            <h2 id="auth-title">Entrar no PubliCopilot</h2>
            <p id="auth-subtitle">Acesse os modulos de avaliacao e geracao</p>
          </div>

          <div class="auth-tabs">
            <button class="auth-tab active" data-mode="login">Login</button>
            <button class="auth-tab" data-mode="signup">Cadastro</button>
          </div>

          <form id="auth-form" class="auth-form" novalidate>
            <!-- Campos comuns -->
            <div class="auth-field" id="field-nome" style="display:none">
              <label>Nome Completo *</label>
              <input type="text" id="input-nome" placeholder="Seu nome" autocomplete="name" maxlength="100">
            </div>
            <div class="auth-field" id="field-whatsapp" style="display:none">
              <label>WhatsApp (com DDD) *</label>
              <input type="tel" id="input-whatsapp" placeholder="(11) 98765-4321" maxlength="16">
            </div>
            <div class="auth-field">
              <label>E-mail *</label>
              <input type="email" id="input-email" placeholder="seu@email.com" autocomplete="email" required maxlength="120">
            </div>
            <div class="auth-field">
              <label id="label-senha">Senha *</label>
              <input type="password" id="input-senha" placeholder="••••••••" autocomplete="current-password" minlength="8" maxlength="128" required>
              <small class="auth-hint" id="hint-senha">Mínimo 8 caracteres, 1 maiúscula, 1 minúscula, 1 número</small>
            </div>
            <div class="auth-field" id="field-confirmar" style="display:none">
              <label>Confirmar Senha *</label>
              <input type="password" id="input-confirmar" placeholder="••••••••" autocomplete="new-password" minlength="8" maxlength="128">
            </div>

            <!-- CAPTCHA (apenas no cadastro) -->
            <div class="auth-field" id="field-captcha" style="display:none">
              <label>Verificação anti-bot *</label>
              <div class="captcha-row">
                <span class="captcha-question" id="captcha-question">? + ?</span>
                <button type="button" class="captcha-refresh" id="captcha-refresh" title="Gerar novo desafio">↻</button>
                <input type="number" id="captcha-input" placeholder="Resultado" min="-100" max="100">
              </div>
              <small class="auth-hint">Resolva a operação matemática para confirmar que você não é um robô</small>
            </div>

            <div class="auth-error" id="auth-error"></div>

            <button type="submit" class="auth-submit" id="auth-submit">Entrar</button>

            <div class="auth-divider"><span>ou continue com</span></div>
            <button type="button" class="auth-google" id="auth-google">
              <svg width="18" height="18" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg">
                <path fill="#4285F4" d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z"/>
                <path fill="#34A853" d="M9 18c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 0 0 9 18z"/>
                <path fill="#FBBC05" d="M3.964 10.71A5.41 5.41 0 0 1 3.682 9c0-.593.102-1.17.282-1.71V4.958H.957A8.996 8.996 0 0 0 0 9c0 1.452.348 2.827.957 4.042l3.007-2.332z"/>
                <path fill="#EA4335" d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 0 0 .957 4.958L3.964 7.29C4.672 5.163 6.656 3.58 9 3.58z"/>
              </svg>
              Google
            </button>
          </form>
        </div>
      `;

      document.body.appendChild(overlay);
      this.overlay = overlay;
      this.vincularEventos();
    },

    vincularEventos() {
      document.getElementById('auth-close').onclick = () => this.fechar();
      this.overlay.onclick = (e) => {
        if (e.target === this.overlay) this.fechar();
      };

      document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.onclick = () => this.mudarModo(tab.dataset.mode);
      });

      document.getElementById('input-whatsapp').oninput = (e) => {
        e.target.value = Masks.whatsapp(e.target.value);
      };

      document.getElementById('captcha-refresh').onclick = () => Captcha.novo();

      document.getElementById('auth-google').onclick = async () => {
        try {
          this.mostrarErro('');
          this.desabilitarBotao(true);
          await Auth.loginGoogle();
          this.fechar();
        } catch (e) {
          this.mostrarErro(this.traduzirErro(e));
          this.desabilitarBotao(false);
        }
      };

      document.getElementById('auth-form').onsubmit = async (e) => {
        e.preventDefault();
        this.mostrarErro('');
        this.desabilitarBotao(true);
        try {
          if (this.mode === 'login') {
            const email = document.getElementById('input-email').value.trim();
            const senha = document.getElementById('input-senha').value;
            if (!email || !senha) throw new Error('Preencha todos os campos.');
            await Auth.login(email, senha);
          } else {
            const dados = {
              nome: document.getElementById('input-nome').value.trim(),
              whatsapp: document.getElementById('input-whatsapp').value.trim(),
              email: document.getElementById('input-email').value.trim(),
              senha: document.getElementById('input-senha').value,
              confirmarSenha: document.getElementById('input-confirmar').value,
              captcha: document.getElementById('captcha-input').value
            };
            await Auth.cadastrar(dados);
          }
          this.fechar();
        } catch (err) {
          this.mostrarErro(this.traduzirErro(err));
          if (this.mode === 'signup') Captcha.novo();
        } finally {
          this.desabilitarBotao(false);
        }
      };

      // ESC fecha
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.overlay.classList.contains('show')) {
          this.fechar();
        }
      });
    },

    mudarModo(modo) {
      this.mode = modo;
      document.querySelectorAll('.auth-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.mode === modo);
      });

      const isLogin = modo === 'login';
      document.getElementById('auth-title').textContent = isLogin
        ? 'Entrar no PubliCopilot'
        : 'Criar Conta no PubliCopilot';
      document.getElementById('auth-subtitle').textContent = isLogin
        ? 'Acesse os modulos de avaliacao e geracao'
        : 'Cadastre-se gratuitamente para usar o Copiloto';
      document.getElementById('auth-submit').textContent = isLogin ? 'Entrar' : 'Criar Conta';

      document.getElementById('field-nome').style.display = isLogin ? 'none' : '';
      document.getElementById('field-whatsapp').style.display = isLogin ? 'none' : '';
      document.getElementById('field-confirmar').style.display = isLogin ? 'none' : '';
      document.getElementById('field-captcha').style.display = isLogin ? 'none' : '';
      document.getElementById('input-senha').autocomplete = isLogin ? 'current-password' : 'new-password';
      document.getElementById('label-senha').textContent = isLogin ? 'Senha *' : 'Senha *';
      document.getElementById('hint-senha').style.display = isLogin ? 'none' : '';

      this.mostrarErro('');
      if (!isLogin) Captcha.novo();
    },

    abrir(modo = 'login') {
      this.criar();
      this.mudarModo(modo);
      this.overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
      setTimeout(() => document.getElementById('input-email').focus(), 200);
    },

    fechar() {
      this.overlay.classList.remove('show');
      document.body.style.overflow = '';
      document.getElementById('auth-form').reset();
      this.mostrarErro('');
    },

    mostrarErro(msg) {
      const el = document.getElementById('auth-error');
      el.textContent = msg || '';
      el.style.display = msg ? 'block' : 'none';
    },

    desabilitarBotao(disabled) {
      const btn = document.getElementById('auth-submit');
      btn.disabled = disabled;
      btn.style.opacity = disabled ? '0.6' : '1';
    },

    traduzirErro(err) {
      const code = err.code || '';
      const msg = err.message || '';
      const map = {
        'auth/email-already-in-use': 'Este e-mail ja esta cadastrado. Tente fazer login.',
        'auth/invalid-email': 'E-mail invalido.',
        'auth/weak-password': 'Senha muito fraca. Use no minimo 8 caracteres com 1 maiuscula, 1 minuscula e 1 numero.',
        'auth/user-not-found': 'Usuario nao encontrado.',
        'auth/wrong-password': 'Senha incorreta.',
        'auth/invalid-credential': 'Credenciais invalidas. Verifique e-mail e senha.',
        'auth/too-many-requests': 'Muitas tentativas. Tente novamente em alguns minutos.',
        'auth/user-disabled': 'Usuario desativado. Entre em contato com o administrador.',
        'auth/popup-closed-by-user': 'Login com Google cancelado.',
        'auth/network-request-failed': 'Erro de rede. Verifique sua conexao.',
        'auth/requires-recent-login': 'Sessao expirada. Faca login novamente.'
      };
      return map[code] || msg;
    }
  };

  // ===========================================================
  // API AUTHENTICADA (chamadas ao backend)
  // ===========================================================
  async function fetchAutenticado(url, options = {}) {
    if (!Auth.user) {
      throw new Error('Usuario nao autenticado. Faca login primeiro.');
    }
    const token = await Auth.getIdToken();
    options.headers = options.headers || {};
    options.headers['Authorization'] = 'Bearer ' + token;
    if (options.body && typeof options.body === 'object') {
      options.headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }
    const resp = await fetch(url, options);
    if (resp.status === 401 || resp.status === 403) {
      Modal.abrir('login');
      throw new Error('Sessao expirada. Faca login novamente.');
    }
    return resp;
  }

  // ===========================================================
  // EXPORTAR API PÚBLICA
  // ===========================================================
  window.PubliAuth = {
    Auth,
    Modal,
    Captcha,
    abrirLogin: async (modo) => { await Auth._whenReady(); return Modal.abrir(modo || 'login'); },
    abrirCadastro: async () => { await Auth._whenReady(); return Modal.abrir('signup'); },
    sair: () => Auth.logout(),
    fetchAutenticado,
    isLogado: () => !!Auth.user,
    getUser: () => Auth.user,
    isAdmin: () => Auth.isAdmin(),
    whenReady: () => Auth._whenReady()
  };

  // Inicializar quando DOM estiver pronto
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => Auth.init());
  } else {
    Auth.init();
  }
})();
