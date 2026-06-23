# Manual GitHub Upload Guide

This guide explains how to upload the project manually through the GitHub website.

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

Before uploading, run `python main.py --mock` once to confirm that the output files are generated successfully.
