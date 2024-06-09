from enum import Enum


class WritingFeatureGraphMode(str, Enum):
    """Graph mode for how to graph an extracted writing feature."""

    BAR = "bar"
    COLOR = "color"
