from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Union, List

from treepath.path.exceptions.pop_error import PopError
from treepath.path.traverser.traverser_match import TraverserMatch
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.not_set import not_set

if TYPE_CHECKING:
    from treepath.path.builder.path_builder import PathBuilder  # pragma: no cover


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
    def path(self) -> PathBuilder:
        """
        Returns the explicit path that points to this match
        """
        from treepath.path.utils.match_to_path import match_to_path
        return match_to_path(self)

    @property
    def path_match_list(self) -> List[Match]:
        """
        Returns a list containing this Match and all the ancestor matches.  The list is ordered from root to this Match.
        """
        return [Match(traverser_match) for traverser_match in self._traverser_match.path_match_list]

    @property
    def path_as_str(self) -> str:
        """
        Returns the str representation of the absolute path for this match.  For example $.a.b[0]
        """
        return self._traverser_match.path_as_str

    @property
    def path_segment(self) -> str:
        """
        Returns the str representation of the segment in the path this Match represents.   This is different from
        data_name in that it includes additional symbols.  For example if data_name is a list index of '1' then path
        segment is '[1]'
        """
        return self._traverser_match.path_segment

    @property
    def parent(self) -> Union[Match, None]:
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
    def data(self) -> JsonTypes:
        """
        Return the value the data_name references.
        """
        return self._traverser_match.data

    @data.setter
    def data(self, value: JsonTypes):
        """
        Set the value the data_name references.
        """
        traverser_match = self._traverser_match
        parent_traverser_match = traverser_match.parent
        parent_traverser_match.data[traverser_match.data_name] = value
        traverser_match.data = value

    @data.deleter
    def data(self):
        """
        Remove the data_name references.
        @raise PopError:  Raised when the reference does not exist
        """
        traverser_match = self._traverser_match
        parent_traverser_match = traverser_match.parent
        try:
            del parent_traverser_match.data[traverser_match.data_name]
            traverser_match.data = None
        except LookupError:
            raise PopError(
                self._traverser_match.vertex,
                f"The reference data[{repr(self.data_name)}] does not exist.  Unable to del",
                ""
            )

    def pop(self, default=not_set) -> JsonTypes:
        """
        Remove the data_name references.
        @param default:  An optional value to return when no result is found.
        @raise PopError:  Raised when the reference does not exist and default is not set.
        """
        try:
            old_data = self.data
            del self.data
            return old_data
        except PopError as e:
            if default is not_set:
                raise e
            else:
                return default

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
