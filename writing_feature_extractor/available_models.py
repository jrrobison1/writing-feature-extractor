from enum import Enum


class AvailableModels(str, Enum):
    """Available llm models for text generation."""

    GPT_3_5 = "gpt-3.5-turbo"
    GPT_4o = "gpt-4o"
    LLAMA3_70B = "llama3-70b-8192"
    CLAUDE_OPUS = "claude-3-opus-20240229"
    CLAUDE_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_HAIKU = "claude-3-haiku-20240307"
    GEMINI_PRO = "gemini-pro-1.5"
    TOGETHER_LLAMA3_70B = "together-llama3-70b-8192"
