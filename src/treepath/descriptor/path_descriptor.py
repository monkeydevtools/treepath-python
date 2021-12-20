from __future__ import annotations

from typing import cast, overload, Type, Generic, Callable, TypeVar, Union, Optional

from treepath.descriptor.abstract_document import AbstractDocument
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.builder.root_path_builder import RootPathBuilder
from treepath.path.traverser.traverser_functions import get, set_, pop, find, get_match, find_matches, set_match
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing

T = TypeVar('T')


class PathDescriptor(Generic[T]):
    __slots__ = "_path", "_getter", "_setter", "_validator"

    def __init__(self,
                 path: Optional[PathBuilder] = None,
                 getter: Union[get, find, get_match, find_matches] = get,
                 setter: Union[set_, set_match] = set_,
                 validator: Callable[[JsonTypes], None] = do_nothing
                 ):
        self._path = path
        self._getter = getter
        self._setter = setter
        self._validator = validator

    def __set_name__(self, owner: Type[AbstractDocument], name: str) -> None:
        if not issubclass(owner, AbstractDocument):
            raise ValueError(
                f"{type(self)} can only be assign to a class that implements "
                "AbstractDocument")
        if self._path is None:
            self._path = RootPathBuilder()[name]

    @overload
    def __get__(self, obj: None, objtype: None) -> PathDescriptor:
        ...

    @overload
    def __get__(self, obj: AbstractDocument, objtype: Type[AbstractDocument]) -> T:
        ...

    def __get__(
            self, obj: AbstractDocument | None, objtype: Type[AbstractDocument] | None = None
    ) -> PathDescriptor | T:
        if obj is None:
            return self
        return cast(T, self._getter(self._path, obj.data))

    def __set__(self, obj: AbstractDocument, value: T) -> None:
        self._validator(value)
        self._setter(self._path, value, obj.data)

    def __delete__(self, obj: AbstractDocument) -> None:
        pop(self._path, obj.data)
