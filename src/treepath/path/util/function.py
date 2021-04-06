def create_partial_operator(operator_, right):
    def partial_operator_(left):
        return operator_(left, right)

    return partial_operator_
