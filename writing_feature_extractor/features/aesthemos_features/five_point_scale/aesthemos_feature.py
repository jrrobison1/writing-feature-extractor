from abc import ABC

from writing_feature_extractor.features.aesthemos_features.five_point_scale.aethemos_rating import (
    AethemosRating,
)
from writing_feature_extractor.features.writing_feature import WritingFeature


class AesthemosFeature(WritingFeature, ABC):
    def get_int_for_enum(self, enum_value: AethemosRating) -> int:
        """Aesthemos specific override here: start index at 1"""
        return list(self.pydantic_feature_type).index(enum_value) + 1
