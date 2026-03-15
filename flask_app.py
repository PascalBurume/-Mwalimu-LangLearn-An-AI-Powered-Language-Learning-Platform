"""
flask_app.py — Mwalimu-LangLearn Flask entry point
----------------------------------------------------
Replaces the Gradio interface with a Flask + TypeScript animated web app.

Run:
    python flask_app.py                   # localhost:5000
    python flask_app.py --port 8080       # custom port
    python flask_app.py --debug           # dev mode with auto-reload

Prerequisites:
    pip install flask pillow
    ollama serve  &&  ollama pull gemma3n:e4b
"""

import argparse
import base64
import io
import os
import sys

from flask import Flask, jsonify, render_template, request
from PIL import Image

# ── Allow env-var overrides before mwalimu imports its config defaults ─────────
if "OLLAMA_HOST" in os.environ:
    import mwalimu.config as _cfg
    _cfg.OLLAMA_HOST = os.environ["OLLAMA_HOST"]
if "OLLAMA_MODEL" in os.environ:
    import mwalimu.config as _cfg
    _cfg.OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]

from mwalimu.config import (
    CONVERSATION_SCENARIOS,
    LANGUAGES,
    PROFICIENCY_LEVELS,
)
from mwalimu.features.conversation import conversation_practice
from mwalimu.features.translation import translation_practice
from mwalimu.features.visual import visual_learning
from mwalimu.features.vocabulary import vocabulary_builder
from mwalimu.features.writing import writing_feedback
from mwalimu.inference import HAS_VISION, OLLAMA_MODEL, check_connection

app = Flask(__name__)


# ── Page ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template(
        "index.html",
        languages=LANGUAGES,
        proficiency_levels=PROFICIENCY_LEVELS,
        conversation_scenarios=CONVERSATION_SCENARIOS,
        has_vision=HAS_VISION,
        model=OLLAMA_MODEL,
    )


# ── Status ────────────────────────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    ok, models = check_connection()
    return jsonify({
        "connected": ok,
        "models": models,
        "current_model": OLLAMA_MODEL,
        "has_vision": HAS_VISION,
    })


# ── Feature 1: Writing Feedback ───────────────────────────────────────────────

@app.route("/api/writing", methods=["POST"])
def api_writing():
    data = request.get_json(force=True)
    result, timing = writing_feedback(
        data.get("text", ""),
        data.get("language", "French"),
        data.get("level", "Intermediate (B1-B2)"),
    )
    return jsonify({"result": result, "timing": timing})


# ── Feature 2: Visual Learning ────────────────────────────────────────────────

@app.route("/api/visual", methods=["POST"])
def api_visual():
    # Accept either multipart/form-data (file) or JSON with base64 image
    if request.files.get("image"):
        image = Image.open(request.files["image"].stream)
        target_language = request.form.get("target_language", "French")
        source_language = request.form.get("source_language", "English")
    elif request.is_json:
        data = request.get_json()
        img_bytes = base64.b64decode(data.get("image_b64", ""))
        image = Image.open(io.BytesIO(img_bytes))
        target_language = data.get("target_language", "French")
        source_language = data.get("source_language", "English")
    else:
        return jsonify({"error": "No image provided"}), 400

    result, timing = visual_learning(image, target_language, source_language)
    return jsonify({"result": result, "timing": timing})


# ── Feature 3: Translation Practice ──────────────────────────────────────────

@app.route("/api/translation", methods=["POST"])
def api_translation():
    data = request.get_json(force=True)
    result, timing = translation_practice(
        data.get("original", ""),
        data.get("student_translation", ""),
        data.get("source_lang", "English"),
        data.get("target_lang", "French"),
        data.get("level", "Intermediate (B1-B2)"),
    )
    return jsonify({"result": result, "timing": timing})


# ── Feature 4: Vocabulary Builder ────────────────────────────────────────────

@app.route("/api/vocabulary", methods=["POST"])
def api_vocabulary():
    data = request.get_json(force=True)
    result, timing = vocabulary_builder(
        data.get("topic", ""),
        data.get("language", "Swahili"),
        data.get("level", "Beginner (A1-A2)"),
        int(data.get("num_words", 10)),
    )
    return jsonify({"result": result, "timing": timing})


# ── Feature 5: Conversation Practice ─────────────────────────────────────────

@app.route("/api/conversation", methods=["POST"])
def api_conversation():
    data = request.get_json(force=True)
    result, history, timing = conversation_practice(
        data.get("message", ""),
        data.get("scenario", "At a restaurant ordering food"),
        data.get("language", "French"),
        data.get("level", "Beginner (A1-A2)"),
        data.get("history", ""),
    )
    return jsonify({"result": result, "history": history, "timing": timing})


# ── CLI ───────────────────────────────────────────────────────────────────────

def startup_check() -> None:
    print("\n" + "=" * 58)
    print("  Mwalimu-LangLearn  [Flask + TypeScript UI]")
    print("=" * 58)
    ok, available = check_connection()
    if not ok:
        print(f"  ERROR: Ollama not reachable. Run:  ollama serve")
        sys.exit(1)
    print(f"  Model   : {OLLAMA_MODEL}")
    print(f"  Vision  : {'enabled' if HAS_VISION else 'disabled (text-only)'}")
    print(f"  Models  : {', '.join(available) or '(none pulled)'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mwalimu-LangLearn Flask server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    startup_check()
    print(f"  URL     : http://127.0.0.1:{args.port}")
    print("=" * 58 + "\n")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()