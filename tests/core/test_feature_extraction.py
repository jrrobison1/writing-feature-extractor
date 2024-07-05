import pytest
from unittest.mock import Mock, patch, call
from langchain_core.pydantic_v1 import BaseModel, Field
from enum import Enum

from writing_feature_extractor.core.feature_extraction import (
    process_feature_with_triangulation,
    extract_features,
    extract_features_paragraph_mode,
    extract_features_section_mode,
)
from writing_feature_extractor.features.writing_feature import WritingFeature
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)


class MockEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MockFeature(WritingFeature):
    def __init__(self):
        super().__init__(ResultCollectionMode.NUMBER_REPRESENTATION)
        self.results = []

    @property
    def pydantic_feature_label(self):
        return "mock_feature"

    @property
    def pydantic_feature_type(self):
        return MockEnum

    @property
    def y_level_label(self):
        return "Mock Feature"

    @property
    def pydantic_docstring(self):
        return "A mock feature for testing"


class MockModel(BaseModel):
    mock_feature: MockEnum = Field(description="A mock feature for testing")


def test_process_feature_with_triangulation():
    feature = MockFeature()
    result = MockModel(mock_feature=MockEnum.MEDIUM)
    triangulation_results = [
        MockModel(mock_feature=MockEnum.LOW),
        MockModel(mock_feature=MockEnum.HIGH),
    ]

    process_feature_with_triangulation(result, triangulation_results, feature)

    assert feature.results == [1]  # MEDIUM is index 1 in MockEnum


@patch("writing_feature_extractor.core.feature_extraction.process_text")
@patch("writing_feature_extractor.core.feature_extraction.combine_short_strings")
@patch("writing_feature_extractor.core.feature_extraction.get_text_statistics")
@patch("writing_feature_extractor.core.feature_extraction.save_results_to_csv")
def test_extract_features_paragraph_mode(
    mock_save_csv, mock_get_stats, mock_combine, mock_process_text
):
    feature = MockFeature()
    sections = ["This is a test paragraph.", "This is another test paragraph."]
    llm = Mock()
    mock_combine.return_value = sections  # Simulate the combine_short_strings function

    extract_features_paragraph_mode(sections, [feature], llm)

    assert mock_process_text.call_count == 4
    mock_process_text.assert_has_calls(
        [call(paragraph, [feature], llm, None) for paragraph in sections * 2]
    )
    assert mock_get_stats.call_count == 4
    assert mock_save_csv.call_count == 2


@patch("writing_feature_extractor.core.feature_extraction.process_text")
@patch("writing_feature_extractor.core.feature_extraction.get_text_statistics")
def test_extract_features_section_mode(mock_get_stats, mock_process_text):
    feature = MockFeature()
    sections = ["This is a test section.", "This is another test section."]
    llm = Mock()

    extract_features_section_mode(sections, [feature], llm)

    assert mock_process_text.call_count == 2
    mock_process_text.assert_has_calls(
        [call(section, [feature], llm, None) for section in sections]
    )
    assert mock_get_stats.call_count == 2


def test_extract_features_invalid_mode():
    with pytest.raises(ValueError):
        extract_features([], "invalid_mode", [], Mock())


if __name__ == "__main__":
    pytest.main()
