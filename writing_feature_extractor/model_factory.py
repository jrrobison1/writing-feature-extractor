from enum import Enum

from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from available_models import AvailableModels


class ModelFactory:
    @staticmethod
    def get_llm_model(model: AvailableModels, PydanticModel: type[BaseModel]):
        if model == AvailableModels.GPT_3_5:
            return ChatOpenAI(
                model="gpt-3.5-turbo", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.GPT_4o:
            return ChatOpenAI(model="gpt-4o", temperature=0).with_structured_output(
                PydanticModel
            )
        elif model == AvailableModels.LLAMA3_70B:
            return ChatGroq(
                model_name="llama3-70b-8192", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_OPUS:
            return ChatAnthropic(
                model="claude-3-opus-20240229", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_SONNET:
            return ChatAnthropic(
                model_name="claude-3-sonnet-20240229", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_HAIKU:
            return ChatAnthropic(
                model_name="claude-3-haiku-20240307", temperature=0
            ).with_structured_output(PydanticModel)
        else:
            raise ValueError(f"Model {model} not found")
