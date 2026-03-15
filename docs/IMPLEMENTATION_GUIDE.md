# Mwalimu-LangLearn — Complete Implementation Guide

> **"Mwalimu"** means *Teacher* in Swahili.
> This guide walks through the entire project from zero to a running AI-powered
> language learning platform — explaining every file, every function, and every
> design decision.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Folder Structure](#3-folder-structure)
4. [Prerequisites & Installation](#4-prerequisites--installation)
5. [Layer 1 — Configuration (`mwalimu/config.py`)](#5-layer-1--configuration)
6. [Layer 2 — Inference Engine (`mwalimu/inference.py`)](#6-layer-2--inference-engine)
7. [Layer 3 — Feature Functions (`mwalimu/features/`)](#7-layer-3--feature-functions)
8. [Presentation A — Gradio UI (`mwalimu/ui/interface.py`)](#8-presentation-a--gradio-ui)
9. [Presentation B — Flask + TypeScript UI](#9-presentation-b--flask--typescript-ui)
   - [Flask Server (`flask_app.py`)](#91-flask-server)
   - [HTML Template (`templates/index.html`)](#92-html-template)
   - [CSS Design System (`static/css/style.css`)](#93-css-design-system)
   - [TypeScript Application (`static/ts/main.ts`)](#94-typescript-application)
10. [Entry Points](#10-entry-points)
11. [Data Flow — End to End](#11-data-flow--end-to-end)
12. [How to Build a Similar Solution](#12-how-to-build-a-similar-solution)

---

## 1. Project Overview

Mwalimu-LangLearn is an **AI-powered multilingual language learning platform**
built as part of a Master's thesis at the Kobe Institute of Computing (ABE
Initiative / JICA). It targets learners in the Democratic Republic of Congo
where 200+ local languages, teacher shortages, and limited internet access make
standard ed-tech inaccessible.

**Core idea:** Use a locally-running AI model (via Ollama) to act as a personal
language tutor — correcting writing, teaching vocabulary through images,
evaluating translations, and holding conversations — all through a web browser.

**Key design constraint:** The entire AI runs locally (no internet required for
inference), making the platform viable for low-connectivity environments.

---

## 2. Architecture

The project is structured in **three layers** that are deliberately decoupled so
any layer can be replaced independently.

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│                                                                 │
│   Option A: Gradio UI          Option B: Flask + TypeScript    │
│   mwalimu/ui/interface.py      flask_app.py                    │
│   (5 tabs, gr.Blocks)          templates/index.html            │
│                                static/css/style.css            │
│                                static/ts/main.ts               │
└────────────────────────┬────────────────────────────────────────┘
                         │  calls feature functions
┌────────────────────────▼────────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│                                                                 │
│   mwalimu/features/writing.py       → writing_feedback()       │
│   mwalimu/features/visual.py        → visual_learning()        │
│   mwalimu/features/translation.py   → translation_practice()   │
│   mwalimu/features/vocabulary.py    → vocabulary_builder()     │
│   mwalimu/features/conversation.py  → conversation_practice()  │
└────────────────────────┬────────────────────────────────────────┘
                         │  calls inference functions
┌────────────────────────▼────────────────────────────────────────┐
│                    INFERENCE LAYER                              │
│                                                                 │
│   mwalimu/inference.py                                         │
│   ┌────────────────────┐   ┌──────────────────────────────┐   │
│   │  query_model()     │   │  query_model_with_image()    │   │
│   │  text-only calls   │   │  multimodal calls            │   │
│   └─────────┬──────────┘   └──────────────┬───────────────┘   │
│             └──────────────┬──────────────┘                   │
└──────────────────────────────────────────────────────────────── ┘
                             │  HTTP (localhost:11434)
                    ┌────────▼────────┐
                    │  Ollama Server  │
                    │  gemma3n:e4b    │
                    │  (local GPU)    │
                    └─────────────────┘
```

### Why this separation matters

| Layer | Can be swapped for... | Without touching... |
|---|---|---|
| Inference | GGUF quantized model, OpenAI API, HuggingFace local | Feature or UI code |
| Features | Different prompt strategies, fine-tuned model | UI code |
| Presentation | Mobile app, CLI, different web framework | All backend logic |

---

## 3. Folder Structure

```
Mwalimu-LangLearn/
│
├── README.md                          Project overview
├── requirements.txt                   Python dependencies
├── CLAUDE.md                          AI assistant context file
│
├── main.py                            Entry point → Gradio UI
├── flask_app.py                       Entry point → Flask+TS UI
│
├── mwalimu/                           Core Python package
│   ├── __init__.py                    Package init + public exports
│   ├── config.py                      All constants (model, languages, tokens)
│   ├── inference.py                   Ollama client + query functions
│   ├── features/                      One file per learning mode
│   │   ├── __init__.py
│   │   ├── writing.py                 Tab 1 — Writing Feedback
│   │   ├── visual.py                  Tab 2 — Visual Learning
│   │   ├── translation.py             Tab 3 — Translation Practice
│   │   ├── vocabulary.py              Tab 4 — Vocabulary Builder
│   │   └── conversation.py            Tab 5 — Conversation Practice
│   └── ui/
│       ├── __init__.py
│       └── interface.py               Gradio Blocks interface
│
├── templates/
│   └── index.html                     Flask Jinja2 HTML (5-tab SPA)
│
├── static/
│   ├── css/style.css                  Design system + animations
│   ├── ts/main.ts                     TypeScript source
│   └── js/main.js                     Compiled JavaScript
│
├── notebooks/
│   └── Gemma3n_language_learning_Tool.ipynb   Original prototype
│
├── docs/
│   ├── CODEBASE_ANALYSIS.md           Deep technical analysis
│   └── IMPLEMENTATION_GUIDE.md        ← This file
│
└── scripts/
    └── Code-base.py                   Scratch/utility scripts
```

---

## 4. Prerequisites & Installation

### System requirements

| Component | Requirement |
|---|---|
| Python | 3.10+ |
| Ollama | Latest (ollama.com/download) |
| RAM | 8 GB minimum (16 GB recommended) |
| GPU | Optional but strongly recommended (NVIDIA or Apple Silicon) |

### Step 1 — Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download installer from https://ollama.com/download
```

### Step 2 — Pull the model

```bash
ollama pull gemma3n:e4b        # text-only (6.9 GB)

# Optional: vision-capable model (enables Tab 2)
ollama pull llava
```

### Step 3 — Start Ollama

```bash
ollama serve
# Runs at http://localhost:11434 in the background
```

### Step 4 — Clone and install Python dependencies

```bash
git clone <repo-url>
cd Mwalimu-LangLearn

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Step 5 — Run

```bash
# Gradio UI  →  http://127.0.0.1:7860
python main.py

# Flask + TypeScript UI  →  http://127.0.0.1:8080
python flask_app.py --port 8080
```

---

## 5. Layer 1 — Configuration

**File:** `mwalimu/config.py`

This is the **single source of truth** for all constants in the project.
Every other module imports from here — nothing is hardcoded elsewhere.

```python
OLLAMA_HOST  = "http://localhost:11434"   # Ollama API endpoint
OLLAMA_MODEL = "gemma3n:e4b"              # Model to use
TEMPERATURE  = 0.7                        # Generation creativity
TOP_P        = 0.9                        # Nucleus sampling threshold
```

### Token budgets

Each feature has its own `MAX_TOKENS_*` constant because output length needs
differ significantly between a short translation check and a full vocabulary
lesson.

| Constant | Value | Feature | Why this size |
|---|---|---|---|
| `MAX_TOKENS_WRITING` | 1024 | Writing Feedback | Multi-section detailed feedback |
| `MAX_TOKENS_VISUAL` | 1024 | Visual Learning | Object list + sentences + cultural note |
| `MAX_TOKENS_TRANSLATION` | 512 | Translation | Structured 6-point feedback |
| `MAX_TOKENS_VOCABULARY` | 1500 | Vocabulary | Word list + sentences + quiz + tips |
| `MAX_TOKENS_CONVERSATION` | 768 | Conversation | Reply + language notes |

### Language and scenario lists

```python
LANGUAGES = ["French", "Swahili", "Lingala", ...]   # 14 languages
PROFICIENCY_LEVELS = ["Beginner (A1-A2)", ...]       # 3 CEFR levels
CONVERSATION_SCENARIOS = [...]                        # 8 real-world contexts
```

These lists are injected into both UIs (Gradio dropdowns and Jinja2 template
`<select>` elements) from a single definition, so adding a new language means
changing one line.

---

## 6. Layer 2 — Inference Engine

**File:** `mwalimu/inference.py`

This is the **only file that talks to Ollama**. It provides two functions used
by every feature — and nothing else.

### Module-level setup

```python
client: ollama.Client = ollama.Client(host=OLLAMA_HOST)
HAS_VISION: bool = any(kw in OLLAMA_MODEL for kw in VISION_MODEL_KEYWORDS)
```

- `client` is created **once** at import time and reused by all requests
  (connection pooling, no overhead per call).
- `HAS_VISION` is a boolean flag checked before any image request so the UI can
  show a helpful message instead of crashing when a text-only model is active.

### `query_model(prompt, system_prompt, max_new_tokens)`

**Purpose:** Send a text-only question to the model and return the response.

**How it works:**
```
1. Build messages list:  [{"role":"system",...}, {"role":"user",...}]
2. Call client.chat() with generation options (temperature, top_p, num_predict)
3. Extract .message.content from the response object
4. Return (response_text, execution_time_seconds)
```

**Contribution to the solution:**
Every feature that does not involve an image calls this function. It is the
single integration point with Ollama, so if the backend ever changes (e.g.,
switching to a HuggingFace local model or an API), only this function changes.

### `query_model_with_image(image, prompt, system_prompt, max_new_tokens)`

**Purpose:** Send an image + text prompt to a vision-capable model.

**How it works:**
```
1. Guard — return friendly error if HAS_VISION is False
2. Normalise image: accept PIL Image or file path, convert to RGB
3. Encode image → JPEG bytes via io.BytesIO
4. Build messages list with "images": [image_bytes] field
5. Call client.chat() — Ollama handles vision encoding server-side
6. Return (response_text, execution_time_seconds)
```

**Contribution to the solution:**
Makes Tab 2 (Visual Learning) work. The image encoding to JPEG bytes is the
key step — Ollama's API accepts raw bytes or base64 strings in the `images`
field of a chat message.

### `check_connection()`

**Purpose:** Verify Ollama is running at startup and return available models.

Used by both entry points (`main.py` and `flask_app.py`) to provide a clear
error message rather than a cryptic connection refused exception.

---

## 7. Layer 3 — Feature Functions

**Folder:** `mwalimu/features/`

Each file implements exactly **one learning mode**. All feature functions follow
the same contract:

```
Input:  user form values (strings, PIL Image, int)
Output: (markdown_response: str, timing_string: str)
```

The timing string (e.g. `"Response time: 3.2s"`) is displayed in the UI as a
performance indicator.

---

### Feature 1 — `writing.py` → `writing_feedback()`

**What it does:** Receives a paragraph written by the student in their target
language and returns structured feedback: corrections, explanations, vocabulary
suggestions, style tips, and a score out of 10.

**Key implementation detail — the system prompt role:**
```python
system_prompt = (
    f"You are an expert {target_language} language tutor.\n"
    f"The student's proficiency level is {proficiency_level}.\n"
    "Analyse their writing and provide:\n"
    "1. **Corrections** ...\n"
    "2. **Explanations** ...\n"
    ...
)
```

The numbered list in the system prompt is what forces the model to produce
structured, sectioned output rather than a free-form paragraph. This is the
**"role + numbered format"** prompt engineering pattern used across all features.

**Contribution to the solution:** Writing practice with personalised feedback is
the core pedagogical loop. Students write, get corrected, understand why, and
improve — mimicking a real tutor.

---

### Feature 2 — `visual.py` → `visual_learning()`

**What it does:** Takes a PIL Image and two language codes, then asks the model
to identify every visible object, translate each to the target language, provide
pronunciation, write example sentences, and add cultural notes.

**Key implementation detail — image guard:**
```python
if image is None:
    return "Please upload an image to begin.", ""
```
Early return prevents calling the inference layer with a None image — keeps
error handling in the feature layer where it's easy to customise.

**Contribution to the solution:** Visual learning leverages the multimodal
capability of the AI. A student can photograph real-world objects in their
environment (food, furniture, street signs) and instantly get vocabulary in
their target language — highly contextual and memorable.

---

### Feature 3 — `translation.py` → `translation_practice()`

**What it does:** Given an original sentence and the student's translation
attempt, the model provides: an ideal translation, an accuracy score (1-10),
specific corrections, praise for correct parts, grammar notes, and alternative
valid translations.

**Key implementation detail — dual-input prompt:**
```python
prompt = (
    f"**Original ({source_lang}):** \"{original_text}\"\n"
    f"**Student's Translation ({target_lang}):** \"{student_translation}\"\n\n"
    "Please provide:\n1. **Your ideal translation**\n2. **Accuracy score**..."
)
```

Both the original and the student's attempt are embedded in the prompt so the
model can compare them directly. The bold markdown labels are picked up by the
model as structural cues.

**Contribution to the solution:** Translation is one of the most effective
language learning exercises. Getting scored feedback shows students exactly
where their understanding breaks down.

---

### Feature 4 — `vocabulary.py` → `vocabulary_builder()`

**What it does:** Generates a complete themed vocabulary lesson: N words with
translations + pronunciation + part of speech, one example sentence per word,
3-5 common phrases, a 3-question mini quiz, and memory tips.

**Key implementation detail — configurable word count:**
```python
def vocabulary_builder(topic, target_language, proficiency, num_words=10):
    ...
    f"1. **{num_words} Key Words**: Each with translation..."
```

`num_words` is a runtime parameter injected directly into the prompt, giving
the student control over lesson length (5–20 words) without any code branching.

**Contribution to the solution:** Vocabulary acquisition by topic mirrors how
real language textbooks are structured. The quiz and memory tips make the output
immediately actionable rather than just informational.

---

### Feature 5 — `conversation.py` → `conversation_practice()`

**What it does:** Simulates a scenario-based conversation (restaurant, job
interview, shopping...). The model responds in the target language then adds a
"Language Notes" section that corrects errors, explains grammar, and asks a
follow-up question.

**Key implementation detail — state management:**
```python
def conversation_practice(user_message, scenario, target_language,
                           proficiency, chat_history=""):
    ...
    history_block = f"Previous conversation:\n{chat_history}\n\n" if chat_history else ""
    prompt = f"{history_block}Student says: \"{user_message}\"..."
    ...
    updated_history = f"{chat_history}\nStudent: {user_message}\nTutor: {response}"
    return response, updated_history, timing
```

The conversation history is accumulated as a plain text string and prepended to
every new prompt. This is the **"context injection"** pattern — simpler than
token-level memory management and sufficient for a session-length conversation.
The caller (UI layer) is responsible for storing and passing `chat_history`
back each turn.

**Contribution to the solution:** Conversation practice is the highest-order
skill in language learning. The inline language notes mean students get corrected
without the flow of the conversation being interrupted.

---

## 8. Presentation A — Gradio UI

**File:** `mwalimu/ui/interface.py`
**Entry point:** `main.py`

Gradio is a Python library that turns Python functions into web UIs automatically.
The function `build_interface()` constructs a `gr.Blocks` layout with 5 tabs and
wires each button to the corresponding feature function.

```python
writing_btn.click(
    fn=writing_feedback,
    inputs=[writing_input, writing_lang, writing_level],
    outputs=[writing_output, writing_time]
)
```

This single line tells Gradio: "when the button is clicked, call
`writing_feedback()` with these 3 input components, and put the 2 return values
into these 2 output components."

**Tab 5 is special** — it uses `gr.State` to persist conversation history
between button clicks without a database:

```python
convo_history = gr.State(value="")    # lives in the browser session

convo_btn.click(
    fn=conversation_practice,
    inputs=[..., convo_history],        # reads history from state
    outputs=[convo_output, convo_history, convo_time]  # writes it back
)
```

**Contribution to the solution:** Gradio lets the entire backend be exposed as a
working web app with zero HTML/CSS/JS. It was the right choice for rapid
prototyping and the research demo phase.

---

## 9. Presentation B — Flask + TypeScript UI

The Flask UI replaces Gradio's auto-generated interface with a hand-crafted,
animated, product-quality web application — same features, same backend, better
design.

### 9.1 Flask Server

**File:** `flask_app.py`

```python
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",
        languages=LANGUAGES,
        proficiency_levels=PROFICIENCY_LEVELS,
        ...)

@app.route("/api/writing", methods=["POST"])
def api_writing():
    data = request.get_json()
    result, timing = writing_feedback(data["text"], data["language"], data["level"])
    return jsonify({"result": result, "timing": timing})
```

**How it works:**
- The `/` route renders the HTML template, injecting server-side data
  (language lists, model name, vision flag) as Jinja2 template variables.
- Each `/api/<feature>` route receives a JSON POST request from the browser,
  calls the same feature function as the Gradio UI, and returns JSON.
- The visual route handles both `multipart/form-data` (file upload) and
  `application/json` (base64 image) to support different browser upload methods.

**Contribution to the solution:** Flask decouples the HTTP layer from the
Python business logic. Adding a new endpoint is 5 lines. All existing feature
functions are reused unchanged — the Flask server is purely a thin HTTP adapter.

---

### 9.2 HTML Template

**File:** `templates/index.html`

A single-page application built with Jinja2 templating. Key sections:

```html
<!-- Server injects language list at render time -->
<select id="writing-lang">
  {% for lang in languages %}
  <option value="{{ lang }}">{{ lang }}</option>
  {% endfor %}
</select>

<!-- Server config exposed to TypeScript -->
<script>
  window.MWALIMU_CONFIG = {
    hasVision: {{ 'true' if has_vision else 'false' }},
    model: "{{ model }}"
  };
</script>
```

Jinja2 `{% for %}` loops generate the `<select>` options from the same
`LANGUAGES` list defined in `config.py` — single source of truth flows from
Python to HTML.

The `window.MWALIMU_CONFIG` pattern bridges the server-rendered config into the
TypeScript application without an extra API call.

---

### 9.3 CSS Design System

**File:** `static/css/style.css`

The entire visual language is defined through **CSS custom properties** at the
`:root` level:

```css
:root {
  --bg:       #f8f8ff;          /* near-white background */
  --purple:   #7c6dfa;          /* primary accent */
  --coral:    #ff6b6b;          /* secondary accent */
  --gold:     #e6b800;          /* tertiary accent */
  --cyan:     #0ea5c9;          /* quaternary accent */
  --grad-hero: linear-gradient(135deg, #7c6dfa, #ff6b6b, #f6c90e);
}
```

**Key animation techniques:**

| Animation | CSS technique | Visual effect |
|---|---|---|
| Hero gradient text | `@keyframes gradientShift` + `background-clip: text` | Animated colour cycling on the Mwalimu title |
| Floating orbs | `@keyframes float` (translateY) | Blurred colour blobs drifting in the header |
| Tab ink bar | `transition: left, width` | Smooth sliding underline follows active tab |
| Card appear | `@keyframes fadeInUp` | Content slides up when a tab is opened |
| Button shine | `::before` pseudo + `left: -100% → 150%` on hover | Light sweep across button surface |
| Loading dots | `@keyframes loadingDots` (scale + opacity) | Three bouncing dots while AI processes |
| Chat typing | `@keyframes typingBounce` | Three dots bounce to indicate AI is "typing" |

---

### 9.4 TypeScript Application

**File:** `static/ts/main.ts`
**Compiled:** `static/js/main.js`

The TypeScript is structured as a set of single-responsibility classes that
are composed together in `MwalimuApp`.

---

#### `ParticleSystem`

```typescript
class ParticleSystem {
  constructor(canvas: HTMLCanvasElement) { ... }
  private loop(): void { this.draw(); this.update(); requestAnimationFrame(...) }
}
```

**What it does:** Creates 70 particles on a `<canvas>` element fixed to the
viewport background. Each frame it draws particles as small circles and
connects nearby particles with faint lines (constellation effect), then moves
each particle by its velocity vector, bouncing off canvas edges.

**Contribution:** Provides the animated depth in the background without
affecting page performance — canvas rendering runs on the GPU compositor thread.

---

#### `TabManager`

```typescript
class TabManager {
  switchTo(tabId: string): void {
    // 1. Update aria-selected on all buttons
    // 2. Move the ink bar via getBoundingClientRect()
    // 3. Show/hide panels with animation class
  }
  private moveInk(btn: HTMLButtonElement): void {
    const rect = btn.getBoundingClientRect();
    this.ink.style.left  = `${rect.left - navRect.left}px`;
    this.ink.style.width = `${rect.width}px`;
  }
}
```

**What it does:** Manages which tab panel is visible and moves the sliding
underline (ink bar) to align with the active button. The ink bar position is
calculated with `getBoundingClientRect()` for pixel-perfect accuracy regardless
of button width. CSS transitions animate the movement.

**Contribution:** Provides the navigation experience that ties all 5 learning
modes together in a single page without any page loads.

---

#### `TypewriterEffect`

```typescript
class TypewriterEffect {
  stream(container: HTMLElement, markdown: string, onDone?: () => void): void {
    container.innerHTML = marked.parse(markdown);  // render all markdown at once
    const allText = container.querySelectorAll('p, li, h1, h2, h3, td...');
    allText.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transition = `opacity 0.25s ease ${i * 0.04}s ...`;
    });
    requestAnimationFrame(() => {
      allText.forEach(el => { el.style.opacity = '1'; });
    });
  }
}
```

**What it does:** Instead of truly typing characters one by one (which would
break markdown rendering), this renders the full markdown first then reveals
each block element with a staggered fade-in (40ms delay between elements).
This gives the feel of progressive text appearance while preserving correct
markdown structure including tables, code blocks, and lists.

**Contribution:** Makes the AI response feel alive and dynamic rather than
appearing as a static block of text. The stagger timing (0, 40ms, 80ms...)
guides the user's eye through the structured feedback.

---

#### `ImageUploader`

```typescript
class ImageUploader {
  private bind(): void {
    this.dropZone.addEventListener('dragover', e => { e.preventDefault(); ... });
    this.dropZone.addEventListener('drop', e => { ... this.load(file); });
    this.fileInput.addEventListener('change', e => { this.load(files[0]); });
  }
  private load(file: File): void {
    const reader = new FileReader();
    reader.onload = ev => {
      this.currentB64 = dataUrl.split(',')[1];  // strip data:image/...;base64,
      this.preview.src = dataUrl;
    };
    reader.readAsDataURL(file);
  }
  getBase64(): string | null { return this.currentB64; }
}
```

**What it does:** Handles both drag-and-drop and click-to-browse image
selection. Converts the selected file to a base64 string using the FileReader
API, stores it, and shows a live preview in the drop zone. When the submit
button is clicked, `getBase64()` provides the encoded image for the API call.

**Contribution:** Enables the Visual Learning tab (Tab 2) in the Flask UI.
The base64 encoding is necessary because JSON APIs cannot transmit binary file
data directly.

---

#### `ChatManager`

```typescript
class ChatManager {
  addUserBubble(text: string): void { ... }
  addAIBubble(markdown: string, timing: string): void { ... }
  showTyping(): void {
    row.innerHTML = `<div class="typing-indicator">
      <span></span><span></span><span></span></div>`;
  }
  reset(): void { this.history = ''; ... }
}
```

**What it does:** Manages the chat window for Tab 5. Adds styled bubble
elements to the DOM for each user and AI message. Shows a three-dot typing
animation while waiting for the API response. The typing indicator is removed
and replaced with the AI bubble when the response arrives. Maintains scroll
position at the bottom of the chat window.

**Contribution:** Transforms the conversation feature from a form-and-output
model into a genuine chat interface, which is cognitively closer to a real
language conversation and more engaging for learners.

---

#### `MwalimuApp` (main class)

```typescript
class MwalimuApp {
  constructor() {
    this.tabs     = new TabManager();
    this.uploader = new ImageUploader(...);
    this.chat     = new ChatManager(...);
    this.particles = new ParticleSystem(...);
    this.initWriting();
    this.initVisual();
    this.initTranslation();
    this.initVocabulary();
    this.initConversation();
    animateCounters();
  }
}
document.addEventListener('DOMContentLoaded', () => { new MwalimuApp(); });
```

**What it does:** The root coordinator. Instantiates all sub-systems and wires
each feature tab's form elements to their API endpoints. Each `init*()` method:
1. Attaches event listeners to form controls (chips, selects, buttons)
2. Validates inputs client-side before sending
3. Shows the loading overlay during the API call
4. Calls the appropriate `/api/<feature>` endpoint
5. Passes the result to `showResult()` which triggers `TypewriterEffect`

**Contribution:** The central composition point that makes all the pieces work
together as a single application.

---

## 10. Entry Points

### `main.py` — Gradio

```
parse CLI args (--host, --port, --share)
    ↓
startup_check() — verify Ollama, print status
    ↓
build_interface() — returns gr.Blocks demo
    ↓
demo.launch(server_name, server_port, share)
```

### `flask_app.py` — Flask

```
parse CLI args (--host, --port, --debug)
    ↓
startup_check() — verify Ollama, print status
    ↓
app.run(host, port, debug)
    ↓
Flask routes handle HTTP requests → feature functions → JSON responses
```

Both entry points perform the same startup check so the user gets a clear,
actionable error message if Ollama is not running before the web server starts.

---

## 11. Data Flow — End to End

The following traces one complete request through the system for **Writing
Feedback** in the Flask UI:

```
[Browser]
  User types text, selects French / Intermediate, clicks "Get Feedback"
  JS: fetch('/api/writing', { method:'POST', body: JSON.stringify({...}) })
        │
        ▼
[flask_app.py  /api/writing]
  data = request.get_json()
  result, timing = writing_feedback(data["text"], data["language"], data["level"])
        │
        ▼
[mwalimu/features/writing.py  writing_feedback()]
  Builds system_prompt (role + numbered format instruction)
  Builds user prompt (student text + instruction)
  Calls query_model(prompt, system_prompt, MAX_TOKENS_WRITING=1024)
        │
        ▼
[mwalimu/inference.py  query_model()]
  messages = [{"role":"system",...}, {"role":"user",...}]
  response = client.chat(model="gemma3n:e4b", messages=messages, options={...})
        │
        ▼ HTTP POST  localhost:11434/api/chat
[Ollama Server]
  gemma3n:e4b processes the prompt on GPU
  Returns streamed tokens, assembled into .message.content
        │
        ▼
[query_model()]  returns (response_text, 3.2)
[writing_feedback()]  returns ("## Corrections\n...", "Response time: 3.2s")
[/api/writing]  returns JSON {"result": "...", "timing": "..."}
        │
        ▼
[Browser  TypewriterEffect.stream()]
  marked.parse(result) → HTML
  Staggered fade-in reveals each paragraph
  User reads the feedback
```

---

## 12. How to Build a Similar Solution

Follow these steps to build your own AI-powered learning tool using this
architecture as a template.

### Step 1 — Define your domain

Answer these questions:
- What subject are you teaching? (Languages, math, history...)
- What are the 3-5 core learning interactions? (Write → get feedback,
  Read → get quiz, Practice → get scored...)
- Does any interaction require images? (Visual recognition, diagram analysis...)

### Step 2 — Set up the inference layer

Copy `mwalimu/inference.py` and `mwalimu/config.py`. Change:
- `OLLAMA_MODEL` to a model appropriate for your domain
- `TEMPERATURE` and `TOP_P` to tune creativity vs. consistency
- `MAX_TOKENS_*` constants to match your expected output length

### Step 3 — Write one feature function per interaction

For each learning interaction, create a file in `features/`:

```python
def my_feature(user_input: str, config_param: str) -> tuple[str, str]:
    if not user_input.strip():
        return "Please provide input.", ""

    system_prompt = "You are a [ROLE]. Provide: 1. [Section]  2. [Section]..."
    prompt = f"The student's input: \"{user_input}\"\n\nProvide feedback."

    response, time = query_model(prompt, system_prompt, MAX_TOKENS)
    return response, f"Response time: {time}s"
```

The numbered section format in the system prompt is the key to getting
structured, consistent output from any instruction-tuned model.

### Step 4 — Choose your presentation layer

**Quick demo → Gradio:**
```python
with gr.Blocks() as demo:
    with gr.TabItem("My Feature"):
        input_box = gr.Textbox()
        btn = gr.Button("Submit")
        output = gr.Markdown()
        btn.click(fn=my_feature, inputs=[input_box], outputs=[output])
demo.launch()
```

**Production UI → Flask + TypeScript:**
Copy the Flask + TS structure from this project. For each feature:
1. Add a `@app.route("/api/<feature>")` endpoint in `flask_app.py`
2. Add a tab panel in `templates/index.html`
3. Add an `init<Feature>()` method in `static/ts/main.ts`

### Step 5 — Tune prompts iteratively

The quality of your application is mostly determined by prompt quality.
Iterate on:
- **Role clarity:** "You are a [specific expert]" sets the model's persona.
- **Output format:** Numbered lists and bold headers produce consistently
  parseable markdown.
- **Audience awareness:** Inject the user's level/context so responses scale
  appropriately ("for a {proficiency} student").
- **Encouragement tone:** For educational tools, add "Be encouraging and
  supportive" to the system prompt to prevent harsh feedback.

### Step 6 — Test the full stack

```bash
# 1. Start Ollama
ollama serve

# 2. Run the app
python flask_app.py --port 8080 --debug

# 3. Open browser, test each tab manually
# 4. Check the Ollama logs for token counts and latency
```

---

*Built by Pascal Burume Buhendwa · ABE Initiative @ Kobe Institute of Computing*
*Part of the Mwalimu-STEM-GenAI initiative for AI-powered education in the DRC*