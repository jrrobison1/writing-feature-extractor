from enum import Enum, auto


class AvailableWritingFeatures(str, Enum):
    """Available writing features that can be extracted from a text."""

    PACING = auto()
    EMOTIONAL_INTENSITY = auto()
    MOOD = auto()
    LEVEL_OF_SUSPENSE = auto()
