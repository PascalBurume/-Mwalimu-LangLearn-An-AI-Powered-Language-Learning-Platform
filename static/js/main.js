/**
 * Mwalimu-LangLearn · main.js
 * Compiled from static/ts/main.ts
 * To recompile: tsc --target ES2020 --lib ES2020,DOM --strict --outDir static/js static/ts/main.ts
 */
"use strict";

// ── Particle System ──────────────────────────────────────────────────────────
class ParticleSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.particles = [];
    this.animId = 0;
    this.COUNT = 70;
    this.CONNECT_DIST = 130;
    this.COLORS = ['#7c6dfa','#ff6b6b','#f6c90e','#22d3ee','#34d399'];
    this.ctx = canvas.getContext('2d');
    this.resize();
    this.init();
    window.addEventListener('resize', () => this.resize(), { passive: true });
    this.loop();
  }
  resize() {
    this.canvas.width  = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }
  rand(min, max) { return Math.random() * (max - min) + min; }
  init() {
    this.particles = Array.from({ length: this.COUNT }, () => ({
      x:       this.rand(0, this.canvas.width),
      y:       this.rand(0, this.canvas.height),
      vx:      this.rand(-0.25, 0.25),
      vy:      this.rand(-0.25, 0.25),
      size:    this.rand(1.2, 2.8),
      opacity: this.rand(0.3, 0.8),
      color:   this.COLORS[Math.floor(Math.random() * this.COLORS.length)],
    }));
  }
  draw() {
    const { ctx, canvas, particles } = this;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < this.CONNECT_DIST) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(124,109,250,${0.1 * (1 - dist / this.CONNECT_DIST)})`;
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }
    for (const p of particles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = p.color + Math.round(p.opacity * 255).toString(16).padStart(2,'0');
      ctx.fill();
    }
  }
  update() {
    const { canvas, particles } = this;
    for (const p of particles) {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width)  p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
    }
  }
  loop() {
    this.draw(); this.update();
    this.animId = requestAnimationFrame(() => this.loop());
  }
  destroy() { cancelAnimationFrame(this.animId); }
}

// ── Tab Manager ──────────────────────────────────────────────────────────────
class TabManager {
  constructor() {
    this.current = 'writing';
    this.buttons = document.querySelectorAll('.tab-btn');
    this.panels  = document.querySelectorAll('.tab-panel');
    this.ink     = document.getElementById('tab-ink');
    this.init();
  }
  init() {
    this.buttons.forEach(btn => {
      btn.addEventListener('click', () => this.switchTo(btn.dataset.tab));
    });
    const active = document.querySelector('.tab-btn.active');
    if (active) this.moveInk(active);
  }
  switchTo(tabId) {
    if (tabId === this.current) return;
    this.current = tabId;
    this.buttons.forEach(btn => {
      const isActive = btn.dataset.tab === tabId;
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', String(isActive));
      if (isActive) this.moveInk(btn);
    });
    this.panels.forEach(panel => {
      const isActive = panel.id === `tab-${tabId}`;
      if (isActive) {
        panel.style.display = 'block';
        void panel.offsetWidth;
        panel.classList.add('active');
      } else {
        panel.classList.remove('active');
        panel.style.display = 'none';
      }
    });
  }
  moveInk(btn) {
    const rect    = btn.getBoundingClientRect();
    const navRect = btn.parentElement.getBoundingClientRect();
    this.ink.style.left  = `${rect.left - navRect.left}px`;
    this.ink.style.width = `${rect.width}px`;
  }
}

// ── Typewriter Effect ────────────────────────────────────────────────────────
class TypewriterEffect {
  constructor() { this.interval = null; }
  stream(container, markdown, onDone) {
    this.cancel();
    container.innerHTML = marked.parse(markdown);
    const allText = container.querySelectorAll('p, li, h1, h2, h3, h4, td, th, blockquote');
    allText.forEach((el, i) => {
      el.style.opacity   = '0';
      el.style.transform = 'translateY(8px)';
      el.style.transition = `opacity 0.25s ease ${i * 0.04}s, transform 0.25s ease ${i * 0.04}s`;
    });
    requestAnimationFrame(() => {
      allText.forEach(el => {
        el.style.opacity   = '1';
        el.style.transform = 'translateY(0)';
      });
    });
    const duration = Math.min(allText.length * 40 + 300, 2000);
    this.interval = setTimeout(() => { onDone?.(); }, duration);
  }
  cancel() {
    if (this.interval !== null) { clearTimeout(this.interval); this.interval = null; }
  }
}

// ── Image Uploader ───────────────────────────────────────────────────────────
class ImageUploader {
  constructor(dropZoneId, fileInputId, previewId) {
    this.currentB64 = null;
    this.dropZone  = document.getElementById(dropZoneId);
    this.fileInput = document.getElementById(fileInputId);
    this.preview   = document.getElementById(previewId);
    this.bind();
  }
  bind() {
    this.fileInput.addEventListener('change', e => {
      const file = e.target.files?.[0];
      if (file) this.load(file);
    });
    this.dropZone.addEventListener('dragover', e => {
      e.preventDefault();
      this.dropZone.classList.add('dragging');
    });
    this.dropZone.addEventListener('dragleave', () => {
      this.dropZone.classList.remove('dragging');
    });
    this.dropZone.addEventListener('drop', e => {
      e.preventDefault();
      this.dropZone.classList.remove('dragging');
      const file = e.dataTransfer?.files?.[0];
      if (file && file.type.startsWith('image/')) this.load(file);
    });
  }
  load(file) {
    const reader = new FileReader();
    reader.onload = ev => {
      const dataUrl   = ev.target.result;
      this.currentB64 = dataUrl.split(',')[1];
      this.preview.src = dataUrl;
      this.preview.classList.remove('hidden');
      this.dropZone.classList.add('has-image');
    };
    reader.readAsDataURL(file);
  }
  getBase64() { return this.currentB64; }
  reset() {
    this.currentB64 = null;
    this.preview.src = '';
    this.preview.classList.add('hidden');
    this.dropZone.classList.remove('has-image');
    this.fileInput.value = '';
  }
}

// ── Chat Manager ─────────────────────────────────────────────────────────────
class ChatManager {
  constructor(windowId, emptyId) {
    this.typingRow = null;
    this.history   = '';
    this.window     = document.getElementById(windowId);
    this.emptyState = document.getElementById(emptyId);
  }
  addUserBubble(text) {
    this.hideEmpty();
    this.window.appendChild(this.createBubbleRow('user', '🧑‍🎓', text, undefined, false));
    this.scroll();
  }
  addAIBubble(markdown, timing) {
    this.removeTyping();
    this.window.appendChild(this.createBubbleRow('ai', '🤖', markdown, timing, true));
    this.scroll();
  }
  showTyping() {
    this.removeTyping();
    const row = document.createElement('div');
    row.className = 'bubble-row';
    row.innerHTML = `
      <div class="bubble-avatar">🤖</div>
      <div class="typing-indicator">
        <span></span><span></span><span></span>
      </div>`;
    this.typingRow = row;
    this.window.appendChild(row);
    this.scroll();
  }
  removeTyping() { this.typingRow?.remove(); this.typingRow = null; }
  reset() {
    this.history = '';
    this.window.querySelectorAll('.bubble-row').forEach(r => r.remove());
    this.emptyState.style.display = '';
  }
  setHistory(h) { this.history = h; }
  getHistory()  { return this.history; }
  hideEmpty()   { this.emptyState.style.display = 'none'; }
  createBubbleRow(role, avatar, content, timing, isMarkdown) {
    const row  = document.createElement('div');
    row.className = `bubble-row bubble-row--${role}`;
    const now  = new Date().toLocaleTimeString('en', { hour:'2-digit', minute:'2-digit' });
    const inner = isMarkdown ? marked.parse(content) : escapeHtml(content);
    row.innerHTML = `
      <div class="bubble-avatar">${avatar}</div>
      <div class="bubble bubble--${role}">
        <div class="markdown-body">${inner}</div>
        <div class="bubble-time">${timing ? timing + ' · ' : ''}${now}</div>
      </div>`;
    return row;
  }
  scroll() { requestAnimationFrame(() => { this.window.scrollTop = this.window.scrollHeight; }); }
}

// ── Counter Animation ────────────────────────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target  = parseInt(el.dataset.count, 10);
    let current   = 0;
    const step    = Math.ceil(target / 20);
    const id      = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = String(current);
      if (current >= target) clearInterval(id);
    }, 60);
  });
}

// ── Utilities ────────────────────────────────────────────────────────────────
function $(id) { return document.getElementById(id); }

function escapeHtml(str) {
  return str
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;');
}

function showToast(message, type = 'info') {
  const icons = { success:'✅', error:'❌', info:'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type]}</span><span>${escapeHtml(message)}</span>`;
  $('toast-container').appendChild(toast);
  setTimeout(() => toast.remove(), 4200);
}

