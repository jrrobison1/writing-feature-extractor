from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class MysteryLevelFeature(WritingFeature):
    """Feature extractor for the level of mystery in the text."""

    def __init__(self, graph_mode: GraphMode = GraphMode.BAR):
        self.graph_mode = graph_mode

    results: list[int] = []

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

    def get_graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#CC99CC",
            "2": "#CC99CC",
            "3": "#800080",
        }

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
        if self.graph_mode == GraphMode.BAR:
            self.results.append(self.get_int_for_enum(enum_value))
        elif self.graph_mode == GraphMode.COLOR:
            self.results.append(enum_value)
        elif self.graph_mode == GraphMode.SAVE_ONLY:
            self.results.append(self.get_int_for_enum(enum_value))
        else:
            raise ValueError("Invalid graph mode")

    def set_graph_mode(self, graph_mode: GraphMode):
        self.graph_mode = graph_mode
        return self
