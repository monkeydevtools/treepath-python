from typing import Any

from treepath import path, get, find, log_to, has, Match, has_any, has_all


def test_keys_get_x_y_z_trace(keys):
    expected_trace_messages = [
        " at $.x got {'x': {'x': '1', 'y'...",
        " at $.x.y got {'x': '4', 'y': '5',...",
        " at $.x.y.z got '6'"
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    expected = keys["x"]["y"]["z"]
    actual = get(path.x.y.z, keys, trace=log_to(mock_print))
    assert actual == expected

    assert actual_trace_messages == expected_trace_messages


def test_keys_find_x_y_z_trace(keys):
    expected_trace_messages = [
        " at $.x got {'x': {'x': '1', 'y'...",
        " at $.x.y got {'x': '4', 'y': '5',...",
        " at $.x.y.z got '6'"
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    expected = keys["x"]["y"]["z"]
    for actual in find(path.x.y.z, keys, trace=log_to(mock_print)):
        assert actual == expected
        assert actual_trace_messages == expected_trace_messages


def test_keys_find_x_a_z_trace(keys):
    expected_trace_messages = [
        " at $.x got {'x': {'x': '1', 'y'...",
        ' at $.x.a got no match'
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    for _ in find(path.x.a.z, keys, trace=log_to(mock_print)):
        pass

    assert actual_trace_messages == expected_trace_messages


def test_keys_find_z_y_has_z_then_x_trace(keys):
    expected_trace_messages = [
        " at $.z got {'x': {'x': '19', 'y...",
        " at $.z.y got {'x': '22', 'y': '23...",
        "     has .z got '24'",
        " at $.z.y[has($.z)] got {'x': '22', 'y': '23...",
        " at $.z.y.x got '22'"
    ]

    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    for _ in find(path.z.y[has(path.z)].x, keys, trace=log_to(mock_print)):
        pass

    assert actual_trace_messages == expected_trace_messages


def test_keys_find_z_y_has_a_then_no_match_trace(keys):
    expected_trace_messages = [
        " at $.z got {'x': {'x': '19', 'y...",
        " at $.z.y got {'x': '22', 'y': '23...",
        '     has .a got no match',
        ' at $.z.y[has($.a)] got no match'
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    for _ in find(path.z.y[has(path.a)].x, keys, trace=log_to(mock_print)):
        pass

    assert actual_trace_messages == expected_trace_messages


def test_keys_find_rec_x_trace(keys):
    expected_trace_messages = [
        " at $.x got {'x': {'x': '1', 'y'...",
        " at $.x. got {'x': {'x': '1', 'y'...",
        " at $.x.x got {'x': '1', 'y': '2',...",
        " at $.x. got {'x': '1', 'y': '2',...",
        " at $.x.x.x got '1'",
        " at $.x.x. got '1'",
        ' at $.x.x.x. got no match',
        " at $.x.x. got '2'",
        ' at $.x.x.y. got no match',
        " at $.x.x. got '3'",
        ' at $.x.x.z. got no match',
        ' at $.x.x. got no match',
        " at $.x. got {'x': '4', 'y': '5',...",
        " at $.x.y.x got '4'",
        " at $.x.y. got '4'",
        ' at $.x.y.x. got no match',
        " at $.x.y. got '5'",
        ' at $.x.y.y. got no match',
        " at $.x.y. got '6'",
        ' at $.x.y.z. got no match',
        ' at $.x.y. got no match',
        " at $.x. got {'x': '7', 'y': '8',...",
        " at $.x.z.x got '7'",
        " at $.x.z. got '7'",
        ' at $.x.z.x. got no match',
        " at $.x.z. got '8'",
        ' at $.x.z.y. got no match',
        " at $.x.z. got '9'",
        ' at $.x.z.z. got no match',
        ' at $.x.z. got no match',
        ' at $.x. got no match'
    ]

    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    for _ in find(path.x.rec.x, keys, trace=log_to(mock_print)):
        pass

    assert actual_trace_messages == expected_trace_messages


def test_a_k_k_a_k_k_k_a_multiple_has(a_k_k_a_k_k_k_a):
    expected_trace_messages = [
        " at $[0] got {'x': {'x': [{'x': {...",
        "    has .x got {'x': [{'x': {'x': {...",
        "    has .x.x got [{'x': {'x': {'x': [...",
        "    has .x.x[1] got {'x': {'x': {'x': ['...",
        " at $[0][has($.x.x[1])] got {'x': {'x': [{'x': {...",
        " at $[0].y got {'x': [{'x': {'x': {...",
        " at $[0].y.y got [{'x': {'x': {'x': [...",
        " at $[0].y.y[0] got {'x': {'x': {'x': ['...",
        "           has .x got {'x': {'x': ['973', ...",
        "           has .x.x got {'x': ['973', '974',...",
        "               has .z got ['979', '980', '981'...",
        "           has .x.x[has($.z)] got {'x': ['973', '974',...",
        "           has .x.x.x got ['973', '974', '975'...",
        "           has .x.x.x[1] got '974'",
        " at $[0].y.y[0][has($.x.x[has($.z)].x[1])] got {'x': {'x': {'x': ['...",
        " at $[0].y.y[0].y got {'x': {'x': ['1000',...",
        " at $[0].y.y[0].y.y got {'x': ['1009', '1010...",
        " at $[0].y.y[0].y.y.y got ['1012', '1013', '10...",
        " at $[0].y.y[0].y.y.y[0] got '1012'"
    ]

    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    a = get(path[0][has(path.x.x[1])].y.y[0][has(path.x.x[has(path.z)].x[1])].y.y.y[0], a_k_k_a_k_k_k_a,
            trace=log_to(mock_print))
    assert a == '1012'
    assert actual_trace_messages == expected_trace_messages


def test_keys_find_x_has_x_eq_1_and_has_y_trace(keys):
    expected_trace_messages = [
        " at $.x got {'x': {'x': '1', 'y'...",
        "   has .z got {'x': '7', 'y': '8',...",
        " at $.x[has($.z)] got {'x': {'x': '1', 'y'...",
        " at $.x.x got {'x': '1', 'y': '2',...",
        "     has .x got '1'",
        "     has .y got '2'",
        " at $.x.x[has($.x == 1, <class 'int'>), has($.y)] got {'x': '1', 'y': "
        "'2',...",
        " at $.x.x.x got '1'"
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    @has.these((path.x == 1, int), path.y)
    def predicate(parent_match: Match, x, y) -> Any:
        return x(parent_match) and y(parent_match)

    compiled_one = path.x[has(path.z)].x[predicate].x
    get(compiled_one, keys, trace=log_to(mock_print))

    assert actual_trace_messages == expected_trace_messages


def test_keys_get_root_has_a_or_b_or_z_trace(keys):
    expected_trace_messages = [
        ' has .a got no match',
        ' has .b got no match',
        " has .z got {'x': {'x': '19', 'y...",
        " at $[has($.a) or has($.b) or has($.z)] got {'x': {'x': {'x': '1..."
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    expected = keys
    get(path[has_any(path.a, path.b, path.z)], keys, trace=log_to(mock_print))

    assert actual_trace_messages == expected_trace_messages


def test_keys_get_root_has_x_and_y_and_z_trace(keys):
    expected_trace_messages = [
        " has .x got {'x': {'x': '1', 'y'...",
        " has .y got {'x': {'x': '10', 'y...",
        " has .z got {'x': {'x': '19', 'y...",
        " at $[has($.x) and has($.y) and has($.z)] got {'x': {'x': {'x': '1..."
    ]
    actual_trace_messages = []

    def mock_print(message):
        actual_trace_messages.append(message)

    expected = keys
    get(path[has_all(path.x, path.y, path.z)], keys, trace=log_to(mock_print))

    assert actual_trace_messages == expected_trace_messages
