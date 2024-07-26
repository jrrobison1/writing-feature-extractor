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
) -> None:
    """
    Save the results of all features and text metrics to a CSV file.

    Args:
        feature_collectors (List[WritingFeature]): List of WritingFeature objects containing feature results.
        text_metrics (list[dict[str, Any]]): List of dictionaries containing text metrics for each text unit.
        text_units (List[str]): List of text units (e.g., sentences, paragraphs) analyzed.
        filename (str, optional): Name of the output CSV file. Defaults to DEFAULT_CSV_FILE.

    Raises:
        FileOperationError: If there's an error while saving the results to the CSV file.

    The CSV file will contain the following columns:
    - Unit: Index of the text unit
    - Length: Word count of the text unit
    - Feature columns: One column for each feature in feature_collectors
    - Metric columns: One column for each metric in text_metrics
    - ColorMaps: JSON-encoded color maps for each feature

    Note:
        This function assumes that the length of text_units matches the number of results in each feature collector
        and the number of entries in text_metrics.
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
