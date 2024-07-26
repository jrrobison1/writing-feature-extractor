from enum import Enum, auto


class AvailableWritingFeatures(str, Enum):
    """Available writing features that can be extracted from a text."""

    PACING = auto()
    EMOTIONAL_INTENSITY = auto()
    MOOD = auto()
    LEVEL_OF_SUSPENSE = auto()
    AESTHEMOS_AMUSEMENT = auto()
    AESTHEMOS_BEAUTY = auto()
    AESTHEMOS_CURIOSITY = auto()
    AESTHEMOS_ANIMATION = auto()
    AESTHEMOS_SADNESS = auto()
    AESTHEMOS_RELAXATION = auto()
    AESTHEMOS_DISTRESSED = auto()
