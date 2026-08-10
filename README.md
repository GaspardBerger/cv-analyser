# CV Analyser

An AI-powered resume analysis tool built with Streamlit and Claude. Upload a CV in PDF or DOCX format, and get structured feedback based on customizable evaluation criteria — with no data retained after the session.

## Features

- **Multi-format upload** — accepts PDF and DOCX files
- **AI analysis** — uses Claude to evaluate CVs against a configurable set of criteria
- **Checklist-based criteria** — the criteria in `config/criteria.yaml` mirror the paper CV checklist (layout + content) that students complete manually first; a CV that meets the full checklist scores 100/100
- **Customizable criteria** — trainers can toggle, edit and add their own criteria directly in the UI for the current session
- **Annotated CV preview** — results are shown in two columns: numbered improvement points on the left, and the CV on the right with the corresponding problem areas marked by dashed boxes (PDF pages rendered via PyMuPDF; text-based preview for Word files)
- **Deterministic, transparent scoring** — the AI only judges each criterion as met / partially met / not met; the score itself is computed in Python from the fixed weights in `criteria.yaml`. Every assessed criterion is shown in the results (no hidden criteria), so improving a criterion and re-uploading always raises the score
- **Stable re-uploads** — results are cached in memory (2h) on the extracted text, criteria and language, so re-uploading an unchanged CV returns the exact same score and remarks
- **Address language check** — verifies that the address is written in the same language as the rest of the CV (relevant for bilingual Brussels street names, e.g. *Wetstraat* vs *Rue de la Loi*)
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

- Python 3.10+
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
