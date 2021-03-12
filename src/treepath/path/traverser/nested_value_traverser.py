from typing import Union

from treepath.path.traverser.nested_match_traverser import NestedMatchTraverser


class NestedValueTraverser(NestedMatchTraverser):
    __slots__ = ()

    def __next__(self) -> Union[dict, list, str, int, float, bool, None]:
        return super().__next__().data
