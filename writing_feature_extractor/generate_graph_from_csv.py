import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from writing_feature_extractor.logger_config import logger


def generate_graph_from_csv(filename: str, bar_feature: str, color_feature: str):
    """
    Generate a graph from the saved CSV file using predefined colors and custom y-axis labels.

    :param filename: Name of the CSV file to read results from
    :param bar_feature: Name of the feature to use for bar heights
    :param color_feature: Name of the feature to use for bar colors
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)

        # Extract color maps
        color_maps = json.loads(df["ColorMaps"].iloc[0])
        color_dict = color_maps[color_feature]

        # Create the plot
        fig, ax = plt.subplots(figsize=(15, 8))

        # Calculate bar widths
        max_width = 0.8
        min_width = 0.2
        df["Width"] = (
            (df["Length"] - df["Length"].min())
            / (df["Length"].max() - df["Length"].min())
        ) * (max_width - min_width) + min_width

        # Calculate positions
        positions = np.cumsum(df["Width"].values) - df["Width"].values
        center_positions = positions + df["Width"].values / 2

        # Create the bar plot
        bars = ax.bar(
            positions,
            df[bar_feature],
            width=df["Width"].values,
            color=[
                color_dict.get(str(val).lower(), "#CCCCCC") for val in df[color_feature]
            ],
            edgecolor="black",
            align="edge",
        )

        # Set labels and title
        ax.set_xlabel("Text Unit", fontsize=12)
        ax.set_title(
            f"{bar_feature}. {color_feature} is indicated by color.", fontsize=14
        )

        # Set y-axis limits
        y_min, y_max = 0, df[bar_feature].max() * 1.1
        ax.set_ylim(y_min, y_max)

        # Remove y-axis ticks
        ax.set_yticks([])

        # Add "None" at the bottom and "Very High" at the top
        ax.text(
            -0.05,
            y_min,
            "None",
            va="bottom",
            ha="right",
            fontsize=10,
            transform=ax.get_yaxis_transform(),
        )
        ax.text(
            -0.05,
            y_max,
            "Very High",
            va="top",
            ha="right",
            fontsize=10,
            transform=ax.get_yaxis_transform(),
        )

        # Adjust x-axis ticks and labels
        num_ticks = 10
        tick_indices = np.linspace(0, len(positions) - 1, num_ticks, dtype=int)
        ax.set_xticks(center_positions[tick_indices])
        ax.set_xticklabels(df["Unit"][tick_indices], rotation=45, ha="right")

        # Set y-axis limits
        ax.set_ylim(0, df[bar_feature].max() * 1.1)

        # Add a color legend
        unique_colors = sorted(set(df[color_feature]))
        legend_elements = [
            plt.Rectangle(
                (0, 0),
                1,
                1,
                facecolor=color_dict.get(str(c).lower(), "#CCCCCC"),
                edgecolor="black",
            )
            for c in unique_colors
        ]
        ax.legend(
            legend_elements, unique_colors, title=color_feature, loc="upper right"
        )

        plt.tight_layout()
        output_filename = f"{bar_feature}_{color_feature}_graph.png"
        plt.savefig(output_filename, dpi=300)
        logger.info(f"Graph saved as {output_filename}")
    except Exception as e:
        logger.error(f"Error generating graph from CSV: {e}")
        import traceback

        logger.debug(f"Error traceback: {traceback.format_exc()}")
