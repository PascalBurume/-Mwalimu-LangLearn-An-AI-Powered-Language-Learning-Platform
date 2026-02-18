# 🌍 Mwalimu-LangLearn: An AI-Powered Language Learning Platform

> **"Mwalimu"** means *Teacher* in Swahili — a name that reflects both the cultural roots and the educational mission of this project.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Gemma 3n](https://img.shields.io/badge/Model-Google%20Gemma%203n-orange.svg)](https://ai.google.dev)
[![Gradio](https://img.shields.io/badge/Interface-Gradio-yellow.svg)](https://gradio.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Research](https://img.shields.io/badge/Context-Master's%20Thesis%20Research-purple.svg)]()

---

## 📌 Overview

**Mwalimu-LangLearn** is a research-driven, AI-powered language learning platform developed as part of ongoing graduate research at the **Kobe Institute of Computing, Japan**. The platform provides adaptive, multimodal language instruction — including writing feedback, visual vocabulary recognition, translation evaluation, and conversational simulation — powered by **Google Gemma 3n**, a compact multimodal language model.

This project sits at the intersection of two research questions:

1. Can small, locally-running AI models deliver educationally meaningful feedback comparable to expert human tutors?
2. How can such systems be designed to serve learners in low-resource environments, particularly in Sub-Saharan Africa?

Mwalimu-LangLearn serves as a working prototype and proof-of-concept within the broader **Mwalimu-STEM-GenAI** research initiative, which targets offline-capable AI tutoring for underserved schools in the **Democratic Republic of Congo (DRC)**.

---

## 🎯 Research Motivation & Problem Statement

Access to quality, personalized language education remains deeply unequal globally. Learners in high-income countries benefit from responsive digital tools, AI tutors, and instant feedback systems. In contrast, learners across much of Sub-Saharan Africa — including the DRC, one of the world's most linguistically diverse nations — face compounding barriers:

- **Connectivity gaps:** Reliable internet access is unavailable in large portions of the country, making cloud-dependent tools inaccessible.
- **Language complexity:** The DRC alone has over 200 local languages. French serves as the official language of education, yet many learners speak Swahili, Lingala, or other regional languages at home — creating significant linguistic discontinuity in formal schooling.
- **Resource constraints:** Schools in rural and peri-urban areas often lack qualified language teachers, textbooks, and digital devices.

This project investigates whether **lightweight, multimodal Small Language Models (SLMs)**, running locally on modest hardware, can bridge part of this gap — providing immediate, personalized, and language-sensitive feedback without dependency on cloud infrastructure.

---

## 🔬 Research Context

This work is conducted under the **ABE Initiative (African Business Education for Youth for Africa)** scholarship program, funded by the **Japan International Cooperation Agency (JICA)**, at the **Kobe Institute of Computing, Graduate School of Information Systems**.

**Thesis Title:**
> *"AI in Education for Sustainable Development in the Democratic Republic of Congo"*

Mwalimu-LangLearn contributes to the thesis by:
- Demonstrating the feasibility of SLM-based educational tools in resource-constrained settings
- Examining how AI can support sustainable educational outcomes in the DRC, where teacher shortages, multilingualism, and infrastructure gaps remain critical challenges
- Providing a replicable architecture for multimodal AI tutoring applications deployable in low-connectivity environments
- Informing the design of the forthcoming **Mwalimu-STEM-GenAI** system, which will extend this approach to mathematics and science education with full offline capability

The broader research program is motivated by field experience from two UNDP consultancy assignments in the DRC, where the absence of data-driven educational and monitoring infrastructure was a consistent limiting factor in development program effectiveness.

---

## 🧠 AI & Technical Architecture

### Model: Google Gemma 3n (E2B-IT)

Gemma 3n is a compact, instruction-tuned multimodal model designed for efficient inference on consumer hardware. Its characteristics that make it suitable for this research context include:

- **Low memory footprint** relative to performance, enabling deployment on non-datacenter hardware
- **Multimodal capability** through a MobileNet-V5 vision encoder that processes images at up to 768×768 resolution into 256 tokens
- **Instruction-following quality** sufficient for structured educational feedback tasks
- **Multilingual capacity** spanning the languages relevant to the DRC educational context

### System Architecture

The application follows a strict three-layer separation of concerns:

```
┌─────────────────────────────────────────────────┐
│              PRESENTATION LAYER                 │
│         Gradio Web Interface (Step 7)           │
│   Tabs · Dropdowns · Input/Output Components    │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│              APPLICATION LAYER                  │
│         Feature Functions (Step 5)              │
│  Writing · Visual · Translation · Vocabulary    │
│  Conversation · Prompt Engineering Logic        │
└───────────────────────┬─────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────┐
│              INFERENCE LAYER                    │
│         Core Inference Engine (Step 4)          │
│   query_model() · query_model_with_image()      │
│   HuggingFace Transformers · PyTorch Backend    │
└─────────────────────────────────────────────────┘
```

This architecture is intentional: the inference layer can be replaced with a different SLM — for example, a quantized model optimized for a low-spec Android device — without modifying any feature or interface logic. This modularity is a core design requirement for the planned edge deployment scenario in DRC schools.

### Technology Stack

| Component | Technology | Research Rationale |
|---|---|---|
| Core Model | Google Gemma 3n (E2B-IT) | Multimodal capability with low resource footprint |
| Vision Encoder | MobileNet-V5 | Efficient image understanding at 256 tokens |
| ML Framework | PyTorch + HuggingFace Transformers | Industry-standard, extensive community support |
| Interface | Gradio 4.x | Rapid prototyping without frontend development overhead |
| Runtime | Python 3.10+ | Cross-platform compatibility |

---

## ✨ Platform Features

### 1. 📝 Adaptive Writing Feedback
Learners submit written paragraphs in their target language and receive structured feedback calibrated to their proficiency level (A1–C2). Feedback includes grammar corrections with explanations, vocabulary alternatives, stylistic suggestions, and a score. The system adjusts depth and complexity of feedback based on the declared proficiency level.

### 2. 🖼️ Multimodal Visual Vocabulary Learning
Learners upload any image — a photograph of their classroom, home, or local environment — and the model identifies visible objects, provides translations with pronunciation guides, generates contextual example sentences, and offers cultural notes where relevant. This feature is particularly designed to connect vocabulary learning to the learner's immediate physical context.

### 3. 🔄 Translation Evaluation
Learners attempt their own translation of a given sentence, which the model then evaluates against an ideal reference. Feedback includes an accuracy score, specific error analysis, praise for correct elements, grammar rule explanations, and alternative valid translations.

### 4. 📚 Thematic Vocabulary Generation
Learners specify a topic and the system generates a complete structured vocabulary lesson including key terms with pronunciation, example sentences, common phrases, a fill-in-the-blank quiz, and mnemonic memory aids.

### 5. 💬 Scenario-Based Conversational Simulation
Learners practice dialogue across eight real-world scenarios (restaurant, directions, job interview, shopping, and more). The model responds naturally in the target language while providing inline correction notes after each learner turn. Conversation history is maintained across the full session to simulate authentic dialogue continuity.

---

## 🌍 Supported Languages

The platform currently supports 14 languages, with deliberate inclusion of African languages central to the DRC educational context:

**African & DRC-Relevant Languages:** Swahili · Lingala · French (official DRC language of instruction) · Arabic

**Global Languages:** English · Spanish · Portuguese · Chinese (Mandarin) · German · Japanese · Korean · Hindi · Italian · Russian

---

## 🚀 Installation & Usage

### Requirements
```bash
pip install torch transformers gradio Pillow
```

### Running Locally
```bash
git clone https://github.com/YOUR_USERNAME/mwalimu-langlearn.git
cd mwalimu-langlearn
python app.py
```

The interface launches at `http://127.0.0.1:7860`. A CUDA-compatible GPU is recommended for practical inference speed; CPU inference is functional but significantly slower.

---

## 🔭 Future Work: Mwalimu-STEM-GenAI

The findings and architecture from Mwalimu-LangLearn directly inform the next phase of research — **Mwalimu-STEM-GenAI** — which will focus on:

- Adapting SLMs for STEM tutoring (mathematics, physics, biology) at the secondary school level in the DRC
- Implementing full **offline capability** via model quantization and edge deployment on low-cost hardware
- Integrating geospatial and contextual data to personalize content for DRC learners
- Piloting the system in partnership with schools in Bukavu and Kinshasa

---

## 👤 Author

**Pascal Burume Buhendwa**

Master's Student in Information Systems — Kobe Institute of Computing, Japan (ABE Initiative / JICA)
Microsoft MVP — Business Applications | Founder, Next-gen Cloud Solution
Originally from Bukavu, Democratic Republic of Congo

Former UNDP consultant with field experience developing data-driven monitoring and evaluation systems for development programs in the DRC. Research interests: AI for education, geospatial data systems, disaster recovery infrastructure, and sustainable development technology.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Developed at the Kobe Institute of Computing, Japan · Part of the Mwalimu-STEM-GenAI research initiative · Bridging Japanese AI innovation with African educational development.*