function setLoading(show, text = 'Thinking…') {
  $('loader-text').textContent = text;
  $('loading-overlay').classList.toggle('hidden', !show);
}

async function apiPost(endpoint, payload) {
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
    throw new Error(err.error ?? `HTTP ${res.status}`);
  }
  return res.json();
}

function showResult(cardId, outputId, timingId, result, timing) {
  const card = $(cardId);
  card.classList.remove('hidden');
  $(timingId).textContent = timing;
  new TypewriterEffect().stream($(outputId), result);
}

function setButtonLoading(btn, loading) {
  btn.disabled = loading;
  btn.classList.toggle('loading', loading);
}

// ── Main Application ─────────────────────────────────────────────────────────
class MwalimuApp {
  constructor() {
    this.tabs      = new TabManager();
    this.uploader  = new ImageUploader('drop-zone','visual-file','drop-preview');
    this.chat      = new ChatManager('chat-window','chat-empty');
    this.particles = new ParticleSystem(document.getElementById('particle-canvas'));
    this.initStatus();
    this.initWriting();
    this.initVisual();
    this.initTranslation();
    this.initVocabulary();
    this.initConversation();
    animateCounters();
  }

  // ── Status ───────────────────────────────────────────────────
  async initStatus() {
    try {
      const data = await (await fetch('/api/status')).json();
      const dot  = $('status-dot'), text = $('status-text');
      if (data.connected) {
        dot.classList.add('connected');
        text.textContent = `Connected · ${data.current_model}`;
      } else {
        dot.classList.add('disconnected');
        text.textContent = 'Ollama not reachable — run: ollama serve';
      }
    } catch {
      $('status-dot').classList.add('disconnected');
      $('status-text').textContent = 'Could not reach server';
    }
  }

