import logging
import sys
import textstat

from langchain_core.pydantic_v1 import Field, create_model

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from prompt_templates.basic_prompt import prompt_template
from utils.text_metrics import calculate_dialogue_percentage
from utils.text_metrics import combine_short_strings
from figure_plotter import get_graph

from features.mood_feature import MoodFeature
from features.mystery_level_feature import MysteryLevelFeature
from features.emotional_intensity_feature import EmotionalIntensityFeature
from features.pace_feature import PaceFeature
from structures import Features

from langchain_together import ChatTogether


logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler(sys.stdout)],
)
logging.getLogger(__name__).setLevel(logging.INFO)


SECTION_DELIMETER = "***"


mystery_level_feature = MysteryLevelFeature()
mood_feature = MoodFeature()
pace_feature = PaceFeature()
emotional_intensity_feature = EmotionalIntensityFeature()
selected_features = dict()

# Mystery Level Feature
selected_features[mystery_level_feature.get_pydantic_feature_label()] = (
    mystery_level_feature.get_pydantic_feature_type(),
    Field(
        ...,
        description="Level of mystery in the text. Can be 'low', 'medium', 'high', or 'none'.",
    ),
)

# Mood Feature
selected_features[mood_feature.get_pydantic_feature_label()] = (
    mood_feature.get_pydantic_feature_type(),
    Field(
        ...,
        description="Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match.",
    ),
)

# Emotional Intensity Feature
selected_features[emotional_intensity_feature.get_pydantic_feature_label()] = (
    emotional_intensity_feature.get_pydantic_feature_type(),
    Field(
        ...,
        description="Strength or intensity of emotions expressed in the text.",
    ),
)

# Pace Feature
selected_features[pace_feature.get_pydantic_feature_label()] = (
    pace_feature.get_pydantic_feature_type(),
    Field(
        ...,
        description="Pace/speed of the narrative. Can be 'very slow', 'slow', 'medium slow', 'medium', 'medium fast', 'fast', or 'very fast'.",
    ),
)

DynamicFeatureModel = create_model(
    "DynamicFeatureModel",
    __doc__="Features contained in the creative writing text",
    **selected_features,
)


def get_text_statistics(text: str) -> dict[str]:
    text_statistics = dict()
    dialogue_percentage = calculate_dialogue_percentage(text)
    dp_as_string = f"{dialogue_percentage:.2f}%"
    text_statistics["dialogue_percentage"] = dp_as_string
    text_statistics["readability_ease"] = textstat.flesch_reading_ease(text)
    text_statistics["readability_grade"] = textstat.flesch_kincaid_grade(text)
    text_statistics["sentence_count"] = textstat.sentence_count(text)
    text_statistics["word_count"] = textstat.lexicon_count(text, removepunct=True)

    return text_statistics


# llm = ChatAnthropic(
#     model="claude-3-opus-20240229", temperature=0
# ).with_structured_output(DynamicFeatureModel)
# llm = ChatAnthropic(model_name="claude-3-sonnet-20240229", temperature=0).with_structured_output(Features)
# llm = ChatAnthropic(
#     model_name="claude-3-haiku-20240307", temperature=0
# ).with_structured_output(Features)
# llm = ChatVertexAI(model="gemini-1.5-pro-latest", temperature=0).with_structured_output(Features)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
# llm = ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(
#     DynamicFeatureModel
# )
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0).with_structured_output(
    DynamicFeatureModel
)


# Together.ai
# ChatTogether(model="meta-llama/Llama-3-70b-chat-hf")
# llm = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key="8ad294d976b5b5eb6d0e65c27b6b793db049edc05e79ae21ad4011ba78001d41",
#     model="meta-llama/Llama-3-70b-chat-hf",
#     temperature=0,
# ).with_structured_output(DynamicFeatureModel)


# llm = ChatGroq(model_name="llama3-70b-8192", temperature=0).with_structured_output(
#     Features
# )


def extract_features(sections: list[str]):
    for section in sections:
        try:
            print(f"----------SECTION BEGIN----------")
            paragraph_metadata = []
            this_paragraph_pace_data = []
            this_paragraph_mood = []
            # this_paragraph_suspense = []
            this_paragraph_emotional_intensity = []
            this_paragraph_mystery_level = []
            paragraphs = section.split("\n")
            for paragraph in paragraphs:
                paragraphs = combine_short_strings(paragraphs)
                try:
                    try:
                        result = llm.invoke(prompt_template.format(input=paragraph))
                        print(f"Result: [{str(result)}]")
                    except Exception as e:
                        logger.error(f"Exception is: [{e}]")

                    result_dict = result.dict()
                    result_dict["text_statistics"] = get_text_statistics(paragraph)

                    paragraph_metadata.append(result_dict)
                    this_paragraph_mood.append(result_dict["mood"])
                    this_paragraph_pace_data.append(
                        PaceFeature().get_int_for_enum(result_dict["pace"])
                    )
                    this_paragraph_emotional_intensity.append(
                        EmotionalIntensityFeature().get_int_for_enum(
                            result_dict["emotional_intensity"]
                        )
                    )
                    this_paragraph_mystery_level.append(
                        MysteryLevelFeature().get_int_for_enum(
                            result_dict["mystery_level"]
                        )
                    )
                except Exception as e:
                    logger.error(f"Second exception: [{e}]")
                    continue

            for pm in paragraph_metadata:
                print(pm["pace"])
                print(pm["mood"])
                # print(pm["emotional_intensity"])
                # print(pm["mystery_level"])

            try:
                get_graph(
                    this_paragraph_pace_data,
                    paragraphs,
                    this_paragraph_mood,
                    this_paragraph_emotional_intensity,
                    this_paragraph_mystery_level,
                )
            except Exception as e:
                logger.error(e)

            print(f"----------SECTION END----------\n\n")
        except Exception as e:
            logger.error(e)
            continue


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        file_text = f.read()
        f.close()

    sections = file_text.split(SECTION_DELIMETER)
    extract_features(sections)
