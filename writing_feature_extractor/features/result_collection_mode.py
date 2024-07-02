from enum import Enum


class ResultCollectionMode(str, Enum):
    """Mode for how to collect result for an extracted writing feature."""

    NUMBER_REPRESENTATION = "number representation"
    FIELD_NAME = "field name"
