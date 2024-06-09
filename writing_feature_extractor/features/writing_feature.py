from abc import ABC, abstractmethod

from features.graph_mode import GraphMode


class WritingFeature(ABC):
    """Abstract base class for a 'writing feature': a feature which can be
    extracted by an LLM and be presented in a graph."""

    @abstractmethod
    def get_graph_y_ticks(self) -> list[int]:
        """Used for graphing. Returns the y-ticks for the graph."""
        pass

    @abstractmethod
    def get_graph_y_tick_labels(self) -> list[str]:
        """Used for graphing. The y-axis tick labels."""
        pass

    @abstractmethod
    def get_y_level_label(self) -> str:
        """Used for graphing. The label for the y-axis."""
        pass

    @abstractmethod
    def get_pydantic_feature_label(self) -> str:
        pass

    @abstractmethod
    def get_pydantic_feature_type(self) -> type:
        """The type of the feature, as a Pydantic type. Typically an Enum."""
        pass

    @abstractmethod
    def get_pydantic_docstring(self) -> str:
        """The docstring for the Pydantic type. This is useful as it may be
        passed to the LLM to guide structured output."""
        pass

    @abstractmethod
    def get_graph_colors(self) -> dict[str, str]:
        """Used for graphing. If the graph mode of this feature is COLOR,
        these colors are used to color the bars of the graph."""
        pass

    @abstractmethod
    def get_int_for_enum(self, typ: type) -> int:
        """Get the integer equivalent for an enum. This is a workaround
        for an odd issue with graphing in which using the integer value of
        an enum, or using the enum value itself, resulted in the graph being
        displayed out of order and incorrectly."""
        pass

    @abstractmethod
    def add_result(self, enum_value):
        """For results collection. Add a result to the results list."""
        pass

    @abstractmethod
    def set_graph_mode(self, graph_mode: GraphMode):
        """Set the graph mode for this feature"""
        pass
