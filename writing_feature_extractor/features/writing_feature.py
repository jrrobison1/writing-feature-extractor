from abc import ABC, abstractmethod
from enum import Enum

from writing_feature_extractor.features.graph_mode import GraphMode


class WritingFeature(ABC):
    """Abstract base class for a 'writing feature': a feature which can be
    extracted by an LLM and be presented in a graph."""

    def __init__(self, graph_mode: GraphMode = GraphMode.BAR):
        self.graph_mode = graph_mode
        self.results: list[int] = []

    @property
    @abstractmethod
    def pydantic_feature_label(self) -> str:
        pass

    @property
    @abstractmethod
    def pydantic_feature_type(self) -> type[Enum]:
        pass

    @property
    @abstractmethod
    def y_level_label(self) -> str:
        """Used for graphing. The label for the y-axis."""
        pass

    @property
    @abstractmethod
    def pydantic_feature_label(self) -> str:
        pass

    @property
    @abstractmethod
    def pydantic_docstring(self) -> str:
        """The docstring for the Pydantic type. This is useful as it may be
        passed to the LLM to guide structured output."""
        pass

    @property
    def graph_colors(self) -> dict[str, str]:
        """Used for graphing. If the graph mode of this feature is COLOR,
        these colors are used to color the bars of the graph."""
        pass

    def graph_mode(self) -> GraphMode:
        """Set the graph mode for this feature"""
        return self._graph_mode

    @property
    def graph_y_tick_labels(self) -> list[str]:
        return [e.value for e in self.pydantic_feature_type]

    @property
    def graph_y_ticks(self) -> list[int]:
        return list(range(len(self.pydantic_feature_type)))

    def get_int_for_enum(self, enum_value: Enum) -> int:
        """Get the integer equivalent for an enum. This is a workaround
        for an odd issue with graphing in which using the integer value of
        an enum, or using the enum value itself, resulted in the graph being
        displayed out of order and incorrectly."""
        return list(self.pydantic_feature_type).index(enum_value)

    def add_result(self, enum_value: Enum):
        """For results collection. Add a result to the results list."""
        if self.graph_mode == GraphMode.BAR:
            self.results.append(self.get_int_for_enum(enum_value))
        elif self.graph_mode == GraphMode.COLOR:
            self.results.append(enum_value)
        elif self.graph_mode == GraphMode.SAVE_ONLY:
            self.results.append(self.get_int_for_enum(enum_value))
        else:
            raise ValueError("Invalid graph mode")
