from enum import Enum
from typing import Dict, Tuple, Type, Union

from langchain_core.pydantic_v1 import BaseModel, Field, create_model

from writing_feature_extractor.core.custom_exceptions import (
    FeatureExtractorError,
    ModelError,
)
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.emotional_intensity_feature import (
    EmotionalIntensityFeature,
)
from writing_feature_extractor.features.feature_config_data import FeatureConfigData
from writing_feature_extractor.features.generic_feature import GenericFeature
from writing_feature_extractor.features.level_of_suspense import LevelOfSuspenseFeature
from writing_feature_extractor.features.mood_feature import MoodFeature
from writing_feature_extractor.features.pace_feature import PaceFeature
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)


class WritingFeatureFactory:
    """Factory class to create dynamic pydantic models based on the given
    writing features desired for feature extraction."""

    FEATURE_MAP: Dict[AvailableWritingFeatures, Type[WritingFeature]] = {
        AvailableWritingFeatures.PACING: PaceFeature,
        AvailableWritingFeatures.MOOD: MoodFeature,
        AvailableWritingFeatures.EMOTIONAL_INTENSITY: EmotionalIntensityFeature,
        AvailableWritingFeatures.LEVEL_OF_SUSPENSE: LevelOfSuspenseFeature,
    }

    @staticmethod
    def get_dynamic_model(
        features: list[FeatureConfigData],
    ) -> Tuple[type[BaseModel], list[WritingFeature]]:
        """Creates a dynamic pydantic model based on the given writing features"""
        if features is None or not features:
            raise ModelError("No features provided for dynamic model creation")

        try:
            selected_features = dict()
            feature_collectors = []
            for feature_config in features:

                feature_class = WritingFeatureFactory.FEATURE_MAP.get(
                    feature_config.name
                )
                if feature_class is None:
                    current_feature = WritingFeatureFactory.create_generic_feature(
                        feature_config
                    )
                else:
                    current_feature = feature_class(
                        feature_config.result_collection_mode
                    )

                logger.info(
                    f"Adding feature: [{current_feature.pydantic_feature_label}] to the dynamic model"
                )

                # For some reason, using Union with string with the feature type actually does a
                # better job for feature extraction than just using the feature type. The extracted
                # feature still has the type of the enum.
                selected_features[current_feature.pydantic_feature_label] = (
                    Union[current_feature.pydantic_feature_type, str],
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
            raise FeatureExtractorError("Error creating dynamic model") from e

    @staticmethod
    def create_generic_feature(
        feature_config: FeatureConfigData,
    ) -> GenericFeature:
        """Creates a generic writing feature based on the given feature name"""

        enum_name = (
            feature_config.name.lower().replace("_", " ").title().replace(" ", "")
        )

        logger.debug(
            f"Creating dynamic enum for feature: [{feature_config.name}] with enum name: [{enum_name}] and levels: [{feature_config.levels}]"
        )
        CustomEnum = WritingFeatureFactory.create_dynamic_enum(
            enum_name, feature_config.levels
        )

        logger.info(
            f"Creating generic feature: [{feature_config.name}] with levels: [{feature_config.levels}], colors: [{feature_config.colors}] and graph mode: [{feature_config.result_collection_mode}]"
        )
        return GenericFeature(
            feature_config.name,
            CustomEnum,
            feature_config.colors,
            feature_config.result_collection_mode,
        )

    @staticmethod
    def create_dynamic_enum(enum_name, values) -> Enum:
        return Enum(
            enum_name,
            {value.upper(): value for value in values},
            type=str,
            module=__name__,
        )
