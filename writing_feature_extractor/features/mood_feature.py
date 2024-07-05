from enum import Enum

from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.features.writing_feature import WritingFeature


class MoodFeature(WritingFeature):
    """Feature extractor for the mood of the text."""

    def __init__(
        self,
        result_collection_mode: ResultCollectionMode = ResultCollectionMode.FIELD_NAME,
    ):
        # This feature is only available by adding field name results
        self.result_collection_mode = ResultCollectionMode.FIELD_NAME

    results: list[int] = []

    class Mood(str, Enum):
        """Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match."""

        HAPPY = "happy"
        SAD = "sad"
        TENSE = "tense"
        ANGRY = "angry"
        CONTEMPLATIVE = "contemplative"
        NEUTRAL = "neutral"

    @property
    def pydantic_feature_label(self) -> str:
        return "mood"

    @property
    def pydantic_feature_type(self) -> type[Enum]:
        return self.Mood

    @property
    def pydantic_docstring(self) -> str:
        return "Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match.."

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "positive": "#FFFF00",
            "sad": "#00008B",
            "angry": "#FF0000",
            "suspenseful": "#7328AA",
            "neutral": "#D3D3D3",
        }

    @property
    def graph_y_tick_labels(self) -> list[str]:
        raise NotImplemented("MoodFeature is available only in colors")

    @property
    def graph_y_ticks(self) -> list[int]:
        raise NotImplemented("MoodFeature is available only in colors")

    @property
    def y_level_label(self) -> str:
        return "Mood"

    def get_int_for_enum(self, typ: type) -> int:
        raise NotImplemented("MoodFeature is available only in colors")
