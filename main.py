"""Command-line entry point for the XAI literature analysis support tool."""

import argparse

from src.classifier import ApiUsage, classify_sources
from src.config import (
    CLASSIFICATION_OUTPUT_PATH,
    PROCESSED_DATA_PATH,
    REPORT_OUTPUT_PATH,
    SAMPLE_DATA_PATH,
    THEMATIC_SUMMARY_PATH,
    load_settings,
)
from src.data_loader import load_sources, save_sources
from src.report_generator import generate_report
from src.summarizer import generate_theme_summaries, save_thematic_summary
from src.utils import ensure_directories


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for mock or OpenAI mode."""
    parser = argparse.ArgumentParser(
        description="Organize and classify Explainable AI literature notes."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--mock",
        action="store_true",
        help="Run rule-based mock mode without an OpenAI API key.",
    )
    mode_group.add_argument(
        "--openai",
        action="store_true",
        help="Run optional OpenAI mode using .env settings.",
    )
    return parser.parse_args()


def determine_mode(args: argparse.Namespace, settings: dict) -> bool:
    """Determine whether OpenAI mode should be used for this run."""
    if args.openai:
        return True
    if args.mock:
        return False
    return bool(settings["use_openai"])


def main() -> None:
    """Run the complete literature analysis support workflow."""
    args = parse_args()
    settings = load_settings()
    use_openai = determine_mode(args, settings)
    api_usage = ApiUsage(max_calls=settings["max_api_calls"])

    if use_openai and not settings["openai_api_key"]:
        print("OpenAI mode requested, but no API key was found. Falling back to mock mode.")
        use_openai = False

    ensure_directories(
        [
            PROCESSED_DATA_PATH,
            CLASSIFICATION_OUTPUT_PATH,
            THEMATIC_SUMMARY_PATH,
            REPORT_OUTPUT_PATH,
        ]
    )

    sources = load_sources(SAMPLE_DATA_PATH)
    classifications = classify_sources(
        sources,
        use_openai=use_openai,
        api_key=settings["openai_api_key"],
        max_api_calls=settings["max_api_calls"],
        api_usage=api_usage,
    )
    processed_sources = sources.merge(
        classifications[["id", "themes", "confidence", "justification"]],
        on="id",
        how="left",
    )

    summaries = generate_theme_summaries(
        sources,
        classifications,
        use_openai=use_openai,
        api_key=settings["openai_api_key"],
        max_api_calls=settings["max_api_calls"],
        api_usage=api_usage,
    )

    save_sources(processed_sources, PROCESSED_DATA_PATH)
    save_sources(classifications, CLASSIFICATION_OUTPUT_PATH)
    save_thematic_summary(summaries, THEMATIC_SUMMARY_PATH)
    generate_report(sources, classifications, summaries, REPORT_OUTPUT_PATH)
    print_terminal_summary(sources, classifications, use_openai)


def print_terminal_summary(
    sources, classifications, use_openai: bool
) -> None:
    """Print a clean terminal summary after the workflow finishes."""
    theme_values = sorted(
        {
            theme.strip()
            for value in classifications["themes"]
            for theme in str(value).split(";")
            if theme.strip()
        }
    )
    mode_label = "OpenAI API mode" if use_openai else "Mock rule-based mode"
    print("\nXAI Literature Analysis Support Tool")
    print("------------------------------------")
    print(f"Mode used: {mode_label}")
    print(f"Sources processed: {len(sources)}")
    print(f"Themes found: {', '.join(theme_values)}")
    print("Output files created:")
    print(f"- {PROCESSED_DATA_PATH}")
    print(f"- {CLASSIFICATION_OUTPUT_PATH}")
    print(f"- {THEMATIC_SUMMARY_PATH}")
    print(f"- {REPORT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
