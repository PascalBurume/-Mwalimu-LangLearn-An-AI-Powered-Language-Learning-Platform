"""
mwalimu/features/translation.py
--------------------------------
Feature 3 — Translation Practice with Feedback (Tab 3).

The student is given a sentence in source_language and writes their own
translation into target_language.  The model then:
    1. Provides the ideal reference translation.
    2. Scores the student's attempt (1-10 accuracy).
    3. Lists specific corrections and explains each error.
    4. Praises what the student got right.
    5. Highlights relevant grammar rules to review.
    6. Offers alternative valid translations.

Design notes:
    - Stateless: each submission is evaluated independently.
    - The system prompt marks the model as a "professional translation tutor"
      and injects both the source/target language pair and the proficiency level
      so feedback depth scales with student expertise.
    - max_new_tokens=512 is generous for structured translation feedback.

References:
    - Notebook cell 11, function translation_practice()
    - CODEBASE_ANALYSIS.md §2.3 (feature map — Translation Practice row)
    - CODEBASE_ANALYSIS.md §4.4 (prompt engineering pattern)
"""

from typing import Tuple

from mwalimu.inference import query_model
from mwalimu.config import MAX_TOKENS_TRANSLATION


def translation_practice(
    original_text: str,
    student_translation: str,
    source_lang: str,
    target_lang: str,
    proficiency: str,
) -> Tuple[str, str]:
    """
    Evaluate a student's translation and return structured feedback.

    Args:
        original_text:        The sentence the student was asked to translate.
        student_translation:  The student's attempt in target_lang.
        source_lang:          Language of the original text (e.g. "English").
        target_lang:          Language translated into (e.g. "French").
        proficiency:          CEFR level (e.g. "Intermediate (B1-B2)").

    Returns:
        (feedback_markdown, timing_string)
    """
    if not original_text.strip() or not student_translation.strip():
        return "Please provide both the original text and your translation.", ""

    system_prompt = (
        f"You are a professional {source_lang}-to-{target_lang} translation tutor.\n"
        f"The student's level is {proficiency}. Be encouraging but thorough."
    )

    prompt = (
        f"A {proficiency} student was asked to translate this from "
        f"{source_lang} to {target_lang}:\n\n"
        f"**Original ({source_lang}):** \"{original_text}\"\n"
        f"**Student's Translation ({target_lang}):** \"{student_translation}\"\n\n"
        "Please provide:\n"
        "1. **Your ideal translation** of the original text\n"
        "2. **Accuracy score** (1-10)\n"
        "3. **Specific corrections** — What did the student get wrong?\n"
        "4. **What they got right** — Praise good parts\n"
        "5. **Grammar notes** — Key grammar rules they should review\n"
        "6. **Alternative translations** — Other valid ways to translate this"
    )

    response, exec_time = query_model(prompt, system_prompt, MAX_TOKENS_TRANSLATION)
    return response, f"Response time: {exec_time}s"
