from treepath.path.exceptions.traversing_error import TraversingError


class InfiniteLoopDetected(TraversingError):
    """InfiniteLoopDetected is raised when the next is detect to be in a infinite loop."""

