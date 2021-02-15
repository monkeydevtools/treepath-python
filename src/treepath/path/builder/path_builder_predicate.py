import operator


def create_partial_operator(operator_, b):
    def partial_operator_(a):
        return operator_(a, b)

    return partial_operator_


class PathBuilderPredicate:
    __slots__ = ()

    def __lt__(self, other):
        operator_ = create_partial_operator(operator.__lt__, other)
        return self, operator_

    def __le__(self, other):
        operator_ = create_partial_operator(operator.__le__, other)
        return self, operator_

    def __eq__(self, other):
        operator_ = create_partial_operator(operator.__eq__, other)
        return self, operator_

    def __ne__(self, other):
        operator_ = create_partial_operator(operator.__ne__, other)
        return self, operator_

    def __gt__(self, other):
        operator_ = create_partial_operator(operator.__gt__, other)
        return self, operator_

    def __ge__(self, other):
        operator_ = create_partial_operator(operator.__ge__, other)
        return self, operator_
