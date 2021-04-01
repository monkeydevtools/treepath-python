from treepath import rec, wc


def test_symbol_on_rec_string():
    expected = "recursive"
    assert repr(rec) == expected


def test_symbol_on_wc_string():
    expected = "wildcard"
    assert repr(wc) == expected
