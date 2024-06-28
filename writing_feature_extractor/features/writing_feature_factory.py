from typing import Tuple

from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from writing_feature_extractor.core.custom_exceptions import FeatureExtractorError
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.descriptive_detail_level import (
    DescriptiveDetailLevelFeature,
)
from writing_feature_extractor.features.emotional_intensity_feature import (
    EmotionalIntensityFeature,
)
from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.humor_level import HumorLevelFeature
from writing_feature_extractor.features.level_of_suspense import LevelOfSuspenseFeature
from writing_feature_extractor.features.mood_feature import MoodFeature
from writing_feature_extractor.features.mystery_level_feature import MysteryLevelFeature
from writing_feature_extractor.features.pace_feature import PaceFeature
from writing_feature_extractor.features.romance_level import RomanceLevelFeature
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)


class WritingFeatureFactory:
    """Factory class to create dynamic pydantic models based on the given
    writing features desired for feature extraction."""

    @staticmethod
    def get_dynamic_model(
        features: list[Tuple[AvailableWritingFeatures, GraphMode]],
    ) -> Tuple[type[BaseModel], list[WritingFeature]]:
        """Creates a dynamic pydantic model based on the given writing features"""

        try:
            selected_features = dict()
            feature_collectors = []
            for feature, graph_mode in features:
                if feature == AvailableWritingFeatures.PACING:
                    current_feature = PaceFeature(graph_mode)
                elif feature == AvailableWritingFeatures.MOOD:
                    current_feature = MoodFeature(graph_mode)
                elif feature == AvailableWritingFeatures.EMOTIONAL_INTENSITY:
                    current_feature = EmotionalIntensityFeature(graph_mode)
                elif feature == AvailableWritingFeatures.MYSTERY_LEVEL:
                    current_feature = MysteryLevelFeature(graph_mode)
                elif feature == AvailableWritingFeatures.DESCRIPTIVE_DETAIL_LEVEL:
                    current_feature = DescriptiveDetailLevelFeature(graph_mode)
                elif feature == AvailableWritingFeatures.HUMOR_LEVEL:
                    current_feature = HumorLevelFeature(graph_mode)
                elif feature == AvailableWritingFeatures.ROMANCE_LEVEL:
                    current_feature = RomanceLevelFeature(graph_mode)
                elif feature == AvailableWritingFeatures.LEVEL_OF_SUSPENSE:
                    current_feature = LevelOfSuspenseFeature(graph_mode)
                else:
                    raise ValueError(f"Feature {feature} is not supported.")

                logger.info(
                    f"Adding feature: [{current_feature.pydantic_feature_label}] to the dynamic model"
                )

                selected_features[current_feature.pydantic_feature_label] = (
                    current_feature.pydantic_feature_type,
                    Field(
                        ...,
                        description=current_feature.pydantic_docstring,
                    ),
                )

                feature_collectors.append(current_feature)

            DynamicFeatureModel = create_model(
                "DynamicFeatureModel",
                __doc__="Features contained in the creative writing text",
                **selected_features,
            )

            return feature_collectors, DynamicFeatureModel

        except Exception as e:
            logger.error(f"Error creating dynamic model: {e}")
            logger.debug(f"Error details:", exc_info=True)
            raise FeatureExtractorError("Error creating dynamic model") from e
