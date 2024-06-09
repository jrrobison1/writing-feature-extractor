from enum import Enum


class GraphMode(str, Enum):
    """Graph mode for how to graph an extracted writing feature."""

    BAR = "bar"
    COLOR = "color"
