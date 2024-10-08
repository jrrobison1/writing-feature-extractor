from enum import Enum
from typing import Type

from writing_feature_extractor.features.writing_feature import WritingFeature


class EmotionalIntensityFeature(WritingFeature):
    """Feature extractor for the emotional intensity of the text."""

    class EmotionalIntensity(str, Enum):
        """Strength or intensity of emotions expressed in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    @property
    def y_level_label(self) -> str:
        return "Emotional Intensity"

    @property
    def pydantic_feature_label(self) -> str:
        return "emotional_intensity"

    @property
    def pydantic_feature_type(self) -> Type[Enum]:
        return self.EmotionalIntensity

    @property
    def pydantic_docstring(self) -> str:
        return "Strength or intensity of emotions expressed in the text"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FF9999",
            "2": "#FF3333",
            "3": "#CC0000",
        }
