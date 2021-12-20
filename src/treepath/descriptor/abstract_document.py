from abc import ABC
from typing import Union

from treepath.path.traverser.match import Match
from treepath.path.typing.json_types import JsonTypes


class AbstractDocument(ABC):
    __slots__ = "_data"

    def __init__(self, data: Union[JsonTypes, Match]):
        self._data = data

    @property
    def data(self) -> Union[JsonTypes, Match]:  # pragma: no cover
        return self._data

    @data.setter
    def data(self, data: Union[JsonTypes, Match]):  # pragma: no cover
        self._data = data
