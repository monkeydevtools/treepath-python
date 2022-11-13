from tests.utils.traverser_utils import *
from treepath import get, path, find_matches, has, get_match, wc, find, MatchNotFoundError, PathSyntaxError, Match, \
    has_all, has_any, has_not
from treepath.path.traverser.imaginary_match import ImaginaryMatch


def test_keys_get_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path.a)], keys)


def test_PathSyntaxError_validate_message(keys):
    expected = "PathSyntaxError(Invalid  path [<class 'int'>] argument.   Expecting PathBuilderPredicate, " \
               f"PathPredicate,  or Callable[[Match], Any]])"
    with pytest.raises(PathSyntaxError) as exc_info:
        has(1)

    assert repr(exc_info.value) == expected


def test_keys_get_root_has_x(keys):
    expected = keys
    actual = get(path[has(path.x)], keys)
    assert actual == expected


def test_keys_get_root_x_were_root_has_a_MatchNotFoundError(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path.a)].x, keys)


def test_keys_get_root_x_were_root_has_y(keys):
    expected = keys["x"]
    actual = get(path[has(path.y)].x, keys)
    assert actual == expected


def test_keys_get_match_rec_verify_imaginary_match_path_as_list_correct(keys):
    actual = get_match(path.x.x.rec, keys)
    assert isinstance(actual._traverser_match, ImaginaryMatch)
    assert actual.path_match_list == [actual.parent.parent, actual.parent, actual]


def test_keys_get_match_rec_verify_imaginary_match_path_segment_correct(keys):
    actual = get_match(path.x.x.rec, keys)
    assert isinstance(actual._traverser_match, ImaginaryMatch)
    assert actual.path_segment == '.x'


def test_keys_match_all_root_wc_has_x(keys):
    result = find_matches(path.wc[has(path.x)], keys)
    for expected_path, expected_value in gen_test_data(keys, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_keys_match_all_root_wc_has_a(keys):
    result = find_matches(path.wc[has(path.a)], keys)
    assert_done_iterating(result)


def test_keys_match_all_all_has_x(keys):
    exp_iter = find_matches(path.rec[has(path.x)], keys)
    count = 0
    for expected_path, expected_value in gen_test_data(keys, yria, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_keys_match_all_all_has_a(keys):
    exp_iter = find_matches(path.rec[has(path.a)], keys)
    assert_done_iterating(exp_iter)


def test_keys_match_all_all_has_x_eq_1(keys):
    exp_iter = find_matches(path.rec.x[has(path.rec.x == "1")], keys)
    actual = next(exp_iter)
    expected = get_match(path.x, keys)
    assert repr(actual) == repr(expected)

    actual = next(exp_iter)
    expected = get_match(path.x.x, keys)
    assert repr(actual) == repr(expected)

    assert_done_iterating(exp_iter)


def test_keys_lt(keys):
    expected = [str(v) for v in range(1, 14)]
    actual = [v for v in find(path.wc.wc.wc[has(path < 14, int)], keys)]
    assert actual == expected


def test_keys_le(keys):
    expected = [str(v) for v in range(1, 15)]
    actual = [v for v in find(path.wc.wc.wc[has(path <= 14, int)], keys)]
    assert actual == expected


def test_keys_eq(keys):
    expected = ["14"]
    actual = [v for v in find(path.wc.wc.wc[has(path == 14, int)], keys)]
    assert actual == expected


def test_keys_ne(keys):
    expected = [str(v) for v in range(1, 28)]
    expected.remove("14")
    actual = [v for v in find(path.wc.wc.wc[has(path != 14, int)], keys)]
    assert actual == expected


def test_keys_gt(keys):
    expected = [str(v) for v in range(15, 28)]
    actual = [v for v in find(path.wc.wc.wc[has(path > 14, int)], keys)]
    assert actual == expected


def test_keys_ge(keys):
    expected = [str(v) for v in range(14, 28)]
    actual = [v for v in find(path.wc.wc.wc[has(path >= 14, int)], keys)]
    assert actual == expected


def test_3d_list_get_root_has_a_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path[4])], three_dimensional_list)


