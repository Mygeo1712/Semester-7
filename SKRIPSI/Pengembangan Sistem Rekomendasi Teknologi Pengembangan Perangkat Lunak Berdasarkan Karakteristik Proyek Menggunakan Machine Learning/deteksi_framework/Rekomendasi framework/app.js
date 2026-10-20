/**
 * FrameRec — Framework Recommendation System
 * Main Application JavaScript
 *
 * Implements:
 * - Random Forest inference (client-side, from rf_model.json)
 * - Hybrid Scoring: RF Probability (60%) + Compatibility Score (40%)
 *   sesuai arsitektur Hybrid Recommendation yang dirancang di rancangan_arsitektur_sistem.md
 * - UI state management untuk form 10 pertanyaan
 * - Recommendation rendering dengan penjelasan kontekstual
 */

'use strict';

// ============================================================
// CONSTANTS & MAPPINGS
// ============================================================

const FRAMEWORK_MAP = {
  1: 'Django',
  2: 'FastAPI',
  3: 'Ruby on Rails',
  4: 'Next.js',
  5: 'Flask',
  6: 'Spring Boot',
  7: 'Laravel',
  8: 'Symfony',
  9: 'Express.js'
};

const FRAMEWORK_INFO = {
  'Django': {
    lang: 'Python',
    color: '#092E20',
    accent: '#44B78B',
    dot: '#44B78B',
    desc: 'Framework web Python yang matang dengan pendekatan "batteries included", ORM yang kuat, admin panel bawaan, dan ekosistem library yang lengkap.',
    strengths: [
      'ORM Django yang powerful untuk database relasional',
      'Admin panel otomatis, hemat waktu development',
      'Ekosistem Python yang kaya untuk AI/ML integration',
      'Security built-in: CSRF, XSS, SQL injection protection',
      'Cocok untuk tim dengan pengalaman Python'
    ],
    useCases: ['Sistem Informasi', 'E-commerce', 'API Backend', 'Dashboard Analytics'],
    github: 'https://github.com/django/django'
  },
  'FastAPI': {
    lang: 'Python',
    color: '#009688',
    accent: '#00BFA5',
    dot: '#00BFA5',
    desc: 'Framework Python modern untuk membangun API dengan performa tinggi, type hints, dan dokumentasi otomatis (Swagger/OpenAPI) yang terintegrasi.',
    strengths: [
      'Performa mendekati Node.js dan Go berkat async/await',
      'Dokumentasi API otomatis dengan Swagger UI',
      'Type safety dengan Python type hints',
      'Sangat cocok untuk microservices dan API service',
      'Integrasi mudah dengan ML models (scikit-learn, TensorFlow)'
    ],
    useCases: ['REST API', 'Microservices', 'ML API Endpoint', 'Real-time Backend'],
    github: 'https://github.com/fastapi/fastapi'
  },
  'Ruby on Rails': {
    lang: 'Ruby',
    color: '#CC0000',
    accent: '#E0524C',
    dot: '#E0524C',
    desc: 'Framework web Ruby yang mengikuti prinsip "Convention over Configuration" dengan pendekatan MVC yang opinionated dan produktivitas developer yang tinggi.',
    strengths: [
      'Convention over Configuration, boilerplate minimal',
      'ActiveRecord ORM yang ekspresif',
      'Scaffolding cepat untuk prototyping',
      'Komunitas mature dengan gem ekosistem yang besar',
      'Cocok untuk startup yang butuh development cepat'
    ],
    useCases: ['Web Application', 'E-commerce', 'SaaS', 'Rapid Prototype'],
    github: 'https://github.com/rails/rails'
  },
  'Next.js': {
    lang: 'JavaScript/TypeScript',
    color: '#000000',
    accent: '#FFFFFF',
    dot: '#94A3B8',
    desc: 'Framework React full-stack dari Vercel yang mendukung SSR, SSG, dan ISR, memberikan performa optimal dan DX terbaik untuk aplikasi web modern.',
    strengths: [
      'Server-Side Rendering & Static Generation built-in',
      'File-based routing yang intuitif',
      'API Routes untuk backend ringan',
      'Image & Font optimization otomatis',
      'Edge Runtime support untuk performa global'
    ],
    useCases: ['Web Application', 'E-commerce', 'Dashboard', 'Marketing Site'],
    github: 'https://github.com/vercel/next.js'
  },
  'Flask': {
    lang: 'Python',
    color: '#000000',
    accent: '#A0A0A0',
    dot: '#94A3B8',
    desc: 'Microframework Python yang minimalis dan fleksibel. Memberikan kebebasan penuh dalam arsitektur aplikasi tanpa opini berlebihan.',
    strengths: [
      'Sangat ringan dan mudah dipelajari',
      'Fleksibel: pilih extension sesuai kebutuhan',
      'Cocok untuk prototype dan aplikasi kecil',
      'Integrasi mudah dengan data science tools',
      'Dokumentasi lengkap dan komunitas aktif'
    ],
    useCases: ['API Sederhana', 'Prototype', 'Data Science App', 'Microservice'],
    github: 'https://github.com/pallets/flask'
  },
  'Spring Boot': {
    lang: 'Java',
    color: '#6DB33F',
    accent: '#6DB33F',
    dot: '#6DB33F',
    desc: 'Framework Java enterprise yang matang dengan auto-configuration, dependency injection, dan ekosistem Spring yang komprehensif untuk aplikasi production-grade.',
    strengths: [
      'Ekosistem enterprise Java yang matang dan terpercaya',
      'Auto-configuration mengurangi boilerplate konfigurasi',
      'Spring Security untuk autentikasi & otorisasi robust',
      'Performa tinggi dan mendukung skalabilitas horizontal',
      'Ideal untuk tim besar dengan standar enterprise'
    ],
    useCases: ['Enterprise Application', 'Microservices', 'Banking System', 'Large-scale API'],
    github: 'https://github.com/spring-projects/spring-boot'
  },
  'Laravel': {
    lang: 'PHP',
    color: '#FF2D20',
    accent: '#FF6B6B',
    dot: '#FF6B6B',
    desc: 'Framework PHP yang elegan dengan syntax ekspresif, Eloquent ORM, Blade templating, dan ekosistem lengkap seperti Sanctum, Horizon, dan Nova.',
    strengths: [
      'Eloquent ORM yang intuitif dan powerful',
      'Artisan CLI untuk scaffolding dan automation',
      'Ekosistem Composer PHP yang besar',
      'Hosting shared mudah dan murah',
      'Queue system, caching, dan session built-in'
    ],
    useCases: ['Web Application', 'E-commerce', 'CMS', 'REST API'],
    github: 'https://github.com/laravel/framework'
  },
  'Symfony': {
    lang: 'PHP',
    color: '#000000',
    accent: '#C0C0C0',
    dot: '#94A3B8',
    desc: 'Framework PHP enterprise yang modular dan dapat dikonfigurasi sepenuhnya. Banyak framework lain (termasuk Laravel) dibangun di atas komponen Symfony.',
    strengths: [
      'Arsitektur modular dengan komponen yang reusable',
      'Standar enterprise PHP yang ketat',
      'Doctrine ORM yang sangat powerful',
      'Cocok untuk proyek jangka panjang dan tim besar',
      'Testing framework yang terintegrasi'
    ],
    useCases: ['Enterprise CMS', 'Complex Web App', 'E-commerce Platform', 'API'],
    github: 'https://github.com/symfony/symfony'
  },
  'Express.js': {
    lang: 'JavaScript/Node.js',
    color: '#000000',
    accent: '#68A063',
    dot: '#68A063',
    desc: 'Framework Node.js minimal dan fleksibel yang menjadi standar de-facto untuk backend JavaScript, dengan ekosistem middleware yang luas.',
    strengths: [
      'JavaScript full-stack: frontend & backend satu bahasa',
      'Non-blocking I/O, ideal untuk real-time application',
      'Ekosistem npm terbesar di dunia',
      'Fleksibel: pilih arsitektur sesuai kebutuhan',
      'Ringan dan sangat cepat untuk API sederhana'
    ],
    useCases: ['REST API', 'Real-time App', 'Microservices', 'BFF (Backend for Frontend)'],
    github: 'https://github.com/expressjs/express'
  }
};

