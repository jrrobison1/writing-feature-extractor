import yaml
from writing_feature_extractor.core.custom_exceptions import ConfigurationError
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.feature_config_data import FeatureConfigData
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)

# Constants
FEATURES_KEY = "features"
NAME_KEY = "name"
RESULT_COLLECTION_MODE_KEY = "result_collection_mode"
CUSTOMIZATIONS_KEY = "customizations"
LEVELS_KEY = "levels"
COLOR_MAP_KEY = "color_map"


def load_feature_config(config_file: str) -> list[FeatureConfigData]:
    """
    Load feature configuration from a YAML file.

    This function reads a YAML configuration file and parses it to create a list of
    FeatureConfigData objects. Each object represents a feature with its associated
    settings such as name, levels, color map, and result collection mode.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        list[FeatureConfigData]: A list of FeatureConfigData objects representing
        the configured features.

    Raises:
        ConfigurationError: If the configuration file is invalid, missing, or contains
        errors. This includes cases where required keys are missing, feature names are
        invalid, or the YAML syntax is incorrect.

    Example:
        >>> features = load_feature_config("config.yaml")
        >>> print(features[0].name)
        'SentenceComplexity'
    """
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        if not config or FEATURES_KEY not in config:
            raise ConfigurationError(
                f"Invalid configuration: '{FEATURES_KEY}' key is missing."
            )

        features = []
        for feature in config[FEATURES_KEY]:
            if NAME_KEY not in feature or RESULT_COLLECTION_MODE_KEY not in feature:
                raise ConfigurationError(
                    f"Invalid feature configuration: '{NAME_KEY}' or '{RESULT_COLLECTION_MODE_KEY}' is missing."
                )

            levels = []
            color_map = {}

            if hasattr(AvailableWritingFeatures, feature[NAME_KEY]):
                feature_name = getattr(AvailableWritingFeatures, feature[NAME_KEY])
            else:
                feature_name = feature[NAME_KEY]
                if CUSTOMIZATIONS_KEY not in feature:
                    raise ConfigurationError(
                        f"Custom feature '{feature_name}' is missing '{CUSTOMIZATIONS_KEY}'."
                    )
                feature_customizations = feature[CUSTOMIZATIONS_KEY]
                levels = feature_customizations.get(LEVELS_KEY, [])
                color_map = feature_customizations.get(COLOR_MAP_KEY, {})

            try:
                result_collection_mode = getattr(
                    ResultCollectionMode, feature[RESULT_COLLECTION_MODE_KEY]
                )
            except AttributeError:
                raise ConfigurationError(
                    f"Invalid {RESULT_COLLECTION_MODE_KEY}: {feature[RESULT_COLLECTION_MODE_KEY]}"
                )

            features.append(
                FeatureConfigData(
                    feature_name, levels, color_map, result_collection_mode
                )
            )

        return features

    except FileNotFoundError:
        raise ConfigurationError(f"Configuration file not found: {config_file}")
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing YAML in {config_file}: {str(e)}")
    except Exception as e:
        raise ConfigurationError(
            f"Error loading feature configuration from {config_file}: {str(e)}"
        )
