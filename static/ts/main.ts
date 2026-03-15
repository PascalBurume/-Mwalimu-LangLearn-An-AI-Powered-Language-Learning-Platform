/**
 * Mwalimu-LangLearn · main.ts
 * ────────────────────────────
 * TypeScript source for the animated Flask front-end.
 * Compile:  tsc --target ES2020 --lib ES2020,DOM --strict --outDir ../js static/ts/main.ts
 *
 * Modules:
 *   ParticleSystem   – canvas constellation background
 *   TabManager       – animated ink-bar tab switching
 *   TypewriterEffect – streams text character-by-character
 *   ImageUploader    – drag-and-drop image handler
 *   ChatManager      – conversation bubble state
 *   CounterAnimation – number count-up in hero stats
 *   MwalimuApp       – wires everything together + API calls
 */

// ── Type declarations ────────────────────────────────────────────────────────

declare const marked: { parse(src: string): string };

interface ApiWritingPayload   { text: string; language: string; level: string; }
interface ApiVisualPayload    { image_b64: string; target_language: string; source_language: string; }
interface ApiTranslationPayload { original: string; student_translation: string; source_lang: string; target_lang: string; level: string; }
interface ApiVocabPayload     { topic: string; language: string; level: string; num_words: number; }
interface ApiConvoPayload     { message: string; scenario: string; language: string; level: string; history: string; }

interface ApiResponse {
  result: string;
  timing: string;
  history?: string;
  error?: string;
  connected?: boolean;
  models?: string[];
  current_model?: string;
  has_vision?: boolean;
}

interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  size: number;
  opacity: number;
  color: string;
}

declare global {
  interface Window {
    MWALIMU_CONFIG: { hasVision: boolean; model: string; };
  }
}

// ── Particle System ──────────────────────────────────────────────────────────

class ParticleSystem {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private particles: Particle[] = [];
  private animId = 0;
  private readonly COUNT = 70;
  private readonly CONNECT_DIST = 130;
  private readonly COLORS = ['#7c6dfa', '#ff6b6b', '#f6c90e', '#22d3ee', '#34d399'];

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d')!;
    this.resize();
    this.init();
    window.addEventListener('resize', () => this.resize(), { passive: true });
    this.loop();
  }

  private resize(): void {
    this.canvas.width  = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  private rand(min: number, max: number): number {
    return Math.random() * (max - min) + min;
  }

  private init(): void {
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

  private draw(): void {
    const { ctx, canvas, particles } = this;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw connections
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
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

    // Draw particles
    for (const p of particles) {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = p.color + Math.round(p.opacity * 255).toString(16).padStart(2, '0');
      ctx.fill();
    }
  }

  private update(): void {
    const { canvas, particles } = this;
    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > canvas.width)  p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
    }
  }

  private loop(): void {
    this.draw();
    this.update();
    this.animId = requestAnimationFrame(() => this.loop());
  }

  destroy(): void {
    cancelAnimationFrame(this.animId);
  }
}

// ── Tab Manager ──────────────────────────────────────────────────────────────

class TabManager {
  private buttons: NodeListOf<HTMLButtonElement>;
  private panels: NodeListOf<HTMLElement>;
  private ink: HTMLElement;
  private current = 'writing';

  constructor() {
    this.buttons = document.querySelectorAll<HTMLButtonElement>('.tab-btn');
    this.panels  = document.querySelectorAll<HTMLElement>('.tab-panel');
    this.ink     = document.getElementById('tab-ink')!;
    this.init();
  }

  private init(): void {
    this.buttons.forEach(btn => {
      btn.addEventListener('click', () => this.switchTo(btn.dataset.tab!));
    });
    // Position ink bar on the initial active tab
    const active = document.querySelector<HTMLButtonElement>('.tab-btn.active');
    if (active) this.moveInk(active);
  }

