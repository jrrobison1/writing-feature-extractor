import logging
import sys

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


logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)
logging.getLogger(__name__).setLevel(logging.INFO)


SECTION_DELIMETER = "***"

feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
    [AvailableWritingFeatures.PACING, AvailableWritingFeatures.MOOD]
)
llm = ModelFactory.get_llm_model(AvailableModels.GPT_3_5, DynamicFeatureModel)


def process_paragraph(paragraph: str, feature_collectors: list[WritingFeature]):
    try:
        result = llm.invoke(prompt_template.format(input=paragraph))
        logger.info(f"Result: [{str(result)}]")
    except Exception as e:
        logger.error(f"Exception is: [{e}]")

    result_dict = result.dict()
    result_dict["text_statistics"] = get_text_statistics(paragraph)

    for feature in feature_collectors:
        logger.info(
            f"Adding result [{result_dict[feature.get_pydantic_feature_label()]}] for feature: [{feature.get_pydantic_feature_label()}]"
        )
        feature.add_result(result_dict[feature.get_pydantic_feature_label()])


def process_section(section: str):
    print(f"----------SECTION BEGIN----------")

    for feature in feature_collectors:
        feature.results.clear()
    paragraphs = section.split("\n")
    paragraphs = combine_short_strings(paragraphs)
    for paragraph in paragraphs:
        try:
            process_paragraph(paragraph, feature_collectors)
        except Exception as e:
            logger.error(e)
            continue

    try:
        get_graph(
            feature_collectors,
            paragraphs,
        )
    except Exception as e:
        logger.error(e)

    print(f"----------SECTION END----------\n\n")


def extract_features(sections: list[str]):
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
