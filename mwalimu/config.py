"""
mwalimu/config.py
-----------------
Central configuration for Mwalimu-LangLearn.

All tunable constants live here so every other module imports from one place.
Inspired by the architecture described in CODEBASE_ANALYSIS.md §3 and §5.
"""

# ── Ollama connection ──────────────────────────────────────────────────────────
# Default model: gemma3n:e4b (text-only, Q4_K_M, ~6.9 GB).
# To enable image understanding, pull a vision model and update OLLAMA_MODEL:
#   ollama pull llava
#   Then set OLLAMA_MODEL = "llava" here or via the OLLAMA_MODEL env variable.
OLLAMA_HOST  = "http://localhost:11434"
OLLAMA_MODEL = "gemma3n:e4b"

# Models whose names indicate multimodal (vision) capability.
# Used at startup to set the HAS_VISION flag.
VISION_MODEL_KEYWORDS = ["llava", "llama3.2-vision", "moondream", "bakllava", "minicpm-v"]

# ── Generation parameters ──────────────────────────────────────────────────────
# Shared across all features unless a feature overrides max_new_tokens.
# See CODEBASE_ANALYSIS.md §4.5 for rationale.
TEMPERATURE = 0.7   # Balance creativity and coherence
TOP_P       = 0.9   # Nucleus sampling — keeps diversity, filters low-probability tokens

# Per-feature token budgets (CODEBASE_ANALYSIS.md §4.5)
MAX_TOKENS_WRITING      = 1024
MAX_TOKENS_VISUAL       = 1024
MAX_TOKENS_TRANSLATION  = 512
MAX_TOKENS_VOCABULARY   = 1500
MAX_TOKENS_CONVERSATION = 768

# ── Supported languages ────────────────────────────────────────────────────────
# 14 languages; African/DRC languages (Swahili, Lingala, French) listed first
# as a deliberate priority given the research context.
# Backed by Gemma 3n's 140+ language training corpus.
LANGUAGES = [
    "French",
    "Swahili",
    "Lingala",
    "Arabic",
    "English",
    "Spanish",
    "Portuguese",
    "Chinese (Mandarin)",
    "German",
    "Japanese",
    "Korean",
    "Hindi",
    "Italian",
    "Russian",
]

# ── CEFR proficiency levels ────────────────────────────────────────────────────
PROFICIENCY_LEVELS = [
    "Beginner (A1-A2)",
    "Intermediate (B1-B2)",
    "Advanced (C1-C2)",
]

# ── Conversation scenarios (Tab 5) ─────────────────────────────────────────────
CONVERSATION_SCENARIOS = [
    "At a restaurant ordering food",
    "Asking for directions on the street",
    "Job interview at a tech company",
    "Meeting a new friend at school",
    "Shopping at a market",
    "Visiting a doctor",
    "Checking into a hotel",
    "At the train station buying tickets",
]
