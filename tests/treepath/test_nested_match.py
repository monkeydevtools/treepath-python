from treepath import get, path, get_match, find, find_matches


def test_nested_get(keys):
    expected = "16"
    actual = get_match(path.y.z, keys)
    actual = get(path.x, actual)
    assert actual == expected


def test_nested_find(keys):
    expected = ['13', '14', '15']
    actual = get_match(path.y.y, keys)
    actual = [v for v in find(path.wc, actual)]
    assert actual == expected


def test_nested_get_match(keys):
    expected = "$.y.z.x=16"
    actual = get_match(path.y.z, keys)
    actual = get_match(path.x, actual)
    assert repr(actual) == expected


def test_nested_find_matches(keys):
    expected = "[$.y.y.x=13, $.y.y.y=14, $.y.y.z=15]"
    actual = get_match(path.y.y, keys)
    actual = [v for v in find_matches(path.wc, actual)]
    assert repr(actual) == expected
