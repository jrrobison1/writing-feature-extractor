import re
import textstat
from writing_feature_extractor.utils.logger_config import get_logger

logger = get_logger(__name__)

MININUM_WORDS_PER_PARAGRAPH = 8
NUMBER_OF_CHARACTERS_TO_SHOW_WHEN_COMBINING = 20


def calculate_dialogue_percentage(text: str):
    """Calculate the percentage of text that is within dialogue tags"""

    try:
        dialogue_pattern = r'"[^"]*"'
        dialogues = re.findall(dialogue_pattern, text, re.DOTALL)
        dialogue_length = sum(len(dialogue) for dialogue in dialogues)
        total_length = len(text)
        dialogue_percentage = (
            (dialogue_length / total_length) * 100 if total_length > 0 else 0
        )

        return dialogue_percentage
    except Exception as e:
        logger.error(f"Error calculating dialogue percentage: {e}. Returning zero.")
        logger.debug("Error details:", exc_info=True)
        return 0


def combine_short_strings(
    strings: list[str], minimum_words: int = MININUM_WORDS_PER_PARAGRAPH
) -> list[str]:
    """Combine short strings (less than minimum_words) with the next string in the list.
    This is useful for pieces of text that are too small for an LLM to make inference
    for feature extraction"""

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
        logger.debug("Error details:", exc_info=True)
        return strings


def get_text_statistics(text: str) -> dict[str]:
    """Get statistics about the text, such as readability"""

    try:
        text_statistics = dict()
        dialogue_percentage = calculate_dialogue_percentage(text)
        dp_as_string = f"{dialogue_percentage:.2f}%"
        text_statistics["dialogue_percentage"] = dp_as_string
        text_statistics["readability_ease"] = textstat.flesch_reading_ease(text)
        text_statistics["readability_grade"] = textstat.flesch_kincaid_grade(text)
        text_statistics["sentence_count"] = textstat.sentence_count(text)
        text_statistics["word_count"] = textstat.lexicon_count(text, removepunct=True)

        logger.debug(f"Text statistics: {text_statistics}")
        return text_statistics
    except Exception as e:
        logger.error(f"Error calculating text statistics: {e}")
        logger.debug("Error details:", exc_info=True)
        return dict()
