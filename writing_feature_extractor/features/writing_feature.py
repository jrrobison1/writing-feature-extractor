from abc import ABC, abstractmethod


class WritingFeature(ABC):
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
