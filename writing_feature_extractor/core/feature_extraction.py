from enum import Enum
from typing import Any, Tuple
from langchain_core.language_models import LanguageModelInput
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable

from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.utils.text_metrics import (
    combine_short_strings,
    get_text_statistics,
)

logger = get_logger(__name__)


def process_feature_with_triangulation(
    result: BaseModel, triangulation_results: list[Enum], feature: WritingFeature
):
    """Process a feature with triangulation results"""

    result_dict = result.dict()
    feature_results = list(
        res.dict()[feature.pydantic_feature_label] for res in triangulation_results
    )

    triangulated_result = result_dict[feature.pydantic_feature_label]

    if feature.result_collection_mode == ResultCollectionMode.NUMBER_REPRESENTATION:
        triangulated_result = get_triangulated_number_representation(
            feature, result_dict, feature_results
        )

    else:
        triangulated_result = get_triangulated_mode(
            feature, result_dict, feature_results
        )

    if triangulated_result != result_dict[feature.pydantic_feature_label]:
        logger.info(
            f"Triangulated result is different from main LLM: Average: {triangulated_result}, Main LLM: {result_dict[feature.pydantic_feature_label]}"
        )
    logger.info(
        f"Adding result [{triangulated_result}] for feature: [{feature.pydantic_feature_label}]"
    )

    feature.add_result(triangulated_result)


def get_triangulated_number_representation(
    feature: WritingFeature, result_dict: dict, feature_results: list[Enum]
) -> Enum:
    tri_results_as_ints = [
        feature.get_int_for_enum(feature_result) for feature_result in feature_results
    ]
    tri_results_as_ints.append(
        feature.get_int_for_enum(result_dict[feature.pydantic_feature_label])
    )

    # Get floor of average of triangulation results
    floor_of_average = int(sum(tri_results_as_ints) / len(tri_results_as_ints))
    average_as_enum = list(feature.pydantic_feature_type)[floor_of_average]

    return average_as_enum


def get_triangulated_mode(
    feature: WritingFeature, result_dict: dict, feature_results: list[BaseModel]
) -> Enum:
    feature_results.append(result_dict[feature.pydantic_feature_label])
    mode = max(set(feature_results), key=feature_results.count)

    return mode


def process_text(
    text: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
):
    """Run LLM on a text to perform feature extraction"""

    triangulation_results = []
    try:
        result = llm.invoke(input=text)
        logger.debug(f"LLM Result: [{str(result)}]")
        if triangulation_llms:
            get_triangulation_results(text, triangulation_llms, triangulation_results)
    except Exception as e:
        logger.error("Error invoking the LLM", e)
        logger.debug(f"Text: {text},  llm: {llm}")

    if result:
        result_dict = result.dict()
    else:
        result_dict = {}

    for feature in feature_collectors:
        if len(triangulation_results) > 0:
            process_feature_with_triangulation(result, triangulation_results, feature)
        else:
            logger.info(
                f"Adding result [{result_dict.get(feature.pydantic_feature_label, 'ERROR')}] for feature: [{feature.pydantic_feature_label}]"
            )
            feature.add_result(result_dict.get(feature.pydantic_feature_label, "ERROR"))


def get_triangulation_results(text, triangulation_llms, triangulation_results):
    for llm in triangulation_llms:
        tri_result = llm.invoke(input=text)
        triangulation_results.append(tri_result)
        logger.debug(f"Triangulation Member LLM Result: [{str(tri_result)}]")
    return llm


def extract_features(
    sections: list[str],
    mode: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
) -> Tuple[list[WritingFeature], list[str], dict[str, Any]]:
    """Extract features from the text based on the specified mode."""
    for feature in feature_collectors:
        feature.results.clear()

    if mode == "paragraph":
        return extract_features_paragraph_mode(
            sections, feature_collectors, llm, triangulation_llms
        )
    elif mode == "section":
        return extract_features_section_mode(
            sections, feature_collectors, llm, triangulation_llms
        )
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be 'paragraph' or 'section'.")


def extract_features_paragraph_mode(
    sections: list[str],
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
) -> Tuple[list[WritingFeature], list[str], dict[str, Any]]:
    """Extract features from the text in paragraph mode."""
    text_units = []
    text_metrics = []

    for section in sections:
        paragraphs = combine_short_strings(section.split("\n"))
        for paragraph in paragraphs:
            process_text(paragraph, feature_collectors, llm, triangulation_llms)
            text_metrics.append(get_text_statistics(paragraph))
            text_units.append(paragraph)

        logger.info("Saving results to CSV...")
        save_results_to_csv(feature_collectors, text_metrics, text_units)
        input("Press Enter to continue...")

    log_processing_results(text_units, feature_collectors)
    return feature_collectors, text_units, text_metrics


def extract_features_section_mode(
    sections: list[str],
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
) -> Tuple[list[WritingFeature], list[str], dict[str, Any]]:
    """Extract features from the text in section mode."""
    text_units = []
    section_text_metrics = []
    sections = combine_short_strings(sections, 50)

    for section in sections:
        process_text(section, feature_collectors, llm, triangulation_llms)
        section_text_metrics.append(get_text_statistics(section))
        text_units.append(section)

    log_processing_results(text_units, feature_collectors)
    return feature_collectors, text_units, section_text_metrics


def log_processing_results(
    text_units: list[str], feature_collectors: list[WritingFeature]
):
    """Log the results of text processing."""
    logger.debug(f"Number of text units processed: {len(text_units)}")
    logger.debug(
        f"Number of results in each feature collector: {[len(fc.results) for fc in feature_collectors]}"
    )
