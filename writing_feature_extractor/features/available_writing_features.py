from enum import Enum, auto


class AvailableWritingFeatures(str, Enum):
    """Available writing features that can be extracted from a text."""

    PACING = auto()
    EMOTIONAL_INTENSITY = auto()
    MYSTERY_LEVEL = auto()
    MOOD = auto()
    DESCRIPTIVE_DETAIL_LEVEL = auto()
    HUMOR_LEVEL = auto()
    ROMANCE_LEVEL = auto()
    LEVEL_OF_SUSPENSE = auto()
