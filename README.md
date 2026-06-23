# XAI Literature Analysis Support Tool

## Project Overview

This Python project is an optional supporting prototype for organizing literature-review notes about Explainable AI (XAI). It helps classify sample sources into thesis-relevant themes and generates simple Markdown and CSV outputs that can support documentation, planning, and appendix material.

The project runs in mock mode by default, so no OpenAI API key is required.

## Student Details

- **Student Name:** Milad Pourmohammadi
- **Matriculation Number:** 4232532
- **Study Program:** Bachelor in Computer Science
- **University:** IU International University of Applied Sciences
- **Supervisor:** Tumpala, Uma Santhosh

## Thesis Title

A Literature-Based Analysis of Explainable AI in Modern Intelligent Systems: Opportunities, Challenges, and Practical Implications

## Academic Disclaimer

This tool is not the thesis methodology itself. It is only an optional supporting artefact for organizing literature-review notes. The official thesis methodology remains a structured/narrative literature review with systematic search and selection elements.

The generated classifications and summaries must be checked manually against the original academic sources before any thesis use.

## Features

- Loads a CSV file of XAI literature notes.
- Validates required source columns.
- Classifies sources into one or more XAI themes.
- Runs in mock mode without an API key.
- Optionally uses the OpenAI API with a strict maximum call limit.
- Generates processed CSV and Markdown outputs.
- Produces a thesis-support report with chapter-use suggestions.

## Theme Categories

1. Conceptual Foundations
2. XAI Methods
3. Opportunities
4. Challenges and Limitations
5. Human-Centered XAI
6. Practical Implications
7. Governance and Trustworthy AI

## Folder Structure

```text
xai-literature-analysis-support-tool/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── main.py
├── data/
│   ├── sample_sources.csv
│   └── processed_sources.csv
├── outputs/
│   ├── thematic_summary.md
│   ├── source_classification.csv
│   └── xai_literature_report.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── classifier.py
│   ├── summarizer.py
│   ├── report_generator.py
│   └── utils.py
└── docs/
    ├── methodology_note.md
    ├── thesis_appendix_note.md
    └── manual_github_upload_guide.md
```

## Installation Steps

```bash
cd xai-literature-analysis-support-tool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to Run in Mock Mode

Mock mode is the default mode and does not require an API key.

```bash
python main.py --mock
```

You can also run:

```bash
python main.py
```

## How to Run with OpenAI API

OpenAI mode is optional. It uses short prompts and respects `MAX_API_CALLS` from `.env`.

```bash
cp .env.example .env
```

Then add the API key inside `.env`:

```text
OPENAI_API_KEY=your_real_api_key_here
USE_OPENAI=true
MAX_API_CALLS=3
```

Run:

```bash
python main.py --openai
```

If no API key is found, the program falls back to mock mode.

## Expected Outputs

The program creates or updates:

- `data/processed_sources.csv`
- `outputs/source_classification.csv`
- `outputs/thematic_summary.md`
- `outputs/xai_literature_report.md`

## Manual GitHub Upload Instructions

1. Go to GitHub.
2. Create a new repository named `xai-literature-analysis-support-tool`.
3. Keep it public or private depending on the submission requirement.
4. Do not initialize with README if the local project already has `README.md`.
5. Open the repository.
6. Click **Add file**.
7. Click **Upload files**.
8. Drag and drop the full project files and folders.
9. Make sure these are uploaded:
   - `README.md`
   - `requirements.txt`
   - `.env.example`
   - `.gitignore`
   - `main.py`
   - `src` folder
   - `data` folder
   - `outputs` folder
   - `docs` folder
10. Do NOT upload:
    - `.env`
    - `.venv`
    - `__pycache__`
    - API keys
    - private notes
11. Click **Commit changes** on the GitHub website.

## What Files to Upload to GitHub

Upload the project source code, documentation, sample data, and generated example outputs:

- `README.md`
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `main.py`
- `src/`
- `data/`
- `outputs/`
- `docs/`

## What Files NOT to Upload to GitHub

Do not upload:

- `.env`
- `.venv/`
- `__pycache__/`
- API keys
- private notes
- local temporary files

## How This Project Can Be Mentioned in a Thesis Appendix

With supervisor approval, this project may be mentioned as an optional supporting artefact used to organize literature-review notes. It should not be described as the research method. The official method remains the literature-based review process described in the thesis methodology chapter.

## Ethical and Academic Integrity Note

The tool is intended to support organization and documentation only. It does not decide which sources are academically valid, does not replace critical reading, and does not generate final thesis arguments. Any generated text should be reviewed, edited, and cited according to university requirements.

## Limitations

- Mock mode uses simple keyword rules.
- OpenAI mode depends on the quality of short text snippets.
- Classifications may miss context from full papers.
- The tool does not perform database search, screening, citation verification, or quality appraisal.
- Generated summaries are starting points for student review, not final thesis content.
