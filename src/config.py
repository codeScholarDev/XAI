"""Configuration values for the XAI literature analysis support tool."""

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

SAMPLE_DATA_PATH = DATA_DIR / "sample_sources.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_sources.csv"
CLASSIFICATION_OUTPUT_PATH = OUTPUT_DIR / "source_classification.csv"
THEMATIC_SUMMARY_PATH = OUTPUT_DIR / "thematic_summary.md"
REPORT_OUTPUT_PATH = OUTPUT_DIR / "xai_literature_report.md"

THEMES = [
    "Conceptual Foundations",
    "XAI Methods",
    "Opportunities",
    "Challenges and Limitations",
    "Human-Centered XAI",
    "Practical Implications",
    "Governance and Trustworthy AI",
]

REQUIRED_COLUMNS = [
    "id",
    "author_year",
    "title",
    "source_type",
    "abstract_or_note",
    "domain",
    "relevance_note",
]


def load_settings() -> dict:
    """Load runtime settings from environment variables and defaults."""
    load_dotenv(BASE_DIR / ".env")
    use_openai = os.getenv("USE_OPENAI", "false").strip().lower() == "true"
    max_api_calls = _read_positive_integer("MAX_API_CALLS", default=3)
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "use_openai": use_openai,
        "max_api_calls": max_api_calls,
    }


def _read_positive_integer(name: str, default: int) -> int:
    """Read a positive integer environment variable with a safe fallback."""
    raw_value = os.getenv(name, str(default)).strip()
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return max(value, 0)