  switchTo(tabId: string): void {
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
        // Trigger reflow then animate
        void panel.offsetWidth;
        panel.classList.add('active');
      } else {
        panel.classList.remove('active');
        panel.style.display = 'none';
      }
    });
  }

  private moveInk(btn: HTMLButtonElement): void {
    const rect  = btn.getBoundingClientRect();
    const navRect = btn.parentElement!.getBoundingClientRect();
    this.ink.style.left  = `${rect.left - navRect.left}px`;
    this.ink.style.width = `${rect.width}px`;
  }
}

// ── Typewriter Effect ────────────────────────────────────────────────────────

class TypewriterEffect {
  private interval: number | null = null;

  /**
   * Render markdown in target but reveal characters one by one.
   * We render the full markdown upfront, then fade-in via a CSS trick.
   */
  stream(container: HTMLElement, markdown: string, onDone?: () => void): void {
    this.cancel();

    // Render markdown immediately
    container.innerHTML = marked.parse(markdown);

    // Collect all text nodes and briefly hide them with opacity animation
    const allText = container.querySelectorAll<HTMLElement>('p, li, h1, h2, h3, h4, td, th, blockquote');
    allText.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(8px)';
      el.style.transition = `opacity 0.25s ease ${i * 0.04}s, transform 0.25s ease ${i * 0.04}s`;
    });

    // Trigger the reveal
    requestAnimationFrame(() => {
      allText.forEach(el => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      });
    });

    // Callback after last element
    const duration = Math.min(allText.length * 40 + 300, 2000);
    this.interval = window.setTimeout(() => {
      onDone?.();
    }, duration);
  }

  cancel(): void {
    if (this.interval !== null) {
      clearTimeout(this.interval);
      this.interval = null;
    }
  }
}

// ── Image Uploader ───────────────────────────────────────────────────────────

class ImageUploader {
  private dropZone: HTMLElement;
  private fileInput: HTMLInputElement;
  private preview: HTMLImageElement;
  private currentB64: string | null = null;

  constructor(
    private dropZoneId: string,
    private fileInputId: string,
    private previewId: string,
  ) {
    this.dropZone  = document.getElementById(dropZoneId)!;
    this.fileInput = document.getElementById(fileInputId) as HTMLInputElement;
    this.preview   = document.getElementById(previewId) as HTMLImageElement;
    this.bind();
  }

