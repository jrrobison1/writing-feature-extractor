from abc import ABC, abstractmethod

from features.writing_feature_graph_mode import WritingFeatureGraphMode


class WritingFeature(ABC):
    """Abstract base class for a 'writing feature': a feature which can be
    extracted by an LLM and be presented in a graph."""

    @abstractmethod
    def get_graph_y_ticks(self) -> list[int]:
        pass

    @abstractmethod
    def get_graph_y_tick_labels(self) -> list[str]:
        pass

    @abstractmethod
    def get_y_level_label(self) -> str:
        pass

    @abstractmethod
    def get_pydantic_feature_label(self) -> str:
        pass

    @abstractmethod
    def get_pydantic_feature_type(self) -> type:
        pass

    @abstractmethod
    def get_pydantic_docstring(self) -> str:
        pass

    @abstractmethod
    def get_graph_colors(self) -> dict[str, str]:
        pass

    @abstractmethod
    def get_int_for_enum(self, typ: type) -> int:
        pass

    @abstractmethod
    def add_result(self, enum_value):
        pass

    @abstractmethod
    def set_graph_mode(self, graph_mode: WritingFeatureGraphMode):
        pass
