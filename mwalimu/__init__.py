"""
mwalimu — AI-powered language learning platform.

3-layer architecture:
    PRESENTATION  ->  mwalimu.ui.interface   (Gradio 5-tab web app)
    APPLICATION   ->  mwalimu.features       (5 feature functions)
    INFERENCE     ->  mwalimu.inference      (Ollama client wrapper)

Configuration lives in mwalimu.config (languages, generation params, etc.).

Quick start:
    python main.py

See README.md for full setup instructions.
"""

__version__ = "0.1.0"
__author__  = "Pascal Burume Buhendwa"