from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.logger_config import logger


def bar_and_color_features(
    feature_collectors: list[WritingFeature],
) -> Tuple[Optional[WritingFeature], Optional[WritingFeature]]:
    """Get the feature collectors that have been marked as 'bar' and 'color'"""
    logger.info(f"Collectors: {[f.__class__.__name__ for f in feature_collectors]}")

    bar_feature = None
    color_feature = None
    for collector in feature_collectors:
        if collector.graph_mode == GraphMode.BAR:
            bar_feature = collector
        elif collector.graph_mode == GraphMode.COLOR:
            color_feature = collector

    if bar_feature is None:
        logger.error("No feature collector found with graph type BAR")
    if color_feature is None:
        logger.error("No feature collector found with graph type COLOR")

    return bar_feature, color_feature


def get_graph(
    feature_collectors: list[WritingFeature],
    text_units: list[str],
):
    """Create and display a graph based on data extracted from the text"""
    logger.debug(f"Matplotlib backend: {plt.get_backend()}")

    bar_feature, color_feature = bar_and_color_features(feature_collectors)

    if bar_feature is None or color_feature is None:
        logger.error("Cannot create graph: missing required features")
        return

    logger.info(f"Bar feature: {bar_feature.__class__.__name__}")
    logger.info(f"Color feature: {color_feature.__class__.__name__}")
    colors = color_feature.get_graph_colors()
    logger.debug(f"Color mapping: {colors}")

    # Create the dataframe
    data = dict()
    data["Unit"] = list(range(1, len(text_units) + 1))
    data["Text"] = text_units

    for collector in feature_collectors:
        data[collector.get_y_level_label()] = collector.results
    df = pd.DataFrame(data)
    logger.debug(f"Dataframe:\n {df}")

    # Check if the dataframe is empty or if all values are 0
    if df.empty or df[bar_feature.get_y_level_label()].sum() == 0:
        logger.error("No data to plot. The dataframe is empty or all values are 0.")
        return

    # Create the full custom plot
    fig, ax = plt.subplots(figsize=(15, 8))

    try:
        # Adjust widths of bars to be proportional to the number of words in the text unit
        df["Length"] = df["Text"].apply(lambda x: len(x.split()))
        logger.debug(f"Text lengths: {df['Length'].tolist()}")

        max_width = 0.8
        min_width = 0.2
        if df["Length"].max() == df["Length"].min():
            df["Width"] = [max_width] * len(df)
        else:
            df["Width"] = (
                (df["Length"] - df["Length"].min())
                / (df["Length"].max() - df["Length"].min())
            ) * (max_width - min_width) + min_width

        logger.debug(f"Bar widths: {df['Width'].tolist()}")

        # Calculate positions correctly
        positions = np.cumsum(df["Width"].values) - df["Width"].values
        center_positions = positions + df["Width"].values / 2

        logger.debug(f"Bar positions: {positions.tolist()}")
        logger.debug(f"Center positions: {center_positions.tolist()}")

        bar_heights = df[bar_feature.get_y_level_label()]
        logger.debug(f"Bar heights: {bar_heights.tolist()}")

        # Update color mapping
        color_values = [
            colors.get(str(feature).split(".")[-1].lower(), "#1f77b4")
            for feature in df[color_feature.get_y_level_label()]
        ]
        logger.debug(f"Mapped colors: {color_values}")

        bars = ax.bar(
            positions,
            bar_heights,
            width=df["Width"].values,
            color=color_values,
            edgecolor="black",
            align="edge",
        )
        logger.debug("Full custom bar plot created successfully")

        ax.set_xlabel("Text Unit", fontsize=12)
        ax.set_ylabel(bar_feature.get_y_level_label(), fontsize=12)
        title = f"{bar_feature.get_y_level_label()}. {color_feature.get_y_level_label()} is indicated by color."
        ax.set_title(title, fontsize=14)

        # Adjust x-axis ticks and labels
        num_ticks = 10  # Adjust this number to control how many ticks are shown
        tick_indices = np.linspace(0, len(positions) - 1, num_ticks, dtype=int)
        ax.set_xticks(center_positions[tick_indices])
        ax.set_xticklabels(df["Unit"][tick_indices], rotation=45, ha="right")

        # Set y-axis limits
        ax.set_ylim(0, max(bar_heights) * 1.1)  # Add 10% padding on top

        # Add a color legend
        unique_colors = sorted(set(df[color_feature.get_y_level_label()]))
        legend_elements = [
            plt.Rectangle(
                (0, 0),
                1,
                1,
                facecolor=colors.get(str(c).split(".")[-1].lower(), "#1f77b4"),
                edgecolor="black",
            )
            for c in unique_colors
        ]
        ax.legend(
            legend_elements,
            [str(c).split(".")[-1] for c in unique_colors],
            title=color_feature.get_y_level_label(),
            loc="upper right",
        )

        plt.tight_layout()

        plt.savefig("final_plot_proportional.png", dpi=300)
        logger.debug(
            "Final plot with proportional widths saved as final_plot_proportional.png"
        )
    except Exception as e:
        logger.error(f"Error creating or saving final plot: {e}")
        import traceback

        logger.debug(f"Error traceback: {traceback.format_exc()}")

    logger.debug(f"Graph creation completed with {len(df)} data points.")
