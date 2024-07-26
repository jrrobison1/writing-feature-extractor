from typing import List
from writing_feature_extractor.core.custom_exceptions import FileOperationError
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.text_metrics import combine_short_strings

SECTION_DELIMITER = "***"
logger = get_logger(__name__)


def load_text(file_path: str) -> str:
    """
    Load text content from a file.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.

    Raises:
        FileOperationError: If there's an error reading the file.
    """
    try:
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading text from {file_path}: {e}")
        raise FileOperationError("Could not load text from the given file/path.") from e


def split_into_sections(text: str) -> List[str]:
    """
    Split the input text into sections using the SECTION_DELIMITER.

    Args:
        text (str): The input text to be split.

    Returns:
        List[str]: A list of text sections.
    """
    return text.split(SECTION_DELIMITER)


def split_into_paragraphs(section: str) -> List[str]:
    """
    Split a section of text into paragraphs and combine short strings.

    Args:
        section (str): The section of text to be split into paragraphs.

    Returns:
        List[str]: A list of paragraphs, with short strings combined.
    """
    paragraphs = section.split("\n")
    return combine_short_strings(paragraphs)
