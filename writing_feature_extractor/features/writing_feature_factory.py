from typing import Tuple
from features.writing_feature import WritingFeature
from features.available_writing_features import (
    AvailableWritingFeatures,
)
from features.emotional_intensity_feature import EmotionalIntensityFeature
from features.mood_feature import MoodFeature
from features.mystery_level_feature import MysteryLevelFeature
from features.pace_feature import PaceFeature

from langchain_core.pydantic_v1 import Field, BaseModel, create_model


class WritingFeatureFactory:
    @staticmethod
    def get_dynamic_model(
        features: list[AvailableWritingFeatures],
    ) -> Tuple[type[BaseModel], list[WritingFeature]]:
        selected_features = dict()
        feature_collectors = []
        for feature in features:
            if feature == AvailableWritingFeatures.PACING:
                current_feature = PaceFeature()
            if feature == AvailableWritingFeatures.MOOD:
                current_feature = MoodFeature()
            if feature == AvailableWritingFeatures.EMOTIONAL_INTENSITY:
                current_feature = EmotionalIntensityFeature()
            if feature == AvailableWritingFeatures.MYSTERY_LEVEL:
                current_feature = MysteryLevelFeature()

            selected_features[current_feature.get_pydantic_feature_label()] = (
                current_feature.get_pydantic_feature_type(),
                Field(
                    ...,
                    description=current_feature.get_pydantic_docstring(),
                ),
            )

            feature_collectors.append(current_feature)
        DynamicFeatureModel = create_model(
            "DynamicFeatureModel",
            __doc__="Features contained in the creative writing text",
            **selected_features,
        )

        return feature_collectors, DynamicFeatureModel
