from typing import Union, List, Any

from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.vertex.vertex import Vertex


class Match:
    """
    The Match Class contains all the details that describe the Match.
    """
    __slots__ = '_traverser_match'

    def __init__(self,
                 traverser_match: TraverserMatch,
                 ):
        self._traverser_match = traverser_match

    @property
    def path_as_list(self) -> List[Any]:
        """
        Returns a list containing this Mtch and all the ancestor matches.  The list is order from root to this Match.
        """
        return [Match(traverser_match) for traverser_match in self._traverser_match.path_as_list]

    @property
    def path(self) -> str:
        """
        Returns the str representation of the absolute path for this match.  For example $.a.b[0]
        """
        return self._traverser_match.path

    @property
    def path_segment(self):
        """
        Returns the str representation of the segment in the path this Match represents.   This is different from
        data_name in that it includes additional symbols.  For example if data_name is a list index of '1' then path
        segment is '[1]'
        """
        return self._traverser_match.path_segment

    @property
    def parent(self) -> Union[Any, None]:
        """
        Returns the parent Match.
        """
        parent = self._traverser_match.parent
        if parent:
            return Match(parent)
        else:
            return None

    @property
    def data_name(self) -> Union[str, int]:
        """
        Return the dictionary key or the list index this Match represents.
        """
        return self._traverser_match.data_name

    @property
    def data(self) -> Union[dict, list, str, int, float, bool, None]:
        """
        Return the value the data_name references.
        """
        return self._traverser_match.data

    @property
    def vertex(self) -> Vertex:
        """
        Returns the path vertex that generated this match.
        """
        return self._traverser_match.vertex

    def __repr__(self):
        """
        Return  the match in the format f"{self.path}=={self.data}"
        """
        return repr(self._traverser_match)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        """
        Return True if other Match data_name, data and parent are all equal.
        """
        return (
                self is other
                or (
                        isinstance(other, Match)
                        and (
                                self._traverser_match is other._traverser_match
                                or (
                                        self.data == other.data
                                        and self.data_name == other.data_name
                                        and self.parent == other.parent
                                )
                        )
                )
        )

    def __ne__(self, other):
        return not self.__eq__(other)
