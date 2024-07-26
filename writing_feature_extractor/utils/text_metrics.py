import re
import textstat
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)

MININUM_WORDS_PER_PARAGRAPH = 8
NUMBER_OF_CHARACTERS_TO_SHOW_WHEN_COMBINING = 20


def calculate_dialogue_percentage(text: str) -> float:
    """
    Calculate the percentage of text that is within dialogue tags.

    Args:
        text (str): The input text to analyze.

    Returns:
        str: The percentage of dialogue in the text, formatted as a string with two decimal places and a '%' symbol.
              Returns '0' if an error occurs during calculation.
    """
    try:
        dialogue_pattern = r'"[^"]*"'
        dialogues = re.findall(dialogue_pattern, text, re.DOTALL)
        dialogue_length = sum(len(dialogue) for dialogue in dialogues)
        total_length = len(text)
        dialogue_percentage = (
            (dialogue_length / total_length) * 100 if total_length > 0 else 0
        )

        dp_as_string = f"{dialogue_percentage:.2f}%"

        return dp_as_string
    except Exception as e:
        logger.error(f"Error calculating dialogue percentage: {e}. Returning zero.")
        return 0


def combine_short_strings(
    strings: list[str], minimum_words: int = MININUM_WORDS_PER_PARAGRAPH
) -> list[str]:
    """
    Combine short strings with the next string in the list if they contain fewer than the specified minimum words.

    This is useful for consolidating text segments that are too small for an LLM to make accurate inferences
    during feature extraction.

    Args:
        strings (list[str]): A list of strings to process.
        minimum_words (int, optional): The minimum number of words a string should contain.
                                       Defaults to MININUM_WORDS_PER_PARAGRAPH.

    Returns:
        list[str]: A new list with short strings combined. If an error occurs, returns the original list.
    """
    for string in strings:
        if len(string) == 0:
            logger.info("Removing empty string from list of strings")
            strings.remove(string)

    try:
        i = 0
        while i < len(strings) - 1:
            if (len(strings[i].split()) < minimum_words) and (len(strings[i]) > 0):
                logger.info(
                    f"Combining ...[{strings[i][:NUMBER_OF_CHARACTERS_TO_SHOW_WHEN_COMBINING]}] and [{strings[i + 1][:NUMBER_OF_CHARACTERS_TO_SHOW_WHEN_COMBINING]}...]"
                )
                strings[i + 1] = strings[i] + " " + strings[i + 1]
                strings.pop(i)
            else:
                i += 1
        return strings
    except Exception as e:
        logger.error(
            f"Failure while combining short strings: {e}. Returning original list of strings"
        )
        return strings


def get_text_statistics(text: str) -> dict[str]:
    """
    Calculate various statistics about the given text.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict[str]: A dictionary containing the following text statistics:
            - dialogue_percentage: Percentage of text within dialogue tags
            - readability_ease: Flesch Reading Ease score
            - readability_grade: Flesch-Kincaid Grade Level
            - sentence_count: Number of sentences
            - word_count: Number of words
            - syllable_count: Number of syllables
            - average_words_per_sentence: Average number of words per sentence
            - average_syllables_per_word: Average number of syllables per word

    Note:
        Returns an empty dictionary if an error occurs during calculation.
    """
    try:
        text_statistics = dict()
        text_statistics["dialogue_percentage"] = calculate_dialogue_percentage(text)
        text_statistics["readability_ease"] = textstat.flesch_reading_ease(text)
        text_statistics["readability_grade"] = textstat.flesch_kincaid_grade(text)
        text_statistics["sentence_count"] = textstat.sentence_count(text)
        text_statistics["word_count"] = textstat.lexicon_count(text, removepunct=True)
        text_statistics["syllable_count"] = textstat.syllable_count(text)
        text_statistics["average_words_per_sentence"] = (
            text_statistics["word_count"] / text_statistics["sentence_count"]
        )
        text_statistics["average_syllables_per_word"] = (
            text_statistics["syllable_count"] / text_statistics["word_count"]
        )

        logger.debug(f"Text statistics: {text_statistics}")
        return text_statistics
    except Exception as e:
        logger.error(f"Error calculating text statistics: {e}")
        return dict()
