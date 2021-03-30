from unittest.mock import patch

from treepath import path, get
from treepath.path.util.trace import to_console


def test_keys_x_y_z(keys):
    expected = keys["x"]["y"]["z"]
    actual = get(path.x.y.z, keys, trace=to_console)
    assert actual == expected


def test_keys_x_y_z_trace(keys):
    expected_trace_messages = [
        " at $.x got .x == {'x': {'x': '1', 'y'...",
        " at $.x.y got .y == {'x': '4', 'y': '5',...",
        " at $.x.y.z got .z == '6'"
    ]
    actual_trace_messages = []

    def my_print(message):
        actual_trace_messages.append(message)

    with patch('builtins.print') as mock_print:
        mock_print.side_effect = my_print

        expected = keys["x"]["y"]["z"]
        actual = get(path.x.y.z, keys, trace=to_console)
        assert actual == expected

    assert actual_trace_messages == expected_trace_messages
