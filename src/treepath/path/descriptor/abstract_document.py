from abc import ABC, abstractmethod

from treepath.path.typing_alias import JsonTypes


class AbstractDocument(ABC):
    @property
    @abstractmethod
    def data(self) -> JsonTypes:  # pragma: no cover
        pass

    @data.setter
    @abstractmethod
    def data(self, data: JsonTypes):  # pragma: no cover
        pass
