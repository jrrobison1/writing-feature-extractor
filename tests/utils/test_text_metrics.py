import pytest
from writing_feature_extractor.utils.text_metrics import (
    calculate_dialogue_percentage,
    combine_short_strings,
    get_text_statistics,
)


def test_calculate_dialogue_percentage():
    text_with_dialogue = (
        'He said, "Hello!" She replied, "Hi there!" The rest is not dialogue.'
    )
    assert calculate_dialogue_percentage(text_with_dialogue) == "27.94%"

    text_without_dialogue = "This text contains no dialogue at all."
    assert calculate_dialogue_percentage(text_without_dialogue) == "0.00%"

    empty_text = ""
    assert calculate_dialogue_percentage(empty_text) == "0.00%"


def test_combine_short_strings():
    short_strings = ["Hello", "This is", "a test", "of combining", "short strings"]
    combined = combine_short_strings(short_strings, minimum_words=3)
    assert len(combined) == 3
    assert combined[0] == "Hello This is"
    assert combined[1] == "a test of combining"
    assert combined[2] == "short strings"

    long_strings = ["This is a long string", "Another long string", "Yet another"]
    assert combine_short_strings(long_strings, minimum_words=3) == long_strings

    empty_list = []
    assert combine_short_strings(empty_list) == []


def test_get_text_statistics():
    sample_text = 'This is a sample text. It has two sentences. And some dialogue: "Hello, world!"'
    stats = get_text_statistics(sample_text)

    assert "dialogue_percentage" in stats
    assert "readability_ease" in stats
    assert "readability_grade" in stats
    assert "sentence_count" in stats
    assert "word_count" in stats
    assert "syllable_count" in stats
    assert "average_words_per_sentence" in stats
    assert "average_syllables_per_word" in stats

    assert stats["dialogue_percentage"] == "18.99%"
    assert stats["sentence_count"] == 3
    assert stats["word_count"] == 14

    # These assertions might need adjustment based on the exact implementation of textstat
    assert isinstance(stats["readability_ease"], float)
    assert isinstance(stats["readability_grade"], float)
    assert isinstance(stats["syllable_count"], int)
    assert isinstance(stats["average_words_per_sentence"], float)
    assert isinstance(stats["average_syllables_per_word"], float)


def test_get_text_statistics_empty_text():
    empty_text = ""
    stats = get_text_statistics(empty_text)

    assert stats == {}  # Expecting an empty dictionary for empty text


def test_get_text_statistics_error_handling(mocker):
    # Mock textstat to raise an exception
    mocker.patch("textstat.flesch_reading_ease", side_effect=Exception("Mocked error"))

    sample_text = "This is a sample text."
    stats = get_text_statistics(sample_text)

    assert stats == {}  # Expecting an empty dictionary when an error occurs