def test_3d_list_get_root_has_1(three_dimensional_list):
    expected = three_dimensional_list
    actual = get(path[has(path[1])], three_dimensional_list)
    assert actual == expected


def test_3d_list_get_root_1_were_root_has_a_MatchNotFoundError(three_dimensional_list):
    with pytest.raises(MatchNotFoundError):
        get(path[has(path[4])][1], three_dimensional_list)


def test_3d_list_get_root_1_were_root_has_1(three_dimensional_list):
    expected = three_dimensional_list[1]
    actual = get(path[has(path[1])][1], three_dimensional_list)
    assert actual == expected


def test_3d_list_match_all_root_wc_has_1(three_dimensional_list):
    result = find_matches(path[wc][has(path[1])], three_dimensional_list)
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yaia):
        actual = next(result)
        assert str(actual) == f"{expected_path}={actual.data}"
    assert_done_iterating(result)


def test_3d_list_match_all_root_wc_has_a(three_dimensional_list):
    result = find_matches(path[wc][has(path[4])], three_dimensional_list)
    assert_done_iterating(result)


def test_3d_list_match_all_all_has_1(three_dimensional_list):
    exp_iter = find_matches(path.rec[has(path[1])], three_dimensional_list)
    count = 0
    for expected_path, expected_value in gen_test_data(three_dimensional_list, yria, yaia, yaia):
        count += 1
        actual = next(exp_iter)
        assert repr(actual) == f"{expected_path}={expected_value}"
    assert count == 13
    assert_done_iterating(exp_iter)


def test_3d_list_match_all_all_has_a(three_dimensional_list):
    exp_iter = find_matches(path.rec[has(path[4])], three_dimensional_list)
    assert_done_iterating(exp_iter)


def test_3d_list_match_all_all_has_1_eq_1(three_dimensional_list):
    exp_iter = find_matches(path.rec[1][has(path.rec[1] == 14)], three_dimensional_list)
    actual = next(exp_iter)
    expected = get_match(path[1], three_dimensional_list)
    assert repr(actual) == repr(expected)

    actual = next(exp_iter)
    expected = get_match(path[1][1], three_dimensional_list)
    assert repr(actual) == repr(expected)

    assert_done_iterating(exp_iter)


