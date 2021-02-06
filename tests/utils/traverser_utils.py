import pytest


class WildMatch():

    def __init__(self, name, _yield, iterate):
        self.name = name
        self._yield = _yield
        self._iterate = iterate

    def yield_(self, key):
        return self._yield

    def iterate(self, key):
        return self._iterate

    def __repr__(self):
        return self.name


class KeyMatch():

    def __init__(self, name, key, _yield, iterate, always_iterate):
        self.name = name
        self.key = key
        self._yield = _yield
        self._iterate = iterate
        self._always_iterate = always_iterate

    def yield_(self, key):
        return self._yield and self.key == key

    def iterate(self, key):
        return self._always_iterate or self._iterate and self.key == key

    def __repr__(self):
        return self.name


yaia = WildMatch("yaia", True, True)
naia = WildMatch("naia", False, True)

yxix = KeyMatch("yxix", "x", True, True, False)
yxia = KeyMatch("yxia", "x", True, False, True)
yxin = KeyMatch("yxin", "x", True, False, False)
nxix = KeyMatch("nxix", "x", False, True, False)

yyiy = KeyMatch("yyiy", "y", True, True, False)
yyia = KeyMatch("yyia", "y", True, False, True)
yyin = KeyMatch("yyin", "y", True, False, False)
nyiy = KeyMatch("nyiy", "y", False, True, False)

yziz = KeyMatch("yziz", "z", True, True, False)
yzia = KeyMatch("yzia", "z", True, False, True)
yzin = KeyMatch("yzin", "z", True, False, False)
nziz = KeyMatch("nziz", "z", False, True, False)

y0i0 = KeyMatch("y0i0", 0, True, True, False)
y0ia = KeyMatch("y0ia", 0, True, False, True)
y0in = KeyMatch("y0in", 0, True, False, False)
n0i0 = KeyMatch("n0i0", 0, False, True, False)

y1i1 = KeyMatch("y1i1", 1, True, True, False)
y1ia = KeyMatch("y1ia", 1, True, False, True)
y1in = KeyMatch("y1in", 1, True, False, False)
n1i1 = KeyMatch("n1i1", 1, False, True, False)

y2i2 = KeyMatch("y2i2", 2, True, True, False)
y2ia = KeyMatch("y2ia", 2, True, False, True)
y2in = KeyMatch("y2in", 2, True, False, False)
n2i2 = KeyMatch("n2i2", 2, False, True, False)


def get_iter(data):
    if isinstance(data, dict):
        return data.items()
    elif isinstance(data, list):
        return enumerate(data)
    else:
        return []


def path_item_name(data, name):
    if isinstance(data, dict):
        return f".{name}"
    elif isinstance(data, list):
        return f"[{name}]"
    else:
        raise StopIteration


def loop(level, path, data, *args):
    if not args:
        return
    match = args[0]
    args = args[1:]
    next_level = level + 1
    for name, value in get_iter(data):
        path[level] = path_item_name(data, name)
        path_str = "".join(i for i in path[0:level + 1])
        is_yield = match.yield_(name)
        is_iterate = match.iterate(name)
        if is_yield:
            yield path_str, value
        if is_iterate:
            yield from loop(next_level, path, value, *args)


def gen_test_data(data, *args):
    path = [i for i in range(20)]
    path[0] = "$"
    level = 1
    for item in loop(level, path, data, *args):
        yield item[0], item[1]


def assert_done_iterating(iterator):
    with pytest.raises(StopIteration):
        actual = next(iterator)
        print(f"Unexpected next {actual} expected StopIteration")
