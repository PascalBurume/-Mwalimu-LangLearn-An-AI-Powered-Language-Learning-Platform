"""
mwalimu/ui/interface.py
------------------------
Presentation layer — the full Gradio Blocks interface.

Builds a 5-tab web application and wires each tab's button to the
corresponding feature function from mwalimu.features.

Tab layout (mirrors CODEBASE_ANALYSIS.md §7.1):
    Tab 1 — Writing Feedback       (stateless, two-column layout)
    Tab 2 — Visual Learning        (stateless, image upload + output)
    Tab 3 — Translation Practice   (stateless, two-column layout)
    Tab 4 — Vocabulary Builder     (stateless, slider for word count)
    Tab 5 — Conversation Practice  (STATEFUL — gr.State chat_history)

Design principles:
    - The UI layer imports from mwalimu.features only; it never calls
      inference functions directly.  This keeps the 3-layer boundary clean.
    - gr.Examples are provided for Tabs 1, 3, and 4 to reduce the barrier
      for first-time users.
    - Tab 5 stores conversation history in gr.State (browser memory).
      The "New Conversation" button resets state to empty strings.

References:
    - Notebook cell 17 (full Gradio Blocks implementation)
    - CODEBASE_ANALYSIS.md §7 (UX & Interface Design)
    - CODEBASE_ANALYSIS.md §4.7 (Gradio component hierarchy diagram)
"""

import gradio as gr

