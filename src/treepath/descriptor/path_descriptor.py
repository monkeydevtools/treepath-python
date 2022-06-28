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
    """
    Treepath implementation of the python descriptor.
    See details on descriptors: https://docs.python.org/3/howto/descriptor.html

    See descriptor_functions for usage.
    """
    __slots__ = "_expression", "_getter", "_setter", "_to_wrapped_value", "_to_json_value"

    def __init__(self,
                 expression: Optional[PathBuilder] = None,
                 *,
                 getter: Union[get, find, get_match, find_matches] = get,
                 setter: Union[set_, set_match] = set_,
                 to_wrapped_value: Callable[[JsonTypes], T] = do_nothing,
                 to_json_value: Callable[[T], JsonTypes] = do_nothing
                 ):
        self._expression = expression
        self._getter = getter
        self._setter = setter
        self._to_wrapped_value = to_wrapped_value
        self._to_json_value = to_json_value

    def __set_name__(self, owner: Type[AbstractDocument], name: str) -> None:
        if not issubclass(owner, AbstractDocument):
            raise ValueError(
                f"{type(self)} can only be assign to a class that implements "
                f"{AbstractDocument}")
        if self._expression is None:
            self._expression = RootPathBuilder()[name]

    @overload
    def __get__(self, owner_obj: None, owner_obj_type: None) -> PathDescriptor:  # pragma: no cover
        ...

    @overload
    def __get__(self, owner_obj: AbstractDocument, owner_obj_type: Type[AbstractDocument]) -> T:  # pragma: no cover
        ...

    def __get__(
            self, owner_obj: AbstractDocument | None, owner_obj_type: Type[AbstractDocument] | None = None
    ) -> PathDescriptor | T:
        if owner_obj is None:
            return self
        json_value = self._getter(self._expression, owner_obj.data)
        wrapped_value = self._to_wrapped_value(json_value)
        return cast(T, wrapped_value)

    def __set__(self, owner_obj: AbstractDocument, wrapped_value: T) -> None:
        json_value = self._to_json_value(wrapped_value)
        self._setter(self._expression, json_value, owner_obj.data)

    def __delete__(self, owner_obj: AbstractDocument) -> None:
        pop(self._expression, owner_obj.data)
