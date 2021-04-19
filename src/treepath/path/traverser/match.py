from typing import Union, List, Any

from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class Match:
    """

    """
    __slots__ = '_traverser_match'

    def __init__(self,
                 traverser_match: TraverserMatch,
                 ):
        self._traverser_match = traverser_match

    @property
    def path_as_list(self) -> List[Any]:
        """

        """
        return [Match(traverser_match) for traverser_match in self._traverser_match.path_as_list]

    @property
    def path(self) -> str:
        """

        """
        return self._traverser_match.path

    @property
    def path_segment(self):
        """

        """
        return self._traverser_match.path_segment

    @property
    def parent(self) -> Union[Any, None]:
        """

        """
        parent = self._traverser_match.parent
        if parent:
            return Match(parent)
        else:
            return None

    @property
    def data_name(self) -> Union[str, int]:
        """

        """
        return self._traverser_match.data_name

    @property
    def data(self) -> Union[dict, list, str, int, float, bool, None]:
        """

        """
        return self._traverser_match.data

    @property
    def vertex(self) -> Vertex:
        """

        """
        return self._traverser_match.vertex

    def __repr__(self):
        return repr(self._traverser_match)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self is other \
               or isinstance(other, Match) and \
               ((self._traverser_match is other._traverser_match)
                or (self.data == other.data) and (self.parent == other.parent)
                )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.path)
