---
name: Flask + TypeScript UI
description: Flask web app replacing Gradio — 5 API endpoints + animated TypeScript frontend
type: project
---

Added Flask+TypeScript animated front-end as an alternative to the Gradio UI (original remains in main.py).

**Files created:**
- `flask_app.py` — Flask server with 5 REST endpoints (/api/writing, /api/visual, /api/translation, /api/vocabulary, /api/conversation) + /api/status
- `templates/index.html` — Jinja2 template, 5 tabs matching the Gradio layout, injects server config into `window.MWALIMU_CONFIG`
- `static/css/style.css` — Dark glassmorphism design; palette: purple #7c6dfa, coral #ff6b6b, gold #f6c90e, cyan #22d3ee; animated hero orbs, particle canvas, sliding ink-bar tabs, typewriter result reveal, chat bubbles, loading overlay
- `static/ts/main.ts` — TypeScript source with classes: ParticleSystem, TabManager, TypewriterEffect, ImageUploader, ChatManager, MwalimuApp
- `static/js/main.js` — Compiled JS (manually transpiled from main.ts — re-run `tsc` if TS is changed)

**Run:** `python flask_app.py` (default port 5000)

**Why:** User requested Gradio → Flask replacement with TypeScript animations for attractive product-design-quality UI.

**How to apply:** If user asks about the web UI, reference the Flask app. The Gradio interface (main.py) is kept for backward compatibility.