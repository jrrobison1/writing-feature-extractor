import yaml

from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.graph_mode import GraphMode


def load_feature_config(config_file: str):
    """Load feature configuration from a YAML file."""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    features = []
    for feature in config["features"]:
        feature_name = getattr(AvailableWritingFeatures, feature["name"])
        graph_mode = getattr(GraphMode, feature["graph_mode"])
        features.append((feature_name, graph_mode))

    return features
