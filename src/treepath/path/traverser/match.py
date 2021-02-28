from __future__ import annotations

from typing import Union

from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class Match:
    __slots__ = '_traverser_match'

    def __init__(self,
                 traverser_match: TraverserMatch,
                 ):
        self._traverser_match = traverser_match

    @property
    def path_as_list(self) -> list:
        return self._traverser_match.path_as_list

    @property
    def path(self) -> str:
        return self._traverser_match.path

    @property
    def parent(self) -> Union[Match, None]:
        parent = self._traverser_match.parent
        if parent:
            return Match(parent)
        else:
            return None

    @property
    def data_name(self) -> str:
        return self._traverser_match.data_name

    @property
    def data(self) -> Union[dict, list, str, int, float,  bool, None]:
        return self._traverser_match.data

    @property
    def vertex(self) -> Vertex:
        return self._traverser_match.vertex

    def __repr__(self):
        return repr(self._traverser_match)

    def __str__(self):
        return repr(self._traverser_match)
