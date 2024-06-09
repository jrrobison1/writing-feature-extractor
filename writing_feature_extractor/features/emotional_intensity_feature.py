from abc import abstractmethod
from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field

from features.writing_feature import WritingFeature
from features.writing_feature_graph_mode import WritingFeatureGraphMode


class EmotionalIntensityFeature(WritingFeature):
    """Feature extractor for the emotional intensity of the text."""

    def __init__(
        self, graph_mode: WritingFeatureGraphMode = WritingFeatureGraphMode.BAR
    ):
        self.graph_mode = graph_mode

    results: list[int] = []

    class EmotionalIntensity(str, Enum):
        """Strength or intensity of emotions expressed in the text. Can be 'none', 'very low', 'low', 'medium low', 'medium', 'medium high', 'high', or 'very high'."""

        NONE = "none"
        VERY_LOW = "very low"
        LOW = "low"
        MEDIUM_LOW = "medium low"
        MEDIUM = "medium"
        MEDIUM_HIGH = "medium high"
        HIGH = "high"
        VERY_HIGH = "very high"

    def get_graph_y_ticks(self):
        return [0, 1, 2, 3, 4, 5, 6, 7]

    def get_graph_y_tick_labels(self):
        return [
            "none",
            "very low",
            "low",
            "medium low",
            "medium",
            "medium high",
            "high",
            "very high",
        ]

    def get_y_level_label(self):
        return "Emotional Intensity"

    def get_pydantic_feature_label(self):
        return "emotional_intensity"

    def get_pydantic_feature_type(self):
        return EmotionalIntensityFeature.EmotionalIntensity

    def get_pydantic_docstring(self):
        return "Strength or intensity of emotions expressed in the text"

    def get_graph_colors(self) -> dict[str, str]:
        raise NotImplemented("EmotionalIntensityFeature does not have graph colors")

    def get_int_for_enum(self, emotional_intensity: EmotionalIntensity):
        if emotional_intensity == EmotionalIntensityFeature.EmotionalIntensity.NONE:
            return 0
        if emotional_intensity == EmotionalIntensityFeature.EmotionalIntensity.VERY_LOW:
            return 1
        if emotional_intensity == EmotionalIntensityFeature.EmotionalIntensity.LOW:
            return 2
        if (
            emotional_intensity
            == EmotionalIntensityFeature.EmotionalIntensity.MEDIUM_LOW
        ):
            return 3
        if emotional_intensity == EmotionalIntensityFeature.EmotionalIntensity.MEDIUM:
            return 4
        if (
            emotional_intensity
            == EmotionalIntensityFeature.EmotionalIntensity.MEDIUM_HIGH
        ):
            return 5
        if emotional_intensity == EmotionalIntensityFeature.EmotionalIntensity.HIGH:
            return 6
        if (
            emotional_intensity
            == EmotionalIntensityFeature.EmotionalIntensity.VERY_HIGH
        ):
            return 7

    def add_result(self, enum_value):
        self.results.append(self.get_int_for_enum(enum_value))

    def set_graph_mode(self, graph_mode: WritingFeatureGraphMode):
        self.graph_mode = graph_mode
        return self
