from treepath.path.exceptions.treepath_exception import TreepathException


class StopTraversing(TreepathException, StopIteration):
    """StopTraversing is raised when the data structure has no more element to traverse."""

    def _resolve_msg(self):
        path = repr(self.vertex)
        return f"StopTraversing(Traversing has completed on path: {path})"
