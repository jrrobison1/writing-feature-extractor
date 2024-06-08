from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field


class MoodFeature:

    class Mood(str, Enum):
        """Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match."""

        POSITIVE = "positive"
        SAD = "sad"
        ANGRY = "angry"
        SUSPENSEFUL = "suspenseful"
        NEUTRAL = "neutral"

    def get_pydantic_feature_label(self):
        return "mood"

    def get_pydantic_feature_type(self):
        return MoodFeature.Mood

    def get_pydantic_docstring(self):
        return "Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match.."

    def get_graph_colors():
        return {
            "positive": "#FFFF00",
            "sad": "#00008B",
            "angry": "#FF0000",
            "suspenseful": "#7328AA",
            "neutral": "#D3D3D3",
        }