  private bind(): void {
    this.fileInput.addEventListener('change', e => {
      const file = (e.target as HTMLInputElement).files?.[0];
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

  private load(file: File): void {
    const reader = new FileReader();
    reader.onload = ev => {
      const dataUrl = ev.target?.result as string;
      this.currentB64 = dataUrl.split(',')[1];      // strip data:image/...;base64,
      this.preview.src = dataUrl;
      this.preview.classList.remove('hidden');
      this.dropZone.classList.add('has-image');
    };
    reader.readAsDataURL(file);
  }

  getBase64(): string | null {
    return this.currentB64;
  }

  reset(): void {
    this.currentB64 = null;
    this.preview.src = '';
    this.preview.classList.add('hidden');
    this.dropZone.classList.remove('has-image');
    this.fileInput.value = '';
  }
}

// ── Chat Manager ─────────────────────────────────────────────────────────────

class ChatManager {
  private window: HTMLElement;
  private emptyState: HTMLElement;
  private history = '';
  private typingRow: HTMLElement | null = null;

  constructor(private windowId: string, private emptyId: string) {
    this.window     = document.getElementById(windowId)!;
    this.emptyState = document.getElementById(emptyId)!;
  }

  addUserBubble(text: string): void {
    this.hideEmpty();
    const row = this.createBubbleRow('user', '🧑‍🎓', text);
    this.window.appendChild(row);
    this.scroll();
  }

  addAIBubble(markdown: string, timing: string): void {
    this.removeTyping();
    const row = this.createBubbleRow('ai', '🤖', markdown, timing, true);
    this.window.appendChild(row);
    this.scroll();
  }

  showTyping(): void {
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

  removeTyping(): void {
    this.typingRow?.remove();
    this.typingRow = null;
  }

  reset(): void {
    this.history = '';
    // Clear all bubble rows
    const rows = this.window.querySelectorAll('.bubble-row');
    rows.forEach(r => r.remove());
    this.emptyState.style.display = '';
  }

  setHistory(h: string): void {
    this.history = h;
  }

  getHistory(): string {
    return this.history;
  }

  private hideEmpty(): void {
    this.emptyState.style.display = 'none';
  }

  private createBubbleRow(
    role: 'user' | 'ai',
    avatar: string,
    content: string,
    timing?: string,
    isMarkdown = false,
  ): HTMLElement {
    const row = document.createElement('div');
    row.className = `bubble-row bubble-row--${role}`;

    const now = new Date().toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' });
    const inner = isMarkdown ? marked.parse(content) : escapeHtml(content);

    row.innerHTML = `
      <div class="bubble-avatar">${avatar}</div>
      <div class="bubble bubble--${role}">
        <div class="markdown-body">${inner}</div>
        <div class="bubble-time">${timing ? timing + ' · ' : ''}${now}</div>
      </div>`;

    return row;
  }

  private scroll(): void {
    requestAnimationFrame(() => {
      this.window.scrollTop = this.window.scrollHeight;
    });
  }
}

// ── Counter Animation ────────────────────────────────────────────────────────

function animateCounters(): void {
  const els = document.querySelectorAll<HTMLElement>('[data-count]');
  els.forEach(el => {
    const target = parseInt(el.dataset.count!, 10);
    let current = 0;
    const step = Math.ceil(target / 20);
    const id = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = String(current);
      if (current >= target) clearInterval(id);
    }, 60);
  });
}

// ── Utilities ────────────────────────────────────────────────────────────────

function $(id: string): HTMLElement {
  return document.getElementById(id)!;
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function showToast(message: string, type: 'success' | 'error' | 'info' = 'info'): void {
  const container = $('toast-container');
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${icons[type]}</span><span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4200);
}

function setLoading(show: boolean, text = 'Thinking…'): void {
  const overlay = $('loading-overlay') as HTMLElement;
  const loaderText = $('loader-text');
  if (show) {
    loaderText.textContent = text;
    overlay.classList.remove('hidden');
  } else {
    overlay.classList.add('hidden');
  }
}

async function apiPost<T extends object>(
  endpoint: string,
  payload: T,
): Promise<ApiResponse> {
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

function showResult(
  cardId: string,
  outputId: string,
  timingId: string,
  result: string,
  timing: string,
): void {
  const card = $(cardId);
  const output = $(outputId);
  const timingEl = $(timingId);
  card.classList.remove('hidden');
  timingEl.textContent = timing;
  new TypewriterEffect().stream(output, result);
}

function setButtonLoading(btn: HTMLButtonElement, loading: boolean): void {
  btn.disabled = loading;
  btn.classList.toggle('loading', loading);
}

// ── Main Application ─────────────────────────────────────────────────────────

class MwalimuApp {
  private tabs: TabManager;
  private uploader: ImageUploader;
  private chat: ChatManager;
  private particles: ParticleSystem;

  constructor() {
    this.tabs     = new TabManager();
    this.uploader = new ImageUploader('drop-zone', 'visual-file', 'drop-preview');
    this.chat     = new ChatManager('chat-window', 'chat-empty');
    this.particles = new ParticleSystem(
      document.getElementById('particle-canvas') as HTMLCanvasElement,
    );

    this.initStatus();
    this.initWriting();
    this.initVisual();
    this.initTranslation();
    this.initVocabulary();
    this.initConversation();
    animateCounters();
  }

  // ── Connection status ────────────────────────────────────────
  private async initStatus(): Promise<void> {
    try {
      const res = await fetch('/api/status');
      const data: ApiResponse = await res.json();
      const dot  = $('status-dot');
      const text = $('status-text');
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
  private initWriting(): void {
    // Example chips
    document.querySelectorAll<HTMLButtonElement>('[data-feature="writing"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        (document.getElementById('writing-text') as HTMLTextAreaElement).value = chip.dataset.text!;
        (document.getElementById('writing-lang') as HTMLSelectElement).value  = chip.dataset.lang!;
        (document.getElementById('writing-level') as HTMLSelectElement).value = chip.dataset.level!;
      });
    });

    const btn = document.getElementById('writing-submit') as HTMLButtonElement;
    btn.addEventListener('click', async () => {
      const text  = ($('writing-text') as HTMLTextAreaElement).value.trim();
      const lang  = ($('writing-lang') as HTMLSelectElement).value;
      const level = ($('writing-level') as HTMLSelectElement).value;
      if (!text) { showToast('Please enter some text to analyse.', 'error'); return; }

      setButtonLoading(btn, true);
      setLoading(true, 'Analysing your writing…');
      try {
        const data = await apiPost<ApiWritingPayload>('/api/writing', { text, language: lang, level });
        showResult('writing-result', 'writing-output', 'writing-timing', data.result, data.timing);
      } catch (e: unknown) {
        showToast((e as Error).message, 'error');
      } finally {
        setButtonLoading(btn, false);
        setLoading(false);
      }
    });
  }

  // ── Tab 2: Visual ────────────────────────────────────────────
  private initVisual(): void {
    const btn = document.getElementById('visual-submit') as HTMLButtonElement;
    btn.addEventListener('click', async () => {
      const b64 = this.uploader.getBase64();
      if (!b64) { showToast('Please upload an image first.', 'error'); return; }
      const target = ($('visual-target') as HTMLSelectElement).value;
      const source = ($('visual-source') as HTMLSelectElement).value;

      setButtonLoading(btn, true);
      setLoading(true, 'Identifying objects…');
      try {
        const data = await apiPost<ApiVisualPayload>('/api/visual', {
          image_b64: b64, target_language: target, source_language: source,
        });
        showResult('visual-result', 'visual-output', 'visual-timing', data.result, data.timing);
      } catch (e: unknown) {
        showToast((e as Error).message, 'error');
      } finally {
        setButtonLoading(btn, false);
        setLoading(false);
      }
    });
  }

  // ── Tab 3: Translation ───────────────────────────────────────
  private initTranslation(): void {
    // Sync language tags with selects
    const srcSel = $('trans-source-lang') as HTMLSelectElement;
    const tgtSel = $('trans-target-lang') as HTMLSelectElement;
    const fromTag = $('trans-from-tag');
    const toTag   = $('trans-to-tag');

    const sync = (): void => {
      fromTag.textContent = srcSel.value;
      toTag.textContent   = tgtSel.value;
    };
    srcSel.addEventListener('change', sync);
    tgtSel.addEventListener('change', sync);

    // Swap button
    $('trans-swap').addEventListener('click', () => {
      [srcSel.value, tgtSel.value] = [tgtSel.value, srcSel.value];
      const orig    = $('trans-original') as HTMLTextAreaElement;
      const student = $('trans-student') as HTMLTextAreaElement;
      [orig.value, student.value] = [student.value, orig.value];
      sync();
    });

    // Example chips
    document.querySelectorAll<HTMLButtonElement>('[data-feature="translation"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        ($('trans-original') as HTMLTextAreaElement).value  = chip.dataset.original!;
        ($('trans-student') as HTMLTextAreaElement).value   = chip.dataset.student!;
        srcSel.value = chip.dataset.src!;
        tgtSel.value = chip.dataset.tgt!;
        ($('trans-level') as HTMLSelectElement).value = chip.dataset.level!;
        sync();
      });
    });

