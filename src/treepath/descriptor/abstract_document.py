from abc import ABC, abstractmethod

from treepath.path.typing.json_types import JsonTypes


class AbstractDocument(ABC):
    @property
    @abstractmethod
    def data(self) -> JsonTypes:  # pragma: no cover
        ...

    @data.setter
    @abstractmethod
    def data(self, data: JsonTypes):  # pragma: no cover
        ...