const APP_TYPE_LABELS = {
  1: 'Web Application', 2: 'API / Backend', 3: 'CMS', 4: 'Dashboard', 5: 'E-commerce', 6: 'CLI'
};
const LANG_LABELS = {
  1: 'Python', 2: 'PHP', 3: 'Java', 4: 'JavaScript', 5: 'TypeScript', 6: 'Ruby'
};
const DB_LABELS = {
  1: 'PostgreSQL', 2: 'MySQL', 3: 'MongoDB', 4: 'SQLite', 5: 'Redis', 6: 'Relasional (ORM)'
};

// ============================================================
// RANDOM FOREST INFERENCE ENGINE
// ============================================================

class RandomForestInference {
  constructor(modelData) {
    this.trees = modelData.trees;
    this.classes = modelData.classes;
    this.nClasses = modelData.n_classes;
    this.nEstimators = modelData.n_estimators;
  }

  /**
   * Traverse a single decision tree node recursively.
   * Returns the leaf probability array.
   */
  _traverseTree(tree, features, nodeIdx = 0) {
    const node = tree[nodeIdx];
    if (node.is_leaf) {
      return node.proba;
    }
    const featureVal = features[node.feature];
    if (featureVal <= node.threshold) {
      return this._traverseTree(tree, features, node.left);
    } else {
      return this._traverseTree(tree, features, node.right);
    }
  }

  /**
   * Hitung raw RF probabilities untuk semua kelas.
   * @param {number[]} features
   * @returns {{ classId, name, rfProb }[]}
   */
  getRawProbs(features) {
    const avgProba = new Array(this.nClasses).fill(0);
    for (const tree of this.trees) {
      const proba = this._traverseTree(tree, features);
      for (let i = 0; i < this.nClasses; i++) avgProba[i] += proba[i];
    }
    for (let i = 0; i < this.nClasses; i++) avgProba[i] /= this.nEstimators;
    return this.classes.map((cls, i) => ({
      classId: cls,
      name: FRAMEWORK_MAP[cls],
      rfProb: avgProba[i]
    }));
  }

