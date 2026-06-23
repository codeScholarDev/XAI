"""CSV loading, validation, and saving helpers."""

from pathlib import Path

import pandas as pd

from src.config import REQUIRED_COLUMNS


def load_sources(csv_path: Path) -> pd.DataFrame:
    """Load literature sources from a CSV file and validate the schema."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    validate_sources(dataframe)
    return dataframe


def validate_sources(dataframe: pd.DataFrame) -> None:
    """Validate that the source data contains all required columns."""
    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in dataframe.columns
    ]
    if missing_columns:
        missing_text = ", ".join(missing_columns)
        raise ValueError(f"Missing required column(s): {missing_text}")


def save_sources(dataframe: pd.DataFrame, csv_path: Path) -> None:
    """Save a dataframe to CSV using UTF-8 encoding."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(csv_path, index=False, encoding="utf-8")
