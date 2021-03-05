def create_partial_operator(operator_, b):
    def partial_operator_(a):
        return operator_(a, b)

    return partial_operator_


class AbstractPathBuilder:
    __slots__ = ()

    def create_path_builder(self, *args, **kwargs):
        pass

    def tranform_attribute_name(self, name):
        pass