  /**
   * Predict dengan Hybrid Scoring:
   *   hybridScore = RF_WEIGHT * rfNorm + COMPAT_WEIGHT * compatNorm
   * di mana rfNorm dinormalisasi relatif terhadap nilai tertinggi.
   *
   * @param {number[]} features
   * @param {Object} answers  - jawaban user (untuk compatibility score)
   * @returns {{ classProbs, ranking }}
   */
  predictProba(features, answers) {
    const rawProbs = this.getRawProbs(features);

    // Normalisasi RF: nilai tertinggi = 1.0, yang lain relatif
    const maxRf = Math.max(...rawProbs.map(r => r.rfProb));

    // Hitung hybrid score per framework
    const RF_WEIGHT   = 0.60;
    const COMPAT_WEIGHT = 0.40;
    const SCORE_CEILING = 96; // skor maksimum yang bisa ditampilkan (%)
    const SCORE_FLOOR   = 8;  // skor minimum

    const ranking = rawProbs.map(item => {
      const rfNorm   = maxRf > 0 ? item.rfProb / maxRf : 0; // 0–1
      const compat   = answers ? computeCompatibilityScore(item.name, answers) : 50;
      const compatNorm = compat / 100; // 0–1

      // Hybrid score dipetakan ke rentang [FLOOR, CEILING]
      const rawHybrid = RF_WEIGHT * rfNorm + COMPAT_WEIGHT * compatNorm;
      const hybridPct = SCORE_FLOOR + rawHybrid * (SCORE_CEILING - SCORE_FLOOR);

      return {
        classId:    item.classId,
        name:       item.name,
        rfProb:     item.rfProb,          // probabilitas RF mentah (0–1)
        rfPct:      Math.round(item.rfProb * 100), // untuk ditampilkan
        compatPct:  Math.round(compat),    // skor kompatibilitas (0–100)
        hybridPct:  Math.round(hybridPct), // skor akhir yang ditampilkan
        rfNorm,
        compatNorm
      };
    });

    // Urutkan berdasarkan hybridPct (skor akhir)
    ranking.sort((a, b) => b.hybridPct - a.hybridPct);

    return { ranking };
  }

  predict(features, answers) {
    const { ranking } = this.predictProba(features, answers);
    return ranking[0];
  }
}

// ============================================================
// APPLICATION STATE
// ============================================================

const state = {
  modelLoaded: false,
  rfModel: null,
  answers: {},   // { 1: value, 2: value, ... }
  totalQuestions: 10
};

// ============================================================
// DOM REFERENCES
// ============================================================

const $ = id => document.getElementById(id);

// ============================================================
// PROGRESS MANAGEMENT
// ============================================================

function initProgressSteps() {
  const container = $('progress-steps');
  container.innerHTML = '';
  for (let i = 1; i <= state.totalQuestions; i++) {
    const step = document.createElement('div');
    step.className = 'progress-step';
    step.id = `step-${i}`;
    step.textContent = i;
    step.title = `Pertanyaan ${i}`;
    step.onclick = () => {
      const card = $(`card-${i}`);
      if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    };
    container.appendChild(step);
  }
}

function updateProgress() {
  const answered = Object.keys(state.answers).length;
  const pct = (answered / state.totalQuestions) * 100;

  $('progress-fill').style.width = pct + '%';
  $('progress-count').textContent = `${answered} / ${state.totalQuestions}`;

  // Update steps
  for (let i = 1; i <= state.totalQuestions; i++) {
    const step = $(`step-${i}`);
    if (step) {
      step.classList.toggle('done', state.answers[i] !== undefined);
      step.textContent = state.answers[i] !== undefined ? '' : i;
    }
  }

  // Enable/disable analyze button
  const allAnswered = answered === state.totalQuestions;
  $('btn-analyze').disabled = !allAnswered || !state.modelLoaded;

  if (allAnswered) {
    $('submit-info').style.opacity = '0';
  } else {
    $('submit-info').style.opacity = '1';
    $('submit-info').querySelector('span').textContent =
      `Lengkapi ${state.totalQuestions - answered} pertanyaan lagi sebelum analisis`;
  }
}

// ============================================================
// OPTION SELECTION HANDLING
// ============================================================

function setupOptionListeners() {
  const allOptions = document.querySelectorAll('.option-card input[type="radio"]');
  allOptions.forEach(input => {
    input.addEventListener('change', (e) => {
      const qNum = parseInt(e.target.dataset.q);
      const value = parseInt(e.target.value);
      state.answers[qNum] = value;

      // Update visual state for all options in this group
      const groupOptions = document.querySelectorAll(`input[name="${e.target.name}"]`);
      groupOptions.forEach(opt => {
        opt.closest('.option-card').classList.toggle('selected', opt === e.target);
      });

      // Mark card as answered
      const card = $(`card-${qNum}`);
      if (card) card.classList.add('answered');

      updateProgress();

      // Auto-scroll to next unanswered question
      setTimeout(() => autoScrollToNext(qNum), 300);
    });
  });
}

