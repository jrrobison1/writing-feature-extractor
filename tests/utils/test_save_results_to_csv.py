import pytest
import csv
import json
from unittest.mock import mock_open, patch
from writing_feature_extractor.utils.save_results_to_csv import save_results_to_csv
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.core.custom_exceptions import FileOperationError


class MockWritingFeature(WritingFeature):
    def __init__(self, label, results):
        super().__init__()
        self._label = label
        self.results = results

    @property
    def y_level_label(self):
        return self._label

    @property
    def graph_colors(self):
        return {"0": "#FFFFFF", "1": "#000000"}

    # Implement other abstract methods with dummy returns
    @property
    def pydantic_feature_label(self):
        return "mock_feature"

    @property
    def pydantic_feature_type(self):
        return str

    @property
    def pydantic_docstring(self):
        return "Mock feature for testing"


def test_save_results_to_csv_success():
    feature_collectors = [
        MockWritingFeature("Feature1", [1, 2, 3]),
        MockWritingFeature("Feature2", [4, 5, 6]),
    ]
    text_metrics = [
        {"metric1": 10, "metric2": 20},
        {"metric1": 30, "metric2": 40},
        {"metric1": 50, "metric2": 60},
    ]
    text_units = ["Unit1", "Unit2", "Unit3"]

    m = mock_open()
    with patch("builtins.open", m):
        save_results_to_csv(feature_collectors, text_metrics, text_units, "test.csv")

    m.assert_called_once_with("test.csv", "w", newline="")
    handle = m()

    # Check if write calls were made
    assert handle.write.call_count > 0


def test_save_results_to_csv_file_operation_error():
    feature_collectors = [MockWritingFeature("Feature1", [1, 2, 3])]
    text_metrics = [{"metric1": 10}]
    text_units = ["Unit1"]

    with patch("builtins.open", side_effect=IOError("Mocked IOError")):
        with pytest.raises(FileOperationError):
            save_results_to_csv(
                feature_collectors, text_metrics, text_units, "test.csv"
            )


def test_save_results_to_csv_content():
    feature_collectors = [
        MockWritingFeature("Feature1", [1, 2]),
        MockWritingFeature("Feature2", [3, 4]),
    ]
    text_metrics = [{"metric1": 10, "metric2": 20}, {"metric1": 30, "metric2": 40}]
    text_units = ["Unit1", "Unit2"]

    m = mock_open()
    with patch("builtins.open", m):
        save_results_to_csv(feature_collectors, text_metrics, text_units, "test.csv")

    written_content = "".join(call.args[0] for call in m().write.call_args_list)
    csv_content = list(csv.reader(written_content.splitlines()))

    expected_header = [
        "Unit",
        "Length",
        "Feature1",
        "Feature2",
        "metric1",
        "metric2",
        "ColorMaps",
    ]
    assert csv_content[0] == expected_header

    # Check content of the first data row
    assert csv_content[1][0] == "1"  # Unit
    assert csv_content[1][1] == "1"  # Length (number of words in "Unit1")
    assert csv_content[1][2] == "1"  # Feature1 result
    assert csv_content[1][3] == "3"  # Feature2 result
    assert csv_content[1][4] == "10"  # metric1
    assert csv_content[1][5] == "20"  # metric2

    # Check ColorMaps JSON
    color_maps = json.loads(csv_content[1][6])
    assert color_maps == {
        "Feature1": {"0": "#FFFFFF", "1": "#000000"},
        "Feature2": {"0": "#FFFFFF", "1": "#000000"},
    }


def test_save_results_to_csv_mismatched_lengths():
    feature_collectors = [
        MockWritingFeature("Feature1", [1, 2, 3]),
        MockWritingFeature("Feature2", [4, 5]),  # One less result
    ]
    text_metrics = [
        {"metric1": 10, "metric2": 20},
        {"metric1": 30, "metric2": 40},
        {"metric1": 50, "metric2": 60},
    ]
    text_units = ["Unit1", "Unit2", "Unit3"]

    m = mock_open()
    with patch("builtins.open", m):
        save_results_to_csv(feature_collectors, text_metrics, text_units, "test.csv")

    written_content = "".join(call.args[0] for call in m().write.call_args_list)
    csv_content = list(csv.reader(written_content.splitlines()))

    # Check that the third row has an empty value for Feature2
    assert csv_content[3][3] == ""


if __name__ == "__main__":
    pytest.main()
