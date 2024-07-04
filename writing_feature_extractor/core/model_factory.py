from os import getenv
from typing import Callable, Dict

from langchain.output_parsers import PydanticOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import LanguageModelInput
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from writing_feature_extractor.core.available_models import AvailableModels
from writing_feature_extractor.core.custom_exceptions import ModelError

from writing_feature_extractor.prompt_templates.more_detailed_prompt import (
    more_detailed_prompt,
)

from writing_feature_extractor.prompt_templates.more_detailed_tooling_prompt import (
    more_detailed_tooling_prompt,
)
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)


class ModelFactory:
    @staticmethod
    def create_openai_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        try:
            return more_detailed_tooling_prompt | ChatOpenAI(
                model=model_name, temperature=0
            ).with_structured_output(PydanticModel)
        except Exception as e:
            logger.error(f"Error creating OpenAI model: {e}")
            logger.debug("Error details:", exc_info=True)
            raise ModelError("Failed to create OpenAI model.") from e

    @staticmethod
    def create_anthropic_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        try:
            return more_detailed_tooling_prompt | ChatAnthropic(
                model=model_name, temperature=0
            ).with_structured_output(PydanticModel)
        except Exception as e:
            logger.error(f"Error creating Anthropic model: {e}")
            logger.debug("Error details:", exc_info=True)
            raise ModelError("Failed to create Anthropic model.") from e

    @staticmethod
    def create_groq_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        try:
            return more_detailed_tooling_prompt | ChatGroq(
                model_name=model_name, temperature=0
            ).with_structured_output(PydanticModel)
        except Exception as e:
            logger.error(f"Error creating Groq model: {e}")
            logger.debug("Error details:", exc_info=True)
            raise ModelError("Failed to create Groq model.") from e

    @staticmethod
    def create_gemini_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        try:
            parser = PydanticOutputParser(pydantic_object=PydanticModel)
            prompt = PromptTemplate(
                template=more_detailed_prompt,
                input_variables=["input"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )
            llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
            return prompt | llm | parser
        except Exception as e:
            logger.error(f"Error creating Google Gemini model: {e}")
            logger.debug("Error details:", exc_info=True)
            raise ModelError("Failed to create Google Gemini model.") from e

    @staticmethod
    def create_openrouter_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        parser = PydanticOutputParser(pydantic_object=PydanticModel)

        prompt = PromptTemplate(
            template=more_detailed_prompt,
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

    MODEL_CREATORS: Dict[AvailableModels, Callable] = {
        AvailableModels.GPT_3_5: lambda PydanticModel: ModelFactory.create_openai_model(
            "gpt-3.5-turbo", PydanticModel
        ),
        AvailableModels.GPT_4o: lambda PydanticModel: ModelFactory.create_openai_model(
            "gpt-4o", PydanticModel
        ),
        AvailableModels.LLAMA3_70B: lambda PydanticModel: ModelFactory.create_groq_model(
            "llama3-70b-8192", PydanticModel
        ),
        AvailableModels.CLAUDE_OPUS: lambda PydanticModel: ModelFactory.create_anthropic_model(
            "claude-3-opus-20240229", PydanticModel
        ),
        AvailableModels.CLAUDE_SONNET: lambda PydanticModel: ModelFactory.create_anthropic_model(
            "claude-3-5-sonnet-20240620", PydanticModel
        ),
        AvailableModels.CLAUDE_HAIKU: lambda PydanticModel: ModelFactory.create_anthropic_model(
            "claude-3-haiku-20240307", PydanticModel
        ),
        AvailableModels.GEMINI_PRO: lambda PydanticModel: ModelFactory.create_gemini_model(
            "gemini-1.5-pro", PydanticModel
        ),
        AvailableModels.OPENOUTER_LLAMA3_70B_INSTRUCT: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "meta-llama/llama-3-70b-instruct", PydanticModel
        ),
        AvailableModels.MIXTRAL_8_22_INSTRUCT: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "mistralai/mixtral-8x22b-instruct", PydanticModel
        ),
        AvailableModels.QWEN_2_72B: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "qwen/qwen-2-72b-instruct", PydanticModel
        ),
        AvailableModels.LLAMA3_8B_INSTRUCT: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "meta-llama/llama-3-8b-instruct:free", PydanticModel
        ),
        AvailableModels.MIXTRAL_8_7_INSTRUCT: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "mistralai/mixtral-8x7b-instruct", PydanticModel
        ),
        AvailableModels.QWEN_1_5_14B: lambda PydanticModel: ModelFactory.create_openrouter_model(
            "qwen/qwen-14b-chat", PydanticModel
        ),
    }

    @classmethod
    def get_llm_model(
        cls, model: AvailableModels, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        creator = cls.MODEL_CREATORS.get(model)
        if creator:
            return creator(PydanticModel)
        else:
            raise ValueError(f"Model {model} not found")
