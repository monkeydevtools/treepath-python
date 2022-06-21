from __future__ import annotations

from typing import Callable, Union, Any, Type, Optional, List, Generic

from treepath.descriptor.document import Document
from treepath.descriptor.document_iterator import DocumentIterator
from treepath.descriptor.document_list import DocumentList
from treepath.descriptor.path_descriptor import T, PathDescriptor
from treepath.path.builder.path_builder import PathBuilder, get_vertex_from_path_builder
from treepath.path.exceptions.set_error import SetError
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


class DocTypeIteratorTransformer(Generic[T]):
    __slots__ = '_path', '_to_wrapped_value'

    def __init__(self, path, to_wrapped_value):
        self._path = path
        self._to_wrapped_value = to_wrapped_value

    def to_wrapped_value(self, inner_iterator) -> DocumentIterator[T]:
        outer_iterator = DocumentIterator[T](inner_iterator, to_wrapped_value=self._to_wrapped_value)
        return outer_iterator

    def to_json_value(self, doc: Document):
        vertex = get_vertex_from_path_builder(self._path)
        raise SetError(
            vertex,
            f"The iterator descriptor for path '{self._path}' does not support set",
            vertex.path_segment
        )


class DocTypeListTransformer(Generic[T]):
    __slots__ = '_to_wrapped_value', '_to_json_value'

    def __init__(self, to_wrapped_value, to_json_value):
        self._to_wrapped_value = to_wrapped_value
        self._to_json_value = to_json_value

    def to_wrapped_value(self, list_: List[JsonTypes]) -> DocumentList[T]:
        outer_iterator = DocumentList[T](
            list_,
            to_wrapped_value=self._to_wrapped_value,
            to_json_value=self._to_json_value
        )
        return outer_iterator

    def to_json_value(self, doc: DocumentList[T]):
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
                 to_json_value: Callable[[Any], JsonTypes] = do_nothing,
                 is_for_json_list=False
                 ):
        self._type = type_
        self._path = path
        self._getter = getter
        self._setter = setter
        self._to_wrapped_value = to_wrapped_value
        self._to_json_value = to_json_value
        self._is_for_json_list = is_for_json_list
        self.__build = [
            [
                self.__build_doc_type_for_single,
                self.__build_doc_type_for_iterator,
                self.__build_doc_type_for_list
            ],
            [
                self.__custom_type_for_single,
                self.__custom_type_for_iterator,
                self.__custom_type_for_list,
            ],
        ]

    def build_single(self) -> PathDescriptor:
        type_index = self.__index_for_type_column()
        return self.__build[type_index][0]()

    def build_iterator(self) -> PathDescriptor:
        type_index = self.__index_for_type_column()
        return self.__build[type_index][1]()

    def build_list(self) -> PathDescriptor:
        type_index = self.__index_for_type_column()
        return self.__build[type_index][2]()

    def __index_for_type_column(self) -> int:
        if issubclass(self._type, Document):
            return 0
        else:
            return 1

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
        self._to_wrapped_value = doc_type_transformer.to_wrapped_value
        self._to_json_value = doc_type_transformer.to_json_value
        return self.__build_path_descriptor()

    def __build_doc_type_for_iterator(self) -> PathDescriptor:
        doc_type_transformer = DocTypeTransformer(self._type)
        doc_list_type_transformer = DocTypeIteratorTransformer(self._path, doc_type_transformer.to_wrapped_value)
        self._to_wrapped_value = doc_list_type_transformer.to_wrapped_value
        self._to_json_value = doc_list_type_transformer.to_json_value
        return self.__build_path_descriptor()

    def __build_doc_type_for_list(self) -> PathDescriptor:
        doc_type_transformer = DocTypeTransformer(self._type)
        doc_list_type_transformer = DocTypeListTransformer(
            doc_type_transformer.to_wrapped_value,
            doc_type_transformer.to_json_value
        )
        self._to_wrapped_value = doc_list_type_transformer.to_wrapped_value
        self._to_json_value = doc_list_type_transformer.to_json_value
        return self.__build_path_descriptor()

    def __custom_type_for_single(self) -> PathDescriptor:
        return self.__build_path_descriptor()

    def __custom_type_for_iterator(self) -> PathDescriptor:
        doc_list_type_transformer = DocTypeIteratorTransformer(self._path, self._to_wrapped_value)
        self._to_wrapped_value = doc_list_type_transformer.to_wrapped_value
        self._to_json_value = doc_list_type_transformer.to_json_value

        return self.__build_path_descriptor()

    def __custom_type_for_list(self) -> PathDescriptor:
        doc_list_type_transformer = DocTypeListTransformer(
            self._to_wrapped_value,
            self._to_json_value
        )
        self._to_wrapped_value = doc_list_type_transformer.to_wrapped_value
        self._to_json_value = doc_list_type_transformer.to_json_value
        return self.__build_path_descriptor()
