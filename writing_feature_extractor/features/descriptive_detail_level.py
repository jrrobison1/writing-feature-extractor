from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class DescriptiveDetailLevelFeature(WritingFeature):
    """Feature extractor for the level of descriptive detail in the text."""

    class DescriptiveDetailLevel(str, Enum):
        """Level of the richness and vividness of descriptions."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    @property
    def y_level_label(self):
        return "Descriptive Detail Level"

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
        return "descriptive_detail_level"

    @property
    def pydantic_feature_type(self):
        return self.DescriptiveDetailLevel

    @property
    def pydantic_docstring(self):
        return "Level of descriptive detail in the text. Can be 'none', 'low', 'medium', 'high'."
