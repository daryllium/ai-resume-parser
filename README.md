# 📄 AI Resume Matcher & PDF Reporter

A high-performance, **privacy-first** recruitment automation tool. This application uses a local Large Language Model (LLM) to analyze candidate resumes against job descriptions, providing a match score, executive summary, and a downloadable PDF analysis report.



---

## 🌟 Project Purpose
This tool was built to bridge the gap between complex AI analysis and practical recruitment workflows. 
- **Privacy:** By using **Ollama**, candidate data never leaves the local machine.
- **Actionability:** Instead of just a "match %", it identifies exactly which skills are missing.
- **Professionalism:** Automatically generates a branded PDF report for easy sharing.

## ✨ Key Features
- **Local AI Analysis:** Powered by `Llama 3.2` for zero-latency, private processing.
- **Match Scoring:** Intelligent percentage-based alignment score.
- **Skill Gap Detection:** Specifically identifies "Missing Skills" from the Job Description.
- **Professional PDF Export:** Recruiter-ready reports generated via `ReportLab`.
- **Modern UI:** Responsive FastAPI web interface with real-time loading feedback.

---

## 🛠️ Tech Stack
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **AI/ML:** [Ollama](https://ollama.com/) (Llama 3.2)
- **PDF Extraction:** [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM)
- **PDF Generation:** [ReportLab](https://www.reportlab.com/)
- **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## 📋 Prerequisites
Before running, ensure you have:
1. **Python 3.10+**
2. **Ollama Desktop:** [Download here](https://ollama.com/download)
3. **Llama 3.2:** Run `ollama pull llama3.2` in your terminal.

## ⚙️ Quick Start

### 1. Clone & Setup
```bash
git clone [https://github.com/daryllium/ai-resume-parser.git]
cd ai-resume-parser
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the app
```bash
python3 uvicorn api:app --reload
```

Navigate to http://127.0.0.1:8000