    const btn = $('translation-submit') as HTMLButtonElement;
    btn.addEventListener('click', async () => {
      const original    = ($('trans-original') as HTMLTextAreaElement).value.trim();
      const studentTr   = ($('trans-student') as HTMLTextAreaElement).value.trim();
      const srcLang     = srcSel.value;
      const tgtLang     = tgtSel.value;
      const level       = ($('trans-level') as HTMLSelectElement).value;
      if (!original || !studentTr) {
        showToast('Please provide both the original text and your translation.', 'error'); return;
      }

      setButtonLoading(btn, true);
      setLoading(true, 'Checking your translation…');
      try {
        const data = await apiPost<ApiTranslationPayload>('/api/translation', {
          original, student_translation: studentTr, source_lang: srcLang, target_lang: tgtLang, level,
        });
        showResult('translation-result', 'translation-output', 'translation-timing', data.result, data.timing);
      } catch (e: unknown) {
        showToast((e as Error).message, 'error');
      } finally {
        setButtonLoading(btn, false);
        setLoading(false);
      }
    });
  }

  // ── Tab 4: Vocabulary ────────────────────────────────────────
  private initVocabulary(): void {
    const rangeInput = $('vocab-num') as HTMLInputElement;
    const display    = $('vocab-num-display');
    rangeInput.addEventListener('input', () => {
      display.textContent = rangeInput.value;
    });

    // Example chips
    document.querySelectorAll<HTMLButtonElement>('[data-feature="vocab"] .chip').forEach(chip => {
      chip.addEventListener('click', () => {
        ($('vocab-topic') as HTMLInputElement).value      = chip.dataset.topic!;
        ($('vocab-lang') as HTMLSelectElement).value     = chip.dataset.lang!;
        ($('vocab-level') as HTMLSelectElement).value    = chip.dataset.level!;
      });
    });

    const btn = $('vocabulary-submit') as HTMLButtonElement;
    btn.addEventListener('click', async () => {
      const topic  = ($('vocab-topic') as HTMLInputElement).value.trim();
      const lang   = ($('vocab-lang') as HTMLSelectElement).value;
      const level  = ($('vocab-level') as HTMLSelectElement).value;
      const numW   = parseInt(rangeInput.value, 10);
      if (!topic) { showToast('Please enter a topic.', 'error'); return; }

      setButtonLoading(btn, true);
      setLoading(true, `Building ${lang} vocabulary…`);
      try {
        const data = await apiPost<ApiVocabPayload>('/api/vocabulary', {
          topic, language: lang, level, num_words: numW,
        });
        showResult('vocabulary-result', 'vocabulary-output', 'vocabulary-timing', data.result, data.timing);
      } catch (e: unknown) {
        showToast((e as Error).message, 'error');
      } finally {
        setButtonLoading(btn, false);
        setLoading(false);
      }
    });
  }

  // ── Tab 5: Conversation ──────────────────────────────────────
  private initConversation(): void {
    const inputEl = $('convo-input') as HTMLTextAreaElement;
    const sendBtn = $('convo-submit') as HTMLButtonElement;
    const resetBtn = $('convo-reset') as HTMLButtonElement;

    const sendMessage = async (): Promise<void> => {
      const message  = inputEl.value.trim();
      const scenario = ($('convo-scenario') as HTMLSelectElement).value;
      const lang     = ($('convo-lang') as HTMLSelectElement).value;
      const level    = ($('convo-level') as HTMLSelectElement).value;
      if (!message) { showToast('Please type a message.', 'error'); return; }

      inputEl.value = '';
      inputEl.style.height = 'auto';
      sendBtn.disabled = true;

      this.chat.addUserBubble(message);
      this.chat.showTyping();

      try {
        const data = await apiPost<ApiConvoPayload>('/api/conversation', {
          message, scenario, language: lang, level, history: this.chat.getHistory(),
        });
        this.chat.setHistory(data.history ?? '');
        this.chat.addAIBubble(data.result, data.timing);
        const timing = $('convo-timing');
        timing.textContent = data.timing;
        timing.classList.remove('hidden');
      } catch (e: unknown) {
        this.chat.removeTyping();
        showToast((e as Error).message, 'error');
      } finally {
        sendBtn.disabled = false;
        inputEl.focus();
      }
    };

    sendBtn.addEventListener('click', sendMessage);

    inputEl.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Auto-resize textarea
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

document.addEventListener('DOMContentLoaded', () => {
  // eslint-disable-next-line no-new
  new MwalimuApp();
});