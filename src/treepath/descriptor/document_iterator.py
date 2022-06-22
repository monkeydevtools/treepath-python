from typing import TypeVar, Generic, Callable, Iterable

from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing

T = TypeVar('T')


class DocumentIterator(Generic[T]):
    """
    DocumentIterator decorates a json iterator.  The  DocumentIterator marshals each entry in the json iterator
    before return it to the caller.
    """
    __slots__ = "_iterable", "_to_wrapped_value"

    def __init__(self,
                 iterable: Iterable[JsonTypes],
                 *,
                 to_wrapped_value: Callable[[JsonTypes], T] = do_nothing):
        self._iterable = iterable
        self._to_wrapped_value = to_wrapped_value

    def __iter__(self) -> T:
        class _Iterator(Generic[T]):
            __slots__ = "_iterator", "_to_wrapped_value"

            def __init__(self, iterator, to_wrapped_value):
                self._to_wrapped_value = to_wrapped_value
                self._iterator = iterator

            def __next__(self) -> T:
                json_value = next(self._iterator)
                return self._to_wrapped_value(json_value)

        return _Iterator[T](iter(self._iterable), self._to_wrapped_value)
