import pytest
from unittest.mock import patch, MagicMock
from argparse import Namespace
from main import (
    main,
    handle_feature_extraction,
    handle_graph_generation,
)
from writing_feature_extractor.core.custom_exceptions import FeatureExtractorError


@pytest.fixture
def mock_args():
    return Namespace(
        file="test.txt",
        graph=False,
        mode="paragraph",
        save=False,
        csv_file="test_results.csv",
        config="test_config.yaml",
        provider="test_provider",
        model="test_model",
    )


@patch("main.parse_arguments")
@patch("main.handle_feature_extraction")
@patch("main.handle_graph_generation")
def test_main_feature_extraction(
    mock_handle_graph, mock_handle_feature, mock_parse_args, mock_args
):
    mock_parse_args.return_value = mock_args
    main()
    mock_handle_feature.assert_called_once_with(mock_args)
    mock_handle_graph.assert_not_called()


@patch("main.parse_arguments")
@patch("main.handle_feature_extraction")
@patch("main.handle_graph_generation")
def test_main_graph_generation(mock_handle_graph, mock_handle_feature, mock_parse_args):
    args = Namespace(
        graph=True,
        csv_file="test.csv",
        bar_feature="test_bar",
        color_feature="test_color",
    )
    mock_parse_args.return_value = args
    main()
    mock_handle_graph.assert_called_once_with(args)
    mock_handle_feature.assert_not_called()


@patch("main.parse_arguments")
@patch("main.logger")
def test_main_error_handling(mock_logger, mock_parse_args):
    mock_parse_args.side_effect = FeatureExtractorError("Test error")
    main()
    mock_logger.error.assert_called_once_with("Feature extractor error: Test error")


@patch("main.load_text")
@patch("main.load_feature_config")
@patch("main.WritingFeatureFactory.get_dynamic_model")
@patch("main.ModelFactory.get_llm_model")
@patch("main.split_into_sections")
@patch("main.extract_features")
@patch("main.save_results_to_csv")
def test_handle_feature_extraction(
    mock_save_results,
    mock_extract_features,
    mock_split_sections,
    mock_get_llm,
    mock_get_dynamic_model,
    mock_load_config,
    mock_load_text,
    mock_args,
):
    mock_load_text.return_value = "Test text"
    mock_load_config.return_value = ["feature1", "feature2"]
    mock_get_dynamic_model.return_value = (["collector1", "collector2"], "DynamicModel")
    mock_get_llm.return_value = "LLM"
    mock_split_sections.return_value = ["section1", "section2"]
    mock_extract_features.return_value = (
        ["collector1", "collector2"],
        ["unit1", "unit2"],
        ["metric1", "metric2"],
    )

    handle_feature_extraction(mock_args)

    mock_load_text.assert_called_once_with(mock_args.file)
    mock_load_config.assert_called_once_with(mock_args.config)
    mock_get_dynamic_model.assert_called_once_with(["feature1", "feature2"])
    mock_get_llm.assert_called_once_with(
        mock_args.provider, mock_args.model, "DynamicModel"
    )
    mock_split_sections.assert_called_once_with("Test text")
    mock_extract_features.assert_called_once_with(
        ["section1", "section2"],
        mock_args.mode,
        ["collector1", "collector2"],
        "LLM",
        [],
    )
    mock_save_results.assert_not_called()  # Because mock_args.save is False


@patch("main.generate_graph_from_csv")
def test_handle_graph_generation(mock_generate_graph):
    args = Namespace(
        csv_file="test.csv", bar_feature="test_bar", color_feature="test_color"
    )
    handle_graph_generation(args)
    mock_generate_graph.assert_called_once_with("test.csv", "test_bar", "test_color")


@patch("main.logger")
def test_handle_graph_generation_error(mock_logger):
    args = Namespace(csv_file="test.csv", bar_feature=None, color_feature=None)
    handle_graph_generation(args)
    mock_logger.error.assert_called_once_with(
        "Please specify --bar-feature and --color-feature when using --graph"
    )


if __name__ == "__main__":
    pytest.main()
