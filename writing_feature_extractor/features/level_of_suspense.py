from enum import Enum

from writing_feature_extractor.features.writing_feature import WritingFeature


class LevelOfSuspenseFeature(WritingFeature):
    """Feature extractor for the level of suspense in the text."""

    class LevelOfSuspense(str, Enum):
        """Level of suspense and tension in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    @property
    def y_level_label(self):
        return "Level of Suspense"

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
        return "level_of_suspense"

    @property
    def pydantic_feature_type(self):
        return self.LevelOfSuspense

    @property
    def pydantic_docstring(self):
        return "Level of suspense and tension in the text."
