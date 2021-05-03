from treepath.path.exceptions.treepath_exception import TreepathException


class MatchNotFoundError(TreepathException, LookupError):
    """
    MatchNotFoundError is raised when get_match query fails to generate a result for the specified path.
    """

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"MatchNotFoundError(No get_match occurred on path: {path})"
