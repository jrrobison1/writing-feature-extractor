from enum import Enum
from typing import Dict, Type

from writing_feature_extractor.features.graph_mode import GraphMode
from writing_feature_extractor.features.writing_feature import WritingFeature


class GenericFeature(WritingFeature):
    def __init__(
        self,
        name: str,
        levels: Type[Enum],
        colors: Dict[str, str],
        graph_mode: GraphMode = GraphMode.BAR,
    ):
        super().__init__(graph_mode)
        self.name = name
        self.levels = levels
        self.colors = colors

    @property
    def y_level_label(self):
        return self.name

    @property
    def graph_colors(self) -> Dict[str, str]:
        return self.colors

    @property
    def pydantic_feature_label(self):
        return self.name.lower().replace(" ", "_")

    @property
    def pydantic_feature_type(self):
        return self.levels

    @property
    def pydantic_docstring(self):
        return f"Level of {self.name.lower()} in the text."
