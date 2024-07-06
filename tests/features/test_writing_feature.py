import pytest
from enum import Enum
from unittest.mock import Mock, PropertyMock
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)


class FixtureEnum(str, Enum):
    A = "a"
    B = "b"
    C = "c"


@pytest.fixture
def mock_writing_feature():
    feature = Mock(spec=WritingFeature)
    type(feature).pydantic_feature_type = PropertyMock(return_value=FixtureEnum)
    feature.result_collection_mode = ResultCollectionMode.NUMBER_REPRESENTATION
    feature.results = []

    # Implement get_int_for_enum
    feature.get_int_for_enum = WritingFeature.get_int_for_enum.__get__(feature)

    # Implement add_result
    feature.add_result = WritingFeature.add_result.__get__(feature)
    type(feature).graph_y_tick_labels = WritingFeature.graph_y_tick_labels
    type(feature).graph_y_ticks = WritingFeature.graph_y_ticks

    return feature


def test_get_int_for_enum(mock_writing_feature):
    assert mock_writing_feature.get_int_for_enum(FixtureEnum.A) == 0
    assert mock_writing_feature.get_int_for_enum(FixtureEnum.B) == 1
    assert mock_writing_feature.get_int_for_enum(FixtureEnum.C) == 2


def test_add_result_number_representation(mock_writing_feature):
    mock_writing_feature.add_result(FixtureEnum.B)
    assert mock_writing_feature.results == [1]


def test_add_result_field_name(mock_writing_feature):
    mock_writing_feature.result_collection_mode = ResultCollectionMode.FIELD_NAME
    mock_writing_feature.add_result(FixtureEnum.B)
    assert mock_writing_feature.results == [FixtureEnum.B]


def test_graph_y_tick_labels(mock_writing_feature):
    expected = ["a", "b", "c"]
    assert mock_writing_feature.graph_y_tick_labels == expected


def test_graph_y_ticks(mock_writing_feature):
    expected = [0, 1, 2]
    assert mock_writing_feature.graph_y_ticks == expected
