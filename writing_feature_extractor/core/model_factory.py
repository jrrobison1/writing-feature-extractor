from functools import wraps
from os import getenv
from typing import Callable, Dict, Type

from langchain.output_parsers import PydanticOutputParser
from langchain_core.language_models import LanguageModelInput
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable

from writing_feature_extractor.core.custom_exceptions import ModelError
from writing_feature_extractor.prompt_templates.aesthemos_prompt_non_tooling_prompt import (
    aesthemos_non_tooling_prompt,
)
from writing_feature_extractor.prompt_templates.aesthemos_prompt import aesthemos_prompt
from writing_feature_extractor.prompt_templates.more_detailed_prompt import (
    more_detailed_prompt,
)
from writing_feature_extractor.prompt_templates.more_detailed_tooling_prompt import (
    more_detailed_tooling_prompt,
)
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.prompt_templates.basic_prompt import basic_prompt
from writing_feature_extractor.prompt_templates.advanced_emotional_intensity_prompt_tooling import (
    advanced_emotional_intensity_prompt,
)
from writing_feature_extractor.prompt_templates.non_tooling_advanced_emotional_intensity_prompt import (
    non_tooling_advanced_emotional_intensity_prompt,
)
from writing_feature_extractor.prompt_templates.non_tooling_advanced_descriptive_level_detail_prompt import (
    non_tooling_advanced_descriptive_level_detail_prompt,
)

logger = get_logger(__name__)


class ModelFactory:
    _creators: Dict[str, Callable] = {}

    @classmethod
    def register(cls, provider: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            cls._creators[provider] = wrapper
            return wrapper

        return decorator

    @classmethod
    def get_llm_model(
        cls, provider: str, model_name: str, PydanticModel: Type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        creator = cls._creators.get(provider)
        if creator:
            try:
                return creator(model_name, PydanticModel)
            except Exception as e:
                raise ModelError(f"Failed to create {provider} model: {str(e)}")
        else:
            raise ValueError(f"Provider {provider} not found")


@ModelFactory.register("openai")
def create_openai_model(
    model_name: str, PydanticModel: type[BaseModel]
) -> Runnable[LanguageModelInput, BaseModel]:
    from langchain_openai import ChatOpenAI

    try:
        return aesthemos_prompt | ChatOpenAI(
            model=model_name, temperature=0
        ).with_structured_output(PydanticModel)
    except Exception as e:
        logger.error(f"Error creating OpenAI model: {e}")
        raise ModelError("Failed to create OpenAI model.") from e


@ModelFactory.register("anthropic")
def create_anthropic_model(
    model_name: str, PydanticModel: type[BaseModel]
) -> Runnable[LanguageModelInput, BaseModel]:
    from langchain_anthropic import ChatAnthropic

    try:
        return aesthemos_prompt | ChatAnthropic(
            model=model_name, temperature=0
        ).with_structured_output(PydanticModel)
    except Exception as e:
        logger.error(f"Error creating Anthropic model: {e}")
        raise ModelError("Failed to create Anthropic model.") from e


@ModelFactory.register("groq")
def create_groq_model(
    model_name: str, PydanticModel: type[BaseModel]
) -> Runnable[LanguageModelInput, BaseModel]:
    from langchain_groq import ChatGroq

    try:
        return aesthemos_prompt | ChatGroq(
            model_name=model_name, temperature=0
        ).with_structured_output(PydanticModel)
    except Exception as e:
        logger.error(f"Error creating Groq model: {e}")
        raise ModelError("Failed to create Groq model.") from e


@ModelFactory.register("google")
def create_gemini_model(
    model_name: str, PydanticModel: type[BaseModel]
) -> Runnable[LanguageModelInput, BaseModel]:
    from langchain_google_genai import ChatGoogleGenerativeAI

    try:
        parser = PydanticOutputParser(pydantic_object=PydanticModel)
        prompt = PromptTemplate(
            template=aesthemos_non_tooling_prompt,
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        return prompt | llm | parser
    except Exception as e:
        logger.error(f"Error creating Google Gemini model: {e}")
        raise ModelError("Failed to create Google Gemini model.") from e


@ModelFactory.register("openrouter")
def create_openrouter_model(
    model_name: str, PydanticModel: type[BaseModel]
) -> Runnable[LanguageModelInput, BaseModel]:
    from langchain_openai import ChatOpenAI

    try:
        parser = PydanticOutputParser(pydantic_object=PydanticModel)

        prompt = PromptTemplate(
            template=aesthemos_non_tooling_prompt,
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=getenv("OPENROUTER_API_KEY"),
            model=model_name,
            temperature=0,
        )

        return prompt | llm | parser
    except Exception as e:
        logger.error(f"Error creating OpenRouter model: {e}")
        raise ModelError("Failed to create OpenRouter model.") from e
