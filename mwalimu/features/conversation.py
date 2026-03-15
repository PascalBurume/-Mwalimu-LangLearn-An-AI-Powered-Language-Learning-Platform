"""
mwalimu/features/conversation.py
----------------------------------
Feature 5 — Conversation Practice (Tab 5).

This is the ONLY stateful feature.  The model plays a conversation partner
in a chosen real-world scenario, responding in the target language.  After
each reply it also adds a "Language Notes" section that:
    - Corrects errors in the student's message.
    - Explains relevant grammar points.
    - Suggests more natural phrasing.
    - Asks a follow-up question to keep the dialogue going.

State management:
    The chat_history string accumulates across turns and is stored in a
    Gradio gr.State() component (browser memory, not a database).
    The function appends the new student + tutor exchange to the history
    and returns the updated string to be saved back into gr.State().
    On "New Conversation", the UI resets history to "".

    See CODEBASE_ANALYSIS.md §4.6 (conversation state sequence diagram)
    and §6.3 (Conversation Practice state machine).

Design notes:
    - All other features (Tabs 1-4) are stateless; this one is not.
    - max_new_tokens=768 balances conversation length and response speed.
    - The scenario is injected into the system prompt so the model adopts
      the correct role (waiter, interviewer, shopkeeper, etc.).

References:
    - Notebook cell 11, function conversation_practice()
    - CODEBASE_ANALYSIS.md §3.5 (stateful vs. stateless features diagram)
    - CODEBASE_ANALYSIS.md §7.2 (conversation scenarios list)
"""

from typing import Tuple

from mwalimu.inference import query_model
from mwalimu.config import MAX_TOKENS_CONVERSATION


def conversation_practice(
    user_message: str,
    scenario: str,
    target_language: str,
    proficiency: str,
    chat_history: str = "",
) -> Tuple[str, str, str]:
    """
    Continue a scenario-based conversation and provide inline language notes.

    Args:
        user_message:  The student's latest message (in target_language ideally).
        scenario:      Real-world scenario string from CONVERSATION_SCENARIOS.
        target_language: Language being practised.
        proficiency:   CEFR level to calibrate response complexity.
        chat_history:  Accumulated conversation so far (plain text).
                       Empty string at the start of a new session.

    Returns:
        (response_markdown, updated_history, timing_string)
        response_markdown — AI reply + Language Notes section.
        updated_history   — chat_history with the new exchange appended;
                            must be stored back into gr.State by the caller.
        timing_string     — e.g. "Response time: 2.1s".
    """
    if not user_message.strip():
        return "Please type a message to continue the conversation.", chat_history, ""

    system_prompt = (
        f"You are a friendly conversation partner helping a {proficiency} student "
        f"practise {target_language}. The scenario is: {scenario}.\n\n"
        "Rules:\n"
        f"- Respond naturally IN {target_language}\n"
        "- After your response, add a section called \"Language Notes:\" where you:\n"
        "  * Correct any errors in the student's message\n"
        "  * Explain grammar points\n"
        "  * Suggest more natural ways to say things\n"
        "- Keep the conversation going by asking a follow-up question\n"
        f"- Adjust complexity to {proficiency} level"
    )

    history_block = (
        f"Previous conversation:\n{chat_history}\n\n" if chat_history else ""
    )
    prompt = (
        f"{history_block}"
        f"Student says: \"{user_message}\"\n\n"
        f"Respond in character (in {target_language}), then provide language notes."
    )

    response, exec_time = query_model(prompt, system_prompt, MAX_TOKENS_CONVERSATION)

    updated_history = f"{chat_history}\nStudent: {user_message}\nTutor: {response}"
    return response, updated_history, f"Response time: {exec_time}s"
