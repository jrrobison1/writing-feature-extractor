from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class HumorLevelFeature(WritingFeature):
    """Feature extractor for the level of humor in the text."""

    def __init__(self, graph_mode: GraphMode = GraphMode.BAR):
        self.graph_mode = graph_mode

    results: list[int] = []

    class HumorLevel(str, Enum):
        """Level of humor in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    def get_graph_y_ticks(self):
        return [0, 1, 2, 3]

    def get_graph_y_tick_labels(self):
        return ["none", "low", "medium", "high"]

    def get_y_level_label(self):
        return "Humor Level"

    def get_graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FFE5CC",
            "2": "#FFB266",
            "3": "#FF8C00",
        }

    def get_pydantic_feature_label(self):
        return "humor_level"

    def get_pydantic_feature_type(self):
        return HumorLevelFeature.HumorLevel

    def get_pydantic_docstring(self):
        return "Level of humor in the text."

    def get_int_for_enum(self, humor_level: HumorLevel):
        if humor_level == HumorLevelFeature.HumorLevel.NONE:
            return 0
        if humor_level == HumorLevelFeature.HumorLevel.LOW:
            return 1
        if humor_level == HumorLevelFeature.HumorLevel.MEDIUM:
            return 2
        if humor_level == HumorLevelFeature.HumorLevel.HIGH:
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
