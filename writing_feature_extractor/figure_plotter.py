import logging
from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

from features.writing_feature import WritingFeature
from features.writing_feature_graph_mode import (
    WritingFeatureGraphMode,
)

logger = logging.getLogger(__name__)


def bar_and_color_features(
    feature_collectors: list[WritingFeature],
) -> Tuple[WritingFeature, WritingFeature]:
    """Get the feature collectors that have been marked as 'bar' and 'color'"""

    # Validate that there is exactly one feature collector with a graph type of WritingFeatureGraphMode.BAR, and exactly one with WritingFeatureGraphMode.COLOR
    bar_count = 0
    color_count = 0
    bar_feature = None
    color_feature = None
    for collector in feature_collectors:
        if collector.graph_mode == WritingFeatureGraphMode.BAR:
            bar_count += 1
            bar_feature = collector
        elif collector.graph_mode == WritingFeatureGraphMode.COLOR:
            color_count += 1
            color_feature = collector
    if bar_count != 1:
        raise ValueError(
            "There must be exactly one feature collector with a graph type of WritingFeatureGraphMode.BAR"
        )
    if color_count != 1:
        raise ValueError(
            "There must be exactly one feature collector with a graph type of WritingFeatureGraphMode.COLOR"
        )
    return bar_feature, color_feature


def get_graph(
    feature_collectors: list[WritingFeature],
    paragraphs: list[str],
):
    """Create and display a graph based on data extracted from the text"""

    bar_feature, color_feature = bar_and_color_features(feature_collectors)
    logger.info(f"Bar feature: {bar_feature}")
    logger.info(f"Color feature: {color_feature}")
    colors = color_feature.get_graph_colors()

    # Create the dataframe
    data = dict()
    data["Paragraph"] = list(range(1, len(paragraphs) + 1))
    data["Text"] = paragraphs

    for collector in feature_collectors:
        data[collector.get_y_level_label()] = collector.results
    df = pd.DataFrame(data)

    # Adjust widths of bars to be proportional to the number of words in the paragraph
    df["Length"] = df["Text"].apply(lambda x: len(x.split()))
    max_width = 0.4
    min_width = 0.1
    df["Width"] = (
        (df["Length"] - df["Length"].min()) / (df["Length"].max() - df["Length"].min())
    ) * (max_width - min_width) + min_width

    positions = [sum(df["Width"][:i]) for i in range(len(df))]
    center_positions = [pos + df["Width"][i] / 2 for i, pos in enumerate(positions)]

    _, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(
        positions,
        df[bar_feature.get_y_level_label()],
        width=df["Width"],
        color=[colors[feature] for feature in df[color_feature.get_y_level_label()]],
        edgecolor="black",
        align="edge",
        hatch="//",
    )

    ax.set_xlabel("Paragraph")
    ax.set_ylabel(bar_feature.get_y_level_label())

    title = f"{bar_feature.get_y_level_label()}. {color_feature.get_y_level_label()} is indicated by color."
    ax.set_title(title)
    ax.set_xticks(center_positions)
    ax.set_xticklabels(df["Paragraph"], ha="right")
    ax.set_yticks(bar_feature.get_graph_y_ticks())
    ax.set_yticklabels(bar_feature.get_graph_y_tick_labels())

    ax.yaxis.grid(False)

    cursor = mplcursors.cursor(bars, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        color_annotation = df.iloc[index][color_feature.get_y_level_label()]
        sel.annotation.set(
            text=f"{color_feature.get_y_level_label()}: {color_annotation}", fontsize=10
        )

    plt.show()
