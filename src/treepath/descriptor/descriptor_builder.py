from __future__ import annotations

from functools import partial
from typing import Callable, Union, Any, Type, Optional

from treepath.descriptor.document import Document
from treepath.descriptor.path_descriptor import T, PathDescriptor
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_, find, get_match, find_matches, set_match
from treepath.path.typing.json_arg_types import JsonArgTypes
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing


class DocTypeTransformer:
    __slots__ = '_type'

    def __init__(self, _type):
        self._type = _type

    def to_wrapped_value(self, json_: JsonArgTypes) -> Document:
        return self._type(json_)

    def to_json_value(self, doc: Document) -> JsonArgTypes:
        return doc.data


class DocListTypeTransformer:
    __slots__ = '_type'

    def __init__(self, _type):
        self._type = _type

    def to_wrapped_value(self, json_: JsonArgTypes) -> Document:
        return self._type(json_)

    def to_json_value(self, doc: Document) -> JsonArgTypes:
        return doc.data


class DescriptorBuilder:
    """
    custom type = ct
    doc type  = dt
    itr = i
    single = s

    ct,s
    ct,i
    dt,s
    dt,i

    """

    def __init__(self,
                 type_: Type[T],
                 path: Optional[PathBuilder] = None,
                 *,
                 getter: Union[get, find, get_match, find_matches] = get,
                 setter: Union[set_, set_match] = set_,
                 to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
                 to_json_value: Callable[[Any], JsonTypes] = do_nothing
                 ):
        self._type = type_
        self._path = path
        self._getter = getter
        self._setter = setter
        self._to_wrapped_value = to_wrapped_value
        self._to_json_value = to_json_value
        self.__build = [
            [
                self.__build_doc_type_for_single,
                self.__build_doc_type_for_iterator
            ],
            [
                self.__custom_type_for_single,
                self.__custom_type_for_iterator
            ],
        ]

    def build(self):
        type_index = self.__index_for_type_column()
        getter_index = self.__index_for_getter_column(self._getter)
        return self.__build[type_index][getter_index]()

    def __index_for_type_column(self) -> int:
        if issubclass(self._type, Document):
            return 0
        else:
            return 1

    def __index_for_getter_column(self, getter) -> int:
        if getter is get or getter is get_match:
            return 0
        elif getter is find or getter is find_matches:
            return 1
        elif isinstance(getter, partial):
            return self.__index_for_getter_column(getter.func)
        else:
            raise ValueError(
                f"The getter argument {type(getter)} is invalid.  "
                f"The value must be either get, find, get_match, or find_matches. or a partial of one of these "
                f"functions ")

    def __build_path_descriptor(self):
        return PathDescriptor(
            path=self._path,
            getter=self._getter,
            setter=self._setter,
            to_wrapped_value=self._to_wrapped_value,
            to_json_value=self._to_json_value
        )

    def __build_doc_type_for_single(self) -> PathDescriptor:
        doc_type_transformer = DocTypeTransformer(self._type)

        if self._to_wrapped_value is do_nothing:
            self._to_wrapped_value = doc_type_transformer.to_wrapped_value

        if self._to_json_value is do_nothing:
            self._to_json_value = doc_type_transformer.to_json_value

        return self.__build_path_descriptor()

    def __build_doc_type_for_iterator(self) -> PathDescriptor:
        doc_list_type_transformer = DocListTypeTransformer(self._type)

        if self._to_wrapped_value is do_nothing:
            self._to_wrapped_value = doc_list_type_transformer.to_wrapped_value

        if self._to_json_value is do_nothing:
            self._to_json_value = doc_list_type_transformer.to_json_value

        return self.__build_path_descriptor()

    def __custom_type_for_single(self) -> PathDescriptor:
        return self.__build_path_descriptor()

    def __custom_type_for_iterator(self) -> PathDescriptor:
        pass
