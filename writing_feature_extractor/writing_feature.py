from abc import ABC, abstractmethod


class WritingFeature(ABC):
    @abstractmethod
    def get_graph_y_ticks():
        pass

    @abstractmethod
    def get_graph_y_tick_labels():
        pass

    @abstractmethod
    def get_y_level_label():
        pass
