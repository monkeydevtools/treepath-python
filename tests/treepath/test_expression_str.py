from treepath import path, wildcard, wc, has


def test_root():
    expected = "$"
    actual = repr(path)
    assert actual == expected


def test_root_a():
    root = path
    expected = "$.a"
    actual = repr(root.a)
    assert actual == expected


def test_root_a_aa():
    root = path
    expected = "$.a.aa"
    actual = repr(root.a.aa)
    assert actual == expected


def test_root_a_aa_aaa():
    root = path
    expected = "$.a.aa.aaa"
    actual = repr(root.a.aa.aaa)
    assert actual == expected


def test_root_0():
    expected = "$[0]"
    actual = str(path[0])
    assert actual == expected


def test_root_0_0():
    expected = "$[0][0]"
    actual = str(path[0][0])
    assert actual == expected


def test_root_0_0_0():
    expected = "$[0][0][0]"
    actual = str(path[0][0][0])
    assert actual == expected


def test_root_a_0():
    expected = "$.a[0]"
    actual = str(path.a[0])
    assert actual == expected


def test_root_a_0_a():
    expected = "$.a[0].a"
    actual = str(path.a[0].a)
    assert actual == expected


def test_root_slice_wild():
    expected = "$[:]"
    actual = str(path[:])
    assert actual == expected


def test_root_slice_start():
    expected = "$[1:]"
    actual = str(path[1:])
    assert actual == expected


def test_root_slice_stop():
    expected = "$[:1]"
    actual = str(path[:1])
    assert actual == expected


def test_root_slice_start_stop():
    expected = "$[1:1]"
    actual = str(path[1:1])
    assert actual == expected


def test_root_slice_start_step():
    expected = "$[1:6:3]"
    actual = str(path[1:6:3])
    assert actual == expected


def test_root_list_wildcard():
    expected = "$[*]"
    actual = str(path[wildcard])
    assert actual == expected


def test_root_a_list_wildcard():
    expected = "$.a[*]"
    actual = str(path.a[wildcard])
    assert actual == expected


def test_root_list_wc():
    expected = "$[*]"
    actual = str(path[wc])
    assert actual == expected


def test_root_a_list_wc():
    expected = "$.a[*]"
    actual = str(path.a[wc])
    assert actual == expected


def test_root_wildcard():
    expected = "$.*"
    actual = str(path.wildcard)
    assert actual == expected


def test_root_a_wildcard():
    expected = "$.a.*"
    actual = str(path.a.wildcard)
    assert actual == expected


def test_root_wc():
    expected = "$.*"
    actual = str(path.wc)
    assert actual == expected


def test_root_a_wc():
    expected = "$.a.*"
    actual = str(path.a.wc)
    assert actual == expected


def test_root_recursive():
    expected = "$.."
    actual = str(path.recursive)
    assert actual == expected


def test_root_a_recursive():
    expected = "$.a.."
    actual = str(path.a.recursive)
    assert actual == expected


def test_root_recursive_a():
    expected = "$..a"
    actual = str(path.recursive.a)
    assert actual == expected


def test_root_a_recursive_b():
    expected = "$.a..b"
    actual = str(path.a.recursive.b)
    assert actual == expected


def test_root_rec():
    expected = "$.."
    actual = str(path.rec)
    assert actual == expected


def test_root_a_rec():
    expected = "$.a.."
    actual = str(path.a.rec)
    assert actual == expected


def test_root_a_has_b():
    expected = "$.a[has($.b)]"
    actual = str(path.a[has(path.b)])
    assert actual == expected


def test_root_a_has_b_lt():
    expected = "$.a[has($.b < 1)]"
    actual = str(path.a[has(path.b < 1)])
    assert actual == expected


def test_root_a_has_b_le():
    expected = "$.a[has($.b <= 1)]"
    actual = str(path.a[has(path.b <= 1)])
    assert actual == expected


def test_root_a_has_b_eq():
    expected = "$.a[has($.b == 1)]"
    actual = str(path.a[has(path.b == 1)])
    assert actual == expected


def test_root_a_has_b_ne():
    expected = "$.a[has($.b != 1)]"
    actual = str(path.a[has(path.b != 1)])
    assert actual == expected


def test_root_a_has_b_gt():
    expected = "$.a[has($.b > 1)]"
    actual = str(path.a[has(path.b > 1)])
    assert actual == expected


def test_root_a_has_b_ge():
    expected = "$.a[has($.b >= 1)]"
    actual = str(path.a[has(path.b >= 1)])
    assert actual == expected


def test_root_a_has_b_one_func():
    expected = f"$.a[has($.b, {int})]"
    actual = str(path.a[has(path.b, int)])
    assert actual == expected


def test_root_a_has_b_two_func():
    expected = f"$.a[has($.b, {float}, {float})]"
    actual = str(path.a[has(path.b, float, float)])
    assert actual == expected


def test_root_a_has_b_three_func():
    expected = f"$.a[has($.b, {test_root_a_has_b_three_func}, {test_root_a_has_b_three_func}, {test_root_a_has_b_three_func})]"
    actual = str(
        path.a[has(path.b, test_root_a_has_b_three_func, test_root_a_has_b_three_func, test_root_a_has_b_three_func)])
    assert actual == expected


def test_root_a_has_b_eq_one_func():
    expected = f"$.a[has($.b == 1, {int})]"
    actual = str(path.a[has(path.b == 1, int)])
    assert actual == expected