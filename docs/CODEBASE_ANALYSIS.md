# Mwalimu-LangLearn: Comprehensive Codebase Analysis

> A multi-perspective deep-dive covering product strategy, system architecture, and implementation details.

---

## Table of Contents

1. [Project Identity & Purpose](#1-project-identity--purpose)
2. [Product Manager Perspective](#2-product-manager-perspective)
3. [Software Architect Perspective](#3-software-architect-perspective)
4. [Software Developer Perspective](#4-software-developer-perspective)
5. [AI/ML Engineering Deep-Dive](#5-aiml-engineering-deep-dive)
6. [Data Flows & State Management](#6-data-flows--state-management)
7. [User Experience & Interface Design](#7-user-experience--interface-design)
8. [Gaps, Risks & Recommendations](#8-gaps-risks--recommendations)

---

## 1. Project Identity & Purpose

**Mwalimu-LangLearn** is an AI-powered, multimodal language learning platform developed as part of a Master's thesis at the **Kobe Institute of Computing, Japan**. "Mwalimu" means *Teacher* in Swahili — a name that anchors the project to its core mission: delivering high-quality, personalized language education in resource-constrained environments.

| Attribute | Detail |
|---|---|
| Author | Pascal Burume Buhendwa |
| Institution | Kobe Institute of Computing (ABE Initiative / JICA) |
| Thesis | *"AI in Education for Sustainable Development in the Democratic Republic of Congo"* |
| License | MIT |
| Primary Target | Learners in Sub-Saharan Africa (DRC) |
| Core Model | Google Gemma 3n E2B-IT |
| Interface | Gradio 4.x Web Application |
| Repository Type | Jupyter Notebook (research prototype) |

### Research Questions

1. Can small, locally-running AI models deliver educationally meaningful feedback comparable to expert human tutors?
2. How can such systems serve learners in low-resource, low-connectivity environments?

---

## 2. Product Manager Perspective

### 2.1 Problem Space

```mermaid
mindmap
  root((Education Gap in DRC))
    Connectivity
      No reliable internet in rural areas
      Cloud tools inaccessible
    Language Complexity
      200+ local languages
      French as official school language
      Home languages: Swahili, Lingala, others
    Resources
      Teacher shortages
      No textbooks
      Few digital devices
    AI Access
      Expensive cloud APIs
      English-centric tools
      No offline capability
```

The Democratic Republic of Congo faces compounding educational barriers. Students switch between home languages (Swahili, Lingala) and the official school language (French), while schools lack qualified language teachers, textbooks, and digital infrastructure. Cloud-based AI tools cannot reach these learners due to connectivity gaps.

### 2.2 Value Proposition

```mermaid
graph LR
    A[Student] -->|uploads image / types text| B[Mwalimu-LangLearn]
    B -->|runs locally on modest GPU| C[Google Gemma 3n]
    C -->|structured feedback| D[Personalized Learning]
    D -->|no internet required| A

    style B fill:#4CAF50,color:#fff
    style C fill:#FF9800,color:#fff
    style D fill:#2196F3,color:#fff
```

**Core Value**: Immediate, personalized, multilingual language feedback — without cloud dependency, without subscription costs, without qualified teacher availability.

### 2.3 Feature Map

```mermaid
graph TD
    Platform[Mwalimu-LangLearn Platform]

    Platform --> F1[📝 Writing Feedback]
    Platform --> F2[🖼️ Visual Learning]
    Platform --> F3[🔄 Translation Practice]
    Platform --> F4[📚 Vocabulary Builder]
    Platform --> F5[💬 Conversation Practice]

    F1 --> F1a[Grammar correction]
    F1 --> F1b[Vocabulary alternatives]
    F1 --> F1c[Style tips]
    F1 --> F1d[Score A1-C2]

    F2 --> F2a[Object identification from photo]
    F2 --> F2b[Translations + pronunciation]
    F2 --> F2c[Example sentences]
    F2 --> F2d[Cultural notes]

    F3 --> F3a[Student translation evaluation]
    F3 --> F3b[Accuracy score 1-10]
    F3 --> F3c[Error analysis]
    F3 --> F3d[Alternative translations]

    F4 --> F4a[Themed vocabulary lesson]
    F4 --> F4b[Fill-in-blank quiz]
    F4 --> F4c[Memory mnemonics]
    F4 --> F4d[5 to 20 words]

    F5 --> F5a[8 real-world scenarios]
    F5 --> F5b[Inline correction notes]
    F5 --> F5c[Stateful session history]
    F5 --> F5d[Natural dialogue]
```

### 2.4 Supported Languages

The platform deliberately includes African languages under-represented in commercial tools:

| Region | Languages |
|---|---|
| African / DRC-Relevant | Swahili, Lingala, French, Arabic |
| European | English, Spanish, Portuguese, German, Italian, Russian |
| Asian | Japanese, Chinese (Mandarin), Korean, Hindi |

**Total: 14 languages** — backed by Gemma 3n's 140+ language training corpus.

### 2.5 User Journeys

```mermaid
journey
    title Student Learning Journey — Writing Feedback
    section Input
      Select target language: 5: Student
      Choose proficiency level: 5: Student
      Type paragraph in French: 4: Student
    section Processing
      Model analyzes text: 3: System
      Generates structured feedback: 3: System
    section Output
      Reads grammar corrections: 5: Student
      Reviews vocabulary tips: 4: Student
      Notes score and improves: 5: Student
```

```mermaid
journey
    title Visual Vocabulary Journey
    section Input
      Photograph classroom objects: 5: Student
      Upload image to platform: 4: Student
      Select Swahili as target: 5: Student
    section Processing
      MobileNet-V5 encodes image: 3: System
      Gemma 3n identifies objects: 3: System
      Generates translations + sentences: 3: System
    section Output
      Learns object names in Swahili: 5: Student
      Reads pronunciation guides: 4: Student
      Reviews cultural notes: 4: Student
```

### 2.6 Roadmap & Future Work

```mermaid
timeline
    title Mwalimu Research Roadmap
    2024 : Mwalimu-LangLearn prototype
         : Gemma 3n integration
         : 5 learning modules
         : 14 languages
    2025 : Mwalimu-STEM-GenAI
         : STEM tutoring (Math, Physics, Biology)
         : Full offline capability via quantization
         : Edge deployment on low-cost hardware
    2026 : DRC School Pilots
         : Bukavu and Kinshasa schools
         : Geospatial personalization
         : Teacher support tools
```

---

## 3. Software Architect Perspective

### 3.1 System Architecture Overview

```mermaid
graph TB
    subgraph Presentation["PRESENTATION LAYER — Gradio Web Interface"]
        Tab1[📝 Writing Feedback Tab]
        Tab2[🖼️ Visual Learning Tab]
        Tab3[🔄 Translation Tab]
        Tab4[📚 Vocabulary Tab]
        Tab5[💬 Conversation Tab]
        State[gr.State — Conversation History]
    end

    subgraph Application["APPLICATION LAYER — Feature Functions"]
        WF[writing_feedback]
        VL[visual_learning]
        TP[translation_practice]
        VB[vocabulary_builder]
        CP[conversation_practice]
    end

    subgraph Inference["INFERENCE LAYER — Core Engine"]
        QM[query_model — text only]
        QMI[query_model_with_image — multimodal]
    end

    subgraph Model["MODEL LAYER — Google Gemma 3n E2B-IT"]
        Proc[AutoProcessor]
        LLM[AutoModelForImageTextToText]
        VEnc[MobileNet-V5 Vision Encoder]
        TEnc[Text Tokenizer]
    end

    Tab1 --> WF
    Tab2 --> VL
    Tab3 --> TP
    Tab4 --> VB
    Tab5 --> CP
    State <--> CP

    WF --> QM
    VL --> QMI
    TP --> QM
    VB --> QM
    CP --> QM

    QM --> Proc
    QMI --> Proc
    QMI --> VEnc
    Proc --> LLM
    VEnc --> LLM
    TEnc --> LLM
```

**Key architectural principle**: The inference layer (`query_model`, `query_model_with_image`) is deliberately decoupled from feature logic. This allows swapping the underlying model (e.g., a quantized GGUF model for Android) without touching any feature or UI code.

### 3.2 Deployment Architecture

```mermaid
graph LR
    subgraph Current["Current Deployment"]
        KN[Kaggle Notebook GPU T4 15GB]
        KH[kagglehub Model Registry]
        GShare[Gradio share=True Public URL]
        KN --> KH
        KN --> GShare
    end

    subgraph Planned["Planned Edge Deployment"]
        Android[Low-cost Android Tablet]
        GGUF[Quantized GGUF Model]
        Offline[Offline Inference]
        Android --> GGUF
        GGUF --> Offline
    end

    subgraph Target["Target Environment DRC Schools"]
        School[Rural School in DRC]
        Teacher[Teacher / Student]
        School --> Teacher
    end

    Current -->|"research → production"| Planned
    Planned --> Target
```

### 3.3 Model Loading Strategy

```mermaid
flowchart TD
    Start[Application Start] --> CheckEnv{Environment?}
    CheckEnv -->|Kaggle Notebook| KaggleLoad[kagglehub.model_download]
    CheckEnv -->|Local / Cloud| HFLoad[HuggingFace Hub]
    KaggleLoad --> LoadProc[AutoProcessor.from_pretrained]
    HFLoad --> LoadProc
    LoadProc --> LoadModel[AutoModelForImageTextToText.from_pretrained]
    LoadModel --> Config["torch_dtype=auto\ndevice_map=auto"]
    Config --> Ready[Model Ready for Inference]
    Ready --> GPU{CUDA Available?}
    GPU -->|Yes| VRAM[bfloat16 on GPU T4/A100]
    GPU -->|No| CPU[float32 on CPU slower]
```

### 3.4 Component Dependencies

```mermaid
graph LR
    subgraph Core
        torch[PyTorch]
        transformers[HuggingFace Transformers ≥4.53.0]
        accelerate[accelerate]
    end

    subgraph Vision
        timm[timm — MobileNet-V5]
        pillow[Pillow / PIL]
    end

    subgraph Interface
        gradio[Gradio 4.x]
    end

    subgraph Distribution
        kagglehub[kagglehub]
    end

    transformers --> torch
    transformers --> accelerate
    timm --> torch
    gradio --> pillow
    kagglehub --> transformers
```

### 3.5 Stateful vs. Stateless Features

```mermaid
graph LR
    subgraph Stateless["Stateless Features — Each call is independent"]
        S1[Writing Feedback]
        S2[Visual Learning]
        S3[Translation Practice]
        S4[Vocabulary Builder]
    end

    subgraph Stateful["Stateful Feature — Session persists"]
        ST1[Conversation Practice]
        ST2[gr.State chat_history]
        ST1 <-->|read/write| ST2
    end

    note1[No database — history lives in browser memory]

    Stateless -.->|reset on each call| note1
    Stateful -.->|accumulates within session| note1
```

---

## 4. Software Developer Perspective

### 4.1 Repository Structure

```
/Mwalimu-LangLearn/
├── README.md                              # Project documentation (183 lines)
├── Gemma3n_language_learning_Tool.ipynb   # Complete implementation (21 cells, ~2000 lines)
└── .git/                                  # Version control
```

This is a **notebook-first research project**. The entire application — model loading, inference engine, feature functions, and Gradio UI — lives in a single Jupyter notebook organized into 8 sequential steps.

### 4.2 Notebook Cell Organization

```mermaid
graph TD
    C0[Cell 0 — Markdown: Overview and architecture diagram]
    C1[Cell 1 — Markdown: Step-by-step guide]
    C2[Cell 2 — pip install dependencies]
    C3[Cell 3 — Markdown: Step 2 imports]
    C4[Cell 4 — Library imports]
    C5[Cell 5 — Markdown: Step 3 credentials]
    C6[Cell 6 — Kaggle credentials + model download via kagglehub]
    C7[Cell 7 — Repeat imports safety]
    C8[Cell 8 — Markdown: Step 4 inference engine]
    C9[Cell 9 — query_model + query_model_with_image functions]
    C10[Cell 10 — Markdown: Step 5 feature functions]
    C11[Cell 11 — 5 feature functions with prompt engineering]
    C12[Cell 12 — Markdown: Step 6 testing]
    C13[Cell 13 — Test: writing_feedback + vocabulary_builder]
    C14[Cell 14 — Test: translation_practice]
    C15[Cell 15 — Test: visual_learning with image]
    C16[Cell 16 — Markdown: Step 7 Gradio UI]
    C17[Cell 17 — Full Gradio Blocks interface]
    C18[Cell 18 — Markdown: Step 8 launch]
    C19[Cell 19 — demo.launch]

    C0 --> C2 --> C4 --> C6 --> C9 --> C11 --> C13 --> C17 --> C19
```

### 4.3 Core Inference Functions

```mermaid
classDiagram
    class InferenceEngine {
        +model: AutoModelForImageTextToText
        +processor: AutoProcessor
        +query_model(prompt, system_prompt, max_new_tokens) tuple
        +query_model_with_image(image, prompt, system_prompt, max_new_tokens) tuple
    }

    class query_model {
        -messages: list[dict]
        -input_text: str via apply_chat_template
        -inputs: BatchEncoding on model.device
        -outputs: tensor
        +returns: response str, execution_time float
    }

    class query_model_with_image {
        -messages: list with image dict + text dict
        -inputs: BatchEncoding with pixel values
        -VisionEncoder: MobileNet-V5 → 256 tokens
        +returns: response str, execution_time float
    }

    InferenceEngine --> query_model
    InferenceEngine --> query_model_with_image
```

**Text-Only Inference — `query_model()`**

```python
def query_model(prompt, system_prompt=None, max_new_tokens=512):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    input_text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = processor(text=input_text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )

    response = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    # Extracts only the model's response portion
    return response, execution_time
```

**Multimodal Inference — `query_model_with_image()`**

```python
def query_model_with_image(image, prompt, system_prompt=None, max_new_tokens=512):
    messages = [
        {"role": "user", "content": [
            {"type": "image", "image": pil_image},   # → MobileNet-V5 → 256 tokens
            {"type": "text",  "text": full_prompt}
        ]}
    ]
    inputs = processor(
        text=input_text,
        images=pil_image,
        return_tensors="pt"
    ).to(model.device)
    # Generation identical to text-only path
```

### 4.4 Feature Functions — Prompt Engineering Pattern

Each of the 5 feature functions follows the same structure:

```mermaid
flowchart LR
    A[User Inputs] --> B[Build System Prompt\nwith role + instructions]
    B --> C[Build User Prompt\nwith actual content]
    C --> D{Needs Image?}
    D -->|Yes| E[query_model_with_image]
    D -->|No| F[query_model]
    E --> G[Parse Markdown Response]
    F --> G
    G --> H[Return response + exec time]
```

**System Prompt Pattern — Writing Feedback**

```python
system_prompt = f"""You are an expert {target_language} language tutor working with a {proficiency_level} student.
Provide detailed, encouraging, and educational feedback on their writing.

Format your response as:
1. **Overall Assessment**
2. **Grammar Corrections** (with explanations)
3. **Vocabulary Suggestions**
4. **Style & Flow Tips**
5. **Encouragement & Score** (out of 10)"""
```

All 5 features use this "role + numbered output format" pattern in their system prompts, enabling consistent structured output without post-processing or parsing code.

### 4.5 Generation Parameters

| Parameter | Value | Rationale |
|---|---|---|
| `temperature` | `0.7` | Balance creativity and coherence — avoids both repetition and hallucination |
| `top_p` | `0.9` | Nucleus sampling — maintains diversity while filtering low-probability tokens |
| `do_sample` | `True` | Sampling mode (vs. greedy decoding) for more natural language |
| `max_new_tokens` | `512–1500` | Varies per feature: vocabulary builder uses 1500, writing feedback 1024 |

### 4.6 Conversation State Management

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Gradio Tab 5
    participant S as gr.State (chat_history)
    participant F as conversation_practice()
    participant M as Gemma 3n

    U->>UI: Types message + selects scenario
    UI->>F: (message, scenario, lang, level, history)
    F->>F: Build system prompt with scenario
    F->>F: Append user message to history
    F->>M: query_model(history as messages)
    M-->>F: response text
    F->>F: Append model response to history
    F-->>UI: (response, updated_history, exec_time)
    UI->>S: Store updated_history
    U->>UI: Next message
    UI->>F: (new_message, scenario, lang, level, stored_history)
    Note over S,F: History grows across turns
```

History is stored as a Python list of `{"role": ..., "content": ...}` dicts in `gr.State()` — a Gradio hidden component that persists within a browser session. It is not persisted to disk or database.

### 4.7 Gradio UI Component Hierarchy

```mermaid
graph TD
    Demo[gr.Blocks theme=soft]
    Demo --> CSS[Custom CSS linear-gradient styling]
    Demo --> Header[gr.Markdown — title + description]
    Demo --> Tabs[gr.Tabs]

    Tabs --> T1[Tab: Writing Feedback]
    Tabs --> T2[Tab: Visual Learning]
    Tabs --> T3[Tab: Translation Practice]
    Tabs --> T4[Tab: Vocabulary Builder]
    Tabs --> T5[Tab: Conversation Practice]

    T1 --> T1R1[gr.Row]
    T1R1 --> T1C1[gr.Column — inputs]
    T1R1 --> T1C2[gr.Column — output]
    T1C1 --> T1TXT[gr.Textbox writing_input]
    T1C1 --> T1DD1[gr.Dropdown target_language]
    T1C1 --> T1DD2[gr.Dropdown proficiency_level]
    T1C1 --> T1BTN[gr.Button Analyze Writing]
    T1C2 --> T1MD[gr.Markdown feedback_output]
    T1C2 --> T1TIME[gr.Textbox exec_time]
    T1 --> T1EX[gr.Examples pre-populated]

    T2 --> T2IMG[gr.Image upload PIL format]
    T2 --> T2DD[gr.Dropdown language]
    T2 --> T2BTN[gr.Button Analyze Image]
    T2 --> T2OUT[gr.Markdown output]

    T5 --> T5STATE[gr.State chat_history hidden]
    T5 --> T5IN[gr.Textbox user_message]
    T5 --> T5DD1[gr.Dropdown scenario]
    T5 --> T5BTN[gr.Button Send Message]
    T5 --> T5OUT[gr.Markdown response]
    T5 --> T5CLR[gr.Button Clear Conversation]
```

### 4.8 Dependency Installation (Cell 2)

```bash
pip install transformers>=4.53.0 \
            torch \
            gradio \
            Pillow \
            kagglehub \
            accelerate \
            timm
```

No `requirements.txt`, `pyproject.toml`, or `setup.py` exists. Dependencies are installed via the first notebook cell — standard practice for Kaggle notebooks.

### 4.9 Environment & Credentials

```python
# Kaggle API credentials (set as environment variables — never hardcoded)
os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
os.environ['KAGGLE_KEY']      = 'your_kaggle_api_key'

# Model download
model_path = kagglehub.model_download("google/gemma-3n/transformers/gemma-3n-e2b-it")
```

On local/non-Kaggle environments, the model is loaded directly from HuggingFace Hub using the same `from_pretrained()` API.

---

## 5. AI/ML Engineering Deep-Dive

### 5.1 Gemma 3n Architecture

```mermaid
graph TB
    subgraph Input
        TXT[Text Input]
        IMG[Image Input up to 768×768]
    end

    subgraph Processing
        Tok[Tokenizer — text tokens]
        VEnc[MobileNet-V5 Vision Encoder → 256 image tokens]
        Concat[Token Concatenation]
    end

    subgraph Gemma3n["Gemma 3n Transformer E2B-IT"]
        Att[Multi-head Self-Attention]
        FFN[Feed-Forward Network]
        Layers[~26 Transformer Layers]
    end

    subgraph Output
        LogitGen[Logit Generation]
        Sampling[Nucleus Sampling top_p=0.9 temp=0.7]
        Response[Structured Text Response]
    end

    TXT --> Tok
    IMG --> VEnc
    Tok --> Concat
    VEnc --> Concat
    Concat --> Att
    Att --> FFN
    FFN --> Layers
    Layers --> LogitGen
    LogitGen --> Sampling
    Sampling --> Response
```

### 5.2 Chat Template Structure

Gemma 3n uses HuggingFace's standard chat template with model-specific special tokens:

```
<start_of_turn>system
You are an expert French language tutor...
<end_of_turn>
<start_of_turn>user
Je suis allé au magazin...
<end_of_turn>
<start_of_turn>model
[GENERATED RESPONSE]
```

The `apply_chat_template()` call handles this formatting automatically from the structured `messages` list.

### 5.3 Inference Pipeline

```mermaid
flowchart TD
    Start[Feature Function called]
    BuildMsg[Build messages list\nrole + content dicts]
    ApplyTemplate[processor.apply_chat_template\ntokenize=False]
    Tokenize[processor text=input_text\nreturn_tensors=pt]
    ToDevice[.to model.device\nGPU or CPU]
    Generate[model.generate\nmax_new_tokens, temp, top_p, do_sample]
    Decode[processor.batch_decode\nskip_special_tokens=True]
    Extract[Split on last user message\nextract model response only]
    Return[Return response + execution_time]

    Start --> BuildMsg --> ApplyTemplate --> Tokenize --> ToDevice --> Generate --> Decode --> Extract --> Return
```

### 5.4 Model Variants

| Variant | Effective Params | Total Params | VRAM Req. | Use Case |
|---|---|---|---|---|
| Gemma 3n E2B-IT | ~2B effective | ~6B total | ~8GB | Used in this project — Kaggle T4 GPU |
| Gemma 3n E4B-IT | ~4B effective | ~12B total | ~15GB | Higher quality, still fits T4 |
| Quantized GGUF | ~1-2B effective | varies | ~4GB | Planned for Android edge deployment |

The E2B variant uses **parameter sharing** across transformer layers, achieving effective 2B parameter inference with a full 6B parameter model — the key to its efficient memory footprint.

### 5.5 Prompt Engineering Strategy

```mermaid
graph LR
    subgraph SystemPrompt["System Prompt Components"]
        Role[Role Definition\ne.g. expert tutor]
        Level[Proficiency Context\nA1-C2]
        Format[Output Format\nnumbered sections]
        Style[Tone Instruction\nencouraging, educational]
    end

    subgraph UserPrompt["User Prompt Components"]
        Content[User's actual content\ntext or image]
        Task[Specific task instruction]
        Lang[Language specification]
    end

    SystemPrompt --> Model[Gemma 3n]
    UserPrompt --> Model
    Model --> StructuredOutput[Structured Markdown Response]
```

No output parsers, JSON schemas, or regex post-processing are used. All structure is achieved through prompt engineering alone — the model reliably produces numbered sections with bold headers due to the instruction-tuned training.

---

## 6. Data Flows & State Management

### 6.1 Writing Feedback Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Gradio UI
    participant WF as writing_feedback()
    participant QM as query_model()
    participant G as Gemma 3n

    U->>UI: text + language + proficiency
    UI->>WF: writing_feedback(text, lang, level)
    WF->>WF: Build system_prompt with role + level
    WF->>WF: Build user_prompt with text
    WF->>QM: query_model(user_prompt, system_prompt, max_new_tokens=1024)
    QM->>QM: apply_chat_template(messages)
    QM->>G: model.generate(inputs, max_new_tokens=1024)
    G-->>QM: token sequence
    QM->>QM: batch_decode → extract response
    QM-->>WF: (response_str, exec_time)
    WF-->>UI: (markdown_feedback, time_string)
    UI->>U: Rendered markdown + execution time
```

### 6.2 Visual Learning Data Flow

```mermaid
sequenceDiagram
    participant U as User
    participant UI as Gradio UI
    participant VL as visual_learning()
    participant QMI as query_model_with_image()
    participant VE as MobileNet-V5
    participant G as Gemma 3n

    U->>UI: image file + target language + source language
    UI->>VL: visual_learning(image, target_lang, source_lang)
    VL->>VL: Build system_prompt for visual vocabulary
    VL->>VL: Build user_prompt requesting object list + translations
    VL->>QMI: query_model_with_image(image, prompt, system_prompt)
    QMI->>QMI: Construct multimodal messages dict
    QMI->>VE: Encode image → 256 tokens
    VE-->>QMI: pixel_values tensor
    QMI->>G: model.generate(text_tokens + image_tokens)
    G-->>QMI: token sequence
    QMI->>QMI: decode → extract response
    QMI-->>VL: (response_str, exec_time)
    VL-->>UI: (vocabulary_markdown, time_string)
    UI->>U: Objects + translations + cultural notes
```

### 6.3 Conversation Practice State Machine

```mermaid
stateDiagram-v2
    [*] --> Empty: Session Start
    Empty --> FirstTurn: User sends first message
    FirstTurn --> OngoingConversation: Model responds
    OngoingConversation --> OngoingConversation: User sends follow-up
    OngoingConversation --> Empty: User clicks Clear
    Empty --> [*]: Tab closed / session ends

    note right of OngoingConversation
        chat_history: [
          {role: system, content: scenario_prompt},
          {role: user, content: msg1},
          {role: assistant, content: resp1},
          {role: user, content: msg2},
          ...
        ]
    end note
```

### 6.4 Session Data Model

```mermaid
erDiagram
    SESSION {
        list chat_history
    }

    CHAT_MESSAGE {
        string role
        string content
    }

    INFERENCE_CALL {
        string prompt
        string system_prompt
        int max_new_tokens
        float temperature
        float top_p
        bool do_sample
    }

    INFERENCE_RESULT {
        string response
        float execution_time_seconds
    }

    SESSION ||--o{ CHAT_MESSAGE : contains
    INFERENCE_CALL ||--|| INFERENCE_RESULT : produces
```

No persistent storage. All data lives in memory for the duration of the Gradio session. Image data is processed as `PIL.Image` objects — never saved to disk.

---

## 7. User Experience & Interface Design

### 7.1 UI Layout

```mermaid
graph TD
    App[Gradio App max-width: 1200px]
    App --> Header[Header with gradient background]
    Header --> Title[🌍 Mwalimu-LangLearn title]
    Header --> Desc[Feature summary list]
    App --> Tabs[Tabbed Navigation]

    Tabs --> T1[Tab 1: 📝 Writing]
    Tabs --> T2[Tab 2: 🖼️ Visual]
    Tabs --> T3[Tab 3: 🔄 Translation]
    Tabs --> T4[Tab 4: 📚 Vocabulary]
    Tabs --> T5[Tab 5: 💬 Conversation]

    T1 --> T1Layout[Two-column layout]
    T1Layout --> T1Left[Left: inputs textarea + dropdowns + button]
    T1Layout --> T1Right[Right: markdown output + time display]
    T1 --> T1Examples[Examples: French paragraph with errors]

    T2 --> T2Layout[Two-column layout]
    T2Layout --> T2Left[Left: image upload + language dropdowns + button]
    T2Layout --> T2Right[Right: vocabulary markdown output]
    T2 --> T2Examples[Examples: classroom photo scenarios]

    T4 --> T4Special[Slider for word count 5-20]
    T5 --> T5Special[Scenario dropdown 8 options + Clear button]
```

### 7.2 Conversation Scenarios

The 8 built-in scenarios for Tab 5:

```
1. General Conversation
2. At a Restaurant
3. Asking for Directions
4. Shopping
5. Job Interview
6. Meeting New People
7. Travel & Tourism
8. Healthcare & Medical
```

### 7.3 Proficiency Levels (CEFR)

| Level Code | Label Used in UI |
|---|---|
| A1-A2 | Beginner (A1-A2) |
| B1-B2 | Intermediate (B1-B2) |
| C1-C2 | Advanced (C1-C2) |

The proficiency level is injected into the system prompt, causing the model to calibrate feedback depth, vocabulary complexity, and explanation detail accordingly.

### 7.4 Application Launch Configuration

```python
demo.launch(
    share=True,            # Generates public tunneled URL via Gradio servers
    server_name="0.0.0.0", # Listens on all network interfaces
    server_port=7860,       # Standard Gradio port
    show_error=True         # Surfaces Python exceptions in the UI for debugging
)
```

---

## 8. Gaps, Risks & Recommendations

### 8.1 Current Gaps

```mermaid
mindmap
  root((Current Gaps))
    Infrastructure
      No requirements.txt
      No Dockerfile
      No CI/CD pipeline
      No automated tests
    Security
      Credentials in notebook cells
      No authentication on Gradio interface
      No input validation
    Production Readiness
      No persistent storage
      No user accounts
      No usage logging
      No error monitoring
    Scalability
      Single-user inference model
      No request queuing
      GPU memory not managed between requests
```

### 8.2 Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Kaggle API key exposed in notebook | High | High | Move to environment variables / secrets manager |
| Model hallucination in educational feedback | Medium | High | Add confidence scoring; human review layer |
| GPU memory exhaustion under concurrent load | Medium | High | Request queuing; `torch.cuda.empty_cache()` |
| Conversation history lost on page refresh | High | Medium | Acceptable for prototype; add persistence for production |
| No offline mode currently working | High | High | Model quantization (GGUF/ONNX) required for DRC deployment |
| Single point of failure (no fallback model) | Low | High | Add lighter fallback model for CPU-only environments |

### 8.3 Recommended Next Steps for Production

```mermaid
graph LR
    A[Current Prototype] --> B[Phase 1: Hardening]
    B --> B1[Add requirements.txt]
    B --> B2[Externalize credentials]
    B --> B3[Add basic input validation]
    B --> B4[Structure as Python package]

    B --> C[Phase 2: Offline Capability]
    C --> C1[Quantize model to GGUF 4-bit]
    C --> C2[Test on CPU-only hardware]
    C --> C3[Package as standalone app]
    C --> C4[Android / Raspberry Pi deployment]

    C --> D[Phase 3: Production]
    D --> D1[Add user authentication]
    D --> D2[Persist conversation history]
    D --> D3[Usage analytics for research]
    D --> D4[Teacher dashboard]
    D --> D5[DRC school pilot deployment]
```

### 8.4 Architecture for Edge Deployment (Planned)

```mermaid
graph TB
    subgraph EdgeDevice["Edge Device — Low-cost Android Tablet"]
        GGUF[Quantized Gemma 3n GGUF 4-bit ~3GB]
        LocalApp[Flutter / React Native App]
        SQLite[SQLite — Student Progress]
        LocalApp --> GGUF
        LocalApp --> SQLite
    end

    subgraph School["School Network optional"]
        Teacher[Teacher Dashboard]
        SyncServer[Sync Server]
        Teacher --> SyncServer
    end

    EdgeDevice -->|WiFi sync when available| School
    EdgeDevice -->|always works offline| EdgeDevice
```

---

## Summary

| Dimension | Current State | Maturity Level |
|---|---|---|
| AI/ML Core | Gemma 3n with 5 specialized features | Production-quality prompt engineering |
| Architecture | Clean 3-layer separation | Well-designed for future extension |
| Interface | Gradio 5-tab web app | Research prototype quality |
| Testing | Manual notebook tests only | Pre-alpha |
| Deployment | Kaggle notebook with share URL | Research demo |
| Security | Credentials in notebook | Needs hardening before any public deployment |
| Offline Capability | Not yet implemented | Planned for Mwalimu-STEM-GenAI phase |
| Language Coverage | 14 languages incl. Swahili, Lingala | Strong multilingual foundation |

**Mwalimu-LangLearn** is a technically sound research prototype that successfully demonstrates the feasibility of SLM-powered multilingual education. Its three-layer architecture is genuinely forward-looking — the clean inference abstraction will significantly reduce refactoring cost when transitioning to edge deployment. The primary work ahead is transforming the notebook into a deployable application with offline capability, persistence, and the security hardening needed for deployment in DRC schools.

---

*Analysis generated: 2026-03-12 | Repository: Mwalimu-LangLearn | Model: Google Gemma 3n E2B-IT*
