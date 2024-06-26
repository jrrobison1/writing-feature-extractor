from typing import List
from writing_feature_extractor.utils.text_metrics import combine_short_strings

SECTION_DELIMITER = "***"


def load_text(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()


def split_into_sections(text: str) -> List[str]:
    return text.split(SECTION_DELIMITER)


def split_into_paragraphs(section: str) -> List[str]:
    paragraphs = section.split("\n")
    return combine_short_strings(paragraphs)
