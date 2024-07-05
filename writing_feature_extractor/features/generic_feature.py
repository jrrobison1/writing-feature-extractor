from enum import Enum
from typing import Dict, Type

from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)
from writing_feature_extractor.features.writing_feature import WritingFeature


class GenericFeature(WritingFeature):
    def __init__(
        self,
        name: str,
        levels: Type[Enum],
        colors: Dict[str, str],
        result_collection_mode: ResultCollectionMode = ResultCollectionMode.NUMBER_REPRESENTATION,
    ):
        super().__init__(result_collection_mode)
        self.name = name
        self.levels = levels
        self.colors = colors

    @property
    def y_level_label(self) -> str:
        return self.name

    @property
    def graph_colors(self) -> Dict[str, str]:
        return self.colors

    @property
    def pydantic_feature_label(self) -> str:
        return self.name.lower().replace(" ", "_")

    @property
    def pydantic_feature_type(self) -> Type[Enum]:
        return self.levels

    @property
    def pydantic_docstring(self) -> str:
        return f"Level of {self.name.lower()} in the text."
