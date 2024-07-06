from enum import Enum
from pathlib import Path
from dotenv import load_dotenv
import typer

from writing_feature_extractor.cli import parse_arguments
from writing_feature_extractor.core.custom_exceptions import FeatureExtractorError
from writing_feature_extractor.core.feature_config import load_feature_config
from writing_feature_extractor.core.feature_extraction import extract_features
from writing_feature_extractor.core.model_factory import ModelFactory
from writing_feature_extractor.features.writing_feature_factory import (
    WritingFeatureFactory,
)
from writing_feature_extractor.utils.generate_graph_from_csv import (
    generate_graph_from_csv,
)
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.utils.text_processing import (
    load_text,
    split_into_sections,
)

logger = get_logger(__name__)

app = typer.Typer()


class CliAnalysisMode(str, Enum):
    paragraph = "paragraph"
    section = "section"


class CliModelProvider(str, Enum):
    anthropic = "anthropic"
    openai = "openai"
    openrouter = "openrouter"
    groq = "groq"
    google = "google"


@app.command("extract")
def extract(
    file: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Input text file to analyze"
    ),
    mode: CliAnalysisMode = typer.Option(
        CliAnalysisMode.paragraph,
        help="Analysis mode: paragraph-by-paragraph or section-by-section",
    ),
    save: bool = typer.Option(False, help="Save results to CSV"),
    csv_file: Path = typer.Option(
        "feature_results.csv", help="CSV file to which results will be saved"
    ),
    config: Path = typer.Option(
        "feature_config.yaml", exists=True, help="YAML configuration file for features"
    ),
    provider: CliModelProvider = typer.Option(
        "anthropic", help="The LLM provider to use"
    ),
    model: str = typer.Option(
        "claude-3-haiku-20240307", help="The specific model to use"
    ),
):
    """Handle feature extraction from the input text."""

    try:
        text = load_text(file)
        features = load_feature_config(config)

        feature_collectors, DynamicFeatureModel = (
            WritingFeatureFactory.get_dynamic_model(features)
        )

        llm = ModelFactory.get_llm_model(provider, model, DynamicFeatureModel)
        logger.info(f"Obtained LLM model: {llm}")

        sections = split_into_sections(text)
        result = extract_features(sections, mode, feature_collectors, llm, [])

        if result and save:
            feature_collectors, text_units, text_metrics = result
            save_results_to_csv(feature_collectors, text_metrics, text_units, csv_file)
    except FeatureExtractorError as fee:
        logger.error(f"Feature extractor error: {fee}")
    except Exception as e:
        logger.error(f"An unhandled general exception has occurred: {e}")


@app.command("graph")
def generate_graph(
    csv_file: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="CSV file to read results from"
    ),
    bar_feature: str = typer.Option(
        ..., help="Feature to use for bar heights when generating graph"
    ),
    color_feature: str = typer.Option(
        ..., help="Feature to use for bar colors when generating graph"
    ),
):
    """Handle graph generation from a saved CSV file."""

    try:
        generate_graph_from_csv(csv_file, bar_feature, color_feature)
    except FeatureExtractorError as fee:
        logger.error(f"Feature extractor error: {fee}")
    except Exception as e:
        logger.errorr(f"An unhandled general exception has occurred: {e}")


def main() -> None:
    load_dotenv()
    app()


if __name__ == "__main__":
    main()
