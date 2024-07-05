import pytest
from writing_feature_extractor.utils.text_processing import (
    load_text,
    split_into_sections,
    split_into_paragraphs,
)
from writing_feature_extractor.core.custom_exceptions import FileOperationError


def test_load_text(tmp_path):
    # Create a temporary file with some content
    test_file = tmp_path / "test.txt"
    test_content = "This is a test file.\nIt has multiple lines.\n"
    test_file.write_text(test_content)

    # Test successful file loading
    assert load_text(str(test_file)) == test_content

    # Test file not found
    with pytest.raises(FileOperationError):
        load_text("nonexistent_file.txt")


# TODO Look into removing newlines around sections after splitting
def test_split_into_sections():
    test_text = "Section 1\n***\nSection 2\n***\nSection 3"
    expected_sections = ["Section 1\n", "\nSection 2\n", "\nSection 3"]
    assert split_into_sections(test_text) == expected_sections


def test_split_into_paragraphs():
    test_section = "Paragraph 1\n\nParagraph 2\nStill paragraph 2\n\nParagraph 3\nParagraph 4\nParagraph 5"
    expected_paragraphs = [
        "Paragraph 1 Paragraph 2 Still paragraph 2 Paragraph 3",
        "Paragraph 4 Paragraph 5",
    ]
    assert split_into_paragraphs(test_section) == expected_paragraphs

    # Test with short paragraphs that should be combined
    test_section_short = (
        "Short 1\n\nShort 2\n\nLonger paragraph here\n\nShort 3\n\nShort 4"
    )
    expected_paragraphs_short = [
        "Short 1 Short 2 Longer paragraph here Short 3",
        "Short 4",
    ]
    assert split_into_paragraphs(test_section_short) == expected_paragraphs_short
