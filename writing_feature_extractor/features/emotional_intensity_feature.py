from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class EmotionalIntensityFeature(WritingFeature):
    """Feature extractor for the emotional intensity of the text."""

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

    @property
    def y_level_label(self):
        return "Emotional Intensity"

    @property
    def pydantic_feature_label(self):
        return "emotional_intensity"

    @property
    def pydantic_feature_type(self):
        return self.EmotionalIntensity

    @property
    def pydantic_docstring(self):
        return "Strength or intensity of emotions expressed in the text"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FFCCCC",
            "2": "#FF9999",
            "3": "#FF6666",
            "4": "#FF3333",
            "5": "#FF0000",
            "6": "#CC0000",
            "7": "#990000",
        }
