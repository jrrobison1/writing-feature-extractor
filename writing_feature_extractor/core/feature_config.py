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


def load_feature_config(
    config_file: str,
) -> list[FeatureConfigData]:
    """Load feature configuration from a YAML file."""
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        features = []
        levels = []
        color_map = {}
        for feature in config["features"]:
            if hasattr(AvailableWritingFeatures, feature["name"]) is True:
                feature_name = getattr(AvailableWritingFeatures, feature["name"])
            else:
                feature_name = feature["name"]
                feature_customizations = feature["customizations"]
                levels = feature_customizations["levels"]
                color_map = feature_customizations["color_map"]

            result_collection_mode = getattr(
                ResultCollectionMode, feature["result_collection_mode"]
            )

            features.append(
                FeatureConfigData(
                    feature_name, levels, color_map, result_collection_mode
                )
            )

        return features
    except Exception as e:
        logger.error(f"Error loading feature configuration from {config_file}: {e}")
        logger.debug("Error details:", exc_info=True)
        raise ConfigurationError(
            "A problem occurred when loading the feature configuration from file {config_file}."
        ) from e
