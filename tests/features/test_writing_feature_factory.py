import pytest
from enum import Enum
from typing import Type
from langchain_core.pydantic_v1 import BaseModel

from writing_feature_extractor.features.writing_feature_factory import (
    WritingFeatureFactory,
)
from writing_feature_extractor.features.feature_config_data import FeatureConfigData
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.features.generic_feature import GenericFeature
from writing_feature_extractor.features.pace_feature import PaceFeature
from writing_feature_extractor.features.mood_feature import MoodFeature
from writing_feature_extractor.features.emotional_intensity_feature import (
    EmotionalIntensityFeature,
)
from writing_feature_extractor.features.level_of_suspense import LevelOfSuspenseFeature


def test_get_dynamic_model_with_predefined_features():
    features = [
        FeatureConfigData(AvailableWritingFeatures.PACING, None, None),
        FeatureConfigData(AvailableWritingFeatures.MOOD, None, None),
        FeatureConfigData(AvailableWritingFeatures.EMOTIONAL_INTENSITY, None, None),
        FeatureConfigData(AvailableWritingFeatures.LEVEL_OF_SUSPENSE, None, None),
    ]

    feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
        features
    )

    assert len(feature_collectors) == 4
    assert isinstance(feature_collectors[0], PaceFeature)
    assert isinstance(feature_collectors[1], MoodFeature)
    assert isinstance(feature_collectors[2], EmotionalIntensityFeature)
    assert isinstance(feature_collectors[3], LevelOfSuspenseFeature)
    assert issubclass(DynamicFeatureModel, BaseModel)
    assert set(DynamicFeatureModel.__fields__.keys()) == {
        "pace",
        "mood",
        "emotional_intensity",
        "level_of_suspense",
    }


def test_get_dynamic_model_with_custom_feature():
    custom_levels = ["low", "medium", "high"]
    custom_colors = {"0": "#FFFFFF", "1": "#AAAAAA", "2": "#555555"}

    features = [
        FeatureConfigData(
            "Custom Feature",
            custom_levels,
            custom_colors,
            ResultCollectionMode.NUMBER_REPRESENTATION,
        )
    ]

    feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
        features
    )

    assert len(feature_collectors) == 1
    assert isinstance(feature_collectors[0], GenericFeature)
    assert issubclass(DynamicFeatureModel, BaseModel)
    assert set(DynamicFeatureModel.__fields__.keys()) == {"custom_feature"}


def test_create_generic_feature():
    feature_config = FeatureConfigData(
        "Test Feature",
        ["low", "medium", "high"],
        {"0": "#FFFFFF", "1": "#AAAAAA", "2": "#555555"},
        ResultCollectionMode.NUMBER_REPRESENTATION,
    )

    generic_feature = WritingFeatureFactory.create_generic_feature(feature_config)

    assert isinstance(generic_feature, GenericFeature)
    assert generic_feature.name == "Test Feature"
    assert issubclass(generic_feature.pydantic_feature_type, Enum)
    assert set(generic_feature.pydantic_feature_type.__members__.keys()) == {
        "LOW",
        "MEDIUM",
        "HIGH",
    }
    assert generic_feature.graph_colors == {
        "0": "#FFFFFF",
        "1": "#AAAAAA",
        "2": "#555555",
    }
    assert (
        generic_feature.result_collection_mode
        == ResultCollectionMode.NUMBER_REPRESENTATION
    )


def test_create_dynamic_enum():
    enum_name = "TestEnum"
    values = ["low", "medium", "high"]

    DynamicEnum = WritingFeatureFactory.create_dynamic_enum(enum_name, values)

    assert issubclass(DynamicEnum, Enum)
    assert set(DynamicEnum.__members__.keys()) == {"LOW", "MEDIUM", "HIGH"}
    assert DynamicEnum.LOW.value == "low"
    assert DynamicEnum.MEDIUM.value == "medium"
    assert DynamicEnum.HIGH.value == "high"


def test_get_dynamic_model_with_mixed_features():
    features = [
        FeatureConfigData(AvailableWritingFeatures.PACING, None, None),
        FeatureConfigData(
            "Custom Feature",
            ["low", "medium", "high"],
            {"0": "#FFFFFF", "1": "#AAAAAA", "2": "#555555"},
        ),
    ]

    feature_collectors, DynamicFeatureModel = WritingFeatureFactory.get_dynamic_model(
        features
    )

    assert len(feature_collectors) == 2
    assert isinstance(feature_collectors[0], PaceFeature)
    assert isinstance(feature_collectors[1], GenericFeature)
    assert issubclass(DynamicFeatureModel, BaseModel)
    assert set(DynamicFeatureModel.__fields__.keys()) == {"pace", "custom_feature"}


def test_get_dynamic_model_error_handling():
    with pytest.raises(
        Exception
    ):  # You might want to use a more specific exception here
        WritingFeatureFactory.get_dynamic_model([])


# Add more tests as needed to cover edge cases and error scenarios
