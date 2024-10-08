import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from writing_feature_extractor.core.custom_exceptions import (
    FileOperationError,
    GraphError,
)
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)


def generate_graph_from_csv(
    filename: str, bar_feature: str, color_feature: str
) -> None:
    """
    Generate a bar graph from a CSV file with custom colors and y-axis labels.

    This function reads data from a CSV file, creates a bar graph where the height
    of each bar represents the 'bar_feature' value, and the color of each bar
    represents the 'color_feature' value. The graph is saved as a PNG file.

    Args:
        filename (str): Path to the input CSV file.
        bar_feature (str): Column name in the CSV to use for bar heights.
        color_feature (str): Column name in the CSV to use for bar colors.

    Raises:
        FileOperationError: If the specified file is not found or cannot be read.
        GraphError: If there's an error during graph generation.

    Notes:
        - The CSV file should contain 'Unit', 'Length', and 'ColorMaps' columns,
          in addition to the columns specified by bar_feature and color_feature.
        - The 'ColorMaps' column should contain a JSON string with color mappings.
        - The output graph will be saved as '{bar_feature}_{color_feature}_graph.png'.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)

        # Extract color maps
        color_maps = json.loads(df["ColorMaps"].iloc[0])
        color_dict = color_maps[color_feature]

        logger.debug(f"Color maps: {color_maps}")
        logger.debug(f"Color dictionary for {color_feature}: {color_dict}")

        logger.debug(f"Unique values in {color_feature}: {df[color_feature].unique()}")

        bar_colors = [
            color_dict.get(str(val).lower(), "#CCCCCC") for val in df[color_feature]
        ]
        logger.debug(f"Bar colors: {bar_colors}")

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
    except FileNotFoundError as fnfe:
        logger.error(f"File not found: {filename}, {fnfe}")
        raise FileOperationError(f"File not found: {filename}")
    except OSError as ose:
        logger.error(f"An OS Error occurred: {filename}, {ose}")
        raise FileOperationError(f"File not found: {filename}")
    except Exception as e:
        logger.error(f"Error generating graph from CSV: {e}")
        raise GraphError("Failed to generate graph from the given CSV file.") from e
