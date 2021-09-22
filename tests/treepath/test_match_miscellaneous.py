import re

from treepath import path, get_match
from treepath.path.util.match_to_path import match_to_path


def test_match_vertex(keys):
    x_vertex = path.x
    y_vertex = x_vertex.y
    z_vertex = y_vertex.z
    match = get_match(z_vertex, keys)

    assert match.vertex == z_vertex
    assert match.parent.vertex == y_vertex
    assert match.parent.parent.vertex == x_vertex


def test_root_match_path_as_list(keys):
    match = get_match(path, keys)
    path_as_list = match.path_as_list
    assert len(path_as_list) == 1


def test_match_str(keys):
    regex_expected = r'self=\d+ self=KeyMatch parent=\d+ real_data_name=x data=dict vertex=KeyVertex ' \
                     r'vertex_index=1 remembered_catch_state=NoneType remembered_on_catch_match=\d+ ' \
                     r'remembered_on_catch_action=method path=\$.x'

    match = get_match(path.x, keys)
    assert re.fullmatch(regex_expected, str(match._traverser_match))


def test_match_to_path_keys(keys):
    expected = repr(path.x.y.z)
    match = get_match(path.x.y.z, keys)
    actual = repr(match_to_path(match))
    assert actual == expected

def test_match_to_path_index(three_dimensional_list):
    expected = repr(path[0][1][2])
    match = get_match(path[0][1][2], three_dimensional_list)
    actual = repr(match_to_path(match))
    assert actual == expected
