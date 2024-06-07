from enum import Enum
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field

from writing_feature_extractor.features.mystery_level_feature import MysteryLevelFeature
from writing_feature_extractor.features.mood_feature import MoodFeature


class EmotionalIntensity(str, Enum):
    """Strength or intensity of emotions expressed in the text. Can be 'very low', 'low', 'medium low', 'medium', 'medium high', 'high', or 'very high'."""

    VERY_LOW = "very low"
    LOW = "low"
    MEDIUM_LOW = "medium low"
    MEDIUM = "medium"
    MEDIUM_HIGH = "medium high"
    HIGH = "high"
    VERY_HIGH = "very high"


class LevelOfSuspense(str, Enum):
    """Level of suspense in the text. Can be 'low', 'medium', or 'high'."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Genre(str, Enum):
    MYSTERY = "mystery"
    THRILLER = "thriller"
    HORROR = "horror"
    HISTORICAL = "historical"
    ROMANCE = "romance"
    WESTERN = "western"
    BILDUNGSROMAN = "bildungsroman"
    SCIENCE_FICTION = "science fiction"
    FANTASY = "fantasy"
    DYSTOPIAN = "dystopian"
    MAGICAL_REALISM = "magical realism"
    REALIST_LITERATURE = "realist literature"
    OTHER = "other"
    NONE = "none"


class Sense(str, Enum):
    SIGHT = "sight"
    SOUND = "sound"
    SMELL = "smell"
    TASTE = "taste"
    TOUCH = "touch"
    NONE = "none"
    OTHER = "other"
    UNKNOWN = "unknown"


# structured objects (Pydantic)
class Features(BaseModel):
    """Features contained in the creative writing text"""

    # tone: str = Field(description="Tone of the text")
    # pace: Pace = Field(
    #     description="Pace/speed of the narrative. Can be 'very slow', 'slow', 'medium slow', 'medium', 'medium fast', 'fast', or 'very fast'."
    # )
    mood: MoodFeature.Mood = Field(
        ...,
        description="Mood of the text. The mood MUST be one of these selections. If the mood is not listed, choose the closest semantic match.",
    )
    # emotional_intensity: EmotionalIntensity = Field(
    #     description="Strength or intensity of emotions expressed in the text. Can be 'very low', 'low', 'medium low', 'medium', 'medium high', 'high', or 'very high'."
    # )
    mystery_level: MysteryLevelFeature.MysteryLevel = Field(
        ...,
        description="Level of mystery in the text. Can be 'low', 'medium', 'high', or 'none'.",
    )

    # level_of_suspense: LevelOfSuspense = Field(
    #     """Level of suspense in the text. Can be 'low', 'medium', or 'high'."""
    # )
    # mood: Union[Mood, Tuple[Mood, ...]] = Field(
    #     description="Mood of the text. The mood MUST be one or two of these selections. If the mood is not listed, choose the closest semantic match."
    # )

    # genre: Genre = Field(description="Genre of the text")
    # pov: str = Field(
    #     description="[first-person, second-person, third-person limited, third-person omniscient]"
    # )
    # major_plot_points: str = Field(description="List of major plot points")
    # narrative_arc: str = Field(
    #     description="[exposition, rising action, climax, falling action, resolution]"
    # )
    # setting_place: str = Field(description="[urban, rural, fictional, real, etc.]")
    # themes: str = Field(
    #     description="List of main themes, e.g., love, loss, identity, etc."
    # )
    # sentence_structure: str = Field(
    #     description="[simple, compound, complex, varied, etc.]"
    # )
    # use_of_senses: List[Sense] = Field(description="Senses invoked by the text")
    # style: str = Field(
    #     description="[minimalist, elaborate, poetic, journalistic, etc.]"
    # )
    # setting_time: str = Field(
    #     description="[contemporary, historical, futuristic, etc.]"
    # )
    # conflict: str = Field(description="Internal, external, central problem, etc.")
    # narrator_reliability: str = Field(description="Reliable, Unreliable, Biased, etc.")
    # dialogue: str = Field(description="naturarlistic, stilted, sparse, abundant, etc.")
    # target_audience: str = Field(description="age group, gender, niche, etc.")
    # resolution_type: str = Field(
    #     description="cliffhanger, denouement, open-ended, etc."
    # )
    # number_of_similes_metaphors: int = Field(
    #     description="Number of similes and metaphors"
    # )


# Characters - Protagonist: [name, age, gender, occupation, etc.]
# Characters - Antagonist: [name, age, gender, occupation, etc.]
# Characters - Supporting: [list of names, roles]
# Plot - Conflict: [person vs. person, person vs. self, person vs. society, person vs. nature, etc.]
# Symbolism: [list of symbols and their meanings]
# Motifs: [list of recurring elements, e.g., colors, objects, phrases]
# Language - Figurative Devices: [metaphors, similes, personification, etc.]
# Language - Dialogue: [present, absent, dialect, slang, etc.]
# Foreshadowing: [present, absent, subtle, obvious]
# Flashbacks/Flash-forwards: [present, absent, frequency]
# Allusions: [historical, literary, cultural, biblical, etc.]
# Intertextuality: [references to other texts, authors, or works]
# Target Audience: [age group, gender, niche, etc.]
# Author's Purpose: [to entertain, to inform, to persuade, to express, etc.]
