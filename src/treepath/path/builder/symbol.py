class Symbol:
    __slots__ = 'name'

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
