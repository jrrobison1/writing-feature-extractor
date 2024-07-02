from enum import Enum

from writing_feature_extractor.features.writing_feature import WritingFeature


class RomanceLevelFeature(WritingFeature):
    """Feature extractor for the level of romance in the text."""

    class RomanceLevel(str, Enum):
        """Level of romance in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    @property
    def y_level_label(self):
        return "Romance Level"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#CC99CC",
            "2": "#CC99CC",
            "3": "#800080",
        }

    @property
    def pydantic_feature_label(self):
        return "romance_level"

    @property
    def pydantic_feature_type(self):
        return self.RomanceLevel

    @property
    def pydantic_docstring(self):
        return "Level of romance in the text."
