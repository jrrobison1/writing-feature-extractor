import csv
import json
import traceback
from typing import List

from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.logger_config import get_logger

logger = get_logger(__name__)


def save_results_to_csv(
    feature_collectors: List[WritingFeature],
    text_units: List[str],
    filename: str = "feature_results.csv",
):
    """
    Save the results of all features to a CSV file.

    :param feature_collectors: List of feature collector objects
    :param text_units: List of text units (paragraphs or sections)
    :param filename: Name of the CSV file to save results
    """
    try:
        with open(filename, "w", newline="") as csvfile:
            fieldnames = (
                ["Unit", "Text", "Length"]
                + [fc.get_y_level_label() for fc in feature_collectors]
                + ["ColorMaps"]
            )
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i, text in enumerate(text_units, 1):
                row = {"Unit": i, "Text": text, "Length": len(text.split())}
                for fc in feature_collectors:
                    row[fc.get_y_level_label()] = (
                        fc.results[i - 1] if i <= len(fc.results) else ""
                    )

                # Add color maps
                color_maps = {
                    fc.get_y_level_label(): fc.get_graph_colors()
                    for fc in feature_collectors
                }
                row["ColorMaps"] = json.dumps(color_maps)

                writer.writerow(row)

        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving results to CSV: {e}")
        logger.debug(f"Error traceback: {traceback.format_exc()}")
