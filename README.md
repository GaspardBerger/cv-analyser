# CV Analyser

An AI-powered resume analysis tool built with Streamlit and Claude. Upload a CV in PDF or DOCX format, and get structured feedback based on customizable evaluation criteria — with no data retained after the session.

## Features

- **Multi-format upload** — accepts PDF and DOCX files
- **AI analysis** — uses Claude to evaluate CVs against a configurable set of criteria
- **Customizable criteria** — reviewers can edit the evaluation standards directly in the UI via `config/criteria.yaml`
- **Privacy-first** — uploaded files are handled temporarily and not stored after analysis

## Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [Anthropic Claude](https://www.anthropic.com/) — AI analysis
- [pdfplumber](https://github.com/jsvine/pdfplumber) / [pypdf](https://github.com/py-pdf/pypdf) — PDF text extraction
- [python-docx](https://python-docx.readthedocs.io/) — DOCX text extraction

## Project Structure

```
cv-analyser/
├── app.py                  # Main entry point
├── requirements.txt
├── start.bat               # Windows launcher
├── config/
│   └── criteria.yaml       # Evaluation criteria
├── core/
│   ├── analyzer.py         # Claude API integration
│   ├── extractor.py        # Document text extraction
│   └── privacy.py          # Temporary file handling
└── ui/
    ├── upload.py           # File upload component
    ├── criteria_editor.py  # Criteria editing interface
    └── results.py          # Results display
```

## Getting Started

### Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone https://github.com/GaspardBerger/cv-analyser.git
cd cv-analyser
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

When deploying to Streamlit Cloud, add the key under **Settings → Secrets** instead.

### Run

```bash
streamlit run app.py
```

On Windows, you can also double-click `start.bat`.

The app will open at `http://localhost:8501`.

## Deployment

This app is compatible with [Streamlit Community Cloud](https://streamlit.io/cloud). Connect your GitHub repo, set your `ANTHROPIC_API_KEY` as a secret, and deploy directly from the main branch.