  // ── Tab 1: Writing ───────────────────────────────────────────
  initWriting() {
    document.querySelectorAll('[data-feature="writing"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        $('writing-text').value = chip.dataset.text;
        $('writing-lang').value = chip.dataset.lang;
        $('writing-level').value = chip.dataset.level;
      });
    });
    const btn = $('writing-submit');
    btn.addEventListener('click', async () => {
      const text  = $('writing-text').value.trim();
      const lang  = $('writing-lang').value;
      const level = $('writing-level').value;
      if (!text) { showToast('Please enter some text to analyse.','error'); return; }
      setButtonLoading(btn, true);
      setLoading(true, 'Analysing your writing…');
      try {
        const data = await apiPost('/api/writing', { text, language: lang, level });
        showResult('writing-result','writing-output','writing-timing', data.result, data.timing);
      } catch(e) { showToast(e.message, 'error'); }
      finally { setButtonLoading(btn, false); setLoading(false); }
    });
  }

  // ── Tab 2: Visual ────────────────────────────────────────────
  initVisual() {
    const btn = $('visual-submit');
    btn.addEventListener('click', async () => {
      const b64 = this.uploader.getBase64();
      if (!b64) { showToast('Please upload an image first.','error'); return; }
      const target = $('visual-target').value;
      const source = $('visual-source').value;
      setButtonLoading(btn, true);
      setLoading(true, 'Identifying objects…');
      try {
        const data = await apiPost('/api/visual',{ image_b64:b64, target_language:target, source_language:source });
        showResult('visual-result','visual-output','visual-timing', data.result, data.timing);
      } catch(e) { showToast(e.message,'error'); }
      finally { setButtonLoading(btn, false); setLoading(false); }
    });
  }

  // ── Tab 3: Translation ───────────────────────────────────────
  initTranslation() {
    const srcSel  = $('trans-source-lang');
    const tgtSel  = $('trans-target-lang');
    const fromTag = $('trans-from-tag');
    const toTag   = $('trans-to-tag');
    const sync    = () => { fromTag.textContent = srcSel.value; toTag.textContent = tgtSel.value; };
    srcSel.addEventListener('change', sync);
    tgtSel.addEventListener('change', sync);

    $('trans-swap').addEventListener('click', () => {
      [srcSel.value, tgtSel.value] = [tgtSel.value, srcSel.value];
      const orig = $('trans-original'), stu = $('trans-student');
      [orig.value, stu.value] = [stu.value, orig.value];
      sync();
    });

    document.querySelectorAll('[data-feature="translation"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        $('trans-original').value  = chip.dataset.original;
        $('trans-student').value   = chip.dataset.student;
        srcSel.value = chip.dataset.src;
        tgtSel.value = chip.dataset.tgt;
        $('trans-level').value = chip.dataset.level;
        sync();
      });
    });

    const btn = $('translation-submit');
    btn.addEventListener('click', async () => {
      const original   = $('trans-original').value.trim();
      const studentTr  = $('trans-student').value.trim();
      const srcLang    = srcSel.value;
      const tgtLang    = tgtSel.value;
      const level      = $('trans-level').value;
      if (!original || !studentTr) { showToast('Please provide both texts.','error'); return; }
      setButtonLoading(btn, true);
      setLoading(true, 'Checking your translation…');
      try {
        const data = await apiPost('/api/translation',{
          original, student_translation: studentTr, source_lang: srcLang, target_lang: tgtLang, level,
        });
        showResult('translation-result','translation-output','translation-timing', data.result, data.timing);
      } catch(e) { showToast(e.message,'error'); }
      finally { setButtonLoading(btn, false); setLoading(false); }
    });
  }

  // ── Tab 4: Vocabulary ────────────────────────────────────────
  initVocabulary() {
    const rangeInput = $('vocab-num');
    const display    = $('vocab-num-display');
    rangeInput.addEventListener('input', () => { display.textContent = rangeInput.value; });

    document.querySelectorAll('[data-feature="vocab"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        $('vocab-topic').value  = chip.dataset.topic;
        $('vocab-lang').value   = chip.dataset.lang;
        $('vocab-level').value  = chip.dataset.level;
      });
    });

    const btn = $('vocabulary-submit');
    btn.addEventListener('click', async () => {
      const topic  = $('vocab-topic').value.trim();
      const lang   = $('vocab-lang').value;
      const level  = $('vocab-level').value;
      const numW   = parseInt(rangeInput.value, 10);
      if (!topic) { showToast('Please enter a topic.','error'); return; }
      setButtonLoading(btn, true);
      setLoading(true, `Building ${lang} vocabulary…`);
      try {
        const data = await apiPost('/api/vocabulary',{ topic, language: lang, level, num_words: numW });
        showResult('vocabulary-result','vocabulary-output','vocabulary-timing', data.result, data.timing);
      } catch(e) { showToast(e.message,'error'); }
      finally { setButtonLoading(btn, false); setLoading(false); }
    });
  }

  // ── Tab 5: Conversation ──────────────────────────────────────
  initConversation() {
    const inputEl  = $('convo-input');
    const sendBtn  = $('convo-submit');
    const resetBtn = $('convo-reset');

    const sendMessage = async () => {
      const message  = inputEl.value.trim();
      const scenario = $('convo-scenario').value;
      const lang     = $('convo-lang').value;
      const level    = $('convo-level').value;
      if (!message) { showToast('Please type a message.','error'); return; }
      inputEl.value = '';
      inputEl.style.height = 'auto';
      sendBtn.disabled = true;
      this.chat.addUserBubble(message);
      this.chat.showTyping();
      try {
        const data = await apiPost('/api/conversation',{
          message, scenario, language: lang, level, history: this.chat.getHistory(),
        });
        this.chat.setHistory(data.history ?? '');
        this.chat.addAIBubble(data.result, data.timing);
        const t = $('convo-timing');
        t.textContent = data.timing;
        t.classList.remove('hidden');
      } catch(e) {
        this.chat.removeTyping();
        showToast(e.message,'error');
      } finally {
        sendBtn.disabled = false;
        inputEl.focus();
      }
    };

    sendBtn.addEventListener('click', sendMessage);

    inputEl.addEventListener('keydown', e => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
    });

    inputEl.addEventListener('input', () => {
      inputEl.style.height = 'auto';
      inputEl.style.height = `${Math.min(inputEl.scrollHeight, 140)}px`;
    });

    resetBtn.addEventListener('click', () => {
      this.chat.reset();
      $('convo-timing').classList.add('hidden');
      showToast('Conversation reset. Start fresh!', 'success');
    });
  }
}

// ── Bootstrap ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => { new MwalimuApp(); });