from enum import Enum
from typing import Type


from writing_feature_extractor.features.aesthemos_features.five_point_scale.aesthemos_feature import (
    AesthemosFeature,
)
from writing_feature_extractor.features.aesthemos_features.five_point_scale.aethemos_rating import (
    AethemosRating,
)
from writing_feature_extractor.features.writing_feature import WritingFeature


class AesthemosBeauty(AesthemosFeature):
    """Feature extractor for the AETHEMOS beauty in the text."""

    @property
    def y_level_label(self) -> str:
        return "AESTHEMOS_BEAUTY"

    @property
    def pydantic_feature_label(self) -> str:
        return "beauty"

    @property
    def pydantic_feature_type(self) -> Type[Enum]:
        return AethemosRating

    @property
    def pydantic_docstring(self) -> str:
        return "How strongly did you experience a sense of beauty or being moved by this passage?"

    @property
    def graph_colors(self) -> dict[str, str]:
        return {
            "0": "#FFFFFF",
            "1": "#FF9999",
            "2": "#FF3333",
            "3": "#CC0000",
        }
