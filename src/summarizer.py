"""Generate theme-wise summaries from classified literature sources."""

from __future__ import annotations

from collections import Counter

import pandas as pd

from src.classifier import ApiUsage
from src.config import THEMES
from src.utils import split_theme_string


def generate_theme_summaries(
    sources: pd.DataFrame,
    classifications: pd.DataFrame,
    use_openai: bool = False,
    api_key: str = "",
    max_api_calls: int = 3,
    api_usage: ApiUsage | None = None,
) -> dict[str, str]:
    """Generate neutral academic summaries for each theme."""
    usage = api_usage or ApiUsage(max_calls=max_api_calls)
    client = _build_openai_client(api_key) if use_openai and api_key else None
    summaries = {}

    for theme in THEMES:
        theme_sources = _sources_for_theme(sources, classifications, theme)
        if client and usage.can_call() and not theme_sources.empty:
            summaries[theme] = _summarize_with_openai(theme, theme_sources, client, usage)
        else:
            summaries[theme] = _summarize_with_template(theme, theme_sources)

    return summaries


def save_thematic_summary(summaries: dict[str, str], output_path) -> None:
    """Save theme summaries to a Markdown file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Thematic Summary", ""]
    for theme, summary in summaries.items():
        lines.extend([f"## {theme}", "", summary, ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _build_openai_client(api_key: str):
    """Create an OpenAI client only when the package is available."""
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI(api_key=api_key)


def _sources_for_theme(
    sources: pd.DataFrame, classifications: pd.DataFrame, theme: str
) -> pd.DataFrame:
    """Return source rows assigned to a selected theme."""
    matching_ids = []
    for _, row in classifications.iterrows():
        if theme in split_theme_string(row.get("themes", "")):
            matching_ids.append(row["id"])
    return sources[sources["id"].isin(matching_ids)]


def _summarize_with_template(theme: str, theme_sources: pd.DataFrame) -> str:
    """Create a template-based academic summary for one theme."""
    if theme_sources.empty:
        return (
            "No sample source was strongly assigned to this theme. In a complete "
            "thesis literature review, this area should still be checked manually "
            "against the final search and selection results."
        )

    domains = _count_values(theme_sources["domain"].tolist())
    source_examples = _format_source_examples(theme_sources)
    return (
        f"The sample literature classified under **{theme}** indicates that this "
        "theme is relevant across the reviewed XAI discussion. The included notes "
        f"connect the theme to {domains}. Representative entries include "
        f"{source_examples}. For a Bachelor-level literature review, these sources "
        "can support a balanced synthesis by identifying repeated concepts, likely "
        "benefits, and issues requiring critical discussion. The classification "
        "should be treated as an organizational aid and verified through manual "
        "reading of the original academic sources."
    )


def _summarize_with_openai(theme: str, theme_sources: pd.DataFrame, client, usage: ApiUsage) -> str:
    """Create one concise OpenAI-generated summary if the API limit allows it."""
    notes = []
    for _, row in theme_sources.head(4).iterrows():
        notes.append(f"- {row['author_year']}: {str(row['abstract_or_note'])[:220]}")
    prompt = (
        f"Write one neutral academic paragraph for a Bachelor thesis literature review.\n"
        f"Theme: {theme}\n"
        f"Sources:\n{chr(10).join(notes)}\n"
        "Mention that automated classification requires manual checking."
    )
    usage.mark_call()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Write concise academic synthesis."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=220,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return _summarize_with_template(theme, theme_sources)


def _count_values(values: list[str]) -> str:
    """Summarize the most common domain values as readable text."""
    counts = Counter(values)
    parts = [f"{domain} ({count})" for domain, count in counts.most_common(4)]
    return ", ".join(parts)


def _format_source_examples(theme_sources: pd.DataFrame) -> str:
    """Format a short list of representative source labels."""
    labels = [
        f"{row['author_year']} on {row['domain']}"
        for _, row in theme_sources.head(3).iterrows()
    ]
    return "; ".join(labels)
