"""Utility helpers used across the XAI literature analysis support tool."""

from pathlib import Path


def ensure_directories(paths: list[Path]) -> None:
    """Create parent directories for a list of file paths if needed."""
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)


def format_theme_list(themes: list[str]) -> str:
    """Return a readable semicolon-separated theme list."""
    return "; ".join(themes)


def split_theme_string(theme_text: str) -> list[str]:
    """Split a saved theme string back into individual theme names."""
    if not theme_text:
        return []
    return [theme.strip() for theme in theme_text.split(";") if theme.strip()]
