import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to allow importing the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_feature_extractor import (
    process_paragraph,
    process_section,
    extract_features,
    feature_collectors,
    DynamicFeatureModel,
)
from features.writing_feature import WritingFeature
from features.graph_mode import GraphMode


class TestLLMFeatureExtractor(unittest.TestCase):

    def setUp(self):
        # Create mock feature collectors
        self.mock_feature1 = MagicMock(spec=WritingFeature)
        self.mock_feature1.graph_mode = GraphMode.BAR
        self.mock_feature1.get_pydantic_feature_label.return_value = "level_of_suspense"

        self.mock_feature2 = MagicMock(spec=WritingFeature)
        self.mock_feature2.graph_mode = GraphMode.COLOR
        self.mock_feature2.get_pydantic_feature_label.return_value = (
            "emotional_intensity"
        )

        self.feature_collectors = [self.mock_feature1, self.mock_feature2]

    @patch("llm_feature_extractor.llm")
    @patch("llm_feature_extractor.get_text_statistics")
    def test_process_paragraph(self, mock_get_text_statistics, mock_llm):
        # Arrange
        paragraph = "This is a test paragraph."
        mock_llm.invoke.return_value = MagicMock(
            dict=lambda: {
                "level_of_suspense": "value1",
                "emotional_intensity": "value2",
            }
        )
        mock_get_text_statistics.return_value = {"word_count": 5}

        # Act
        process_paragraph(paragraph, self.feature_collectors)

        # Assert
        mock_llm.invoke.assert_called_once_with(input=paragraph)
        mock_get_text_statistics.assert_called_once_with(paragraph)
        self.mock_feature1.add_result.assert_called_once_with("value1")
        self.mock_feature2.add_result.assert_called_once_with("value2")

    @patch("llm_feature_extractor.process_paragraph")
    @patch("llm_feature_extractor.get_graph")
    @patch("llm_feature_extractor.combine_short_strings")
    def test_process_section(
        self, mock_combine_short_strings, mock_get_graph, mock_process_paragraph
    ):
        # Arrange
        section = "Paragraph 1\nParagraph 2"
        mock_combine_short_strings.return_value = ["Paragraph 1", "Paragraph 2"]

        # Act
        process_section(section)

        # Assert
        self.assertEqual(mock_process_paragraph.call_count, 2)
        mock_get_graph.assert_called_once()

    @patch("llm_feature_extractor.process_section")
    def test_extract_features(self, mock_process_section):
        # Arrange
        sections = ["Section 1", "Section 2"]

        # Act
        extract_features(sections)

        # Assert
        self.assertEqual(mock_process_section.call_count, 2)

    def test_feature_collectors_setup(self):
        # Assert
        self.assertEqual(len(feature_collectors), 2)
        self.assertTrue(any(f.graph_mode == GraphMode.BAR for f in feature_collectors))
        self.assertTrue(
            any(f.graph_mode == GraphMode.COLOR for f in feature_collectors)
        )

    def test_dynamic_feature_model(self):
        # Print out the fields of DynamicFeatureModel for debugging
        print("DynamicFeatureModel fields:", DynamicFeatureModel.__fields__.keys())

        # Assert
        self.assertIn("level_of_suspense", DynamicFeatureModel.__fields__)
        self.assertIn("emotional_intensity", DynamicFeatureModel.__fields__)


if __name__ == "__main__":
    unittest.main()
