from treepath.path.typing.json_arg_types import JsonArgTypes


class AbstractDocument:
    @property
    def data(self) -> JsonArgTypes:  # pragma: no cover
        ...

    @data.setter
    def data(self, data: JsonArgTypes):  # pragma: no cover
        ...
