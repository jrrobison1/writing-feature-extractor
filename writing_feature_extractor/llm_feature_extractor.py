import sys
import traceback
from logger_config import logger

from prompt_templates.basic_prompt import prompt_template
from utils.text_metrics import get_text_statistics
from utils.text_metrics import combine_short_strings
from figure_plotter import get_graph


from features.writing_feature_factory import WritingFeatureFactory
from features.available_writing_features import (
    AvailableWritingFeatures,
)
from features.writing_feature import WritingFeature
from model_factory import ModelFactory
from available_models import AvailableModels
from features.writing_feature_graph_mode import (
    WritingFeatureGraphMode,
)


SECTION_DELIMETER = "***"

feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
    [
        (
            AvailableWritingFeatures.DESCRIPTIVE_DETAIL_LEVEL,
            WritingFeatureGraphMode.BAR,
        ),
        (AvailableWritingFeatures.ROMANCE_LEVEL, WritingFeatureGraphMode.COLOR),
    ]
)
llm = ModelFactory.get_llm_model(AvailableModels.GPT_3_5, DynamicFeatureModel)


def process_paragraph(paragraph: str, feature_collectors: list[WritingFeature]):
    """Run LLM on a paragraph to perform feature extraction"""

    try:
        result = llm.invoke(prompt_template.format(input=paragraph))
        logger.info(f"LLM Result: [{str(result)}]")
    except Exception as e:
        logger.error("Error invoking the LLM", e)
        logger.error(traceback.format_exc())

    result_dict = result.dict()
    result_dict["text_statistics"] = get_text_statistics(paragraph)

    for feature in feature_collectors:
        logger.info(
            f"Adding result [{result_dict[feature.get_pydantic_feature_label()]}] for feature: [{feature.get_pydantic_feature_label()}]"
        )
        feature.add_result(result_dict[feature.get_pydantic_feature_label()])


def process_section(section: str):
    """Process a 'section' of text. A section of text is expected to be broken up into
    smaller chunks separated by newlines ('paragraphs')"""

    print(f"----------SECTION BEGIN----------")

    for feature in feature_collectors:
        feature.results.clear()
    paragraphs = section.split("\n")
    paragraphs = combine_short_strings(paragraphs)
    for paragraph in paragraphs:
        try:
            process_paragraph(paragraph, feature_collectors)
        except Exception as e:
            logger.error("Error processing paragraph", e)
            logger.error(traceback.format_exc())
            continue

    try:
        get_graph(
            feature_collectors,
            paragraphs,
        )
    except Exception as e:
        logger.error("Error generating graph", e)
        logger.error(traceback.format_exc())

    print(f"----------SECTION END----------\n\n")


def extract_features(sections: list[str]):
    """Extract features from the text and display them in a graph."""

    for section in sections:
        try:
            process_section(section)
        except Exception as e:
            logger.error(e)
            continue


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        file_text = f.read()
        f.close()

    sections = file_text.split(SECTION_DELIMETER)
    extract_features(sections)
