from enum import Enum


class AethemosRating(str, Enum):
    NOT_AT_ALL = "Not at all"
    SLIGHTLY = "Slightly"
    MODERATELY = "Moderately"
    STRONGLY = "Strongly"
    VERY_STRONGLY = "Very strongly"
