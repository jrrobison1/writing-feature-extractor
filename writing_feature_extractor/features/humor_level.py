from enum import Enum

from writing_feature_extractor.features.writing_feature import WritingFeature


class HumorLevelFeature(WritingFeature):
    """Feature extractor for the level of humor in the text."""

    class HumorLevel(str, Enum):
        """Level of humor in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    @property
    def y_level_label(self):
        return "Humor Level"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FFE5CC",
            "2": "#FFB266",
            "3": "#FF8C00",
        }

    @property
    def pydantic_feature_label(self):
        return "humor_level"

    @property
    def pydantic_feature_type(self):
        return self.HumorLevel

    @property
    def pydantic_docstring(self):
        return "Level of humor in the text."
