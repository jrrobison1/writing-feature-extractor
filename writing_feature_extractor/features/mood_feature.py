from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class MoodFeature(WritingFeature):
    """Feature extractor for the mood of the text."""

    def __init__(self, graph_mode: GraphMode = GraphMode.COLOR):
        self.graph_mode = graph_mode

    results: list[int] = []

    class Mood(str, Enum):
        """Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match."""

        POSITIVE = "positive"
        SAD = "sad"
        ANGRY = "angry"
        SUSPENSEFUL = "suspenseful"
        NEUTRAL = "neutral"

    def get_pydantic_feature_label(self):
        return "mood"

    def get_pydantic_feature_type(self):
        return MoodFeature.Mood

    def get_pydantic_docstring(self):
        return "Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match.."

    def get_graph_colors(self):
        return {
            "positive": "#FFFF00",
            "sad": "#00008B",
            "angry": "#FF0000",
            "suspenseful": "#7328AA",
            "neutral": "#D3D3D3",
        }

    def get_graph_y_tick_labels(self):
        raise NotImplemented("MoodFeature is available only in colors")

    def get_graph_y_ticks(self):
        raise NotImplemented("MoodFeature is available only in colors")

    def get_y_level_label(self):
        return "Mood"

    def get_int_for_enum(self, typ: type):
        raise NotImplemented("MoodFeature is available only in colors")

    def add_result(self, enum_value):
        self.results.append(enum_value)

    def set_graph_mode(self, graph_mode: GraphMode):
        self.graph_mode = graph_mode
        return self