from mwalimu.config import (
    LANGUAGES,
    PROFICIENCY_LEVELS,
    CONVERSATION_SCENARIOS,
)
from mwalimu.features import (
    writing_feedback,
    visual_learning,
    translation_practice,
    vocabulary_builder,
    conversation_practice,
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
_CSS = """
.gradio-container { max-width: 1200px !important; }
"""


def build_interface() -> gr.Blocks:
    """
    Construct and return the Gradio Blocks application.

    Call ``demo.launch()`` on the returned object to start the server.
    """
    with gr.Blocks(
        title="Mwalimu-LangLearn: AI Language Tutor",
        css=_CSS,
        theme=gr.themes.Soft(),
    ) as demo:

        # ── Header ─────────────────────────────────────────────────────────────
        gr.Markdown("""
# Mwalimu-LangLearn: Interactive Language Learning Tool
### Powered by Google Gemma 3n via Ollama — Multilingual AI Tutor

Learn any of **14 languages** with AI-powered feedback on writing,
visual vocabulary, translation, and real conversation practice.

*"Mwalimu" means Teacher in Swahili.*

---
        """)

        with gr.Tabs():

            # ══════════════════════════════════════════════════════════════
            # TAB 1 — Writing Feedback
            # ══════════════════════════════════════════════════════════════
            with gr.TabItem("Writing Feedback", id=1):
                gr.Markdown("""
### Get AI Feedback on Your Writing
Write a paragraph in your target language and receive detailed corrections,
explanations, and improvement suggestions.
                """)

                with gr.Row():
                    with gr.Column(scale=1):
                        w_lang  = gr.Dropdown(LANGUAGES, value="French",
                                              label="Target Language")
                        w_level = gr.Dropdown(PROFICIENCY_LEVELS,
                                              value="Intermediate (B1-B2)",
                                              label="Proficiency Level")
                        w_input = gr.Textbox(
                            label="Your Text",
                            placeholder="Write something in your target language...",
                            lines=6,
                        )
                        w_btn = gr.Button("Get Feedback", variant="primary")

                    with gr.Column(scale=2):
                        w_output = gr.Markdown(label="Feedback")
                        w_time   = gr.Textbox(label="Performance", interactive=False)

                gr.Examples(
                    examples=[
                        [
                            "Je suis allé au magazin hier pour acheter du pain. "
                            "Le pain était très bon et je mange beaucoup.",
                            "French", "Intermediate (B1-B2)",
                        ],
                        [
                            "Ninajifunza Kiswahili kwa sababu ninapenda lugha ya Afrika. "
                            "Mimi ni mwanafunzi mzuri.",
                            "Swahili", "Beginner (A1-A2)",
                        ],
                        [
                            "きのう友達とレストランに食べました。とても美味しいでした。",
                            "Japanese", "Beginner (A1-A2)",
                        ],
                    ],
                    inputs=[w_input, w_lang, w_level],
                )

                w_btn.click(
                    fn=writing_feedback,
                    inputs=[w_input, w_lang, w_level],
                    outputs=[w_output, w_time],
                )

            # ══════════════════════════════════════════════════════════════
            # TAB 2 — Visual Learning
            # ══════════════════════════════════════════════════════════════
            with gr.TabItem("Visual Learning", id=2):
                gr.Markdown("""
### Learn Vocabulary Through Images
Upload any photo — the AI identifies objects and teaches their names in your
target language with pronunciation guides and example sentences.
                """)

                with gr.Row():
                    with gr.Column(scale=1):
                        v_image  = gr.Image(label="Upload an Image",
                                            type="pil", height=300)
                        v_target = gr.Dropdown(LANGUAGES, value="French",
                                               label="Learn Words In")
                        v_source = gr.Dropdown(LANGUAGES, value="English",
                                               label="Translate From")
                        v_btn    = gr.Button("Identify & Translate", variant="primary")

                    with gr.Column(scale=2):
                        v_output = gr.Markdown(label="Visual Vocabulary")
                        v_time   = gr.Textbox(label="Performance", interactive=False)

                v_btn.click(
                    fn=visual_learning,
                    inputs=[v_image, v_target, v_source],
                    outputs=[v_output, v_time],
                )

            # ══════════════════════════════════════════════════════════════
            # TAB 3 — Translation Practice
            # ══════════════════════════════════════════════════════════════
            with gr.TabItem("Translation Practice", id=3):
                gr.Markdown("""
### Practice Translating and Get Scored
Translate a sentence yourself, then the AI compares your version to the ideal
translation and shows you exactly what to improve.
                """)

                with gr.Row():
                    t_src_lang = gr.Dropdown(LANGUAGES, value="English",
                                             label="From Language")
                    t_tgt_lang = gr.Dropdown(LANGUAGES, value="French",
                                             label="To Language")
                    t_level    = gr.Dropdown(PROFICIENCY_LEVELS,
                                             value="Intermediate (B1-B2)",
                                             label="Level")

                t_original = gr.Textbox(
                    label="Original Text (to translate)",
                    placeholder="Enter the text to translate...",
                    lines=3,
                )
                t_student = gr.Textbox(
                    label="Your Translation",
                    placeholder="Write your translation here...",
                    lines=3,
                )

                t_btn    = gr.Button("Check My Translation", variant="primary")
                t_output = gr.Markdown(label="Translation Feedback")
                t_time   = gr.Textbox(label="Performance", interactive=False)

                gr.Examples(
                    examples=[
                        [
                            "The children are playing in the park near the river.",
                            "Les enfants jouent dans le parc près de la rivière.",
                            "English", "French", "Intermediate (B1-B2)",
                        ],
                        [
                            "I would like to book a table for two people tonight.",
                            "Je voudrais réserver une table pour deux personnes ce soir.",
                            "English", "French", "Beginner (A1-A2)",
                        ],
                    ],
                    inputs=[t_original, t_student, t_src_lang, t_tgt_lang, t_level],
                )

                t_btn.click(
                    fn=translation_practice,
                    inputs=[t_original, t_student, t_src_lang, t_tgt_lang, t_level],
                    outputs=[t_output, t_time],
                )

            # ══════════════════════════════════════════════════════════════
            # TAB 4 — Vocabulary Builder
            # ══════════════════════════════════════════════════════════════
            with gr.TabItem("Vocabulary Builder", id=4):
                gr.Markdown("""
### Build Your Vocabulary by Topic
Choose any topic and get a complete vocabulary lesson with words, sentences,
common phrases, and a mini quiz to test yourself.
                """)

                with gr.Row():
                    voc_topic = gr.Textbox(
                        label="Topic",
                        placeholder="e.g. Food, Travel, School, Weather…",
                        scale=2,
                    )
                    voc_lang  = gr.Dropdown(LANGUAGES, value="Swahili",
                                            label="Target Language", scale=1)
                    voc_level = gr.Dropdown(PROFICIENCY_LEVELS,
                                            value="Beginner (A1-A2)",
                                            label="Level", scale=1)

                voc_num = gr.Slider(minimum=5, maximum=20, value=10, step=1,
                                    label="Number of Words")
                voc_btn    = gr.Button("Generate Lesson", variant="primary")
                voc_output = gr.Markdown(label="Vocabulary Lesson")
                voc_time   = gr.Textbox(label="Performance", interactive=False)

                gr.Examples(
                    examples=[
                        ["Food and Cooking",       "Swahili", "Beginner (A1-A2)"],
                        ["School and Education",   "French",  "Intermediate (B1-B2)"],
                        ["Transportation",         "Japanese","Beginner (A1-A2)"],
                        ["Family and Relationships","Lingala", "Beginner (A1-A2)"],
                    ],
                    inputs=[voc_topic, voc_lang, voc_level],
                )

                voc_btn.click(
                    fn=vocabulary_builder,
                    inputs=[voc_topic, voc_lang, voc_level, voc_num],
                    outputs=[voc_output, voc_time],
                )

            # ══════════════════════════════════════════════════════════════
            # TAB 5 — Conversation Practice  (STATEFUL)
            # ══════════════════════════════════════════════════════════════
            with gr.TabItem("Conversation Practice", id=5):
                gr.Markdown("""
### Practice Real Conversations
Choose a scenario and chat with the AI in your target language.
You will receive corrections and language tips after every message.
                """)

                with gr.Row():
                    c_lang     = gr.Dropdown(LANGUAGES, value="French",
                                             label="Practice Language")
                    c_level    = gr.Dropdown(PROFICIENCY_LEVELS,
                                             value="Beginner (A1-A2)",
                                             label="Level")
                    c_scenario = gr.Dropdown(
                        CONVERSATION_SCENARIOS,
                        value="At a restaurant ordering food",
                        label="Conversation Scenario",
                    )

                # Hidden state — stores the growing conversation string.
                # Never shown in the UI; reset by the "New Conversation" button.
                c_history = gr.State(value="")

                c_input = gr.Textbox(
                    label="Your Message",
                    placeholder="Type in your target language… (e.g. 'Bonjour, je voudrais…')",
                    lines=2,
                )

                with gr.Row():
                    c_btn   = gr.Button("Send Message", variant="primary")
                    c_reset = gr.Button("New Conversation", variant="secondary")

                c_output = gr.Markdown(label="AI Response & Language Notes")
                c_time   = gr.Textbox(label="Performance", interactive=False)

                c_btn.click(
                    fn=conversation_practice,
                    inputs=[c_input, c_scenario, c_lang, c_level, c_history],
                    outputs=[c_output, c_history, c_time],
                )

                c_reset.click(
                    fn=lambda: ("", "", ""),
                    outputs=[c_output, c_history, c_time],
                )

        # ── Footer ─────────────────────────────────────────────────────────────
        gr.Markdown("""
---
### About Mwalimu-LangLearn

**Mwalimu-LangLearn** is an AI-powered language learning platform built as part of a
Master's thesis at the **Kobe Institute of Computing, Japan** (ABE Initiative / JICA).

**Thesis**: *"AI in Education for Sustainable Development in the Democratic Republic of Congo"*

**Author**: Pascal Burume Buhendwa

- Core model: Google Gemma 3n E2B-IT (via Ollama)
- Interface: Gradio 4.x
- 14 languages including Swahili, Lingala, and French

*Part of the Mwalimu-STEM-GenAI research initiative for AI-powered education in the DRC.*
        """)

    return demo