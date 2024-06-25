import os
from enum import Enum

from langchain.output_parsers import PydanticOutputParser
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from writing_feature_extractor.available_models import AvailableModels
from writing_feature_extractor.prompt_templates.basic_prompt import prompt_template


class ModelFactory:
    """Factory for creating instances of large language models"""

    @staticmethod
    def get_llm_model(model: AvailableModels, PydanticModel: type[BaseModel]):
        """Get a language model based on the model type and a pydantic model representing
        the structured output of the model."""

        if model == AvailableModels.GPT_3_5:
            return prompt_template | ChatOpenAI(
                model="gpt-3.5-turbo", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.GPT_4o:
            return prompt_template | ChatOpenAI(
                model="gpt-4o", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.LLAMA3_70B:
            return prompt_template | ChatGroq(
                model_name="llama3-70b-8192", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_OPUS:
            return prompt_template | ChatAnthropic(
                model="claude-3-opus-20240229", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_SONNET:
            return prompt_template | ChatAnthropic(
                model_name="claude-3-sonnet-20240229", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.CLAUDE_HAIKU:
            return prompt_template | ChatAnthropic(
                model_name="claude-3-haiku-20240307", temperature=0
            ).with_structured_output(PydanticModel)
        elif model == AvailableModels.GEMINI_PRO:
            # Set up a parser + inject instructions into the prompt template.
            parser = PydanticOutputParser(pydantic_object=PydanticModel)

            prompt = PromptTemplate(
                template="Extract features from the following creative writing.\n{format_instructions}\n{input}\n",
                input_variables=["input"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
            parser = PydanticOutputParser(pydantic_object=PydanticModel)

            return prompt | llm | parser
        elif model == AvailableModels.TOGETHER_LLAMA3_70B:
            parser = PydanticOutputParser(pydantic_object=PydanticModel)

            prompt = PromptTemplate(
                template="Extract features from the following creative writing.\n{format_instructions}\n{input}\n",
                input_variables=["input"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )

            model = ChatOpenAI(
                base_url="https://api.together.xyz/v1",
                api_key=os.environ["TOGETHER_API_KEY"],
                model="meta-llama/Meta-Llama-3-70B",
                temperature=0,
            )

            return prompt | model | parser

        else:
            raise ValueError(f"Model {model} not found")
