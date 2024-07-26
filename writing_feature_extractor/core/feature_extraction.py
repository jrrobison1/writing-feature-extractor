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
    result: BaseModel, triangulation_results: list[BaseModel], feature: WritingFeature
) -> None:
    """
    Process a feature with triangulation results.

    Args:
        result (BaseModel): The main LLM result.
        triangulation_results (list[BaseModel]): Results from triangulation LLMs.
        feature (WritingFeature): The writing feature being processed.

    This function compares the main LLM result with triangulation results and
    determines the final result based on the feature's result collection mode.
    """
    result_dict = result.dict()
    feature_results = [
        res.dict()[feature.pydantic_feature_label] for res in triangulation_results
    ]

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
    feature: WritingFeature, result_dict: dict[str, Any], feature_results: list[Enum]
) -> Enum:
    """
    Calculate the triangulated result for number representation features.

    Args:
        feature (WritingFeature): The writing feature being processed.
        result_dict (dict[str, Any]): The main LLM result as a dictionary.
        feature_results (list[Enum]): Results from triangulation LLMs.

    Returns:
        Enum: The triangulated result as an Enum value.
    """
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
    feature: WritingFeature, result_dict: dict[str, Any], feature_results: list[Enum]
) -> Enum:
    """
    Calculate the triangulated result using mode for non-number representation features.

    Args:
        feature (WritingFeature): The writing feature being processed.
        result_dict (dict[str, Any]): The main LLM result as a dictionary.
        feature_results (list[Enum]): Results from triangulation LLMs.

    Returns:
        Enum: The most common (mode) result among all LLMs.
    """
    feature_results.append(result_dict[feature.pydantic_feature_label])
    mode = max(set(feature_results), key=feature_results.count)

    return mode


def process_text(
    text: str,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] | None = None,
) -> None:
    """
    Run LLM on a text to perform feature extraction.

    Args:
        text (str): The input text to process.
        feature_collectors (list[WritingFeature]): List of writing features to extract.
        llm (Runnable[LanguageModelInput, BaseModel]): The main language model.
        triangulation_llms (list[Runnable[LanguageModelInput, BaseModel]] | None):
            Optional list of triangulation language models.

    This function processes the input text using the main LLM and optional
    triangulation LLMs to extract writing features.
    """
    triangulation_results = []
    try:
        result = llm.invoke(input=text)
        logger.debug(f"LLM Result: [{str(result)}]")
        result_dict = result.dict()
        if triangulation_llms:
            get_triangulation_results(text, triangulation_llms, triangulation_results)
    except Exception as e:
        logger.error("Error invoking the LLM", e)
        logger.debug(f"Text: {text},  llm: {llm}")
        result_dict = {}

    for feature in feature_collectors:
        if len(triangulation_results) > 0:
            process_feature_with_triangulation(result, triangulation_results, feature)
        else:
            logger.info(
                f"Adding result [{result_dict.get(feature.pydantic_feature_label, 'ERROR')}] for feature: [{feature.pydantic_feature_label}]"
            )
            feature.add_result(result_dict.get(feature.pydantic_feature_label, "ERROR"))


def get_triangulation_results(
    text: str,
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]],
    triangulation_results: list[BaseModel],
) -> None:
    """
    Get results from triangulation LLMs and append them to the triangulation_results list.

    Args:
        text (str): The input text to process.
        triangulation_llms (list[Runnable[LanguageModelInput, BaseModel]]): List of triangulation language models.
        triangulation_results (list[BaseModel]): List to store the results from triangulation LLMs.
    """
    for llm in triangulation_llms:
        tri_result = llm.invoke(input=text)
        triangulation_results.append(tri_result)
        logger.debug(f"Triangulation Member LLM Result: [{str(tri_result)}]")


class ExtractionMode(Enum):
    PARAGRAPH = "paragraph"
    SECTION = "section"


def extract_features(
    sections: list[str],
    mode: ExtractionMode,
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
) -> Tuple[list[WritingFeature], list[str], dict[str, Any]]:
    """
    Extract features from the text based on the specified mode.

    Args:
        sections (list[str]): List of text sections to process.
        mode (ExtractionMode): The extraction mode (PARAGRAPH or SECTION).
        feature_collectors (list[WritingFeature]): List of writing features to extract.
        llm (Runnable[LanguageModelInput, BaseModel]): The main language model.
        triangulation_llms (list[Runnable[LanguageModelInput, BaseModel]]):
            Optional list of triangulation language models.

    Returns:
        Tuple[list[WritingFeature], list[str], dict[str, Any]]:
            A tuple containing the updated feature collectors, processed text units,
            and text metrics.

    Raises:
        ValueError: If an invalid extraction mode is provided.
    """
    for feature in feature_collectors:
        feature.results.clear()

    if mode == ExtractionMode.PARAGRAPH:
        return extract_features_paragraph_mode(
            sections, feature_collectors, llm, triangulation_llms
        )
    elif mode == ExtractionMode.SECTION:
        return extract_features_section_mode(
            sections, feature_collectors, llm, triangulation_llms
        )
    else:
        raise ValueError(f"Invalid mode: {mode}. Must be a valid ExtractionMode.")


def extract_features_paragraph_mode(
    sections: list[str],
    feature_collectors: list[WritingFeature],
    llm: Runnable[LanguageModelInput, BaseModel],
    triangulation_llms: list[Runnable[LanguageModelInput, BaseModel]] = None,
) -> Tuple[list[WritingFeature], list[str], dict[str, Any]]:
    """
    Extract features from the text in paragraph mode.

    Args:
        sections (list[str]): List of text sections to process.
        feature_collectors (list[WritingFeature]): List of writing features to extract.
        llm (Runnable[LanguageModelInput, BaseModel]): The main language model.
        triangulation_llms (list[Runnable[LanguageModelInput, BaseModel]]):
            Optional list of triangulation language models.

    Returns:
        Tuple[list[WritingFeature], list[str], dict[str, Any]]:
            A tuple containing the updated feature collectors, processed paragraphs,
            and text metrics for each paragraph.
    """
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
    """
    Extract features from the text in section mode.

    Args:
        sections (list[str]): List of text sections to process.
        feature_collectors (list[WritingFeature]): List of writing features to extract.
        llm (Runnable[LanguageModelInput, BaseModel]): The main language model.
        triangulation_llms (list[Runnable[LanguageModelInput, BaseModel]]):
            Optional list of triangulation language models.

    Returns:
        Tuple[list[WritingFeature], list[str], dict[str, Any]]:
            A tuple containing the updated feature collectors, processed sections,
            and text metrics for each section.
    """
    text_units = []
    section_text_metrics = []
    sections = combine_short_strings(sections, 50)
    section_number = 1

    for section in sections:
        logger.info(f"Processing section number {section_number}")
        process_text(section, feature_collectors, llm, triangulation_llms)
        section_text_metrics.append(get_text_statistics(section))
        text_units.append(section)
        section_number += 1

    log_processing_results(text_units, feature_collectors)
    return feature_collectors, text_units, section_text_metrics


def log_processing_results(
    text_units: list[str], feature_collectors: list[WritingFeature]
) -> None:
    """
    Log the results of text processing.

    Args:
        text_units (list[str]): List of processed text units (paragraphs or sections).
        feature_collectors (list[WritingFeature]): List of writing features with collected results.
    """
    logger.debug(f"Number of text units processed: {len(text_units)}")
    logger.debug(
        f"Number of results in each feature collector: {[len(fc.results) for fc in feature_collectors]}"
    )
