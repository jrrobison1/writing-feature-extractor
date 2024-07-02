from dataclasses import dataclass
from enum import Enum
from typing import Dict, Type
from writing_feature_extractor.features.available_writing_features import (
    AvailableWritingFeatures,
)
from writing_feature_extractor.features.result_collection_mode import (
    ResultCollectionMode,
)


@dataclass
class FeatureConfigData:
    def __init__(
        self,
        name: AvailableWritingFeatures | str,
        levels: Type[Enum],
        colors: Dict[str, str],
        result_collection_mode: ResultCollectionMode = ResultCollectionMode.NUMBER_REPRESENTATION,
    ):
        self._name = name
        self._levels = levels
        self._colors = colors
        self._result_collection_mode = result_collection_mode

    @property
    def name(self) -> str:
        return self._name

    @property
    def levels(self) -> Type[Enum]:
        return self._levels

    @property
    def colors(self) -> Dict[str, str]:
        return self._colors

    @property
    def result_collection_mode(self) -> ResultCollectionMode:
        return self._result_collection_mode
