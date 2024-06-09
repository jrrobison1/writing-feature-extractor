from enum import Enum


class AvailableWritingFeatures(str, Enum):
    """Available writing features that can be extracted from a text."""

    PACING = "pacing"
    EMOTIONAL_INTENSITY = "emotional intensity"
    MYSTERY_LEVEL = "mystery level"
    MOOD = "mood"
    DESCRIPTIVE_DETAIL_LEVEL = "descriptive level detail"
    HUMOR_LEVEL = "humor level"
    ROMANCE_LEVEL = "romance level"
