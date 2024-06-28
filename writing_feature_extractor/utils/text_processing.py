from typing import List
from writing_feature_extractor.core.custom_exceptions import FileOperationError
from writing_feature_extractor.utils.logger_config import get_logger
from writing_feature_extractor.utils.text_metrics import combine_short_strings

SECTION_DELIMITER = "***"
logger = get_logger()


def load_text(file_path: str) -> str:
    try:
        with open(file_path) as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error loading text from {file_path}: {e}")
        logger.debug("Error details:", exc_info=True)
        raise FileOperationError("Could not load text from the given file/path.") from e


def split_into_sections(text: str) -> List[str]:
    return text.split(SECTION_DELIMITER)


def split_into_paragraphs(section: str) -> List[str]:
    paragraphs = section.split("\n")
    return combine_short_strings(paragraphs)
