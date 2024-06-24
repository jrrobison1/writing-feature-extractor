import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from writing_feature_extractor.logger_config import logger


def generate_graph_from_csv(filename: str, bar_feature: str, color_feature: str):
    """
    Generate a graph from the saved CSV file.

    :param filename: Name of the CSV file to read results from
    :param bar_feature: Name of the feature to use for bar heights
    :param color_feature: Name of the feature to use for bar colors
    """
    try:
        # Read the CSV file
        df = pd.read_csv(filename)

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

        # Get unique values for color mapping
        unique_colors = sorted(df[color_feature].unique())
        color_map = plt.colormaps["Set1"](np.linspace(0, 1, len(unique_colors)))
        color_dict = dict(zip(unique_colors, color_map))

        # Create the bar plot
        bars = ax.bar(
            positions,
            df[bar_feature],
            width=df["Width"].values,
            color=[color_dict[val] for val in df[color_feature]],
            edgecolor="black",
            align="edge",
        )

        # Set labels and title
        ax.set_xlabel("Text Unit", fontsize=12)
        ax.set_ylabel(bar_feature, fontsize=12)
        title = f"{bar_feature}. {color_feature} is indicated by color."
        ax.set_title(title, fontsize=14)

        # Adjust x-axis ticks and labels
        num_ticks = 10
        tick_indices = np.linspace(0, len(positions) - 1, num_ticks, dtype=int)
        ax.set_xticks(center_positions[tick_indices])
        ax.set_xticklabels(df["Unit"][tick_indices], rotation=45, ha="right")

        # Set y-axis limits
        ax.set_ylim(0, df[bar_feature].max() * 1.1)

        # Add a color legend
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor=color_dict[c], edgecolor="black")
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
