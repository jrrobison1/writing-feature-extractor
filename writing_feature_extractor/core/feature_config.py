import yaml

from writing_feature_extractor.core.custom_exceptions import ConfigurationError
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)


def load_feature_config(config_file: str):
    """Load feature configuration from a YAML file."""
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        features = []
        for feature in config["features"]:
            feature_name = getattr(AvailableWritingFeatures, feature["name"])
            graph_mode = getattr(GraphMode, feature["graph_mode"])
            features.append((feature_name, graph_mode))

        return features
    except Exception as e:
        logger.error(f"Error loading feature configuration from {config_file}: {e}")
        logger.debug("Error details:", exc_info=True)
        raise ConfigurationError(
            "A problem occurred when loading the feature configuration from file {config_file}."
        ) from e
