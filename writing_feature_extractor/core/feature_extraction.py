import traceback

from langchain_core.language_models import LanguageModelInput
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable

from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.utils.text_processing import split_into_paragraphs
from writing_feature_extractor.utils.text_metrics import (
    combine_short_strings,
    get_text_statistics,
)

logger = get_logger(__name__)


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


def extract_features(
    sections: list[str],
    mode: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
):
    """Extract features from the text and display them in a graph."""
    for feature in feature_collectors:
        feature.results.clear()

    text_units = []
    for section in sections:
        if mode == "paragraph":
            paragraphs = section.split("\n")
            paragraphs = combine_short_strings(paragraphs)
            for paragraph in paragraphs:
                process_text(paragraph, feature_collectors, llm)
                text_units.append(paragraph)
            logger.info("Saving results to CSV...")
            save_results_to_csv(
                feature_collectors,
                text_units,
            )
            input("Press Enter to continue...")

        elif mode == "section":
            process_text(section, feature_collectors, llm)
            text_units.append(section)

    logger.debug(f"Number of text units processed: {len(text_units)}")
    logger.debug(
        f"Number of results in each feature collector: {[len(fc.results) for fc in feature_collectors]}"
    )

    return feature_collectors, text_units
