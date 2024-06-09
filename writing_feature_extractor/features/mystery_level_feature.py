from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field

from features.writing_feature_graph_mode import WritingFeatureGraphMode


class MysteryLevelFeature:

    results: list[int] = []
    graph_mode = WritingFeatureGraphMode.BAR

    class MysteryLevel(str, Enum):
        """Level of mystery in the text. Can be 'low', 'medium', 'high', or 'none'."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    def get_graph_y_ticks(self):
        return [0, 1, 2, 3]

    def get_graph_y_tick_labels(self):
        return ["none", "low", "medium", "high"]

    def get_y_level_label(self):
        return "Mystery Level"

    def get_pydantic_feature_label(self):
        return "mystery_level"

    def get_pydantic_feature_type(self):
        return MysteryLevelFeature.MysteryLevel

    def get_pydantic_docstring(self):
        return (
            "Level of mystery in the text. Can be 'low', 'medium', 'high', or 'none'."
        )

    def get_int_for_enum(self, mystery_level: MysteryLevel):
        if mystery_level == MysteryLevelFeature.MysteryLevel.NONE:
            return 0
        if mystery_level == MysteryLevelFeature.MysteryLevel.LOW:
            return 1
        if mystery_level == MysteryLevelFeature.MysteryLevel.MEDIUM:
            return 2
        if mystery_level == MysteryLevelFeature.MysteryLevel.HIGH:
            return 3

    def add_result(self, enum_value):
        self.results.append(self.get_int_for_enum(enum_value))

    def set_graph_mode(self, graph_mode: WritingFeatureGraphMode):
        self.graph_mode = graph_mode
        return self
