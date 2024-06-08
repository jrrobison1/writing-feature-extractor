import logging
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
from features.mood_feature import MoodFeature

from features.emotional_intensity_feature import (
    EmotionalIntensityFeature,
)
from features.writing_feature import WritingFeature

logger = logging.getLogger(__name__)


# Define mood colors (assuming this dictionary exists in your code)
# mood to rgb mapping
colors = MoodFeature.get_graph_colors()


def get_graph(
    feature_collectors: list[WritingFeature],
    # pace_numbers,
    paragraphs: list[str],
    # moods,
    # emotional_intensities,
    # mystery_levels,
):
    print("Made it inside get_graph...")
    data = dict()
    data["Paragraph"] = list(range(1, len(paragraphs) + 1))
    data["Text"] = paragraphs

    # print("Adding collector data to dict...")
    for collector in feature_collectors:
        data[collector.get_y_level_label()] = collector.results
    # print(f"Data keys: {data.keys()}")
    # print(f"Pace: {data['Pace']}")
    # print(f"Mood: {data['Mood']}")
    # data["Pacing"] = pace_numbers
    # data["Mood"] = moods
    # data["Emotional Intensity"] = emotional_intensities
    # data["Mystery Level"] = mystery_levels

    print("Creating DataFrame...")
    df = pd.DataFrame(data)
    print(f"DataFrame created: {df}")
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
        df["Pace"],
        width=df["Width"],
        color=[colors[mood] for mood in df["Mood"]],
        edgecolor="black",
        align="edge",
        hatch="//",
    )

    ax.set_xlabel("Paragraph")
    ax.set_ylabel("Pace")
    ax.set_title("Pace. Mood is indicated by color.")
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
