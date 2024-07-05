import pytest
from unittest.mock import mock_open, patch
from writing_feature_extractor.core.feature_config import load_feature_config
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.core.custom_exceptions import ConfigurationError


@pytest.fixture
def sample_yaml_content():
    return """
features:
  - name: EMOTIONAL_INTENSITY
    result_collection_mode: NUMBER_REPRESENTATION
  - name: MOOD
    result_collection_mode: FIELD_NAME
  - name: "Custom Feature"
    result_collection_mode: NUMBER_REPRESENTATION
    customizations:
      levels:
        - "none"
        - "low"
        - "medium"
        - "high"
      color_map:
        "0": "#FFFFFF"
        "1": "#FFCCCC"
        "2": "#FF9999"
        "3": "#FF6666"
"""


def test_load_feature_config_standard_features(sample_yaml_content):
    with patch("builtins.open", mock_open(read_data=sample_yaml_content)):
        features = load_feature_config("dummy_path.yaml")

        assert len(features) == 3

        assert features[0].name == AvailableWritingFeatures.EMOTIONAL_INTENSITY
        assert (
            features[0].result_collection_mode
            == ResultCollectionMode.NUMBER_REPRESENTATION
        )
        assert features[0].levels == []
        assert features[0].colors == {}

        assert features[1].name == AvailableWritingFeatures.MOOD
        assert features[1].result_collection_mode == ResultCollectionMode.FIELD_NAME
        assert features[1].levels == []
        assert features[1].colors == {}


def test_load_feature_config_custom_feature(sample_yaml_content):
    with patch("builtins.open", mock_open(read_data=sample_yaml_content)):
        features = load_feature_config("dummy_path.yaml")

        custom_feature = features[2]
        assert custom_feature.name == "Custom Feature"
        assert (
            custom_feature.result_collection_mode
            == ResultCollectionMode.NUMBER_REPRESENTATION
        )
        assert custom_feature.levels == ["none", "low", "medium", "high"]
        assert custom_feature.colors == {
            "0": "#FFFFFF",
            "1": "#FFCCCC",
            "2": "#FF9999",
            "3": "#FF6666",
        }


def test_load_feature_config_file_not_found():
    with pytest.raises(ConfigurationError, match="Configuration file not found"):
        load_feature_config("non_existent_file.yaml")


def test_load_feature_config_invalid_yaml():
    invalid_yaml = "invalid: yaml: content:"
    with patch("builtins.open", mock_open(read_data=invalid_yaml)):
        with pytest.raises(ConfigurationError, match="Error parsing YAML"):
            load_feature_config("invalid_yaml.yaml")


def test_load_feature_config_missing_required_fields():
    incomplete_yaml = """
features:
  - name: EMOTIONAL_INTENSITY
    # Missing result_collection_mode
"""
    with patch("builtins.open", mock_open(read_data=incomplete_yaml)):
        with pytest.raises(
            ConfigurationError, match="'name' or 'result_collection_mode' is missing"
        ):
            load_feature_config("incomplete_yaml.yaml")


def test_load_feature_config_invalid_feature_name():
    invalid_feature_yaml = """
features:
  - name: INVALID_FEATURE
    result_collection_mode: NUMBER_REPRESENTATION
"""
    with patch("builtins.open", mock_open(read_data=invalid_feature_yaml)):
        with pytest.raises(
            ConfigurationError, match="Custom feature .* is missing 'customizations'"
        ):
            load_feature_config("invalid_feature.yaml")


def test_load_feature_config_invalid_result_collection_mode():
    invalid_mode_yaml = """
features:
  - name: EMOTIONAL_INTENSITY
    result_collection_mode: INVALID_MODE
"""
    with patch("builtins.open", mock_open(read_data=invalid_mode_yaml)):
        with pytest.raises(ConfigurationError, match="Invalid result_collection_mode"):
            load_feature_config("invalid_mode.yaml")


def test_load_feature_config_empty_file():
    with patch("builtins.open", mock_open(read_data="")):
        with pytest.raises(
            ConfigurationError, match="Invalid configuration: 'features' key is missing"
        ):
            load_feature_config("empty_file.yaml")


def test_load_feature_config_no_features():
    no_features_yaml = """
features: []
"""
    with patch("builtins.open", mock_open(read_data=no_features_yaml)):
        features = load_feature_config("no_features.yaml")
        assert len(features) == 0
