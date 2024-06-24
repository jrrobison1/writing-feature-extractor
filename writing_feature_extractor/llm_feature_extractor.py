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

SECTION_DELIMETER = "***"

feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
    [
        (AvailableWritingFeatures.EMOTIONAL_INTENSITY, GraphMode.BAR),
        (AvailableWritingFeatures.MOOD, GraphMode.COLOR),
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
    for section in sections:
        try:
            process_section(section, mode)
        except Exception as e:
            logger.error(e)
            continue

    if mode == "section":
        try:
            logger.info(
                f"Feature collectors before graph generation: {feature_collectors}"
            )
            logger.info(
                f"Feature collector types: {[type(fc) for fc in feature_collectors]}"
            )
            logger.info(
                f"Feature collector graph modes: {[fc.graph_mode for fc in feature_collectors]}"
            )
            get_graph(
                feature_collectors, [f"Section {i+1}" for i in range(len(sections))]
            )
        except Exception as e:
            logger.error("Error generating graph", e)
            logger.debug(traceback.format_exc())


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Extract writing features from text.")
    parser.add_argument("file", help="Input text file to analyze")
    parser.add_argument(
        "--mode",
        choices=["paragraph", "section"],
        default="paragraph",
        help="Analysis mode: paragraph-by-paragraph or section-by-section",
    )

    args = parser.parse_args()

    with open(args.file) as f:
        file_text = f.read()

    sections = file_text.split(SECTION_DELIMETER)
    extract_features(sections, args.mode)
