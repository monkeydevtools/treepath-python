def create_partial_operator(operator_, right):
    def partial_operator_(left):
        return operator_(left, right)

    return partial_operator_


def tuple_iterable(tuple_: tuple):
    for entry in tuple_:
        yield str(entry)
