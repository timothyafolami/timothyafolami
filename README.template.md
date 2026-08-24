<div align="center">
  <img src="assets/hero.svg" alt="Timothy Afolami — Machine Learning Engineer" width="100%">
</div>

<a href="https://pypi.org/project/markitup-py/"><img src="https://img.shields.io/pypi/v/markitup-py?label=markitup-py&color=58a6ff&style=flat-square&logo=pypi&logoColor=white" alt="markitup-py on PyPI"></a>
<a href="https://www.linkedin.com/in/timothy-afolami"><img src="https://img.shields.io/badge/LinkedIn-timothy--afolami-0a66c2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="mailto:timmyafolami8469@gmail.com"><img src="https://img.shields.io/badge/Email-get%20in%20touch-ea4335?style=flat-square&logo=gmail&logoColor=white" alt="Email"></a>

---

## Start here

If you only open one thing, make it the first.

- 📦 **[markitup-py](https://github.com/timothyafolami/MarkItUp-py)** — *published on PyPI, MIT.* Markdown in, themed `.docx`/`.pdf`/`.html` out. A deterministic pipeline, not an LLM regenerating documents per request.
- 🌱 **[bean-lesion-classification](https://github.com/timothyafolami/bean-lesion-classification)** — *PyTorch → ONNX → FastAPI → React → Docker.* A model shipped as a system, tested end to end.
- 🛡️ **[Powershell-Malicious-Code-Detection](https://github.com/timothyafolami/Powershell-Malicious-Code-Detection)** — *recall-first security ML.* Safe deobfuscation, pseudo-label training, ranked analyst review queues.
- ⚡ **[Torque-Ripple-AI](https://github.com/timothyafolami/Torque-Ripple-AI)** — *physics-informed residual learning* for EV PMSM motors, sized to fit inside a real-time control loop.

---

## Coding activity

<div align="center">
  <img src="assets/activity.svg" alt="Contribution activity over the past year" width="100%">
</div>

<!--START:streak-->
<!--END:streak-->

Both cards are SVGs rendered by [`scripts/build_readme.py`](scripts/build_readme.py) from the
public GitHub API and committed here, so no third-party image host sits in the critical path.
Two deliberate choices: days are bucketed by **quantile** rather than against the single busiest
day, which stops one 3,891-contribution month flattening the rest of the year into a single
shade; and **amber marks the top 1% of days**, because a one-hue ramp buries the outliers among
the merely busy.

### Recently pushed

<!--START:recent-->
<!--END:recent-->

---

## The work

### Published packages

<!--START:pypi-->
<!--END:pypi-->

### ML systems

| Project | What it is | Stack |
|---|---|---|
| **[bean-lesion-classification](https://github.com/timothyafolami/bean-lesion-classification)** | Leaf-disease classification built as production software: multiple CNN architectures compared on accuracy *and* latency, ONNX export, FastAPI inference, React upload UI, tests from data loading through API. | PyTorch, ONNX, FastAPI, React, Docker |
| **[Powershell-Malicious-Code-Detection](https://github.com/timothyafolami/Powershell-Malicious-Code-Detection)** | Recall-first detection over large, partly-labelled PowerShell corpora. Normalises and safely deobfuscates script text, trains incrementally on reviewed and pseudo labels, exports ranked review queues. | Python, scikit-learn |
| **[Torque-Ripple-AI](https://github.com/timothyafolami/Torque-Ripple-AI)** | Predicts instantaneous torque ripple in EV PMSM drive motors at low speed and applies feedforward compensation — residual learning constrained by the physics. | PyTorch |
| **[SAMH](https://github.com/timothyafolami/SAMH-Sentiment-Analysis-For-Mental-Health)** | Sentiment analysis served as an API, aimed at mental-health text. | Python, FastAPI |

### LLM & agent systems

| Project | What it is | Stack |
|---|---|---|
| **[ai-chat-simulation](https://github.com/timothyafolami/ai-chat-simulation)** | AI-to-AI persona conversation engine: a state machine drives the exchange, personas are generated from profile and résumé text, and a separate LLM reviewer scores the outcome afterwards. | LangChain, OpenAI, Streamlit |
| **[AI-AGENTIC-HELPER](https://github.com/timothyafolami/AI-AGENTIC-HELPER)** | Daily planning assistant built on an agentic loop. | Python, LangChain |
| **[Resturant-Ai](https://github.com/timothyafolami/Resturant-Ai)** | Restaurant CRM chat application. | Python |
| **[MSE-AI](https://github.com/timothyafolami/MSE-AI)** | Materials-science conversation assistant. | Python |
| **[RAG Product Recommendation](https://github.com/timothyafolami/RAG---Product-Recommendation-System)** | Retrieval-augmented recommendation over a product catalogue. | Python, RAG |
| **[Youtube_Videos_summarizer](https://github.com/timothyafolami/Youtube_Videos_summarizer)** | Transcribes a video, then produces a summary, top keywords, and structured blog points. | Gemini Pro, Streamlit |

### Developer tools

| Project | What it is | Stack |
|---|---|---|
| **[MarkItDown-UI](https://github.com/timothyafolami/MarkItDown-UI)** | Browser front-end for Microsoft's MarkItDown — drag-and-drop conversion for PDF/DOCX/PPTX/XLSX and more, live preview, local history, keyboard-first. | FastAPI, TypeScript |
| **[svg-transformer](https://github.com/timothyafolami/svg-transformer)** | High-fidelity SVG → PNG/PDF/HTML conversion with a multi-engine renderer and fallbacks. | Python |
| **[msg_data_extractor](https://github.com/timothyafolami/msg_data_extractor)** | Batch-processes Outlook `.msg` trees, extracting attachments and applicant data into Excel. | Python |

---

## What I write <sub>(last 18 months)</sub>

<!--START:languages-->
<!--END:languages-->

**Serving & infra** — FastAPI · ONNX Runtime · Docker · AWS · Google Cloud · GitHub Actions
**LLM & agents** — LangChain · OpenAI · Gemini · RAG pipelines · evaluation harnesses
**Data** — PostgreSQL · MongoDB · Streamlit · Jupyter

---

## Currently

A self-directed ten-layer systems engineering lab — CPU cache behaviour and concurrency models
at the bottom, distributed failure and inference-serving economics at the top. Every experiment
opens with a **written prediction**, so the measurement gets a fair chance to prove me wrong.
Concurrency topics ship in six languages, because the lesson isn't the syntax — it's watching one
runtime hit a wall another one removed for you.

Alongside it: LLM agent systems, evaluation that isn't vibes, and serving models at a cost that
survives a spreadsheet.

---

<div align="center">
  <a href="https://www.linkedin.com/in/timothy-afolami"><b>LinkedIn</b></a> ·
  <a href="https://twitter.com/timothy_afolami"><b>Twitter</b></a> ·
  <a href="https://www.kaggle.com/timothyafolami"><b>Kaggle</b></a> ·
  <a href="mailto:timmyafolami8469@gmail.com"><b>Email</b></a>
  <br><br>
  <sub>Open to interesting problems in ML systems, LLM infrastructure, and applied AI.</sub>
  <br>
  <sub>Prose written by hand · activity, packages and languages rebuilt daily
  <!--START:updated--><!--END:updated--> · <a href="scripts/build_readme.py">see how</a></sub>
</div>
