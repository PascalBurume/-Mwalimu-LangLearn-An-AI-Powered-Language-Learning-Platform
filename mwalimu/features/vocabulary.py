"""
mwalimu/features/vocabulary.py
-------------------------------
Feature 4 — Vocabulary Builder (Tab 4).

Given a topic and proficiency level the model generates a complete themed
vocabulary lesson including:
    1. N key words with translation, pronunciation, and part of speech.
    2. One example sentence per word showing it in context.
    3. 3-5 common phrases related to the topic.
    4. A 3-question fill-in-the-blank mini quiz.
    5. Memory tips / mnemonics for difficult words.

Design notes:
    - Stateless: each lesson generation is independent.
    - num_words is user-configurable (5-20) via a Gradio Slider.
    - max_new_tokens=1500 is the largest budget of all 5 features because the
      output is intentionally verbose (word list + sentences + quiz + tips).
    - The topic is free-form text so students can request niche vocabulary.

References:
    - Notebook cell 11, function vocabulary_builder()
    - CODEBASE_ANALYSIS.md §2.3 (feature map — Vocabulary Builder row)
    - CODEBASE_ANALYSIS.md §4.5 (generation parameters table)
"""

from typing import Tuple

from mwalimu.inference import query_model
from mwalimu.config import MAX_TOKENS_VOCABULARY


def vocabulary_builder(
    topic: str,
    target_language: str,
    proficiency: str,
    num_words: int = 10,
) -> Tuple[str, str]:
    """
    Generate a themed vocabulary lesson for the given topic and language.

    Args:
        topic:           Free-form topic string (e.g. "Food and Cooking",
                         "School", "Transportation").
        target_language: Language of the vocabulary lesson.
        proficiency:     CEFR level to calibrate word complexity.
        num_words:       Number of vocabulary words to include (5-20).

    Returns:
        (lesson_markdown, timing_string)
    """
    if not topic.strip():
        return "Please enter a topic to generate a vocabulary lesson.", ""

    system_prompt = (
        f"You are a {target_language} vocabulary tutor.\n"
        f"Create engaging vocabulary lessons appropriate for {proficiency} learners.\n"
        "Make learning fun and memorable."
    )

    prompt = (
        f"Create a vocabulary lesson about \"{topic}\" in {target_language} "
        f"for a {proficiency} student.\n\n"
        "Include:\n"
        f"1. **{num_words} Key Words**: Each with translation, pronunciation, "
        "and part of speech\n"
        "2. **Example Sentences**: One sentence per word showing it in context\n"
        "3. **Common Phrases**: 3-5 useful phrases related to the topic\n"
        "4. **Mini Quiz**: 3 fill-in-the-blank questions to test the vocabulary\n"
        "5. **Memory Tips**: Mnemonics or tricks to remember difficult words"
    )

    response, exec_time = query_model(prompt, system_prompt, MAX_TOKENS_VOCABULARY)
    return response, f"Response time: {exec_time}s"
