# 🚀 AI Resume Analyzer & PDF Reporter

A privacy-first, local AI tool that analyzes resumes against job descriptions. This application extracts content from PDF resumes, performs a deep analysis using a local LLM, and generates a professional PDF report detailing the candidate's fit.



## ✨ Features
- **Local AI Analysis:** Powered by Llama 3.2 via Ollama—no data leaves your machine.
- **Match Scoring:** Provides a percentage-based score for candidate alignment.
- **Gap Identification:** Automatically detects "Missing Skills" not present in the resume.
- **Automated Reporting:** Generates a downloadable PDF summary for recruiters.
- **Modern UI:** Responsive web interface with real-time loading states.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python)
- **AI Engine:** Ollama (Llama 3.2)
- **PDF Extraction:** PyMuPDF4LLM
- **PDF Generation:** ReportLab
- **Frontend:** HTML5, CSS3 (with Loading Spinner), Jinja2

## 📋 Prerequisites
Before you begin, ensure you have the following installed:
1. **Python 3.10+**
2. **Ollama:** [Download here](https://ollama.com/)
3. **Llama 3.2 Model:** Run the following command in your terminal:
   ```bash
   ollama pull llama3.2