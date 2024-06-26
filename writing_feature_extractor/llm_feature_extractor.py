import argparse
import traceback

import yaml
from dotenv import load_dotenv

from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable
from langchain_core.language_models import LanguageModelInput

from writing_feature_extractor.available_models import AvailableModels
from writing_feature_extractor.feature_config import load_feature_config
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.features.writing_feature_factory import (
    WritingFeatureFactory,
)
from writing_feature_extractor.figure_plotter import get_graph
from writing_feature_extractor.generate_graph_from_csv import generate_graph_from_csv
from writing_feature_extractor.logger_config import logger
from writing_feature_extractor.model_factory import ModelFactory
from writing_feature_extractor.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.utils.text_metrics import (
    combine_short_strings,
    get_text_statistics,
)

SECTION_DELIMETER = "***"


def process_text(
    text: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
):
    """Run LLM on a text to perform feature extraction"""
    try:
        result = llm.invoke(input=text)
        logger.info(f"LLM Result: [{str(result)}]")
    except Exception as e:
        logger.error("Error invoking the LLM", e)
        logger.debug(traceback.format_exc())
        return

    result_dict = result.dict()
    result_dict["text_statistics"] = get_text_statistics(text)

    for feature in feature_collectors:
        logger.info(
            f"Adding result [{result_dict[feature.get_pydantic_feature_label()]}] for feature: [{feature.get_pydantic_feature_label()}]"
        )
        feature.add_result(result_dict[feature.get_pydantic_feature_label()])


def process_paragraph(
    paragraph: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
):
    """Process a single paragraph"""
    process_text(paragraph, feature_collectors, llm)


def process_section(
    section: str,
    mode: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
):
    """Process a 'section' of text based on the analysis mode"""
    logger.info(f"----------SECTION BEGIN----------")

    if mode == "paragraph":
        for feature in feature_collectors:
            feature.results.clear()
        paragraphs = section.split("\n")
        paragraphs = combine_short_strings(paragraphs)
        for paragraph in paragraphs:
            try:
                process_paragraph(paragraph, feature_collectors, llm)
            except Exception as e:
                logger.error("Error processing paragraph", e)
                logger.debug(traceback.format_exc())
                continue

        try:
            get_graph(feature_collectors, paragraphs)
        except Exception as e:
            logger.error("Error generating graph", e)
            logger.debug(traceback.format_exc())
    elif mode == "section":
        process_text(section, feature_collectors, llm)

    logger.info(f"----------SECTION END----------\n\n")


def extract_features(
    sections: list[str],
    mode: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
):
    """Extract features from the text and display them in a graph."""
    try:
        for feature in feature_collectors:
            feature.results.clear()

        text_units = []
        for section in sections:
            try:
                if mode == "paragraph":
                    paragraphs = section.split("\n")
                    paragraphs = combine_short_strings(paragraphs)
                    for paragraph in paragraphs:
                        process_text(paragraph, feature_collectors, llm)
                        text_units.append(paragraph)
                    logger.info("Saving results to CSV...")
                    save_results_to_csv(
                        feature_collectors, text_units, "paragraphs.csv"
                    )
                    input("Press Enter to continue...")

                elif mode == "section":
                    process_text(section, feature_collectors, llm)
                    text_units.append(section)
                else:
                    logger.error(f"Invalid mode: {mode}")
                    return None
            except Exception as e:
                logger.error(f"Error processing section: {e}")
                logger.debug(traceback.format_exc())

        logger.debug(f"Number of text units processed: {len(text_units)}")
        logger.debug(
            f"Number of results in each feature collector: {[len(fc.results) for fc in feature_collectors]}"
        )

        return feature_collectors, text_units
    except Exception as e:
        logger.error(f"Error in extract_features: {e}")
        logger.debug(traceback.format_exc())
        return None


def load_feature_config(config_file: str):
    """Load feature configuration from a YAML file."""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    features = []
    for feature in config["features"]:
        feature_name = getattr(AvailableWritingFeatures, feature["name"])
        graph_mode = getattr(GraphMode, feature["graph_mode"])
        features.append((feature_name, graph_mode))

    return features


def main():
    parser = argparse.ArgumentParser(
        description="Extract writing features and generate graphs."
    )
    parser.add_argument("file", nargs="?", help="Input text file to analyze")
    parser.add_argument(
        "--mode",
        choices=["paragraph", "section"],
        default="paragraph",
        help="Analysis mode: paragraph-by-paragraph or section-by-section",
    )
    parser.add_argument("--save", action="store_true", help="Save results to CSV")
    parser.add_argument(
        "--graph", action="store_true", help="Generate graph from saved CSV"
    )
    parser.add_argument(
        "--bar-feature", help="Feature to use for bar heights when generating graph"
    )
    parser.add_argument(
        "--color-feature", help="Feature to use for bar colors when generating graph"
    )
    parser.add_argument(
        "--csv-file",
        default="feature_results.csv",
        help="CSV file to save results to or read from",
    )
    parser.add_argument(
        "--config",
        default="feature_config.yaml",
        help="YAML configuration file for features",
    )

    args = parser.parse_args()

    if args.graph:
        if not (args.bar_feature and args.color_feature):
            logger.error(
                "Please specify --bar-feature and --color-feature when using --graph"
            )
            return
        generate_graph_from_csv(args.csv_file, args.bar_feature, args.color_feature)
    elif args.file:
        with open(args.file) as f:
            text = f.read()

        # Load feature configuration
        features = load_feature_config(args.config)

        feature_collectors, DynamicFeatureModel = (
            WritingFeatureFactory.get_dynamic_model(features)
        )

        llm = ModelFactory.get_llm_model(AvailableModels.GPT_3_5, DynamicFeatureModel)
        logger.debug(f"Obtained LLM model: {llm}")

        sections = text.split(SECTION_DELIMETER)
        result = extract_features(sections, args.mode, feature_collectors, llm)

        if result is None:
            logger.error("Failed to extract features. Exiting.")
            return

        feature_collectors, text_units = result

        if args.save:
            save_results_to_csv(feature_collectors, text_units, args.csv_file)
    else:
        logger.error(
            "Please provide an input file or use --graph with a saved CSV file"
        )


if __name__ == "__main__":
    load_dotenv()
    main()
