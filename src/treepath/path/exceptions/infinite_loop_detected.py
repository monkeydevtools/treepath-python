from treepath.path.exceptions.traversing_error import TraversingError


class InfiniteLoopDetected(TraversingError):
    """InfiniteLoopDetected is raised when the next is detect to be in a infinite loop."""

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"InfiniteLoopDetected(Traversing seems to go on for ever on path: {path})"
