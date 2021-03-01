from tests.utils.traverser_utils import *
from treepath import get, path, get_match, find_matches
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_empty_dict_index_MatchNotFoundError():
    empty_dict = {}
    with pytest.raises(MatchNotFoundError):
        get(path.parent, empty_dict)


def test_keys_x_parent_path(keys):
    expected = keys
    actual = get_match(path.x.parent, keys)
    assert str(actual) == f"$.x.<-$={expected}"


def test_keys_x_x_parent_path(keys):
    expected = keys["x"]
    actual = get_match(path.x.y.parent, keys)
    assert str(actual) == f"$.x.y.<-x={expected}"


def test_3d_list_x_parent_path(three_dimensional_list):
    expected = three_dimensional_list
    actual = get_match(path[0].parent, three_dimensional_list)
    assert str(actual) == f"$[0][<-$]={expected}"


def test_3d_list_x_x_parent_path(three_dimensional_list):
    expected = three_dimensional_list[0]
    actual = get_match(path[0][1].parent, three_dimensional_list)
    assert str(actual) == f"$[0][1][<-0]={expected}"


def test_keys_rec_parent_path(keys):
    expected = ['$.x.<-$',
                '$.x.x.<-x',
                '$.x.y.<-x',
                '$.x.z.<-x',
                '$.y.<-$',
                '$.y.x.<-y',
                '$.y.y.<-y',
                '$.y.z.<-y',
                '$.z.<-$',
                '$.z.x.<-z',
                '$.z.y.<-z',
                '$.z.z.<-z']
    actual = [fm.path for fm in find_matches(path.rec.parent, keys)]
    assert actual == expected


def test_keys_parent_rec_path(keys):
    expected = []
    actual = [fm.path for fm in find_matches(path.parent.rec, keys)]
    assert actual == expected


def test_keys_x_y_parent_rec_path(keys):
    expected = ['$.x.y.<-x',
                '$.x.y.<-x.x',
                '$.x.y.<-x.x.x',
                '$.x.y.<-x.x.y',
                '$.x.y.<-x.x.z',
                '$.x.y.<-x.y',
                '$.x.y.<-x.y.x',
                '$.x.y.<-x.y.y',
                '$.x.y.<-x.y.z',
                '$.x.y.<-x.z',
                '$.x.y.<-x.z.x',
                '$.x.y.<-x.z.y',
                '$.x.y.<-x.z.z']
    actual = [fm.path for fm in find_matches(path.x.y.parent.rec, keys)]
    assert actual == expected


def test_keys_rec_x_parent_rec_path(keys):
    expected = ['$.x.<-$',
                '$.x.x.<-x',
                '$.x.x.x.<-x',
                '$.x.y.x.<-y',
                '$.x.z.x.<-z',
                '$.y.x.<-y',
                '$.y.x.x.<-x',
                '$.y.y.x.<-y',
                '$.y.z.x.<-z',
                '$.z.x.<-z',
                '$.z.x.x.<-x',
                '$.z.y.x.<-y',
                '$.z.z.x.<-z']

    actual = [fm.path for fm in find_matches(path.rec.x.parent, keys)]

    assert actual == expected
