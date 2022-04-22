from abc import ABC, abstractmethod

from treepath.path.typing.json_arg_types import JsonArgTypes


class AbstractDocument(ABC):
    @property
    @abstractmethod
    def data(self) -> JsonArgTypes:  # pragma: no cover
        ...

    @data.setter
    @abstractmethod
    def data(self, data: JsonArgTypes):  # pragma: no cover
        ...
