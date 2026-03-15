"""
mwalimu/features/writing.py
---------------------------
Feature 1 — Writing Exercise Feedback (Tab 1).

The student writes a paragraph in their target language and receives:
    1. Grammar corrections with explanations
    2. Vocabulary alternatives
    3. Style and natural-phrasing tips
    4. An encouragement score out of 10

Design notes:
    - Stateless: each call is fully independent (no session history).
    - All pedagogical behaviour is encoded in the system prompt; no post-
      processing or regex parsing is needed because Gemma 3n (instruction-tuned)
      reliably produces numbered markdown sections when the system prompt asks
      for them.  See CODEBASE_ANALYSIS.md §4.4 and §5.5.
    - max_new_tokens=1024 to allow detailed multi-section feedback.

References:
    - Notebook cell 11, function writing_feedback()
    - CODEBASE_ANALYSIS.md §2.3 (feature map), §4.4 (prompt engineering pattern)
    - CODEBASE_ANALYSIS.md §6.1 (Writing Feedback data flow sequence diagram)
"""

from typing import Tuple

from mwalimu.inference import query_model
from mwalimu.config import MAX_TOKENS_WRITING


def writing_feedback(
    text: str,
    target_language: str,
    proficiency_level: str,
) -> Tuple[str, str]:
    """
    Analyse student writing and return structured pedagogical feedback.

    Args:
        text:             The student's written text in the target language.
        target_language:  Language being practised (e.g. "French", "Swahili").
        proficiency_level: CEFR level string (e.g. "Beginner (A1-A2)").

    Returns:
        (feedback_markdown, timing_string)
        feedback_markdown — multi-section markdown ready for gr.Markdown.
        timing_string     — human-readable execution time, e.g. "Response time: 3.2s".
    """
    if not text.strip():
        return "Please enter some text to analyse.", ""

    system_prompt = (
        f"You are an expert {target_language} language tutor.\n"
        f"The student's proficiency level is {proficiency_level}.\n"
        "Analyse their writing and provide:\n"
        "1. **Corrections**: Fix grammar, spelling, and syntax errors. "
        "Show the corrected version.\n"
        "2. **Explanations**: Explain each error briefly so the student learns.\n"
        "3. **Vocabulary**: Suggest better word choices or useful alternatives.\n"
        "4. **Style Tips**: Provide natural phrasing suggestions.\n"
        "5. **Score**: Give a score out of 10 with encouragement.\n"
        "Be encouraging and supportive. Use examples when helpful."
    )

    prompt = (
        f"Please review and correct this {target_language} text written by "
        f"a {proficiency_level} student:\n\n"
        f'"""\n{text}\n"""\n\n'
        "Provide detailed feedback with corrections and explanations."
    )

    response, exec_time = query_model(prompt, system_prompt, MAX_TOKENS_WRITING)
    return response, f"Response time: {exec_time}s"
