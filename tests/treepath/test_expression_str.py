from treepath import exp, wildcard, wc


def test_root():
    expected = "$"
    actual = repr(exp)
    assert actual == expected


def test_root_a():
    root = exp
    expected = "$.a"
    actual = repr(root.a)
    assert actual == expected


def test_root_a_aa():
    root = exp
    expected = "$.a.aa"
    actual = repr(root.a.aa)
    assert actual == expected


def test_root_a_aa_aaa():
    root = exp
    expected = "$.a.aa.aaa"
    actual = repr(root.a.aa.aaa)
    assert actual == expected


def test_root_0():
    expected = "$[0]"
    actual = str(exp[0])
    assert actual == expected


def test_root_0_0():
    expected = "$[0][0]"
    actual = str(exp[0][0])
    assert actual == expected


def test_root_0_0_0():
    expected = "$[0][0][0]"
    actual = str(exp[0][0][0])
    assert actual == expected


def test_root_a_0():
    expected = "$.a[0]"
    actual = str(exp.a[0])
    assert actual == expected


def test_root_a_0_a():
    expected = "$.a[0].a"
    actual = str(exp.a[0].a)
    assert actual == expected


def test_root_slice_wild():
    expected = "$[:]"
    actual = str(exp[:])
    assert actual == expected


def test_root_slice_start():
    expected = "$[1:]"
    actual = str(exp[1:])
    assert actual == expected


def test_root_slice_stop():
    expected = "$[:1]"
    actual = str(exp[:1])
    assert actual == expected


def test_root_slice_start_stop():
    expected = "$[1:1]"
    actual = str(exp[1:1])
    assert actual == expected


def test_root_slice_start_step():
    expected = "$[1:6:3]"
    actual = str(exp[1:6:3])
    assert actual == expected


def test_root_list_wildcard():
    expected = "$[*]"
    actual = str(exp[wildcard])
    assert actual == expected


def test_root_a_list_wildcard():
    expected = "$.a[*]"
    actual = str(exp.a[wildcard])
    assert actual == expected


def test_root_list_wc():
    expected = "$[*]"
    actual = str(exp[wc])
    assert actual == expected


def test_root_a_list_wc():
    expected = "$.a[*]"
    actual = str(exp.a[wc])
    assert actual == expected


def test_root_wildcard():
    expected = "$.*"
    actual = str(exp.wildcard)
    assert actual == expected


def test_root_a_wildcard():
    expected = "$.a.*"
    actual = str(exp.a.wildcard)
    assert actual == expected


def test_root_wc():
    expected = "$.*"
    actual = str(exp.wc)
    assert actual == expected


def test_root_a_wc():
    expected = "$.a.*"
    actual = str(exp.a.wc)
    assert actual == expected


def test_root_recursive():
    expected = "$.."
    actual = str(exp.recursive)
    assert actual == expected


def test_root_a_recursive():
    expected = "$.a.."
    actual = str(exp.a.recursive)
    assert actual == expected


def test_root_recursive_a():
    expected = "$..a"
    actual = str(exp.recursive.a)
    assert actual == expected


def test_root_a_recursive_b():
    expected = "$.a..b"
    actual = str(exp.a.recursive.b)
    assert actual == expected


def test_root_rec():
    expected = "$.."
    actual = str(exp.rec)
    assert actual == expected


def test_root_a_rec():
    expected = "$.a.."
    actual = str(exp.a.rec)
    assert actual == expected
