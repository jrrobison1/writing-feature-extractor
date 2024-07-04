import csv
import json
from typing import Any, List

from writing_feature_extractor.core.custom_exceptions import FileOperationError
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)

DEFAULT_CSV_FILE = "feature_results.csv"


def save_results_to_csv(
    feature_collectors: List[WritingFeature],
    text_metrics: list[dict[str, Any]],
    text_units: List[str],
    filename: str = DEFAULT_CSV_FILE,
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
                ["Unit", "Length"]
                + [fc.y_level_label for fc in feature_collectors]
                + [metric for metric in text_metrics[0]]
                + ["ColorMaps"]
            )
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i, text in enumerate(text_units, 1):
                row = {"Unit": i, "Length": len(text.split())}
                for fc in feature_collectors:
                    row[fc.y_level_label] = (
                        fc.results[i - 1] if i <= len(fc.results) else ""
                    )

                for metric in text_metrics[0].keys():
                    row[metric] = text_metrics[i - 1][metric]

                # Add color maps
                color_maps = {
                    fc.y_level_label: fc.graph_colors for fc in feature_collectors
                }
                row["ColorMaps"] = json.dumps(color_maps)

                writer.writerow(row)

        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving results to CSV: {e}")
        raise FileOperationError(f"Failed to save results to {filename}.") from e
