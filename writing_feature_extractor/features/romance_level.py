from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field

from features.graph_mode import GraphMode
from features.writing_feature import WritingFeature


class RomanceLevelFeature(WritingFeature):
    """Feature extractor for the level of romance in the text."""

    def __init__(self, graph_mode: GraphMode = GraphMode.BAR):
        self.graph_mode = graph_mode

    results: list[int] = []

    class RomanceLevel(str, Enum):
        """Level of romance in the text."""

        NONE = "none"
        LOW = "low"
        MEDIUM = "medium"
        HIGH = "high"

    def get_graph_y_ticks(self):
        return [0, 1, 2, 3]

    def get_graph_y_tick_labels(self):
        return ["none", "low", "medium", "high"]

    def get_y_level_label(self):
        return "Romance Level"

    def get_graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#CC99CC",
            "2": "#CC99CC",
            "3": "#800080",
        }

    def get_pydantic_feature_label(self):
        return "romance_level"

    def get_pydantic_feature_type(self):
        return RomanceLevelFeature.RomanceLevel

    def get_pydantic_docstring(self):
        return "Level of romance in the text."

    def get_int_for_enum(self, romance_level: RomanceLevel):
        if romance_level == RomanceLevelFeature.RomanceLevel.NONE:
            return 0
        if romance_level == RomanceLevelFeature.RomanceLevel.LOW:
            return 1
        if romance_level == RomanceLevelFeature.RomanceLevel.MEDIUM:
            return 2
        if romance_level == RomanceLevelFeature.RomanceLevel.HIGH:
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
