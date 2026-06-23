"""Theme classification logic for XAI literature sources."""

from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd

from src.config import THEMES
from src.utils import format_theme_list


KEYWORD_RULES = {
    "Conceptual Foundations": [
        "explainable",
        "interpretability",
        "interpretable",
        "transparency",
        "black box",
        "conceptual",
        "foundation",
    ],
    "XAI Methods": [
        "lime",
        "shap",
        "saliency",
        "counterfactual",
        "post-hoc",
        "feature attribution",
        "surrogate",
        "method",
    ],
    "Opportunities": [
        "opportunity",
        "benefit",
        "improve",
        "adoption",
        "decision support",
        "trust",
        "communication",
    ],
    "Challenges and Limitations": [
        "challenge",
        "limitation",
        "trade-off",
        "risk",
        "uncertainty",
        "evaluation",
        "robustness",
        "misleading",
    ],
    "Human-Centered XAI": [
        "human",
        "user",
        "stakeholder",
        "clinician",
        "decision-maker",
        "understanding",
        "cognitive",
    ],
    "Practical Implications": [
        "healthcare",
        "finance",
        "cybersecurity",
        "autonomous",
        "deployment",
        "practice",
        "operational",
        "real-world",
    ],
    "Governance and Trustworthy AI": [
        "fairness",
        "accountability",
        "governance",
        "trustworthy",
        "ethical",
        "regulation",
        "audit",
        "responsibility",
    ],
}


@dataclass
class ApiUsage:
    """Track OpenAI API calls during a single program run."""

    max_calls: int
    calls_made: int = 0

    def can_call(self) -> bool:
        """Return True when another API call is allowed."""
        return self.calls_made < self.max_calls

    def mark_call(self) -> None:
        """Record that one API call has been made."""
        self.calls_made += 1


def classify_sources(
    sources: pd.DataFrame,
    use_openai: bool = False,
    api_key: str = "",
    max_api_calls: int = 3,
    api_usage: ApiUsage | None = None,
) -> pd.DataFrame:
    """Classify all sources into one or more XAI themes."""
    usage = api_usage or ApiUsage(max_calls=max_api_calls)
    client = _build_openai_client(api_key) if use_openai and api_key else None
    rows = []

    for _, source in sources.iterrows():
        if client and usage.can_call():
            result = _classify_with_openai(source, client, usage)
        else:
            result = _classify_with_keywords(source)

        rows.append(
            {
                "id": source["id"],
                "author_year": source["author_year"],
                "title": source["title"],
                "domain": source["domain"],
                "themes": format_theme_list(result["themes"]),
                "confidence": result["confidence"],
                "justification": result["justification"],
            }
        )

    return pd.DataFrame(rows)


def _build_openai_client(api_key: str):
    """Create an OpenAI client only when the dependency and key are available."""
    try:
        from openai import OpenAI
    except ImportError:
        return None
    return OpenAI(api_key=api_key)


def _classify_with_keywords(source: pd.Series) -> dict:
    """Classify one source using transparent keyword rules."""
    text = _combined_source_text(source)
    matched_themes = []
    matched_keywords = {}

    for theme, keywords in KEYWORD_RULES.items():
        matches = [keyword for keyword in keywords if keyword in text]
        if matches:
            matched_themes.append(theme)
            matched_keywords[theme] = matches[:3]

    if not matched_themes:
        matched_themes = ["Conceptual Foundations"]
        matched_keywords["Conceptual Foundations"] = ["general XAI relevance"]

    confidence = _estimate_confidence(matched_themes, matched_keywords)
    justification = _build_keyword_justification(matched_keywords)
    return {
        "themes": matched_themes,
        "confidence": confidence,
        "justification": justification,
    }


def _classify_with_openai(source: pd.Series, client, usage: ApiUsage) -> dict:
    """Classify one source using a short OpenAI prompt with a rule-based fallback."""
    prompt = _build_openai_prompt(source)
    usage.mark_call()
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Classify XAI literature into the provided themes. Return compact JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            max_tokens=180,
        )
        content = response.choices[0].message.content or "{}"
        return _parse_openai_result(content)
    except Exception:
        return _classify_with_keywords(source)


def _build_openai_prompt(source: pd.Series) -> str:
    """Build a short prompt that limits API token use."""
    themes = "; ".join(THEMES)
    snippet = str(source["abstract_or_note"])[:700]
    return (
        f"Themes: {themes}\n"
        f"Title: {source['title']}\n"
        f"Domain: {source['domain']}\n"
        f"Note: {snippet}\n"
        "Return JSON with keys themes, confidence, justification. "
        "Themes must be a list using only the provided names."
    )


def _parse_openai_result(content: str) -> dict:
    """Parse the model response and keep only accepted theme names."""
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {
            "themes": ["Conceptual Foundations"],
            "confidence": "Low",
            "justification": "OpenAI response could not be parsed; default theme assigned.",
        }

    themes = [theme for theme in parsed.get("themes", []) if theme in THEMES]
    if not themes:
        themes = ["Conceptual Foundations"]

    confidence = parsed.get("confidence", "Medium")
    if confidence not in {"High", "Medium", "Low"}:
        confidence = "Medium"

    justification = str(parsed.get("justification", "Theme assigned by OpenAI."))
    return {
        "themes": themes,
        "confidence": confidence,
        "justification": justification[:300],
    }


def _combined_source_text(source: pd.Series) -> str:
    """Combine relevant source fields for keyword matching."""
    fields = [
        source.get("title", ""),
        source.get("abstract_or_note", ""),
        source.get("domain", ""),
        source.get("relevance_note", ""),
    ]
    return " ".join(str(field).lower() for field in fields)


def _estimate_confidence(
    matched_themes: list[str], matched_keywords: dict[str, list[str]]
) -> str:
    """Estimate confidence from the number of themes and keyword matches."""
    match_count = sum(len(keywords) for keywords in matched_keywords.values())
    if match_count >= 5 and len(matched_themes) >= 2:
        return "High"
    if match_count >= 2:
        return "Medium"
    return "Low"


def _build_keyword_justification(matched_keywords: dict[str, list[str]]) -> str:
    """Create a short justification from the matched keyword evidence."""
    parts = []
    for theme, keywords in matched_keywords.items():
        keyword_text = ", ".join(keywords)
        parts.append(f"{theme}: {keyword_text}")
    return "Keyword evidence - " + "; ".join(parts)
