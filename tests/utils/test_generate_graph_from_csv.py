import pytest
import pandas as pd
import matplotlib.pyplot as plt
import json
from unittest.mock import patch, MagicMock
from writing_feature_extractor.utils.generate_graph_from_csv import (
    generate_graph_from_csv,
)
from writing_feature_extractor.core.custom_exceptions import (
    FileOperationError,
    GraphError,
)


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Unit": range(1, 6),
            "Length": [100, 150, 200, 180, 120],
            "Emotional Intensity": [1, 2, 3, 2, 1],
            "Mood": ["happy", "sad", "tense", "angry", "neutral"],
            "ColorMaps": [
                '{"Emotional Intensity": {"0": "#FFFFFF", "1": "#FF9999", "2": "#FF3333", "3": "#CC0000"}, "Mood": {"happy": "#FFFF00", "sad": "#00008B", "angry": "#FF0000", "tense": "#7328AA", "neutral": "#D3D3D3"}}'
            ]
            * 5,
        }
    )


def test_generate_graph_from_csv_success(tmp_path, sample_df):
    csv_file = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_file, index=False)

    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        generate_graph_from_csv(str(csv_file), "Emotional Intensity", "Mood")
        mock_savefig.assert_called_once()


def test_generate_graph_from_csv_file_not_found():
    with pytest.raises(FileOperationError):
        generate_graph_from_csv("non_existent_file.csv", "Emotional Intensity", "Mood")


def test_generate_graph_from_csv_invalid_feature(tmp_path, sample_df):
    csv_file = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_file, index=False)

    with pytest.raises(GraphError):
        generate_graph_from_csv(str(csv_file), "Invalid Feature", "Mood")


@patch("matplotlib.pyplot.subplots")
@patch("matplotlib.pyplot.savefig")
def test_generate_graph_from_csv_plot_details(
    mock_savefig, mock_subplots, tmp_path, sample_df
):
    csv_file = tmp_path / "test_data.csv"
    sample_df.to_csv(csv_file, index=False)

    mock_fig, mock_ax = MagicMock(), MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)

    generate_graph_from_csv(str(csv_file), "Emotional Intensity", "Mood")

    # Check if the plot is created with correct parameters
    mock_ax.bar.assert_called_once()
    mock_ax.set_xlabel.assert_called_with("Text Unit", fontsize=12)
    mock_ax.set_title.assert_called_with(
        "Emotional Intensity. Mood is indicated by color.", fontsize=14
    )
    mock_ax.legend.assert_called_once()
    mock_savefig.assert_called_once()


if __name__ == "__main__":
    pytest.main()
