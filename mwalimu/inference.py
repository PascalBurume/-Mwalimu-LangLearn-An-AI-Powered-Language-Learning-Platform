"""
mwalimu/inference.py
--------------------
Core inference engine — the bottom layer of the 3-layer architecture.

    PRESENTATION  ->  Gradio 5-tab interface  (ui/interface.py)
    APPLICATION   ->  Feature functions        (features/)
    INFERENCE     ->  THIS FILE

Why a separate inference layer?
    The inference layer is intentionally decoupled from feature logic so the
    underlying model can be swapped (e.g., for a quantized GGUF/ONNX model
    for offline DRC school deployment) without touching any feature or UI code.
    See CODEBASE_ANALYSIS.md §3.1 for the architectural rationale.

Backend: Ollama (local HTTP server running Gemma 3n or any compatible model).
    Text-only queries  -> query_model()
    Image + text       -> query_model_with_image()  (requires vision-capable model)

References:
    - CODEBASE_ANALYSIS.md §4 (inference pipeline)
    - CODEBASE_ANALYSIS.md §5.3 (inference pipeline flowchart)
    - Notebook cells 6 & 9 (Ollama client setup + function implementations)
"""

import io
from time import time
from typing import Optional, List, Tuple

import ollama
from PIL import Image

from mwalimu.config import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
    TEMPERATURE,
    TOP_P,
    VISION_MODEL_KEYWORDS,
)

# ── Module-level client & capability flag ─────────────────────────────────────
# Initialised once when this module is first imported so that every feature
# function reuses the same persistent connection.

client: ollama.Client = ollama.Client(host=OLLAMA_HOST)

# Detect whether the configured model supports image input.
# HAS_VISION is read by visual_learning() to show a helpful error instead of
# crashing when the user uploads an image to a text-only model.
HAS_VISION: bool = any(kw in OLLAMA_MODEL for kw in VISION_MODEL_KEYWORDS)


def check_connection() -> Tuple[bool, List[str]]:
    """
    Verify that Ollama is reachable and return the list of available models.

    Returns:
        (ok, model_names) — ok=True if connection succeeded.
    """
    try:
        models = client.list()
        names = [m.model for m in models.models]
        return True, names
    except Exception:
        return False, []


# ── Text-only inference ────────────────────────────────────────────────────────

def query_model(
    prompt: str,
    system_prompt: Optional[str] = None,
    max_new_tokens: int = 512,
) -> Tuple[str, float]:
    """
    Send a text-only chat request to the local Ollama model.

    The function builds a standard OpenAI-style messages list and calls
    ``client.chat()``.  Generation hyperparameters (temperature, top_p) are
    taken from ``mwalimu.config`` so there is a single source of truth.

    Args:
        prompt:          The user's question or learning task.
        system_prompt:   Optional role/behaviour instruction for the model.
                         Each feature function crafts a specialised system
                         prompt — see features/*.py.
        max_new_tokens:  Token budget for the response.  Each feature uses a
                         different budget (1024 for writing, 1500 for vocab…).

    Returns:
        (response_text, execution_time_seconds)

    Raises:
        RuntimeError: if the Ollama request fails.

    Pipeline (mirrors CODEBASE_ANALYSIS.md §5.3):
        build messages -> client.chat() -> extract .message.content -> return
    """
    start = time()

    messages: List[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        options={
            "num_predict": max_new_tokens,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
        },
    )

    return response.message.content, round(time() - start, 2)


# ── Multimodal inference (image + text) ───────────────────────────────────────

def query_model_with_image(
    image,
    prompt: str,
    system_prompt: Optional[str] = None,
    max_new_tokens: int = 512,
) -> Tuple[str, float]:
    """
    Send a multimodal (image + text) request to the local Ollama model.

    Requires a vision-capable model (e.g. llava, llama3.2-vision, moondream).
    The image is encoded to JPEG bytes and passed via Ollama's ``images`` field.

    Original notebook used HuggingFace AutoModelForImageTextToText with a
    MobileNet-V5 vision encoder that converts images to 256 tokens; here Ollama
    handles the vision encoding internally.

    Args:
        image:           PIL Image object or file path string.
        prompt:          Text instruction about the image.
        system_prompt:   Optional role/behaviour instruction.
        max_new_tokens:  Token budget for the response.

    Returns:
        (response_text, execution_time_seconds)

    Raises:
        RuntimeError: if vision is not available or the request fails.

    See also:
        CODEBASE_ANALYSIS.md §6.2 — Visual Learning data flow diagram.
    """
    if not HAS_VISION:
        return (
            f"Vision not available — `{OLLAMA_MODEL}` is a text-only model.\n\n"
            "To enable image learning, pull a vision model and update OLLAMA_MODEL "
            "in mwalimu/config.py:\n\n"
            "    ollama pull llava\n\n"
            "Then set OLLAMA_MODEL = \"llava\".",
            0.0,
        )

    start = time()

    # Normalise to PIL Image
    if isinstance(image, str):
        image = Image.open(image)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Encode to JPEG bytes — Ollama accepts raw bytes or base64 strings
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    messages: List[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({
        "role": "user",
        "content": prompt,
        "images": [image_bytes],
    })

    response = client.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        options={
            "num_predict": max_new_tokens,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
        },
    )

    return response.message.content, round(time() - start, 2)
