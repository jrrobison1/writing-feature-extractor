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


def load_feature_config(config_file: str) -> list[FeatureConfigData]:
    """Load feature configuration from a YAML file."""
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        if not config or "features" not in config:
            raise ConfigurationError(
                "Invalid configuration: 'features' key is missing."
            )

        features = []
        for feature in config["features"]:
            if "name" not in feature or "result_collection_mode" not in feature:
                raise ConfigurationError(
                    "Invalid feature configuration: 'name' or 'result_collection_mode' is missing."
                )

            levels = []
            color_map = {}

            if hasattr(AvailableWritingFeatures, feature["name"]):
                feature_name = getattr(AvailableWritingFeatures, feature["name"])
            else:
                feature_name = feature["name"]
                if "customizations" not in feature:
                    raise ConfigurationError(
                        f"Custom feature '{feature_name}' is missing 'customizations'."
                    )
                feature_customizations = feature["customizations"]
                levels = feature_customizations.get("levels", [])
                color_map = feature_customizations.get("color_map", {})

            try:
                result_collection_mode = getattr(
                    ResultCollectionMode, feature["result_collection_mode"]
                )
            except AttributeError:
                raise ConfigurationError(
                    f"Invalid result_collection_mode: {feature['result_collection_mode']}"
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
