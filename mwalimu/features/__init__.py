"""
mwalimu.features
----------------
Application layer — the 5 language learning feature functions.

Each module corresponds to one Gradio tab:
    writing      -> Tab 1: Writing Exercise Feedback
    visual       -> Tab 2: Visual Object Recognition & Translation
    translation  -> Tab 3: Translation Practice with Feedback
    vocabulary   -> Tab 4: Vocabulary Builder
    conversation -> Tab 5: Conversation Practice (stateful)

All feature functions follow the same contract:
    inputs  — user-provided values (text, image, dropdowns)
    outputs — (response_markdown: str, timing_string: str)
              conversation_practice also returns updated_history as a second
              positional value before timing_string.

See CODEBASE_ANALYSIS.md §4.4 for the shared prompt-engineering pattern.
"""

from mwalimu.features.writing import writing_feedback
from mwalimu.features.visual import visual_learning
from mwalimu.features.translation import translation_practice
from mwalimu.features.vocabulary import vocabulary_builder
from mwalimu.features.conversation import conversation_practice

__all__ = [
    "writing_feedback",
    "visual_learning",
    "translation_practice",
    "vocabulary_builder",
    "conversation_practice",
]