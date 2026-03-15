"""
mwalimu/features/visual.py
--------------------------
Feature 2 — Visual Object Recognition & Translation (Tab 2).

The student uploads a photo; the AI:
    1. Identifies all major objects/elements in the image.
    2. Translates each identified item from source_language to target_language.
    3. Provides pronunciation guides for each translated word.
    4. Writes 2-3 example sentences using the new vocabulary.
    5. Adds a cultural note relevant to the target language community.

Design notes:
    - Requires a vision-capable Ollama model (e.g. llava, llama3.2-vision).
      When the configured model is text-only, inference.query_model_with_image()
      returns a friendly explanation instead of crashing.
    - Stateless: each image upload is independent.
    - The original notebook used HuggingFace AutoModelForImageTextToText with
      MobileNet-V5 (256 image tokens).  With Ollama the vision encoding is
      handled server-side, but the prompt structure and output format are
      identical.

References:
    - Notebook cell 11, function visual_learning()
    - CODEBASE_ANALYSIS.md §2.3 (feature map — Visual Learning row)
    - CODEBASE_ANALYSIS.md §6.2 (Visual Learning data flow sequence diagram)
    - CODEBASE_ANALYSIS.md §5.1 (MobileNet-V5 vision encoder notes)
"""

from typing import Optional, Tuple

from PIL import Image

from mwalimu.inference import query_model_with_image
from mwalimu.config import MAX_TOKENS_VISUAL


def visual_learning(
    image: Optional[Image.Image],
    target_language: str,
    source_language: str = "English",
) -> Tuple[str, str]:
    """
    Identify objects in an image and teach their names in target_language.

    Args:
        image:           PIL Image from Gradio's gr.Image(type="pil") component.
                         None if the user has not uploaded anything yet.
        target_language: Language the student is learning (e.g. "Swahili").
        source_language: Base language for object labels (default: "English").

    Returns:
        (vocabulary_markdown, timing_string)
    """
    if image is None:
        return "Please upload an image to begin.", ""

    system_prompt = (
        f"You are a visual language learning assistant.\n"
        f"Help students learn {target_language} vocabulary through images.\n"
        "Be thorough but organised in your response."
    )

    prompt = (
        "Look at this image carefully. Please:\n\n"
        "1. **Identify** all major objects, people, and elements visible in the image.\n"
        f"2. **Translate** each identified item from {source_language} to {target_language}.\n"
        f"3. **Pronunciation**: Include a pronunciation guide for each {target_language} word.\n"
        f"4. **Example Sentences**: Write 2-3 simple sentences in {target_language} "
        "using these vocabulary words.\n"
        "5. **Cultural Note**: If relevant, share cultural context about these items "
        f"in {target_language}-speaking regions.\n\n"
        "Format the response clearly with numbered sections."
    )

    response, exec_time = query_model_with_image(
        image, prompt, system_prompt, MAX_TOKENS_VISUAL
    )
    return response, f"Response time: {exec_time}s"
