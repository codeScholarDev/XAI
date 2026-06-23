"""Generate the final Markdown report for thesis-support documentation."""

from pathlib import Path

import pandas as pd


STUDENT_DETAILS = {
    "Student Name": "Milad Pourmohammadi",
    "Matriculation Number": "4232532",
    "Study Program": "Bachelor in Computer Science",
    "University": "IU International University of Applied Sciences",
    "Supervisor": "Tumpala, Uma Santhosh",
}

THESIS_TITLE = (
    "A Literature-Based Analysis of Explainable AI in Modern Intelligent Systems: "
    "Opportunities, Challenges, and Practical Implications"
)

ACADEMIC_DISCLAIMER = (
    "This tool is not the thesis methodology itself. It is only an optional "
    "supporting artefact for organizing literature-review notes. The official "
    "thesis methodology remains a structured/narrative literature review with "
    "systematic search and selection elements."
)


def generate_report(
    sources: pd.DataFrame,
    classifications: pd.DataFrame,
    summaries: dict[str, str],
    output_path: Path,
) -> None:
    """Generate the complete Markdown literature analysis report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    report = "\n".join(
        [
            "# XAI Literature Analysis Support Tool Report",
            "",
            "## Student Details",
            _student_details_markdown(),
            "",
            "## Thesis Title",
            THESIS_TITLE,
            "",
            "## Academic Disclaimer",
            ACADEMIC_DISCLAIMER,
            "",
            "## Dataset Overview",
            _dataset_overview(sources, classifications),
            "",
            "## Theme Classification Table",
            _classification_table(classifications),
            "",
            "## Theme-Wise Synthesis",
            _theme_summaries_markdown(summaries),
            "",
            "## Practical Implication Notes",
            _practical_implication_notes(),
            "",
            "## Limitations of Automated Classification",
            _limitations(),
            "",
            "## Suggested Thesis Use",
            _suggested_thesis_use(),
            "",
        ]
    )
    output_path.write_text(report, encoding="utf-8")


def _student_details_markdown() -> str:
    """Return student details as Markdown bullet points."""
    return "\n".join(f"- **{label}:** {value}" for label, value in STUDENT_DETAILS.items())


def _dataset_overview(sources: pd.DataFrame, classifications: pd.DataFrame) -> str:
    """Build a concise overview of the input dataset and assigned themes."""
    unique_domains = ", ".join(sorted(sources["domain"].dropna().unique()))
    theme_count = classifications["themes"].nunique()
    return (
        f"The sample dataset contains **{len(sources)}** literature entries across "
        f"the following domains: {unique_domains}. The automated workflow produced "
        f"**{len(classifications)}** classification rows and **{theme_count}** "
        "unique theme combinations."
    )


def _classification_table(classifications: pd.DataFrame) -> str:
    """Convert classification results into a Markdown table."""
    columns = ["id", "author_year", "title", "domain", "themes", "confidence"]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in classifications[columns].iterrows():
        cells = [_escape_markdown_cell(row[column]) for column in columns]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *rows])


def _escape_markdown_cell(value) -> str:
    """Escape Markdown table separators in a cell value."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def _theme_summaries_markdown(summaries: dict[str, str]) -> str:
    """Format all theme summaries as report subsections."""
    lines = []
    for theme, summary in summaries.items():
        lines.extend([f"### {theme}", "", summary, ""])
    return "\n".join(lines).strip()


def _practical_implication_notes() -> str:
    """Return notes about practical implications for modern intelligent systems."""
    return (
        "The classified literature suggests that XAI is practically relevant when "
        "AI systems influence high-impact decisions, such as clinical support, "
        "credit or risk assessment, cybersecurity monitoring, and autonomous "
        "systems. Explanations may improve communication, support accountability, "
        "and help users question model outputs. However, explanations should not "
        "be treated as proof that a model is correct, fair, or safe."
    )


def _limitations() -> str:
    """Return limitations of the automated classification approach."""
    return (
        "The automated classification uses keyword rules in mock mode and optional "
        "short API prompts in OpenAI mode. It cannot replace careful reading, "
        "quality assessment, citation checking, or the thesis search and selection "
        "process. Theme assignments may be incomplete, overly broad, or influenced "
        "by wording in the notes rather than by the full academic publication."
    )


def _suggested_thesis_use() -> str:
    """Return suggested ways to use the generated outputs in thesis chapters."""
    return "\n".join(
        [
            "- **Chapter 2: Theoretical Foundations:** Use conceptual and governance themes to organize core definitions and debates.",
            "- **Chapter 3: Major Approaches and Methods:** Use the XAI methods theme to structure post-hoc, attribution, surrogate, and counterfactual approaches.",
            "- **Chapter 4: Opportunities:** Use opportunity-related entries to discuss trust, adoption, communication, and decision support.",
            "- **Chapter 5: Challenges and Limitations:** Use challenge-related entries to frame reliability, evaluation, misuse, and interpretation limits.",
            "- **Chapter 6: Practical Implications:** Use domain-specific entries to discuss healthcare, finance, cybersecurity, and autonomous systems.",
        ]
    )
