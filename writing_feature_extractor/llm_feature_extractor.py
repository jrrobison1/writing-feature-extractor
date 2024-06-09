import logging
import sys


from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from prompt_templates.basic_prompt import prompt_template
from utils.text_metrics import get_text_statistics
from utils.text_metrics import combine_short_strings
from figure_plotter import get_graph


from features.writing_feature_factory import WritingFeatureFactory
from features.available_writing_features import (
    AvailableWritingFeatures,
)
from features.writing_feature import WritingFeature


logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)
logging.getLogger(__name__).setLevel(logging.INFO)


SECTION_DELIMETER = "***"


# llm = ChatAnthropic(
#     model="claude-3-opus-20240229", temperature=0
# ).with_structured_output(DynamicFeatureModel)
# llm = ChatAnthropic(model_name="claude-3-sonnet-20240229", temperature=0).with_structured_output(Features)
# llm = ChatAnthropic(
#     model_name="claude-3-haiku-20240307", temperature=0
# ).with_structured_output(Features)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(
#     DynamicFeatureModel
# )
# llm = ChatGroq(model_name="llama3-70b-8192", temperature=0).with_structured_output(
#     Features
# )
feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
    [AvailableWritingFeatures.PACING, AvailableWritingFeatures.MOOD]
)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).with_structured_output(
    DynamicFeatureModel
)


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
