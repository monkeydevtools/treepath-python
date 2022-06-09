from typing import TypeVar, Generic, Callable, List

from treepath.descriptor.document import Document
from treepath.path.typing.json_types import JsonTypes
from treepath.path.utils.function import do_nothing

T = TypeVar('T')


class DocumentList(Generic[T], Document):
    __slots__ = "_data", "_to_wrapped_value", "_to_json_value"

    def __init__(self,
                 data: List[JsonTypes],
                 *,
                 to_wrapped_value: Callable[[JsonTypes], T] = do_nothing,
                 to_json_value: Callable[[T], JsonTypes] = do_nothing):
        super().__init__(data)
        self._to_wrapped_value = to_wrapped_value
        self._to_json_value = to_json_value

    def __iter__(self) -> T:
        class _Iterator(Generic[T]):
            __slots__ = "_iterator", "_to_wrapped_value"

            def __init__(self, iterator, to_wrapped_value):
                self._to_wrapped_value = to_wrapped_value
                self._iterator = iterator

            def __next__(self) -> T:
                json_value = next(self._iterator)
                return self._to_wrapped_value(json_value)

        return _Iterator[T](iter(self._data), self._to_wrapped_value)

    def __getitem__(self, index: int) -> T:
        json_value = self.data[index]
        wrapped_value = self._to_wrapped_value(json_value)
        return wrapped_value

    def __setitem__(self, index: int, wrapped_value: T):
        json_value = self._to_json_value(wrapped_value)
        self.data[index] = json_value

    def __len__(self) -> int:
        return len(self.data)

    def __delitem__(self, index):
        del self.data[index]

    def __contains__(self, wrapped_value: T):
        json_value = self._to_json_value(wrapped_value)
        return json_value in self.data

    def append(self, wrapped_value: T):
        json_value = self._to_json_value(wrapped_value)
        self.data.append(json_value)

    def pop(self, index: int) -> T:
        json_value = self.data.pop(index)
        wrapped_value = self._to_wrapped_value(json_value)
        return wrapped_value

    def remove_all(self, is_remove: Callable[[T], bool]):
        def is_not_keep(arg):
            return not is_remove(arg)

        self.keep_all(is_not_keep)

    def keep_all(self, is_keep: Callable[[T], bool]):
        data = self.data
        original_length = len(data)
        last_index = -1
        for last_index, json_value in enumerate(map(self._to_json_value, filter(is_keep, self))):
            data[last_index] = json_value
        for index in range(last_index + 1, original_length):
            data.pop()
