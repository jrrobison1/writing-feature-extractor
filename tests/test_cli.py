import pytest
from argparse import Namespace
from writing_feature_extractor.cli import parse_arguments
import sys


# TODO More validation for arguments, and perhaps exit if conditions not met
def test_parse_arguments_default(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["script_name", "some_file.txt"])
    args = parse_arguments()
    assert isinstance(args, Namespace)
    assert args.file == "some_file.txt"
    assert args.mode == "paragraph"
    assert not args.save
    assert not args.graph
    assert args.csv_file == "feature_results.csv"
    assert args.config == "feature_config.yaml"
    assert args.provider == "anthropic"
    assert args.model == "claude-3-haiku-20240307"


def test_parse_arguments_custom(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "script_name",
            "input.txt",
            "--mode",
            "section",
            "--save",
            "--graph",
            "--bar-feature",
            "emotion",
            "--color-feature",
            "pacing",
            "--csv-file",
            "output.csv",
            "--config",
            "custom_config.yaml",
            "--provider",
            "openai",
            "--model",
            "gpt-4",
        ],
    )
    args = parse_arguments()
    assert args.file == "input.txt"
    assert args.mode == "section"
    assert args.save
    assert args.graph
    assert args.bar_feature == "emotion"
    assert args.color_feature == "pacing"
    assert args.csv_file == "output.csv"
    assert args.config == "custom_config.yaml"
    assert args.provider == "openai"
    assert args.model == "gpt-4"


def test_parse_arguments_graph_without_features(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["script_name", "input.txt", "--graph"])
    args = parse_arguments()
    assert args.graph
    assert args.bar_feature is None
    assert args.color_feature is None


def test_parse_arguments_invalid_mode(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["script_name", "input.txt", "--mode", "invalid"])
    with pytest.raises(SystemExit):
        parse_arguments()


def test_parse_arguments_no_file(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["script_name"])
    args = parse_arguments()
    assert args.file is None
