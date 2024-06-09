from enum import Enum

from features.writing_feature_graph_mode import WritingFeatureGraphMode
from features.writing_feature import WritingFeature


class DescriptiveDetailLevelFeature(WritingFeature):
    """Feature extractor for the level of descriptive detail in the text."""

    def __init__(
        self, graph_mode: WritingFeatureGraphMode = WritingFeatureGraphMode.BAR
    ):
        self.graph_mode = graph_mode

    results: list[int] = []

    class DescriptiveDetailLevel(str, Enum):
        """Level of the richness and vividness of descriptions."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    def get_graph_y_ticks(self):
        return [0, 1, 2, 3]

    def get_graph_y_tick_labels(self):
        return ["none", "low", "medium", "high"]

    def get_y_level_label(self):
        return "Descriptive Detail Level"

    def get_graph_colors(self) -> dict[str, str]:
        return {
            "none": "#FFFFFF",
            "low": "#FFE5CC",
            "medium": "#FFB266",
            "high": "#FF8C00",
        }

    def get_pydantic_feature_label(self):
        return "descriptive_detail_level"

    def get_pydantic_feature_type(self):
        return DescriptiveDetailLevelFeature.DescriptiveDetailLevel

    def get_pydantic_docstring(self):
        return "Level of descriptive detail in the text. Can be 'none', 'low', 'medium', 'high'."

    def get_int_for_enum(self, descriptive_detail_level: DescriptiveDetailLevel):
        if (
            descriptive_detail_level
            == DescriptiveDetailLevelFeature.DescriptiveDetailLevel.NONE
        ):
            return 0
        if (
            descriptive_detail_level
            == DescriptiveDetailLevelFeature.DescriptiveDetailLevel.LOW
        ):
            return 1
        if (
            descriptive_detail_level
            == DescriptiveDetailLevelFeature.DescriptiveDetailLevel.MEDIUM
        ):
            return 2
        if (
            descriptive_detail_level
            == DescriptiveDetailLevelFeature.DescriptiveDetailLevel.HIGH
        ):
            return 3

    def add_result(self, enum_value):
        if self.graph_mode == WritingFeatureGraphMode.BAR:
            self.results.append(self.get_int_for_enum(enum_value))
        elif self.graph_mode == WritingFeatureGraphMode.COLOR:
            self.results.append(enum_value)
        else:
            raise ValueError("Invalid graph mode")

    def set_graph_mode(self, graph_mode: WritingFeatureGraphMode):
        self.graph_mode = graph_mode
        return self
