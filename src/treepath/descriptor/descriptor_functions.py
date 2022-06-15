from __future__ import annotations

from typing import Callable, Union, Any, Type, Optional

from treepath.descriptor.descriptor_builder import DescriptorBuilder
from treepath.descriptor.path_descriptor import PathDescriptor
from treepath.descriptor.path_descriptor import T
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_, find, get_match, find_matches, set_match
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing


def attr(path: Optional[PathBuilder] = None,
         *,
         getter: Union[get, find, get_match, find_matches] = get,
         setter: Union[set_, set_match] = set_,
         to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
         to_json_value: Callable[[Any], JsonTypes] = do_nothing
         ) -> PathDescriptor[T]:
    return PathDescriptor(
        path=path,
        getter=getter,
        setter=setter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
    )


def attr_typed(type_: Type[T],
               path: Optional[PathBuilder] = None,
               *,
               getter: Union[get, find, get_match, find_matches] = get,
               setter: Union[set_, set_match] = set_,
               to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
               to_json_value: Callable[[Any], JsonTypes] = do_nothing
               ) -> PathDescriptor[T]:
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        path=path,
        getter=getter,
        setter=setter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
    )
    return descriptor_builder.build_single()


def attr_iter_typed(type_: Type[T],
                    path: Optional[PathBuilder] = None,
                    *,
                    getter: Union[find, find_matches] = find,
                    to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
                    ) -> PathDescriptor[T]:
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        path=path,
        getter=getter,
        to_wrapped_value=to_wrapped_value,
    )
    return descriptor_builder.build_iterator()


def attr_list_typed(type_: Type[T],
                    path: Optional[PathBuilder] = None,
                    *,
                    getter: Union[get, get_match] = get,
                    to_wrapped_value: Callable[[JsonTypes], Any] = do_nothing,
                    to_json_value: Callable[[Any], JsonTypes] = do_nothing
                    ) -> PathDescriptor[T]:
    descriptor_builder = DescriptorBuilder(
        type_=type_,
        path=path,
        getter=getter,
        to_wrapped_value=to_wrapped_value,
        to_json_value=to_json_value,
        is_for_json_list=True
    )
    return descriptor_builder.build_list()
