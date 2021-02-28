from treepath.path.exceptions.treepath_exception import TreepathException


class MatchNotFoundError(TreepathException, LookupError):
    """
    MatchNotFoundError is raised when a get_match is expected; however, the data structure has no more element to traverse
    """

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"No get_match occurred on path: {path}"
