from enum import Enum
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.features.graph_mode import GraphMode


class PaceFeature(WritingFeature):
    """Feature extractor for the pace of the narrative."""

    def __init__(self, graph_mode: GraphMode = GraphMode.BAR):
        self.graph_mode = graph_mode

    results: list[int] = []

    class Pace(str, Enum):
        """Pace/speed of the narrative."""

        VERY_SLOW = "very slow"
        SLOW = "slow"
        MEDIUM_SLOW = "medium slow"
        MEDIUM = "medium"
        MEDIUM_FAST = "medium fast"
        FAST = "fast"
        VERY_FAST = "very fast"

    def get_graph_y_ticks(self):
        return [1, 2, 3, 4, 5, 6, 7]

    def get_graph_y_tick_labels(self):
        return [
            "very slow",
            "slow",
            "medium slow",
            "medium",
            "medium fast",
            "fast",
            "very fast",
        ]

    def get_y_level_label(self):
        return "Pace"

    def get_pydantic_feature_label(self):
        return "pace"

    def get_pydantic_feature_type(self):
        return PaceFeature.Pace

    def get_pydantic_docstring(self):
        return "Pace/speed of the narrative."

    def get_graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFCCCC",
            "1": "#FF9999",
            "2": "#FF6666",
            "3": "#FF3333",
            "4": "#FF0000",
            "5": "#CC0000",
            "6": "#990000",
        }

    def get_int_for_enum(self, pace: Pace):
        if pace == PaceFeature.Pace.VERY_SLOW:
            return 1
        if pace == PaceFeature.Pace.SLOW:
            return 2
        if pace == PaceFeature.Pace.MEDIUM_SLOW:
            return 3
        if pace == PaceFeature.Pace.MEDIUM:
            return 4
        if pace == PaceFeature.Pace.MEDIUM_FAST:
            return 5
        if pace == PaceFeature.Pace.FAST:
            return 6
        if pace == PaceFeature.Pace.VERY_FAST:
            return 7

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
