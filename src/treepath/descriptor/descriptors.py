from __future__ import annotations

from typing import cast, overload, Type, Generic, Callable, TypeVar

from treepath import RootPathBuilder
from treepath.path.builder.path_builder import PathBuilder
from treepath.descriptor.abstract_document import AbstractDocument
from treepath.path.traverser.traverser_functions import get, set_, not_set, pop
from treepath.path.typing_alias import JsonTypeVar, JsonTypes
from treepath.path.utils.function import do_nothing



class PathDescriptor(Generic[JsonTypeVar]):
    __slots__ = "_path", "_default", "_cascade", "_validator"

    def __init__(self,
                 path: PathBuilder = None,
                 default=not_set,
                 cascade: bool = False,
                 validator: Callable[[JsonTypes], None] = do_nothing
                 ):
        self._path = path
        self._default = default
        self._cascade = cascade
        self._validator = validator

    def __set_name__(self, owner: Type[AbstractDocument], name: str) -> None:
        if not issubclass(owner, AbstractDocument):
            raise ValueError(
                f"{type(self)} can only be assign to a class that implements "
                "AbstractDocument")
        if not self._path:
            self._path = RootPathBuilder()[name]

    @overload
    def __get__(self, obj: None, objtype: None) -> PathDescriptor:
        ...

    @overload
    def __get__(self, obj: AbstractDocument, objtype: Type[AbstractDocument]) -> JsonTypeVar:
        ...

    def __get__(
            self, obj: AbstractDocument | None, objtype: Type[AbstractDocument] | None = None
    ) -> PathDescriptor | JsonTypeVar:
        if obj is None:
            return self
        return cast(JsonTypeVar, get(self._path, obj.data, default=self._default))

    def __set__(self, obj: AbstractDocument, value: JsonTypeVar) -> None:
        self._validator(value)
        set_(self._path, value, obj.data, cascade=self._cascade)

    def __delete__(self, obj: AbstractDocument) -> None:
        pop(self._path, obj.data)

