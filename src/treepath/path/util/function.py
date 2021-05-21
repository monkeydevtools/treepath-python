from typing import List


def create_partial_operator(operator_, right):
    def partial_operator_(left):
        return operator_(left, right)

    return partial_operator_


def enumerate_slice(_slice: slice, _list: List):
    indices = _slice.indices(len(_list))
    slice_range = iter(range(*indices))

    def slice_enumerate(item):
        return next(slice_range), item

    return map(slice_enumerate, _list[_slice])
