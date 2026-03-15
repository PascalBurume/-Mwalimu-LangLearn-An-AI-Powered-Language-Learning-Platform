# Mwalimu-LangLearn — Skills Template

> Reusable specification template for every learning skill (feature) in the platform.
> Use this as a blueprint when building new skills or extending existing ones.

---

## Table of Contents

1. [Design System Reference](#1-design-system-reference)
2. [Skill Template Structure](#2-skill-template-structure)
3. [Skill 1 — Writing Feedback](#3-skill-1--writing-feedback)
4. [Skill 2 — Visual Learning](#4-skill-2--visual-learning)
5. [Skill 3 — Translation Practice](#5-skill-3--translation-practice)
6. [Skill 4 — Vocabulary Builder](#6-skill-4--vocabulary-builder)
7. [Skill 5 — Conversation Practice](#7-skill-5--conversation-practice)
8. [Adding a New Skill — Step-by-Step](#8-adding-a-new-skill--step-by-step)

---

## 1. Design System Reference

### 1.1 Colour Palette

| Token             | Value                      | Usage                                    |
|-------------------|---------------------------|------------------------------------------|
| `--bg`            | `#f8f8ff`                 | Page background                          |
| `--bg-2`          | `#f0f0fc`                 | Secondary background                     |
| `--surface`       | `#ffffff`                 | Cards, inputs, panels                    |
| `--surface-2`     | `#f4f3ff`                 | Hover states, alt surface                |
| `--border`        | `rgba(100,90,200,0.12)`   | Default borders                          |
| `--border-2`      | `rgba(100,90,200,0.2)`    | Emphasized borders                       |
| `--purple`        | `#7c6dfa`                 | Primary brand, focus rings               |
| `--purple-light`  | `#6457e8`                 | Secondary brand                          |
| `--coral`         | `#ff6b6b`                 | Conversation accent, errors              |
| `--gold`          | `#e6b800`                 | Translation accent, hero period          |
| `--cyan`          | `#0ea5c9`                 | Visual accent, hover highlights          |
| `--green`         | `#10b981`                 | Success, connection status               |
| `--text`          | `#1a1730`                 | Primary text (dark on light)             |
| `--text-muted`    | `rgba(26,23,48,0.62)`     | Secondary text                           |
| `--text-dim`      | `rgba(26,23,48,0.38)`     | Tertiary / placeholder text              |

### 1.2 Skill Gradient Map

Each skill has a unique gradient identity used for its icon, submit button, and accents:

| Skill         | CSS Class               | Gradient                                              |
|---------------|-------------------------|-------------------------------------------------------|
| Writing       | `.writing-gradient`     | `linear-gradient(135deg, #7c6dfa 0%, #a594fd 100%)`  |
| Visual        | `.visual-gradient`      | `linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%)`  |
| Translation   | `.translation-gradient` | `linear-gradient(135deg, #f6c90e 0%, #f59e0b 100%)`  |
| Vocabulary    | `.vocab-gradient`       | `linear-gradient(135deg, #34d399 0%, #10b981 100%)`  |
| Conversation  | `.convo-gradient`       | `linear-gradient(135deg, #ff6b6b 0%, #f43f5e 100%)`  |

### 1.3 Typography

| Font              | Weight       | Usage                                       |
|-------------------|-------------|---------------------------------------------|
| Space Grotesk     | 700         | Headings, hero title, stat numbers           |
| Space Grotesk     | 500–600     | Panel titles, tab labels                     |
| Inter             | 300–800     | Body text, labels, inputs, everything else   |

### 1.4 Spacing & Sizing Tokens

| Token          | Value   | Usage                           |
|----------------|---------|----------------------------------|
| `--radius-sm`  | `8px`   | Inputs, small elements           |
| `--radius`     | `14px`  | Cards, buttons, send button      |
| `--radius-lg`  | `20px`  | Result cards, chat window, drop zone |
| `--radius-xl`  | `28px`  | Loader card                      |
| `--max-width`  | `960px` | Content area max width           |
| `--panel-pad`  | `2rem`  | Tab panel internal padding       |

### 1.5 Motion System

| Token       | Value                           | Usage                  |
|-------------|--------------------------------|------------------------|
| `--ease`    | `cubic-bezier(0.4, 0, 0.2, 1)` | Standard transitions   |
| `--spring`  | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Bouncy interactions |
| `--t-fast`  | `0.15s`                        | Focus, hover           |
| `--t-mid`   | `0.28s`                        | Buttons, cards         |
| `--t-slow`  | `0.45s`                        | Tab ink, panels        |

### 1.6 Component Library

#### Form Controls
- **`<select class="form-select">`** — Custom styled dropdown with SVG chevron
- **`<input class="form-input">`** — Text input
- **`<textarea class="form-textarea">`** — Multiline text
- **`<input type="range" class="form-range">`** — Slider with accent colour
- **Focus ring**: `box-shadow: 0 0 0 3px rgba(124,109,250,0.14)`

#### Layout Grids
- **`.form-grid--2col`** — `grid-template-columns: repeat(2, 1fr)` — used by Writing, Visual
- **`.form-grid--3col`** — `grid-template-columns: repeat(3, 1fr)` — used by Translation, Vocabulary, Conversation

#### Interactive Elements
- **`.chip`** — Pill-shaped example button (border-radius 100px, hover lifts -1px)
- **`.submit-btn`** — Gradient button with shimmer `::before` effect on hover
- **`.result-card`** — Collapsible output card with header + scrollable body
- **`.drop-zone`** — Dashed-border drag-and-drop area with preview overlay

---

## 2. Skill Template Structure

Every skill follows this exact pattern across all four layers:

```
┌─────────────────────────────────────────────┐
│  LAYER 1 — Config (mwalimu/config.py)       │
│  • MAX_TOKENS_<SKILL>  token budget          │
│  • Any skill-specific constants              │
├─────────────────────────────────────────────┤
│  LAYER 2 — Feature (mwalimu/features/*.py)  │
│  • System prompt (role + output format)      │
│  • User prompt (task + student data)         │
│  • query_model() or query_model_with_image() │
│  • Returns (markdown, timing)                │
├─────────────────────────────────────────────┤
│  LAYER 3 — API (flask_app.py)               │
│  • POST /api/<skill>                         │
│  • Parse JSON request body                   │
│  • Call feature function                     │
│  • Return JSON { result, timing }            │
├─────────────────────────────────────────────┤
│  LAYER 4 — UI (index.html + main.ts)        │
│  • Tab button in <nav>                       │
│  • Tab panel <section>                       │
│  • Form inputs (dropdowns, text, etc.)       │
│  • Example chips                             │
│  • Submit button → apiPost() → showResult()  │
│  • Result card with markdown rendering       │
└─────────────────────────────────────────────┘
```

### Stateless vs. Stateful

| Type      | Skills              | State management             |
|-----------|---------------------|------------------------------|
| Stateless | Writing, Visual, Translation, Vocabulary | Each call independent — no session data |
| Stateful  | Conversation        | `chat_history` string in JS `ChatManager` — sent with each API call |

---

## 3. Skill 1 — Writing Feedback

### 3.1 Overview

| Property        | Value                                                      |
|-----------------|------------------------------------------------------------|
| **Tab icon**    | ✍️                                                         |
| **Gradient**    | `.writing-gradient` — purple → light purple                |
| **Endpoint**    | `POST /api/writing`                                        |
| **State**       | Stateless                                                  |
| **Token budget**| `MAX_TOKENS_WRITING = 1024`                                |
| **Tagline**     | "Write in your target language · receive corrections, explanations & a score" |

### 3.2 Input Specification

| Field          | HTML Element   | ID              | Type       | Default        | Validation           |
|----------------|----------------|-----------------|------------|----------------|----------------------|
| Target Language| `<select>`     | `writing-lang`  | Dropdown   | French         | Required (preset)    |
| Proficiency    | `<select>`     | `writing-level` | Dropdown   | Intermediate   | Required (preset)    |
| Student Text   | `<textarea>`   | `writing-text`  | Freeform   | —              | Non-empty            |

### 3.3 Example Chips

| Label             | Language | Level               | Sample Text                                                                             |
|-------------------|----------|----------------------|----------------------------------------------------------------------------------------|
| French paragraph  | French   | Intermediate (B1-B2) | "Je suis allé au magazin hier pour acheter du pain. Le pain était très bon et je mange beaucoup." |
| Swahili sentence  | Swahili  | Beginner (A1-A2)     | "Ninajifunza Kiswahili kwa sababu ninapenda lugha ya Afrika."                          |
| Japanese sentence | Japanese | Beginner (A1-A2)     | "きのう友達とレストランに食べました。とても美味しいでした。"                              |

### 3.4 API Contract

**Request:**
```json
{
  "text": "string — student's written text",
  "language": "string — target language name",
  "level": "string — CEFR level label"
}
```

**Response:**
```json
{
  "result": "string — markdown feedback",
  "timing": "string — e.g. 'Response time: 3.2s'"
}
```

### 3.5 Prompt Engineering Pattern

**System prompt structure:**
```
You are an expert {target_language} language tutor.
The student's proficiency level is {proficiency_level}.
Analyse their writing and provide:
1. **Corrections**: Fix grammar, spelling, and syntax errors. Show the corrected version.
2. **Explanations**: Explain each error briefly so the student learns.
3. **Vocabulary**: Suggest better word choices or useful alternatives.
4. **Style Tips**: Provide natural phrasing suggestions.
5. **Score**: Give a score out of 10 with encouragement.
Be encouraging and supportive. Use examples when helpful.
```

**User prompt structure:**
```
Please review and correct this {target_language} text written by
a {proficiency_level} student:

"""
{student_text}
"""

Provide detailed feedback with corrections and explanations.
```

### 3.6 Expected AI Output Sections

1. **Corrections** — corrected version of the text
2. **Explanations** — error-by-error breakdown
3. **Vocabulary** — alternative word suggestions
4. **Style Tips** — phrasing improvements
5. **Score** — numeric score /10 with encouragement

### 3.7 UI Wireframe

```
┌─────────────────────────────────────────────────────┐
│  ✍️  Writing Feedback                                │
│  Write in your target language · receive corrections │
├───────────────────────┬─────────────────────────────┤
│ Target Language ▼     │ Proficiency Level ▼         │
├───────────────────────┴─────────────────────────────┤
│ ┌─────────────────────────────────────────────────┐ │
│ │ Your Text                                       │ │
│ │ [textarea 6 rows]                               │ │
│ └─────────────────────────────────────────────────┘ │
│                                                     │
│ Quick example: [French paragraph] [Swahili] [日本語] │
│                                                     │
│ [ ✍️ Get Feedback → ]                               │
│                                                     │
│ ┌─ AI Feedback ──────────────── Response time: 3s ┐ │
│ │ ## Corrections                                  │ │
│ │ ...rendered markdown...                         │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## 4. Skill 2 — Visual Learning

### 4.1 Overview

| Property        | Value                                                      |
|-----------------|------------------------------------------------------------|
| **Tab icon**    | 🖼️                                                         |
| **Gradient**    | `.visual-gradient` — cyan → blue                           |
| **Endpoint**    | `POST /api/visual`                                         |
| **State**       | Stateless                                                  |
| **Token budget**| `MAX_TOKENS_VISUAL = 1024`                                 |
| **Requires**    | Vision-capable model (llava, llama3.2-vision, etc.)        |
| **Tagline**     | "Upload an image · discover vocabulary in your target language" |

### 4.2 Input Specification

| Field            | HTML Element      | ID              | Type         | Default  | Validation             |
|------------------|-------------------|-----------------|-------------|----------|------------------------|
| Image            | `<input file>`    | `visual-file`   | Image upload | —        | Required, image/*      |
| Target Language  | `<select>`        | `visual-target` | Dropdown     | French   | Required (preset)      |
| Source Language   | `<select>`        | `visual-source` | Dropdown     | English  | Required (preset)      |

### 4.3 Special UI Components

**Drop Zone** (`#drop-zone`):
- Dashed border (`2px dashed rgba(124,109,250,0.3)`)
- Aspect ratio 4:3
- States: default, dragging (cyan glow), has-image (preview overlay)
- Disabled state when no vision model available (`.drop-zone--disabled`)

**Warning Banner** (when vision unavailable):
- Yellow info banner with `⚠️` icon
- Shows current model name and suggests `ollama pull llava`

### 4.4 API Contract

**Request (JSON):**
```json
{
  "image_b64": "string — base64-encoded image data",
  "target_language": "string",
  "source_language": "string"
}
```

**Request (multipart/form-data):**
```
image: File
target_language: string
source_language: string
```

**Response:**
```json
{
  "result": "string — markdown vocabulary from image",
  "timing": "string"
}
```

### 4.5 Prompt Engineering Pattern

**System prompt:**
```
You are a visual language learning assistant.
Help students learn {target_language} vocabulary through images.
Be thorough but organised in your response.
```

**User prompt:**
```
Look at this image carefully. Please:

1. **Identify** all major objects, people, and elements visible in the image.
2. **Translate** each identified item from {source_language} to {target_language}.
3. **Pronunciation**: Include a pronunciation guide for each {target_language} word.
4. **Example Sentences**: Write 2-3 simple sentences in {target_language} using these vocabulary words.
5. **Cultural Note**: If relevant, share cultural context about these items in {target_language}-speaking regions.

Format the response clearly with numbered sections.
```

### 4.6 Expected AI Output Sections

1. **Identified Objects** — list of items found in image
2. **Translations** — source → target for each item
3. **Pronunciation** — phonetic guide per word
4. **Example Sentences** — contextual usage
5. **Cultural Note** — relevant cultural insight

### 4.7 UI Wireframe

```
┌──────────────────────────────────────────────────────────┐
│  🖼️  Visual Learning                                    │
│  Upload an image · discover vocabulary in your language  │
│                                                          │
│  ⚠️ Vision model not detected (if text-only model)      │
│                                                          │
│ ┌──────────────┐   ┌──────────────────────────────────┐ │
│ │              │   │  Visual Vocabulary    2.1s        │ │
│ │  🖼️ Drag &   │   │  ## Identified Objects            │ │
│ │  drop image  │   │  ...                              │ │
│ │  or click    │   │  ## Translations                  │ │
│ │              │   │  ...                              │ │
│ ├──────┬───────┤   │  ## Pronunciation                 │ │
│ │Learn▼│From ▼ │   │  ...                              │ │
│ ├──────┴───────┤   └──────────────────────────────────┘ │
│ [🔍 Identify]  │                                        │
│                │                                        │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Skill 3 — Translation Practice

### 5.1 Overview

| Property        | Value                                                         |
|-----------------|---------------------------------------------------------------|
| **Tab icon**    | 🔄                                                            |
| **Gradient**    | `.translation-gradient` — gold → amber                       |
| **Endpoint**    | `POST /api/translation`                                       |
| **State**       | Stateless                                                     |
| **Token budget**| `MAX_TOKENS_TRANSLATION = 512`                                |
| **Tagline**     | "Translate a sentence · get scored and corrected by AI"       |

### 5.2 Input Specification

| Field              | HTML Element   | ID                 | Type       | Default        | Validation        |
|--------------------|----------------|---------------------|------------|----------------|-------------------|
| Source Language     | `<select>`     | `trans-source-lang` | Dropdown   | English        | Required          |
| Target Language    | `<select>`     | `trans-target-lang` | Dropdown   | French         | Required          |
| Proficiency        | `<select>`     | `trans-level`       | Dropdown   | Intermediate   | Required          |
| Original Text      | `<textarea>`   | `trans-original`    | Freeform   | —              | Non-empty         |
| Student Translation| `<textarea>`   | `trans-student`     | Freeform   | —              | Non-empty         |

### 5.3 Special UI Components

**Language Swap Button** (`#trans-swap`):
- Displays `⇄` between the two textareas
- On click: swaps source/target language selectors AND textarea contents
- Hover: rotates 180deg with scale(1.2), colour changes to cyan

**Language Tags** (`#trans-from-tag`, `#trans-to-tag`):
- Small pill badges next to textarea labels showing the selected language
- Updated dynamically on language selection change

### 5.4 Example Chips

| Label              | Source | Target | Level               | Original                                              | Student Translation                                          |
|--------------------|--------|--------|----------------------|-------------------------------------------------------|--------------------------------------------------------------|
| EN→FR park sentence| English| French | Intermediate (B1-B2) | "The children are playing in the park near the river."| "Les enfants jouent dans le parc près de la rivière."        |
| EN→FR restaurant   | English| French | Beginner (A1-A2)     | "I would like to book a table for two tonight."       | "Je voudrais réserver une table pour deux personnes ce soir."|

### 5.5 API Contract

**Request:**
```json
{
  "original": "string — original text in source language",
  "student_translation": "string — student's attempt",
  "source_lang": "string",
  "target_lang": "string",
  "level": "string — CEFR level"
}
```

**Response:**
```json
{
  "result": "string — markdown feedback",
  "timing": "string"
}
```

### 5.6 Prompt Engineering Pattern

**System prompt:**
```
You are a professional {source_lang}-to-{target_lang} translation tutor.
The student's level is {proficiency}. Be encouraging but thorough.
```

**User prompt:**
```
A {proficiency} student was asked to translate this from {source_lang} to {target_lang}:

**Original ({source_lang}):** "{original_text}"
**Student's Translation ({target_lang}):** "{student_translation}"

Please provide:
1. **Your ideal translation** of the original text
2. **Accuracy score** (1-10)
3. **Specific corrections** — What did the student get wrong?
4. **What they got right** — Praise good parts
5. **Grammar notes** — Key grammar rules they should review
6. **Alternative translations** — Other valid ways to translate this
```

### 5.7 Expected AI Output Sections

1. **Ideal Translation** — model's reference translation
2. **Accuracy Score** — 1-10 numeric rating
3. **Specific Corrections** — detailed error breakdown
4. **Praise** — what the student got right
5. **Grammar Notes** — relevant rules to review
6. **Alternative Translations** — other valid translations

### 5.8 UI Wireframe

```
┌─────────────────────────────────────────────────────────┐
│  🔄  Translation Practice                               │
│  Translate a sentence · get scored and corrected         │
├──────────┬──────────┬───────────────────────────────────┤
│ From ▼   │ To ▼     │ Level ▼                           │
├──────────┴──────────┴───────────────────────────────────┤
│ ┌──────────────┐       ┌──────────────┐                 │
│ │ Original     │  ⇄    │ Translation  │                 │
│ │ [English]    │       │ [French]     │                 │
│ │ [textarea]   │       │ [textarea]   │                 │
│ └──────────────┘       └──────────────┘                 │
│                                                         │
│ Quick example: [EN→FR park] [EN→FR restaurant]          │
│                                                         │
│ [ ✅ Check My Translation → ]                           │
│                                                         │
│ ┌─ Translation Feedback ─────────── Response time: 2s ┐ │
│ │ ## Your ideal translation                           │ │
│ │ ...                                                 │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Skill 4 — Vocabulary Builder

### 6.1 Overview

| Property        | Value                                                      |
|-----------------|------------------------------------------------------------|
| **Tab icon**    | 📚                                                         |
| **Gradient**    | `.vocab-gradient` — green → emerald                        |
| **Endpoint**    | `POST /api/vocabulary`                                     |
| **State**       | Stateless                                                  |
| **Token budget**| `MAX_TOKENS_VOCABULARY = 1500` (largest of all skills)     |
| **Tagline**     | "Enter a topic · get a full vocabulary lesson with a quiz" |

### 6.2 Input Specification

| Field         | HTML Element      | ID             | Type    | Default    | Range / Validation  |
|---------------|-------------------|----------------|---------|------------|---------------------|
| Topic         | `<input text>`    | `vocab-topic`  | Freeform| —          | Non-empty           |
| Target Language| `<select>`       | `vocab-lang`   | Dropdown| Swahili    | Required            |
| Proficiency   | `<select>`        | `vocab-level`  | Dropdown| Beginner   | Required            |
| Word Count    | `<input range>`   | `vocab-num`    | Slider  | 10         | Min 5, Max 20, Step 1 |

### 6.3 Special UI Components

**Range Slider** (`#vocab-num`):
- Live display updates via `#vocab-num-display` span
- Labels: `5` (left) and `20` (right) below the slider
- CSS accent-color: `var(--purple)`

### 6.4 Example Chips

| Label              | Topic               | Language | Level              |
|--------------------|----------------------|----------|--------------------|
| Food · Swahili     | Food and Cooking     | Swahili  | Beginner (A1-A2)   |
| School · French    | School and Education | French   | Intermediate (B1-B2)|
| Family · Lingala   | Family and Relationships | Lingala | Beginner (A1-A2) |
| Transport · Japanese| Transportation      | Japanese | Beginner (A1-A2)   |

### 6.5 API Contract

**Request:**
```json
{
  "topic": "string — freeform topic",
  "language": "string — target language",
  "level": "string — CEFR level",
  "num_words": "integer — 5 to 20"
}
```

**Response:**
```json
{
  "result": "string — markdown lesson",
  "timing": "string"
}
```

### 6.6 Prompt Engineering Pattern

**System prompt:**
```
You are a {target_language} vocabulary tutor.
Create engaging vocabulary lessons appropriate for {proficiency} learners.
Make learning fun and memorable.
```

**User prompt:**
```
Create a vocabulary lesson about "{topic}" in {target_language}
for a {proficiency} student.

Include:
1. **{num_words} Key Words**: Each with translation, pronunciation, and part of speech
2. **Example Sentences**: One sentence per word showing it in context
3. **Common Phrases**: 3-5 useful phrases related to the topic
4. **Mini Quiz**: 3 fill-in-the-blank questions to test the vocabulary
5. **Memory Tips**: Mnemonics or tricks to remember difficult words
```

### 6.7 Expected AI Output Sections

1. **Key Words** — word table: target word | translation | pronunciation | part of speech
2. **Example Sentences** — one per word in context
3. **Common Phrases** — 3–5 practical phrases
4. **Mini Quiz** — 3 fill-in-the-blank exercises
5. **Memory Tips** — mnemonic devices

### 6.8 UI Wireframe

```
┌───────────────────────────────────────────────────────────┐
│  📚  Vocabulary Builder                                   │
│  Enter a topic · get a full vocabulary lesson with quiz   │
├───────────────────────────────────────────────────────────┤
│ Topic: [_________________________________]  (full width)  │
├──────────┬──────────┬─────────────────────────────────────┤
│ Language▼│ Level ▼  │ Words: 10                           │
│          │          │ ├────●──────────────┤               │
│          │          │ 5                 20                │
├──────────┴──────────┴─────────────────────────────────────┤
│ Quick example: [Food·Swahili] [School·French] [Family·Lingala] [Transport·JP] │
│                                                           │
│ [ 📖 Generate Lesson → ]                                 │
│                                                           │
│ ┌─ Vocabulary Lesson ──────────────── Response time: 5s ┐ │
│ │ ## Key Words                                          │ │
│ │ | Word | Translation | Pronunciation | Part of Speech │ │
│ │ ...                                                   │ │
│ │ ## Mini Quiz                                          │ │
│ │ ...                                                   │ │
│ └───────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

---

## 7. Skill 5 — Conversation Practice

### 7.1 Overview

| Property        | Value                                                          |
|-----------------|----------------------------------------------------------------|
| **Tab icon**    | 💬                                                             |
| **Gradient**    | `.convo-gradient` — coral → rose                               |
| **Endpoint**    | `POST /api/conversation`                                       |
| **State**       | **STATEFUL** — chat history persists across turns               |
| **Token budget**| `MAX_TOKENS_CONVERSATION = 768`                                |
| **Tagline**     | "Choose a scenario · chat with your AI partner · get inline corrections" |

### 7.2 Input Specification

| Field           | HTML Element   | ID               | Type       | Default                           | Validation   |
|-----------------|----------------|-------------------|------------|-----------------------------------|-------------|
| Scenario        | `<select>`     | `convo-scenario`  | Dropdown   | "At a restaurant ordering food"   | Required     |
| Target Language | `<select>`     | `convo-lang`      | Dropdown   | French                            | Required     |
| Proficiency     | `<select>`     | `convo-level`     | Dropdown   | Beginner                          | Required     |
| Message Input   | `<textarea>`   | `convo-input`     | Freeform   | —                                 | Non-empty    |

### 7.3 Conversation Scenarios

| # | Scenario                               |
|---|----------------------------------------|
| 1 | At a restaurant ordering food          |
| 2 | Asking for directions on the street    |
| 3 | Job interview at a tech company        |
| 4 | Meeting a new friend at school         |
| 5 | Shopping at a market                   |
| 6 | Visiting a doctor                      |
| 7 | Checking into a hotel                  |
| 8 | At the train station buying tickets    |

### 7.4 Special UI Components

**Chat Window** (`#chat-window`):
- Min height 340px, max height 520px
- Scroll-to-bottom on new message
- Empty state with 🗣️ icon and example prompt
- User bubbles: coral gradient, right-aligned, white text, rounded (bottom-right: 4px)
- AI bubbles: light purple background, left-aligned, markdown-rendered
- Typing indicator: 3 bouncing dots

**Message Input** (`#convo-input`):
- 2 rows, auto-growing on input (max 140px)
- Enter = send, Shift+Enter = newline
- Focus ring: coral `box-shadow: 0 0 0 3px rgba(255,107,107,0.12)`

**Reset Button** (`#convo-reset`):
- 🔄 "New Conversation" — clears chat history and all bubbles
- Shows success toast on reset

### 7.5 State Management

```
Client (ChatManager.history)           Server (stateless)
   ├─ stores history string              ├─ receives history in request
   ├─ sends with every POST              ├─ appends new exchange
   ├─ updates from response              ├─ returns updated history
   └─ resets on "New Conversation"       └─ no persistence
```

**History format** (plain text):
```
Student: {message_1}
Tutor: {response_1}
Student: {message_2}
Tutor: {response_2}
```

### 7.6 API Contract

**Request:**
```json
{
  "message": "string — student's latest message",
  "scenario": "string — selected scenario",
  "language": "string — target language",
  "level": "string — CEFR level",
  "history": "string — accumulated chat history"
}
```

**Response:**
```json
{
  "result": "string — AI response markdown",
  "timing": "string",
  "history": "string — updated chat history"
}
```

### 7.7 Prompt Engineering Pattern

**System prompt:**
```
You are a friendly conversation partner helping a {proficiency} student
practise {target_language}. The scenario is: {scenario}.

Rules:
- Respond naturally IN {target_language}
- After your response, add a section called "Language Notes:" where you:
  * Correct any errors in the student's message
  * Explain grammar points
  * Suggest more natural ways to say things
- Keep the conversation going by asking a follow-up question
- Adjust complexity to {proficiency} level
```

**User prompt:**
```
Previous conversation:
{chat_history}

Student says: "{user_message}"

Respond in character (in {target_language}), then provide language notes.
```

### 7.8 Expected AI Output

1. **In-character response** — natural dialogue in target language
2. **Language Notes section:**
   - Error corrections from student's message
   - Grammar point explanations
   - Natural phrasing suggestions
   - Follow-up question to continue dialogue

### 7.9 UI Wireframe

```
┌───────────────────────────────────────────────────────────┐
│  💬  Conversation Practice                                │
│  Choose a scenario · chat with AI · get inline corrections│
├───────────────────────────────────────────────────────────┤
│ Scenario: [At a restaurant ordering food ▼]  (full width) │
├──────────┬──────────┬─────────────────────────────────────┤
│ Language▼│ Level ▼  │ [🔄 New Conversation]               │
├──────────┴──────────┴─────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐   │
│ │                  🗣️                                 │   │
│ │  Start the conversation by typing a message below.  │   │
│ │  Try: "Bonjour, je voudrais une table pour deux."   │   │
│ │                                                     │   │
│ │           🤖 Bienvenue! Combien de personnes?       │   │
│ │                                                     │   │
│ │                     Bonjour, une table pour deux  🧑‍🎓│   │
│ │                                                     │   │
│ │           🤖 Très bien! Suivez-moi...              │   │
│ │              Language Notes:                        │   │
│ │              ✅ Good greeting...                    │   │
│ └─────────────────────────────────────────────────────┘   │
│ ┌─────────────────────────────────────────────┐ [Send ▶] │
│ │ Type in your target language…                │           │
│ └─────────────────────────────────────────────┘           │
│                                         Response time: 2s │
└───────────────────────────────────────────────────────────┘
```

---

## 8. Adding a New Skill — Step-by-Step

Use this checklist when adding a 6th (or beyond) skill to the platform.

### Step 1 — Config (`mwalimu/config.py`)

```python
# Add token budget
MAX_TOKENS_NEWSKILL = 1024   # Adjust based on expected output length

# Add any skill-specific constants (if needed)
NEWSKILL_OPTIONS = ["Option A", "Option B", "Option C"]
```

### Step 2 — Feature Function (`mwalimu/features/newskill.py`)

```python
"""
mwalimu/features/newskill.py
-----------------------------
Feature N — New Skill Name (Tab N).
"""

from typing import Tuple
from mwalimu.inference import query_model
from mwalimu.config import MAX_TOKENS_NEWSKILL


def new_skill_function(
    param1: str,
    param2: str,
    # ... additional parameters
) -> Tuple[str, str]:
    """Returns (markdown_result, timing_string)."""
    if not param1.strip():
        return "Please provide input.", ""

    system_prompt = (
        "You are a [role description].\n"
        "The student's level is [level].\n"
        "[Output format instructions]"
    )

    prompt = (
        "[Task description with student data]\n\n"
        "[Numbered output sections]"
    )

    response, exec_time = query_model(prompt, system_prompt, MAX_TOKENS_NEWSKILL)
    return response, f"Response time: {exec_time}s"
```

### Step 3 — Register in `mwalimu/features/__init__.py`

```python
from mwalimu.features.newskill import new_skill_function
```

### Step 4 — API Endpoint (`flask_app.py`)

```python
@app.route("/api/newskill", methods=["POST"])
def api_newskill():
    data = request.get_json(force=True)
    result, timing = new_skill_function(
        data.get("param1", ""),
        data.get("param2", "default_value"),
    )
    return jsonify({"result": result, "timing": timing})
```

### Step 5 — Tab Button (`templates/index.html`)

Add inside the `<nav class="tab-nav">`:

```html
<button class="tab-btn" role="tab" aria-selected="false"
        data-tab="newskill" aria-controls="tab-newskill">
  <span class="tab-icon">🆕</span>
  <span class="tab-label">New Skill</span>
</button>
```

### Step 6 — Tab Panel (`templates/index.html`)

Add inside `<main class="tab-content">`:

```html
<section class="tab-panel" id="tab-newskill" role="tabpanel"
         aria-labelledby="btn-newskill">
  <div class="panel-header">
    <div class="panel-icon-wrap newskill-gradient">🆕</div>
    <div>
      <h2 class="panel-title">New Skill Name</h2>
      <p class="panel-desc">Brief tagline describing the skill</p>
    </div>
  </div>

  <!-- Form inputs -->
  <div class="form-grid form-grid--2col">
    <!-- dropdowns, inputs, textareas -->
  </div>

  <!-- Example chips -->
  <div class="example-chips" data-feature="newskill">
    <span class="chip-label">Quick example:</span>
    <button class="chip" data-param1="..." data-param2="...">Example 1</button>
  </div>

  <!-- Submit -->
  <button class="submit-btn newskill-gradient" id="newskill-submit">
    <span class="btn-text">Submit</span>
    <span class="btn-icon">→</span>
  </button>

  <!-- Result -->
  <div class="result-card hidden" id="newskill-result">
    <div class="result-header">
      <span class="result-title">AI Result</span>
      <span class="result-timing" id="newskill-timing"></span>
    </div>
    <div class="result-body markdown-body" id="newskill-output"></div>
  </div>
</section>
```

### Step 7 — CSS Gradient (`static/css/style.css`)

```css
/* Add to :root */
--grad-newskill: linear-gradient(135deg, #color1 0%, #color2 100%);

/* Add gradient class */
.newskill-gradient { background: var(--grad-newskill); }
```

### Step 8 — TypeScript Handler (`static/ts/main.ts`)

Add method to `MwalimuApp` class:

```typescript
initNewSkill(): void {
  // Wire up example chips
  document.querySelectorAll('[data-feature="newskill"] .chip').forEach(chip => {
    chip.addEventListener('click', () => {
      $('newskill-param1').value = (chip as HTMLElement).dataset.param1!;
    });
  });

  // Submit handler
  const btn = $('newskill-submit') as HTMLButtonElement;
  btn.addEventListener('click', async () => {
    const param1 = ($('newskill-param1') as HTMLInputElement).value.trim();
    if (!param1) { showToast('Please provide input.', 'error'); return; }

    setButtonLoading(btn, true);
    setLoading(true, 'Processing…');
    try {
      const data = await apiPost('/api/newskill', { param1 });
      showResult('newskill-result', 'newskill-output', 'newskill-timing',
                 data.result, data.timing);
    } catch (e: any) { showToast(e.message, 'error'); }
    finally { setButtonLoading(btn, false); setLoading(false); }
  });
}
```

Then call `this.initNewSkill()` in the `MwalimuApp` constructor.

### Step 9 — Compile TypeScript

```bash
tsc --target ES2020 --lib ES2020,DOM --strict --outDir static/js static/ts/main.ts
```

### Step 10 — Update Hero Stats

In `templates/index.html`, update the learning modes counter:

```html
<span class="stat-number" data-count="6">0</span>
<span class="stat-label">Learning Modes</span>
```

### Verification Checklist

- [ ] Config constant added to `mwalimu/config.py`
- [ ] Feature function created in `mwalimu/features/`
- [ ] Feature exported from `mwalimu/features/__init__.py`
- [ ] API endpoint added to `flask_app.py`
- [ ] Tab button added to `index.html` nav
- [ ] Tab panel section added to `index.html` main
- [ ] CSS gradient defined in `style.css`
- [ ] TypeScript handler in `main.ts`
- [ ] JavaScript compiled from TypeScript
- [ ] Hero stat counter incremented
- [ ] Manual test: form submission → loading → result rendered
- [ ] Manual test: example chips populate form correctly
- [ ] Manual test: empty input shows toast error
- [ ] Responsive check: mobile layout (form-grid stacks)

---

## Appendix A — Supported Languages

All 14 languages available in every skill dropdown:

| Priority | Language           | Code   | Notes                                   |
|----------|--------------------|--------|-----------------------------------------|
| 1        | French             | fr     | Primary target — DRC official language   |
| 2        | Swahili            | sw     | Primary target — DRC lingua franca       |
| 3        | Lingala            | ln     | Primary target — DRC lingua franca       |
| 4        | Arabic             | ar     | Regional importance                      |
| 5        | English            | en     | International baseline                   |
| 6        | Spanish            | es     | Global demand                            |
| 7        | Portuguese         | pt     | African Portuguese-speaking countries    |
| 8        | Chinese (Mandarin) | zh     | Global demand                            |
| 9        | German             | de     | European language                        |
| 10       | Japanese           | ja     | Research context (Kobe, Japan)           |
| 11       | Korean             | ko     | East Asian language                      |
| 12       | Hindi              | hi     | South Asian language                     |
| 13       | Italian            | it     | European language                        |
| 14       | Russian            | ru     | Global language                          |

## Appendix B — CEFR Proficiency Levels

| Level               | CEFR  | Description                                       |
|---------------------|-------|---------------------------------------------------|
| Beginner (A1-A2)    | A1-A2 | Basic phrases, simple interactions                |
| Intermediate (B1-B2)| B1-B2 | Independent use, can handle most situations       |
| Advanced (C1-C2)    | C1-C2 | Fluent, nuanced, near-native comprehension        |

## Appendix C — Generation Parameters

Shared across all skills (configured in `mwalimu/config.py`):

| Parameter    | Value | Rationale                                         |
|--------------|-------|---------------------------------------------------|
| temperature  | 0.7   | Balance creativity and coherence                  |
| top_p        | 0.9   | Nucleus sampling — keeps diversity                |
| do_sample    | true  | Enable sampling (not greedy)                      |

Per-skill token budgets:

| Skill         | Max Tokens | Reason                                         |
|---------------|------------|------------------------------------------------|
| Writing       | 1024       | Multi-section feedback                          |
| Visual        | 1024       | Object list + translations + sentences          |
| Translation   | 512        | Structured scoring (shorter output)             |
| Vocabulary    | 1500       | Word list + sentences + quiz + tips (longest)   |
| Conversation  | 768        | Dialogue + language notes                       |

## Appendix D — File Map

| Layer         | File                              | Responsibility                        |
|---------------|-----------------------------------|---------------------------------------|
| Config        | `mwalimu/config.py`              | All constants, languages, levels       |
| Inference     | `mwalimu/inference.py`           | `query_model()`, `query_model_with_image()` |
| Features      | `mwalimu/features/writing.py`    | Writing feedback                       |
| Features      | `mwalimu/features/visual.py`     | Visual learning                        |
| Features      | `mwalimu/features/translation.py`| Translation practice                   |
| Features      | `mwalimu/features/vocabulary.py` | Vocabulary builder                     |
| Features      | `mwalimu/features/conversation.py`| Conversation practice                 |
| API Server    | `flask_app.py`                   | Flask routes, JSON endpoints           |
| HTML Template | `templates/index.html`           | Jinja2 template, all 5 tab panels      |
| Styles        | `static/css/style.css`           | Design system, all component styles    |
| TypeScript    | `static/ts/main.ts`             | Source — classes + app wiring           |
| JavaScript    | `static/js/main.js`             | Compiled output (run in browser)        |
