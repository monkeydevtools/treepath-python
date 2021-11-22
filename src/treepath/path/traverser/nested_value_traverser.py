from typing import Union

from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser
from treepath.path.typing_alias import JsonTypes


class NestedValueTraverser(NestedMatchTraverser):
    __slots__ = ()

    def __next__(self) -> JsonTypes:
        return super().__next__().data
