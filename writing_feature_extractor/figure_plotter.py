import logging
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from features.mood_feature import MoodFeature

from features.emotional_intensity_feature import (
    EmotionalIntensityFeature,
)

logger = logging.getLogger(__name__)


# Define mood colors (assuming this dictionary exists in your code)
# mood to rgb mapping
colors = MoodFeature.get_graph_colors()


def get_graph(
    pace_numbers,
    paragraphs,
    moods,
    emotional_intensities,
    mystery_levels,
):
    data = dict()
    data["Paragraph"] = list(range(1, len(paragraphs) + 1))
    data["Text"] = paragraphs
    data["Pacing"] = pace_numbers
    data["Mood"] = moods
    data["Emotional Intensity"] = emotional_intensities
    data["Mystery Level"] = mystery_levels

    df = pd.DataFrame(data)
    df["Length"] = df["Text"].apply(lambda x: len(x.split()))

    max_width = 0.4
    min_width = 0.1
    df["Width"] = (
        (df["Length"] - df["Length"].min()) / (df["Length"].max() - df["Length"].min())
    ) * (max_width - min_width) + min_width

    positions = [sum(df["Width"][:i]) for i in range(len(df))]
    center_positions = [pos + df["Width"][i] / 2 for i, pos in enumerate(positions)]

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(
        positions,
        df["Pacing"],
        width=df["Width"],
        color=[colors[mood] for mood in df["Mood"]],
        edgecolor="black",
        align="edge",
        hatch="//",
    )

    ax.set_xlabel("Paragraph")
    ax.set_ylabel("Pacing")
    ax.set_title("Pacing. Mood is indicated by color.")
    ax.set_xticks(center_positions)
    ax.set_xticklabels(df["Paragraph"], ha="right")
    ax.set_yticks([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticklabels(
        [
            # "none",
            "very low",
            "low",
            "medium low",
            "medium",
            "medium high",
            "high",
            "very high",
        ]
    )

    ax.yaxis.grid(False)

    cursor = mplcursors.cursor(bars, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        mood = df.iloc[index]["Mood"]
        sel.annotation.set(text=f"Mood: {mood}", fontsize=10)

    plt.show()
