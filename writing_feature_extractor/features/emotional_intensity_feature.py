from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field


class EmotionalIntensityFeature:

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
