import json

from treepath import Document


def test_document_when_set_data_then_remember():
    class TDoc(Document):
        pass

    td = TDoc({})

    expected = {"a": 1}
    assert td.data is not expected
    td.data = expected
    assert td.data is expected


def test_document_when_json_str_then_correct():
    class TDoc(Document):
        pass

    expected = '{"a": 1}'
    td = TDoc(json.loads(expected))
    assert td.json_str == expected
    assert repr(td) == expected


def test_document_when_pretty_json_str_then_correct():
    class TDoc(Document):
        pass

    expected = '{\n  "a": 1\n}'
    td = TDoc(json.loads(expected))
    assert td.pretty_json_str == expected


def test_document_when_repr_then_correct():
    class TDoc(Document):
        pass

    expected = '{"a": 1}'
    td = TDoc(json.loads(expected))
    assert repr(td) == expected


def test_document_when_str_then_correct():
    class TDoc(Document):
        pass

    expected = 'TDoc: json: {\n  "a": 1\n}'
    td = TDoc({"a": 1})
    assert str(td) == expected


def test_document_when_equal_then_correct():
    class TDoc(Document):
        pass

    left = TDoc({"a": 1})
    right = TDoc({"a": 1})
    assert left == right


def test_document_when_not_equal_then_correct():
    class TDoc(Document):
        pass

    left = TDoc({"a": 1})
    right = TDoc({"a": 2})
    assert left != right
