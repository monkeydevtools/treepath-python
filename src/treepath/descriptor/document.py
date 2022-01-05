import json

from treepath.descriptor.abstract_document import AbstractDocument
from treepath.path.typing.json_types import JsonTypes


class Document(AbstractDocument):
    __slots__ = "_data"

    def __init__(self, data: JsonTypes = dict()):
        self._data = data

    @property
    def data(self) -> JsonTypes:
        return self._data

    @data.setter
    def data(self, data: JsonTypes):
        self._data = data

    @property
    def json_str(self) -> str:
        return json.dumps(self._data)

    @property
    def pretty_json_str(self) -> str:
        return json.dumps(self._data, sort_keys=True, indent=2)

    def __repr__(self):
        return self.json_str

    def __str__(self):
        return f"{self.__class__.__name__}:" \
               f" json: {self.pretty_json_str}"

    def __eq__(self, other):
        return isinstance(other, AbstractDocument) and self.data == other.data

    def __ne__(self, other):
        return (not isinstance(other, AbstractDocument)) or self.data != other.data