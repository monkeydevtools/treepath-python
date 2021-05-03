from treepath.path.exceptions.traversing_error import TraversingError


class InfiniteLoopDetected(TraversingError):
    """
    InfiniteLoopDetected is raised if a infinite loop is detected while traversing the tree searching for the path.
    This uselessly occurs if the next(...) takes excessive amount of time to return.  Most likely the cause is the
    data-structure is not a tree but is actually a graph with a cyclical dependency.
    """

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"InfiniteLoopDetected(Traversing seems to go on for ever on path: {path})"