def test_3d_list_lt(three_dimensional_list):
    expected = [v for v in range(1, 14)]
    actual = [v for v in find(path[wc][wc][wc][has(path < 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_le(three_dimensional_list):
    expected = [v for v in range(1, 15)]
    actual = [v for v in find(path[wc][wc][wc][has(path <= 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_eq(three_dimensional_list):
    expected = [14]
    actual = [v for v in find(path[wc][wc][wc][has(path == 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_ne(three_dimensional_list):
    expected = [v for v in range(1, 28)]
    expected.remove(14)
    actual = [v for v in find(path[wc][wc][wc][has(path != 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_gt(three_dimensional_list):
    expected = [v for v in range(15, 28)]
    actual = [v for v in find(path[wc][wc][wc][has(path > 14)], three_dimensional_list)]
    assert actual == expected


def test_3d_list_ge(three_dimensional_list):
    expected = [v for v in range(14, 28)]
    actual = [v for v in find(path[wc][wc][wc][has(path >= 14)], three_dimensional_list)]
    assert actual == expected


def test_keys_custom_filter(keys):
    def custom_filter(match: Match):
        return match.data == "2"

    expected = "2"
    actual = get(path.x.x.wc[custom_filter], keys)
    assert actual == expected


def test_keys_get_root_has_x_and_y_and_z(keys):
    expected = keys
    actual = get(path[has_all(path.x, path.y, path.z)], keys)
    assert actual == expected


def test_keys_get_root_has_x_and_y_and_a(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has_all(path.x, path.y, path.a)], keys)


def test_keys_get_root_has_x_or_y_or_z(keys):
    expected = keys
    actual = get(path[has_any(path.x, path.b, path.c)], keys)
    assert actual == expected

    actual = get(path[has_any(path.a, path.y, path.c)], keys)
    assert actual == expected

    actual = get(path[has_any(path.a, path.b, path.z)], keys)
    assert actual == expected


def test_keys_get_root_has_a_or_b_and_c(keys):
    with pytest.raises(MatchNotFoundError):
        get(path[has_any(path.a, path.b, path.c)], keys)


def test_keys_get_root_has_these_order_one(keys):
    keys["a"] = {"b": {"c": ':)'}}

    def zp(parent_match: Match):
        return parent_match.data.get('z', None) == '27'

    @has.these((path.x == 1, int), path.y == '14', path.c, zp)
    def predicate(parent_match: Match, one, two, three, four):
        return one(parent_match) or two(parent_match) or three(parent_match) or four(parent_match)

    itr = find(path.wc.wc[predicate], keys)
    actual = next(itr)
    assert actual == {"x": "1", "y": "2", "z": "3"}

    actual = next(itr)
    assert actual == {'x': '13', 'y': '14', 'z': '15'}

    actual = next(itr)
    assert actual == {"x": "25", "y": "26", "z": "27"}

    actual = next(itr)
    assert actual == {"c": ':)'}


def test_keys_get_root_has_these_order_two(keys):
    keys["a"] = {"b": {"c": ':)'}}

    def zp(parent_match: Match):
        return parent_match.data.get('z', None) == '27'

    @has.these(zp, (path.x == 1, int), path.y == '14', path.c)
    def predicate(parent_match: Match, one, two, three, four):
        return one(parent_match) or two(parent_match) or three(parent_match) or four(parent_match)

    itr = find(path.wc.wc[predicate], keys)

    actual = next(itr)
    assert actual == {"x": "1", "y": "2", "z": "3"}

    actual = next(itr)
    assert actual == {'x': '13', 'y': '14', 'z': '15'}

    actual = next(itr)
    assert actual == {"x": "25", "y": "26", "z": "27"}

    actual = next(itr)
    assert actual == {"c": ':)'}


def test_keys_get_root_has_these_order_three(keys):
    keys["a"] = {"b": {"c": ':)'}}

    def zp(parent_match: Match):
        return parent_match.data.get('z', None) == '27'

    @has.these(path.c, zp, (path.x == 1, int), path.y == '14')
    def predicate(parent_match: Match, one, two, three, four):
        return one(parent_match) or two(parent_match) or three(parent_match) or four(parent_match)

    itr = find(path.wc.wc[predicate], keys)
    actual = next(itr)
    assert actual == {"x": "1", "y": "2", "z": "3"}

    actual = next(itr)
    assert actual == {'x': '13', 'y': '14', 'z': '15'}

    actual = next(itr)
    assert actual == {"x": "25", "y": "26", "z": "27"}

    actual = next(itr)
    assert actual == {"c": ':)'}


def test_keys_get_root_has_these_order_four(keys):
    keys["a"] = {"b": {"c": ':)'}}

    def zp(parent_match: Match):
        return parent_match.data.get('z', None) == '27'

    @has.these(path.y == '14', path.c, zp, (path.x == 1, int))
    def predicate(parent_match: Match, one, two, three, four):
        return one(parent_match) or two(parent_match) or three(parent_match) or four(parent_match)

    itr = find(path.wc.wc[predicate], keys)
    actual = next(itr)
    assert actual == {"x": "1", "y": "2", "z": "3"}

    actual = next(itr)
    assert actual == {'x': '13', 'y': '14', 'z': '15'}

    actual = next(itr)
    assert actual == {"x": "25", "y": "26", "z": "27"}

    actual = next(itr)
    assert actual == {"c": ':)'}


def test_keys_get_root_has_not_a(keys):
    expected = keys
    target_path = path[has_not(path.a)]
    actual = get(target_path, keys)
    assert actual == expected
