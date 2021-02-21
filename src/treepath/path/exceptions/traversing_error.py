import os

from treepath.path.exceptions.treepath_exception import TreepathException
from treepath.path.traverser.match import Match
from treepath.path.traverser.traverser_state_match import TraverserStateMatch


class TraversingError(TreepathException, RuntimeError):
    """TraversingError is raised when path expression cannot traverse the data structure"""

    def __init__(self, match: TraverserStateMatch, error_msg):
        self.match = Match(match)
        self.error_msg = error_msg
        super().__init__(match.vertex)

    def _resolve_msg(self):
        path = repr(self.vertex)
        match = repr(self.match)
        return f"""{self.error_msg}{os.linesep}  path: {path}{os.linesep}  match: {match}"""
