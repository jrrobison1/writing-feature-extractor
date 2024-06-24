import sys
import argparse
import traceback
from logger_config import logger
from dotenv import load_dotenv

from prompt_templates.basic_prompt import prompt_template
from utils.text_metrics import get_text_statistics
from utils.text_metrics import combine_short_strings
from figure_plotter import get_graph

from features.writing_feature_factory import WritingFeatureFactory
from features.available_writing_features import AvailableWritingFeatures
from features.writing_feature import WritingFeature
from model_factory import ModelFactory
from available_models import AvailableModels
from features.graph_mode import GraphMode
from save_results_to_csv import save_results_to_csv
from generate_graph_from_csv import generate_graph_from_csv

SECTION_DELIMETER = "***"

feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
    [
        (AvailableWritingFeatures.EMOTIONAL_INTENSITY, GraphMode.BAR),
        (AvailableWritingFeatures.MOOD, GraphMode.COLOR),
        (AvailableWritingFeatures.DESCRIPTIVE_DETAIL_LEVEL, GraphMode.SAVE_ONLY),
        (AvailableWritingFeatures.MYSTERY_LEVEL, GraphMode.SAVE_ONLY),
        (AvailableWritingFeatures.PACING, GraphMode.SAVE_ONLY),
        (AvailableWritingFeatures.LEVEL_OF_SUSPENSE, GraphMode.SAVE_ONLY),
    ]
)
llm = ModelFactory.get_llm_model(AvailableModels.GPT_3_5, DynamicFeatureModel)
logger.debug(f"Obtained LLM model: {llm}")


def process_text(text: str, feature_collectors: list[WritingFeature]):
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


def process_paragraph(paragraph: str, feature_collectors: list[WritingFeature]):
    """Process a single paragraph"""
    process_text(paragraph, feature_collectors)


def process_section(section: str, mode: str):
    """Process a 'section' of text based on the analysis mode"""
    print(f"----------SECTION BEGIN----------")

    if mode == "paragraph":
        for feature in feature_collectors:
            feature.results.clear()
        paragraphs = section.split("\n")
        paragraphs = combine_short_strings(paragraphs)
        for paragraph in paragraphs:
            try:
                process_paragraph(paragraph, feature_collectors)
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
        process_text(section, feature_collectors)

    print(f"----------SECTION END----------\n\n")


def extract_features(sections: list[str], mode: str):
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
                    logger.info("-----SECTION BEGIN-----")
                    for paragraph in paragraphs:
                        process_text(paragraph, feature_collectors)
                        text_units.append(paragraph)
                    logger.info("-----SECTION END-----")
                    logger.info("Saving results to CSV...")
                    save_results_to_csv(
                        feature_collectors, text_units, "paragraphs.csv"
                    )
                    input("Press Enter to continue...")

                elif mode == "section":
                    process_text(section, feature_collectors)
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

        sections = text.split(SECTION_DELIMETER)
        result = extract_features(sections, args.mode)

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
    main()
