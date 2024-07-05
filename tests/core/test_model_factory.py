import pytest
from unittest.mock import patch, MagicMock
from langchain_core.pydantic_v1 import BaseModel

from writing_feature_extractor.core.model_factory import ModelFactory
from writing_feature_extractor.core.custom_exceptions import ModelError


# Mock PydanticModel for testing
class MockPydanticModel(BaseModel):
    test_field: str


@pytest.fixture(autouse=True)
def reset_model_factory():
    # Reset and re-register providers before each test
    ModelFactory._creators = {}
    ModelFactory.register("openai")(lambda model_name, PydanticModel: "openai_model")
    ModelFactory.register("anthropic")(
        lambda model_name, PydanticModel: "anthropic_model"
    )
    ModelFactory.register("groq")(lambda model_name, PydanticModel: "groq_model")
    ModelFactory.register("google")(lambda model_name, PydanticModel: "google_model")
    ModelFactory.register("openrouter")(
        lambda model_name, PydanticModel: "openrouter_model"
    )
    yield
    ModelFactory._creators = {}


def test_register_decorator():
    @ModelFactory.register("test_provider")
    def test_creator(model_name, PydanticModel):
        return "test_model"

    assert "test_provider" in ModelFactory._creators
    assert (
        ModelFactory._creators["test_provider"]("model", MockPydanticModel)
        == "test_model"
    )


def test_get_llm_model_registered_provider():
    result = ModelFactory.get_llm_model("openai", "gpt-3.5-turbo", MockPydanticModel)
    assert result == "openai_model"


def test_get_llm_model_unregistered_provider():
    with pytest.raises(ValueError, match="Provider unknown_provider not found"):
        ModelFactory.get_llm_model("unknown_provider", "test_model", MockPydanticModel)


def test_create_openai_model():
    result = ModelFactory.get_llm_model("openai", "gpt-3.5-turbo", MockPydanticModel)
    assert result == "openai_model"


def test_create_anthropic_model():
    result = ModelFactory.get_llm_model("anthropic", "claude-2", MockPydanticModel)
    assert result == "anthropic_model"


def test_create_groq_model():
    result = ModelFactory.get_llm_model("groq", "mixtral-8x7b-32768", MockPydanticModel)
    assert result == "groq_model"


def test_create_gemini_model():
    result = ModelFactory.get_llm_model("google", "gemini-pro", MockPydanticModel)
    assert result == "google_model"


def test_create_openrouter_model():
    result = ModelFactory.get_llm_model(
        "openrouter", "openai/gpt-3.5-turbo", MockPydanticModel
    )
    assert result == "openrouter_model"


def test_model_creation_error():
    @ModelFactory.register("error_provider")
    def error_creator(model_name, PydanticModel):
        raise Exception("Test error")

    with pytest.raises(ModelError, match="Failed to create error_provider model"):
        ModelFactory.get_llm_model("error_provider", "test_model", MockPydanticModel)
