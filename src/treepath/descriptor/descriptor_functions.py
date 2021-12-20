from typing import Callable

from treepath.path.builder.path_builder import PathBuilder
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing
from treepath.path.utils.not_set import not_set


def path_descriptor(
        path: PathBuilder = None,
        default=not_set,
        cascade: bool = False,
        validator: Callable[[JsonTypes], None] = do_nothing
):
    ...