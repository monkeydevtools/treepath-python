from __future__ import annotations

from typing import Type, Callable, Union, Optional, Any

from treepath.descriptor.document import Document
from treepath.descriptor.path_descriptor import PathDescriptor
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_, find, get_match, find_matches, set_match
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing


def from_document(value: Document) -> JsonTypes:
    return value.data


def path_descriptor(path: Optional[PathBuilder] = None,
                    getter: Union[get, find, get_match, find_matches] = get,
                    setter: Union[set_, set_match] = set_,
                    validator: Callable[[JsonTypes], None] = do_nothing,
                    getter_type: Callable[[JsonTypes], Any] = do_nothing,
                    setter_type: Callable[[Any], JsonTypes] = do_nothing
                    ):
    return PathDescriptor(
        path=path,
        getter=getter,
        setter=setter,
        validator=validator,
        getter_type=getter_type,
        setter_type=setter_type,
    )


def path_descriptor_doc_typed(path: PathBuilder,
                              getter_type: Type[Document],
                              validator: Callable[[JsonTypes], None] = do_nothing,
                              ):
    return PathDescriptor(
        path=path,
        getter=get_match,
        validator=validator,
        getter_type=getter_type,
        setter_type=from_document
    )