function autoScrollToNext(currentQ) {
  for (let q = currentQ + 1; q <= state.totalQuestions; q++) {
    if (state.answers[q] === undefined) {
      const card = $(`card-${q}`);
      if (card) {
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      return;
    }
  }
  // All answered — scroll to submit
  const submitSection = document.querySelector('.submit-section');
  if (submitSection) {
    submitSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}

// ============================================================
// COMPATIBILITY SCORE ENGINE (domain-knowledge rules)
// Referensi: rancangan_arsitektur_sistem.md §8 Compatibility Score
// ============================================================

/**
 * Hitung Compatibility Score (0–100) untuk satu framework
 * berdasarkan jawaban user. Ini adalah komponen "domain knowledge"
 * dari sistem Hybrid Recommendation.
 *
 * Dimensi & bobot:
 *  - Bahasa pemrograman   : 30 poin  (faktor terkuat)
 *  - Tipe aplikasi        : 20 poin
 *  - Skala pengguna       : 15 poin
 *  - Ukuran tim           : 15 poin
 *  - Database             : 10 poin
 *  - DevOps (Docker+CI)   : 10 poin
 */
function computeCompatibilityScore(frameworkName, answers) {
  let score = 0;

  // ── 1. Bahasa pemrograman (30 poin) ────────────────────────
  // Setiap framework memiliki bahasa "native"-nya
  const langFit = {
    'Django':        { native: [1],    partial: [] },          // Python
    'FastAPI':       { native: [1],    partial: [] },          // Python
    'Flask':         { native: [1],    partial: [] },          // Python
    'Laravel':       { native: [2],    partial: [] },          // PHP
    'Symfony':       { native: [2],    partial: [] },          // PHP
    'Spring Boot':   { native: [3],    partial: [] },          // Java
    'Next.js':       { native: [4, 5], partial: [] },          // JS/TS
    'Express.js':    { native: [4, 5], partial: [] },          // JS/TS
    'Ruby on Rails': { native: [6],    partial: [] },          // Ruby
  };
  const lf = langFit[frameworkName];
  if (lf) {
    if (lf.native.includes(answers[2]))   score += 30;
    else if (lf.partial.includes(answers[2])) score += 12;
    // else: 0 poin (bahasa tidak cocok)
  }

  // ── 2. Tipe aplikasi (20 poin) ──────────────────────────────
  //  1=Web App, 2=API, 3=CMS, 4=Dashboard, 5=E-commerce, 6=CLI
  const appFit = {
    'Django':        { best: [1, 3, 4, 5], ok: [2] },
    'FastAPI':       { best: [2],          ok: [1, 4] },
    'Flask':         { best: [2, 6],       ok: [1, 4] },
    'Laravel':       { best: [1, 3, 5],    ok: [2] },
    'Symfony':       { best: [1, 3],       ok: [2, 5] },
    'Spring Boot':   { best: [2, 1],       ok: [4, 6] },
    'Next.js':       { best: [1, 4, 5],    ok: [2] },
    'Express.js':    { best: [2, 6],       ok: [1] },
    'Ruby on Rails': { best: [1, 5, 3],    ok: [2] },
  };
  const af = appFit[frameworkName];
  if (af) {
    if (af.best.includes(answers[1]))      score += 20;
    else if (af.ok.includes(answers[1]))   score += 10;
    else                                   score += 3;
  }

  // ── 3. Skala pengguna (15 poin) ─────────────────────────────
  // 1=<100, 2=100-1K, 3=1K-10K, 4=10K-100K, 5=>100K
  const scaleFit = {
    'Django':        [12, 15, 15, 12, 10],
    'FastAPI':       [10, 13, 15, 15, 14],
    'Flask':         [15, 14, 10,  6,  3],
    'Laravel':       [12, 15, 14, 10,  7],
    'Symfony':       [10, 12, 14, 15, 13],
    'Spring Boot':   [ 8, 10, 13, 15, 15],
    'Next.js':       [10, 12, 15, 15, 13],
    'Express.js':    [12, 14, 13, 10,  8],
    'Ruby on Rails': [13, 15, 14, 10,  7],
  };
  const sf = scaleFit[frameworkName];
  if (sf && answers[9] >= 1 && answers[9] <= 5) {
    score += sf[answers[9] - 1];
  }

  // ── 4. Ukuran tim (15 poin) ─────────────────────────────────
  // 1=solo, 2=2-3, 3=4-10, 4=>10
  const teamFit = {
    'Django':        [12, 15, 14, 10],
    'FastAPI':       [14, 15, 12,  8],
    'Flask':         [15, 13, 10,  6],
    'Laravel':       [13, 15, 14, 10],
    'Symfony':       [ 7, 10, 14, 15],
    'Spring Boot':   [ 5,  9, 13, 15],
    'Next.js':       [12, 15, 14, 11],
    'Express.js':    [14, 15, 12,  8],
    'Ruby on Rails': [13, 15, 12,  9],
  };
  const tf = teamFit[frameworkName];
  if (tf && answers[8] >= 1 && answers[8] <= 4) {
    score += tf[answers[8] - 1];
  }

  // ── 5. Database (10 poin) ────────────────────────────────────
  // 1=PG, 2=MySQL, 3=Mongo, 4=SQLite, 5=Redis, 6=ORM
  const dbFit = {
    'Django':        { best: [1, 6], ok: [2, 4],    bad: [3] },
    'FastAPI':       { best: [1, 3], ok: [2, 5, 6], bad: [] },
    'Flask':         { best: [1, 4], ok: [2, 3, 6], bad: [] },
    'Laravel':       { best: [2, 6], ok: [1, 4],    bad: [3] },
    'Symfony':       { best: [1, 6], ok: [2, 4],    bad: [3] },
    'Spring Boot':   { best: [1, 2], ok: [3, 5, 6], bad: [] },
    'Next.js':       { best: [1, 3], ok: [2, 4, 5], bad: [] },
    'Express.js':    { best: [3, 5], ok: [1, 2, 4], bad: [] },
    'Ruby on Rails': { best: [1, 2], ok: [4, 6],    bad: [3] },
  };
  const df = dbFit[frameworkName];
  if (df) {
    if (df.best.includes(answers[3]))      score += 10;
    else if (df.ok.includes(answers[3]))   score += 6;
    else if (df.bad.includes(answers[3]))  score += 1;
    else                                   score += 4;
  }

  // ── 6. DevOps: Docker + CI/CD (10 poin) ─────────────────────
  // Framework enterprise (Spring Boot, Symfony, Next.js) lebih
  // diuntungkan oleh Docker & CI/CD
  const devopsFit = {
    'Spring Boot': 3, 'Next.js': 3, 'Symfony': 3,
    'Django': 2, 'FastAPI': 2, 'Laravel': 2,
    'Flask': 1, 'Express.js': 1, 'Ruby on Rails': 1
  };
  const devopsBase = devopsFit[frameworkName] || 1;
  if (answers[4] === 1) score += devopsBase;       // Docker
  if (answers[5] === 1) score += devopsBase;       // CI/CD
  if (answers[6] === 1) score += Math.min(2, devopsBase); // Tests
  // Tanpa DevOps: framework ringan justru lebih cocok
  if (answers[4] === 0 && answers[5] === 0) {
    if (['Flask', 'Express.js'].includes(frameworkName)) score += 4;
    if (['Laravel', 'Ruby on Rails'].includes(frameworkName)) score += 2;
  }

  return Math.min(100, Math.max(0, score));
}

// ============================================================
// RECOMMENDATION ENGINE
// ============================================================

function buildFeatureVector() {
  return [
    state.answers[1],   // X1_application_type
    state.answers[2],   // X2_primary_language
    state.answers[3],   // X3_database
    state.answers[4],   // X4_has_docker
    state.answers[5],   // X5_has_ci_cd
    state.answers[6],   // X6_has_tests
    state.answers[7],   // X7_monorepo
    state.answers[8],   // X8_contributors
    state.answers[9],   // X9_pengguna
    state.answers[10]   // X10_active_weeks
  ];
}

function runAnalysis() {
  if (!state.modelLoaded) {
    showNotification('Model masih dimuat, harap tunggu...', 'warning');
    return;
  }

  // Show loading state on button
  $('btn-analyze-text').textContent = 'Menganalisis...';
  $('btn-spinner').style.display = 'block';
  $('btn-icon').style.display = 'none';
  $('btn-analyze').disabled = true;

  // Small delay for UX
  setTimeout(() => {
    try {
      const features = buildFeatureVector();
      // Hybrid scoring: teruskan answers untuk compatibility score
      const result = state.rfModel.predictProba(features, state.answers);
      renderResults(result);
    } catch (err) {
      console.error('Analysis error:', err);
      showNotification('Terjadi kesalahan saat analisis. Coba refresh halaman.', 'error');
    } finally {
      $('btn-analyze-text').textContent = 'Analisis Sekarang';
      $('btn-spinner').style.display = 'none';
      $('btn-icon').style.display = 'block';
      $('btn-analyze').disabled = false;
    }
  }, 600);
}

// ============================================================
// RESULT RENDERING
// ============================================================

function renderResults(result) {
  const { ranking } = result;
  const top = ranking[0];
  const info = FRAMEWORK_INFO[top.name] || {};
  const displayPct = top.hybridPct; // skor hybrid yang ditampilkan di ring

  // ─── Top Card ────────────────────────────────────
  const topContainer = $('top-recommendation');
  topContainer.innerHTML = `
    <div class="top-card">
      <div class="top-card-body">
        <div class="top-card-header">
          <div class="top-badge">🏆 Rekomendasi Utama</div>
        </div>
        <h2 class="top-framework-name gradient-text">${top.name}</h2>
        <span class="top-language">${info.lang || 'Web Framework'}</span>
        <p class="top-description">${info.desc || ''}</p>
        <p class="strengths-title">Mengapa cocok untuk proyek Anda:</p>
        <ul class="strengths-list">
          ${generateStrengths(top.name).map(s => `<li>${s}</li>`).join('')}
        </ul>
      </div>
      <div class="top-score-block">
        <div class="score-ring">
          <svg width="130" height="130" viewBox="0 0 130 130">
            <defs>
              <linearGradient id="scoreGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#7C3AED"/>
                <stop offset="100%" stop-color="#06B6D4"/>
              </linearGradient>
            </defs>
            <circle class="score-bg" cx="65" cy="65" r="56"/>
            <circle class="score-fill" cx="65" cy="65" r="56"
              stroke-dasharray="${2 * Math.PI * 56}"
              stroke-dashoffset="${2 * Math.PI * 56}"
              id="score-circle"/>
          </svg>
          <div class="score-text">
            <span class="score-number" id="score-num">0</span>
            <span class="score-pct">%</span>
          </div>
        </div>
        <p class="score-label">Skor Hybrid</p>
        <div style="margin-top:16px;display:flex;flex-direction:column;gap:6px;text-align:left">
          ${generateUseCaseTags(top.name, info)}
        </div>
      </div>
    </div>

    <!-- Score Breakdown Card -->
    <div class="score-breakdown" style="
      margin-top:14px;
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px;
    ">
      <div class="breakdown-item" style="
        background:rgba(124,58,237,0.07);
        border:1px solid rgba(124,58,237,0.2);
        border-radius:var(--radius-md);
        padding:16px;
      ">
        <p style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--primary-light);margin-bottom:6px">🤖 Skor ML Model</p>
        <p style="font-size:1.4rem;font-weight:900;color:var(--text-primary);margin-bottom:4px">${top.rfPct}%</p>
        <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.4">Probabilitas dari Random Forest (bobot 60%)</p>
        <div style="margin-top:8px;background:rgba(148,163,184,0.1);border-radius:4px;height:4px;overflow:hidden">
          <div style="height:100%;width:${top.rfPct}%;background:var(--primary);border-radius:4px;transition:width 1s ease"></div>
        </div>
      </div>
      <div class="breakdown-item" style="
        background:rgba(6,182,212,0.07);
        border:1px solid rgba(6,182,212,0.2);
        border-radius:var(--radius-md);
        padding:16px;
      ">
        <p style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--accent-light);margin-bottom:6px">📐 Skor Kompatibilitas</p>
        <p style="font-size:1.4rem;font-weight:900;color:var(--text-primary);margin-bottom:4px">${top.compatPct}%</p>
        <p style="font-size:0.78rem;color:var(--text-muted);line-height:1.4">Kecocokan domain knowledge (bobot 40%)</p>
        <div style="margin-top:8px;background:rgba(148,163,184,0.1);border-radius:4px;height:4px;overflow:hidden">
          <div style="height:100%;width:${top.compatPct}%;background:var(--accent);border-radius:4px;transition:width 1s ease"></div>
        </div>
      </div>
    </div>

    <div class="explanation-card" style="margin-top:14px;background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px">
      <p style="font-size:0.82rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:var(--text-muted);margin-bottom:12px">📋 Konteks Rekomendasi</p>
      <p style="font-size:0.875rem;color:var(--text-secondary);line-height:1.7">${generateExplanation(top.name, state.answers)}</p>
    </div>
  `;

  // Animate score ring dengan hybridPct
  setTimeout(() => {
    const circumference = 2 * Math.PI * 56;
    const dashOffset = circumference - (displayPct / 100) * circumference;
    const circle = $('score-circle');
    if (circle) circle.style.strokeDashoffset = dashOffset;
    animateNumber('score-num', 0, displayPct, 1000);
    // Animate breakdown bars
    document.querySelectorAll('.score-breakdown .breakdown-item div div').forEach(bar => {
      bar.style.width = bar.style.width; // trigger reflow
    });
  }, 200);

  // ─── Rankings List ────────────────────────────────
  const rankList = $('rankings-list');
  rankList.innerHTML = '';

  ranking.forEach((item, idx) => {
    const hybridPct = item.hybridPct;
    const rankInfo  = FRAMEWORK_INFO[item.name] || {};
    const barClass  = hybridPct >= 70 ? 'high' : hybridPct >= 45 ? 'mid' : 'low';
    const posClass  = idx === 0 ? 'pos-1' : idx === 1 ? 'pos-2' : idx === 2 ? 'pos-3' : 'pos-other';
    const posLabel  = idx === 0 ? '🥇' : idx === 1 ? '🥈' : idx === 2 ? '🥉' : `#${idx + 1}`;
    const scoreColor = hybridPct >= 70 ? 'var(--primary-light)' : hybridPct >= 45 ? 'var(--accent-light)' : 'var(--text-muted)';

    const li = document.createElement('div');
    li.className = `rank-item rank-${idx + 1}`;
    li.style.animationDelay = `${idx * 0.07}s`;
    li.innerHTML = `
      <div class="rank-pos ${posClass}">${posLabel}</div>
      <div class="rank-info">
        <div class="rank-name">${item.name}</div>
        <div class="rank-lang" style="display:flex;gap:6px;align-items:center">
          <span style="color:var(--text-muted)">${rankInfo.lang || ''}</span>
          <span style="font-size:0.7rem;color:var(--text-muted);font-family:'JetBrains Mono',monospace">RF:${item.rfPct}% · Compat:${item.compatPct}%</span>
        </div>
      </div>
      <div class="rank-bar-container">
        <div class="rank-bar-track">
          <div class="rank-bar-fill ${barClass}" id="bar-${idx}" style="width:0%"></div>
        </div>
        <div class="rank-score" style="color:${scoreColor}">${hybridPct}%</div>
      </div>
    `;
    rankList.appendChild(li);

    // Animate bars
    setTimeout(() => {
      const bar = $(`bar-${idx}`);
      if (bar) bar.style.width = hybridPct + '%';
    }, 200 + idx * 80);
  });

  // Show result section
  $('result-section').style.display = 'block';
  setTimeout(() => {
    $('result-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
}

function generateStrengths(frameworkName) {
  const info = FRAMEWORK_INFO[frameworkName];
  if (!info) return ['Framework yang sesuai dengan profil proyek Anda'];

  const ans = state.answers;
  const custom = [];

  // Context-aware strength generation
  if (ans[2] === 1 && (frameworkName === 'Django' || frameworkName === 'FastAPI' || frameworkName === 'Flask')) {
    custom.push('Sesuai dengan pengalaman Python tim Anda');
  }
  if (ans[2] === 2 && (frameworkName === 'Laravel' || frameworkName === 'Symfony')) {
    custom.push('Sesuai dengan pengalaman PHP tim Anda');
  }
  if (ans[2] === 3 && frameworkName === 'Spring Boot') {
    custom.push('Sesuai dengan pengalaman Java tim Anda');
  }
  if ((ans[2] === 4 || ans[2] === 5) && (frameworkName === 'Next.js' || frameworkName === 'Express.js')) {
    custom.push('Sesuai dengan pengalaman JavaScript/TypeScript tim Anda');
  }
  if (ans[2] === 6 && frameworkName === 'Ruby on Rails') {
    custom.push('Sesuai dengan pengalaman Ruby tim Anda');
  }
  if (ans[4] === 1 && frameworkName === 'Spring Boot') {
    custom.push('Mendukung containerization Docker dengan baik');
  }
  if (ans[5] === 1) {
    custom.push('Memiliki integrasi CI/CD yang baik dengan berbagai platform');
  }
  if (ans[1] === 2 && frameworkName === 'FastAPI') {
    custom.push('Didesain khusus untuk membangun API berkinerja tinggi');
  }
  if (ans[1] === 2 && frameworkName === 'Express.js') {
    custom.push('Standar de-facto untuk REST API dengan Node.js');
  }
  if (ans[9] >= 4 && frameworkName === 'Spring Boot') {
    custom.push('Terbukti untuk skalabilitas enterprise skala besar');
  }

  // Merge with static strengths
  const staticStrengths = info.strengths.slice(0, 3);
  const allStrengths = [...new Set([...custom, ...staticStrengths])];
  return allStrengths.slice(0, 4);
}

function generateUseCaseTags(frameworkName, info) {
  if (!info.useCases) return '';
  return info.useCases.map(uc =>
    `<span style="display:inline-block;background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2);color:var(--accent-light);font-size:0.72rem;padding:3px 8px;border-radius:4px;margin:2px">${uc}</span>`
  ).join('');
}

function generateExplanation(frameworkName, answers) {
  const appType = APP_TYPE_LABELS[answers[1]] || 'aplikasi';
  const lang = LANG_LABELS[answers[2]] || 'pemrograman yang dipilih';
  const db = DB_LABELS[answers[3]] || 'database';

  const contribLabels = { 1: 'solo developer', 2: 'tim kecil (2-3 orang)', 3: 'tim menengah (4-10 orang)', 4: 'tim besar (10+ orang)' };
  const contrib = contribLabels[answers[8]] || 'tim';

  const userLabels = { 1: 'pengguna sangat kecil (<100)', 2: 'pengguna kecil (100-1K)', 3: 'pengguna menengah (1K-10K)', 4: 'pengguna besar (10K-100K)', 5: 'pengguna sangat besar (>100K)' };
  const users = userLabels[answers[9]] || 'pengguna';

  const docker = answers[4] === 1 ? 'dengan dukungan containerization Docker' : 'tanpa containerization';
  const cicd = answers[5] === 1 ? ', CI/CD pipeline' : '';
  const tests = answers[6] === 1 ? ', dan automated testing' : '';

  return `<strong>${frameworkName}</strong> direkomendasikan sebagai pilihan utama berdasarkan profil proyek Anda: <strong>${appType}</strong> menggunakan bahasa <strong>${lang}</strong> dengan database <strong>${db}</strong>, dikembangkan oleh <strong>${contrib}</strong> untuk skala <strong>${users}</strong>. Proyek ini akan berjalan ${docker}${cicd}${tests}. Kombinasi faktor-faktor ini menghasilkan kecocokan tertinggi dengan karakteristik dan ekosistem ${frameworkName}.`;
}

function animateNumber(id, from, to, duration) {
  const el = $(id);
  if (!el) return;
  const start = performance.now();
  const update = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
    el.textContent = Math.round(from + (to - from) * ease);
    if (progress < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// ============================================================
// ABOUT — FRAMEWORK SHOWCASE
// ============================================================

function renderFrameworksShowcase() {
  const grid = $('frameworks-grid');
  if (!grid) return;

  const frameworkColors = {
    'Django': '#44B78B',
    'FastAPI': '#00BFA5',
    'Ruby on Rails': '#E0524C',
    'Next.js': '#94A3B8',
    'Flask': '#94A3B8',
    'Spring Boot': '#6DB33F',
    'Laravel': '#FF6B6B',
    'Symfony': '#AAAAAA',
    'Express.js': '#68A063'
  };

  const langIcons = {
    'Django': '🐍', 'FastAPI': '🐍', 'Flask': '🐍',
    'Ruby on Rails': '💎',
    'Next.js': '🔷', 'Express.js': '🟨',
    'Spring Boot': '☕',
    'Laravel': '🐘', 'Symfony': '🐘'
  };

  Object.entries(FRAMEWORK_MAP).forEach(([id, name]) => {
    const chip = document.createElement('div');
    chip.className = 'fw-chip';
    chip.innerHTML = `
      <div class="fw-dot" style="background:${frameworkColors[name] || '#7C3AED'}"></div>
      ${langIcons[name] || '⚙️'} ${name}
    `;
    grid.appendChild(chip);
  });
}

// ============================================================
// NAVBAR SCROLL EFFECT
// ============================================================

function setupNavbar() {
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    navbar.classList.toggle('scrolled', window.scrollY > 30);

    // Active nav link
    const sections = ['hero', 'form-section', 'about-section'];
    let current = '';
    sections.forEach(id => {
      const el = $(id);
      if (el && el.getBoundingClientRect().top <= 80) current = id;
    });

    document.querySelectorAll('.nav-link').forEach(link => {
      const href = link.getAttribute('href').replace('#', '');
      link.classList.toggle('active', href === current);
    });
  }, { passive: true });
}

// ============================================================
// RESET
// ============================================================

function resetForm() {
  state.answers = {};

  // Clear all radio selections
  document.querySelectorAll('.option-card').forEach(card => {
    card.classList.remove('selected');
  });
  document.querySelectorAll('input[type="radio"]').forEach(input => {
    input.checked = false;
  });

  // Clear card answered states
  document.querySelectorAll('.question-card').forEach(card => {
    card.classList.remove('answered');
  });

  // Hide results
  $('result-section').style.display = 'none';

  updateProgress();

  // Scroll to form
  $('form-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================================
// MODEL LOADING
// ============================================================

async function loadModel() {
  const overlay = $('loading-overlay');
  const progressText = $('loading-progress-text');

  try {
    // Show loading overlay
    overlay.style.display = 'flex';

    const response = await fetch('rf_model.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}: Cannot load rf_model.json`);

    // Stream and track loading
    const contentLength = response.headers.get('Content-Length');
    const total = contentLength ? parseInt(contentLength) : null;
    let loaded = 0;

    const reader = response.body.getReader();
    const chunks = [];

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      loaded += value.length;
      if (total && progressText) {
        const pct = Math.round((loaded / total) * 100);
        progressText.textContent = `${pct}%`;
      }
    }

    const blob = new Blob(chunks);
    const text = await blob.text();

    if (progressText) progressText.textContent = 'parsing...';

    const modelData = JSON.parse(text);

    state.rfModel = new RandomForestInference(modelData);
    state.modelLoaded = true;

    console.log(`✅ Model loaded: ${modelData.n_estimators} trees, ${modelData.n_classes} classes`);

    // Small delay to show "done"
    if (progressText) progressText.textContent = `${modelData.n_estimators} pohon siap!`;
    await new Promise(r => setTimeout(r, 500));

    overlay.style.display = 'none';
    updateProgress(); // Re-check if analyze button should be enabled

  } catch (err) {
    console.error('Failed to load model:', err);
    overlay.innerHTML = `
      <div class="loading-content">
        <div style="font-size:2rem">⚠️</div>
        <p class="loading-text">Gagal memuat model</p>
        <p class="loading-sub">${err.message}</p>
        <p style="color:var(--text-muted);font-size:0.8rem;margin-top:8px">Pastikan file rf_model.json ada di folder yang sama</p>
        <button onclick="location.reload()" style="margin-top:16px;padding:10px 24px;background:var(--primary);color:white;border:none;border-radius:8px;cursor:pointer;font-size:0.9rem">Coba Lagi</button>
      </div>
    `;
  }
}

// ============================================================
// NOTIFICATION
// ============================================================

function showNotification(message, type = 'info') {
  const existing = document.querySelector('.notification');
  if (existing) existing.remove();

  const n = document.createElement('div');
  n.className = 'notification';
  const colors = { info: '#7C3AED', warning: '#F59E0B', error: '#EF4444', success: '#10B981' };
  n.style.cssText = `
    position:fixed;bottom:24px;right:24px;background:var(--bg-card);
    border:1px solid ${colors[type]};color:var(--text-primary);
    padding:14px 20px;border-radius:var(--radius-md);font-size:0.875rem;
    z-index:9999;animation:fadeUp 0.3s ease both;max-width:320px;
    box-shadow:0 4px 24px rgba(0,0,0,0.4)
  `;
  n.textContent = message;
  document.body.appendChild(n);
  setTimeout(() => n.remove(), 4000);
}

// ============================================================
// MAIN INIT
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  // Initialize UI
  initProgressSteps();
  setupOptionListeners();
  setupNavbar();
  renderFrameworksShowcase();
  updateProgress();

  // Analyze button
  $('btn-analyze').addEventListener('click', runAnalysis);

  // Reset button
  $('btn-reset').addEventListener('click', resetForm);

  // Hero CTA
  $('btn-mulai')?.addEventListener('click', (e) => {
    e.preventDefault();
    $('form-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  // Load the RF model
  loadModel();
});
