from __future__ import annotations

from typing import Callable, Union, Optional

from treepath.descriptor.path_descriptor import PathDescriptor, T
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.traverser.traverser_functions import get, set_, find, get_match, find_matches, set_match
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing


def path_descriptor(path: Optional[PathBuilder] = None,
                    getter: Union[get, find, get_match, find_matches] = get,
                    setter: Union[set_, set_match] = set_,
                    validator: Callable[[JsonTypes], None] = do_nothing
                    ):
    return PathDescriptor[T](path, getter, setter, validator)
