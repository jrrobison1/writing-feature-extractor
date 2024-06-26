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

from writing_feature_extractor.available_models import AvailableModels
from writing_feature_extractor.prompt_templates.basic_prompt import prompt_template


class ModelFactory:
    @staticmethod
    def create_openai_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        return prompt_template | ChatOpenAI(
            model=model_name, temperature=0
        ).with_structured_output(PydanticModel)

    @staticmethod
    def create_anthropic_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        return prompt_template | ChatAnthropic(
            model=model_name, temperature=0
        ).with_structured_output(PydanticModel)

    @staticmethod
    def create_groq_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        return prompt_template | ChatGroq(
            model_name=model_name, temperature=0
        ).with_structured_output(PydanticModel)

    @staticmethod
    def create_gemini_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        parser = PydanticOutputParser(pydantic_object=PydanticModel)
        prompt = PromptTemplate(
            template="Extract features from the following creative writing.\n{format_instructions}\n{input}\n",
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0)
        return prompt | llm | parser

    @staticmethod
    def create_together_model(
        model_name: str, PydanticModel: type[BaseModel]
    ) -> Runnable[LanguageModelInput, BaseModel]:
        parser = PydanticOutputParser(pydantic_object=PydanticModel)
        prompt = PromptTemplate(
            template="Extract features from the following creative writing.\n{format_instructions}\n{input}\n",
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        model = ChatOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.environ["TOGETHER_API_KEY"],
            model=model_name,
            temperature=0,
        )
        return prompt | model | parser

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
            "claude-3-sonnet-20240229", PydanticModel
        ),
        AvailableModels.CLAUDE_HAIKU: lambda PydanticModel: ModelFactory.create_anthropic_model(
            "claude-3-haiku-20240307", PydanticModel
        ),
        AvailableModels.GEMINI_PRO: lambda PydanticModel: ModelFactory.create_gemini_model(
            "gemini-1.5-pro", PydanticModel
        ),
        AvailableModels.TOGETHER_LLAMA3_70B: lambda PydanticModel: ModelFactory.create_together_model(
            "meta-llama/Meta-Llama-3-70B", PydanticModel
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
