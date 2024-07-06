import pytest
from enum import Enum
from writing_feature_extractor.features.generic_feature import GenericFeature
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)


class FixtureLevels(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@pytest.fixture
def generic_feature():
    return GenericFeature(
        name="Test Feature",
        levels=FixtureLevels,
        colors={"0": "#FFFFFF", "1": "#AAAAAA", "2": "#555555", "3": "#000000"},
        result_collection_mode=ResultCollectionMode.NUMBER_REPRESENTATION,
    )


def test_generic_feature_initialization(generic_feature):
    assert generic_feature.name == "Test Feature"
    assert generic_feature.levels == FixtureLevels
    assert generic_feature.colors == {
        "0": "#FFFFFF",
        "1": "#AAAAAA",
        "2": "#555555",
        "3": "#000000",
    }
    assert (
        generic_feature.result_collection_mode
        == ResultCollectionMode.NUMBER_REPRESENTATION
    )


def test_y_level_label(generic_feature):
    assert generic_feature.y_level_label == "Test Feature"


def test_graph_colors(generic_feature):
    assert generic_feature.graph_colors == {
        "0": "#FFFFFF",
        "1": "#AAAAAA",
        "2": "#555555",
        "3": "#000000",
    }


def test_pydantic_feature_label(generic_feature):
    assert generic_feature.pydantic_feature_label == "test_feature"


def test_pydantic_feature_type(generic_feature):
    assert generic_feature.pydantic_feature_type == FixtureLevels


def test_pydantic_docstring(generic_feature):
    assert generic_feature.pydantic_docstring == "Level of test feature in the text."
