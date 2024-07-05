from enum import Enum

from writing_feature_extractor.features.writing_feature import WritingFeature


class PaceFeature(WritingFeature):
    """Feature extractor for the pace of the narrative."""

    class Pace(str, Enum):
        """Pace/speed of the narrative."""

        VERY_SLOW = "very slow"
        SLOW = "slow"
        MEDIUM_SLOW = "medium slow"
        MEDIUM = "medium"
        MEDIUM_FAST = "medium fast"
        FAST = "fast"
        VERY_FAST = "very fast"

    @property
    def y_level_label(self) -> str:
        return "Pace"

    @property
    def pydantic_feature_label(self) -> str:
        return "pace"

    @property
    def pydantic_feature_type(self) -> type[Enum]:
        return self.Pace

    @property
    def pydantic_docstring(self) -> str:
        return "Pace/speed of the narrative."

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFCCCC",
            "1": "#FF9999",
            "2": "#FF6666",
            "3": "#FF3333",
            "4": "#FF0000",
            "5": "#CC0000",
            "6": "#990000",
        }
