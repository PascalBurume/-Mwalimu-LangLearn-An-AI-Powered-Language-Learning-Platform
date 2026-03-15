# CLAUDE.md — Mwalimu-LangLearn Project Context

> Read this before doing anything. A full codebase analysis lives in `CODEBASE_ANALYSIS.md` at the repo root.

---

## What This Project Is

**Mwalimu-LangLearn** is an AI-powered language learning platform — a research prototype built as part of a Master's thesis at the Kobe Institute of Computing, Japan (ABE Initiative / JICA).

- **Author**: Pascal Burume Buhendwa
- **Thesis**: *"AI in Education for Sustainable Development in the Democratic Republic of Congo"*
- **Core model**: Google Gemma 3n E2B-IT (multimodal, 2B effective params)
- **Interface**: Gradio 4.x web app (5 tabs)
- **License**: MIT

The name "Mwalimu" means *Teacher* in Swahili. The platform targets learners in the DRC where 200+ local languages, teacher shortages, and no reliable internet make standard ed-tech inaccessible.

---

## Repository Structure

```
/
├── CLAUDE.md                              ← you are here
├── CODEBASE_ANALYSIS.md                   ← full multi-perspective deep-dive
├── README.md                              ← project overview + research context
└── Gemma3n_language_learning_Tool.ipynb   ← complete implementation (21 cells)
```

**Everything is in the notebook.** There is no `src/`, no `app.py`, no `requirements.txt`. This is a notebook-first research project.

---

## Tech Stack (Quick Reference)

| Layer | Technology |
|---|---|
| Core model | Google Gemma 3n E2B-IT via HuggingFace Transformers ≥4.53.0 |
| Vision encoder | MobileNet-V5 (via `timm`) → 256 image tokens |
| ML backend | PyTorch + `accelerate` |
| Interface | Gradio 4.x (`gr.Blocks`) |
| Model download | `kagglehub` (Kaggle environment) or HuggingFace Hub |
| Image processing | Pillow / PIL |
| Runtime | Python 3.10+ |

---

## Architecture — 3 Layers

```
PRESENTATION  →  Gradio 5-tab interface (Tab 1–5)
APPLICATION   →  5 feature functions with prompt engineering
INFERENCE     →  query_model() + query_model_with_image()
```

The inference layer is intentionally decoupled so it can be swapped for a quantized model (GGUF/ONNX) without touching feature or UI code. This is a core design requirement for the planned edge deployment in DRC schools.

---

## The 5 Features

| Tab | Feature | Input | Key Config |
|---|---|---|---|
| 1 | Writing Feedback | text + language + proficiency | `max_new_tokens=1024` |
| 2 | Visual Learning | image + target/source languages | multimodal — `query_model_with_image()` |
| 3 | Translation Practice | original + student translation + languages | `max_new_tokens=512` |
| 4 | Vocabulary Builder | topic + language + level + count (5–20) | `max_new_tokens=1500` |
| 5 | Conversation Practice | message + scenario + language + level | **stateful** — `gr.State(chat_history)` |

Only Tab 5 is stateful. Tabs 1–4 are stateless (each call is independent).

---

## Supported Languages

14 total: French, Swahili, Lingala, Arabic, English, Spanish, Portuguese, Chinese (Mandarin), German, Japanese, Korean, Hindi, Italian, Russian.

African/DRC languages (Swahili, Lingala, French) are a deliberate priority given the research context.

---

## Key Implementation Details

- **Prompt engineering**: All feature behavior is encoded in system prompts (no separate business logic). Each feature uses a "role + numbered output format" system prompt pattern.
- **Generation params**: `temperature=0.7`, `top_p=0.9`, `do_sample=True` across all features.
- **Response extraction**: The model's response is extracted by splitting on the last user message token after `batch_decode`.
- **Chat template**: Uses HuggingFace `apply_chat_template()` with Gemma 3n's `<start_of_turn>` / `<end_of_turn>` special tokens.
- **Device handling**: `device_map="auto"` and `torch_dtype="auto"` — runs on GPU (bfloat16) or CPU (float32) automatically.
- **Credentials**: Kaggle API key set via `os.environ` — never hardcoded.

---

## What Does NOT Exist (Yet)

- No `requirements.txt` or `pyproject.toml`
- No automated tests (only manual notebook cells)
- No database or persistent storage
- No authentication on the Gradio interface
- No Docker / CI/CD
- No offline/quantized model variant
- No production deployment

---

## Notebook Cell Map (for quick navigation)

| Cells | Content |
|---|---|
| 0–1 | Markdown overview + architecture diagram |
| 2 | `pip install` dependencies |
| 4 | Library imports |
| 6 | Kaggle credentials + `kagglehub.model_download` |
| 9 | `query_model()` and `query_model_with_image()` — core inference |
| 11 | 5 feature functions (`writing_feedback`, `visual_learning`, `translation_practice`, `vocabulary_builder`, `conversation_practice`) |
| 13–15 | Manual tests |
| 17 | Full Gradio `gr.Blocks` interface |
| 19 | `demo.launch(share=True, ...)` |

---

## Research Context

This is part of the broader **Mwalimu-STEM-GenAI** initiative. The next phase will extend the architecture to STEM subjects (math, physics, biology) with full offline capability via model quantization, targeting school pilots in Bukavu and Kinshasa, DRC.

For full architectural diagrams, data flows, risk analysis, and recommendations, see **`CODEBASE_ANALYSIS.md`**.
