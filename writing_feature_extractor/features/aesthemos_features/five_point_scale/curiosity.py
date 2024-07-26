from enum import Enum
from typing import Type


from writing_feature_extractor.features.aesthemos_features.five_point_scale.aesthemos_feature import (
    AesthemosFeature,
)
from writing_feature_extractor.features.aesthemos_features.five_point_scale.aethemos_rating import (
    AethemosRating,
)
from writing_feature_extractor.features.writing_feature import WritingFeature


class AesthemosCuriosity(AesthemosFeature):
    """Feature extractor for the AETHEMOS curiosity in the text."""

    @property
    def y_level_label(self) -> str:
        return "AESTHEMOS_CURIOSITY"

    @property
    def pydantic_feature_label(self) -> str:
        return "curiosity"

    @property
    def pydantic_feature_type(self) -> Type[Enum]:
        return AethemosRating

    @property
    def pydantic_docstring(self) -> str:
        return "How much did this passage spark your curiosity or interest?"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FF9999",
            "2": "#FF3333",
            "3": "#CC0000",
        }
