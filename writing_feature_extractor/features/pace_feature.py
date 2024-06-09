from enum import Enum
from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field

from features.writing_feature import WritingFeature
from features.writing_feature_graph_mode import WritingFeatureGraphMode


class PaceFeature(WritingFeature):
    """Feature extractor for the pace of the narrative."""

    def __init__(
        self, graph_mode: WritingFeatureGraphMode = WritingFeatureGraphMode.BAR
    ):
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
        raise NotImplemented("PaceFeature does not have graph colors")

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
        self.results.append(self.get_int_for_enum(enum_value))

    def set_graph_mode(self, graph_mode: WritingFeatureGraphMode):
        self.graph_mode = graph_mode
        return self
