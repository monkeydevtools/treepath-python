from tests.utils.traverser_utils import gen_test_data, yria, yaia
from treepath import path, find, wc, get, has, get_match, find_matches, nested_get_match
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError


def test_get_earth(solar_system):
    def get_planet(name, the_solar_system):
        try:
            inner = the_solar_system['star']['planets']['inner']
            for planet in inner:
                if name == planet.get('name', None):
                    return planet
        except KeyError:
            pass
        raise Exception(f"The planet {name} not found")

    expected = get_planet('Earth', solar_system)
    actual = get(path.star.planets.inner[wc][has(path.name == 'Earth')], solar_system)
    assert actual == expected


def test_list_names_of_all_inner_planets(solar_system):
    expected = ['Mercury', 'Venus', 'Earth', 'Mars']
    actual = [p for p in find(path.star.planets.inner[wc].name, solar_system)]
    assert actual == expected


def test_list_names_of_all_planets_wc(solar_system):
    expected = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    actual = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
    assert actual == expected


def test_names_of_all_the_celestial_bodies(solar_system):
    expected = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    actual = [p for p in find(path.rec.name, solar_system)]
    assert actual == expected


def test_preorder_tree_traversal(solar_system):
    expected = [ss for _, ss in gen_test_data(solar_system, yria, yaia, yaia, yaia, yaia, yaia)]
    actual = [p for p in find(path.rec, solar_system)]
    assert actual == expected


def test_third_rock_from_the_sun(solar_system):
    expected = {'Equatorial diameter': 1.0, 'has-moons': True, 'name': 'Earth'}
    actual = get(path.star.planets.inner[2], solar_system)
    assert actual == expected


def test_list_first_two_inner_planets(solar_system):
    inner = solar_system["star"]["planets"]["inner"]
    expected = [inner[0], inner[1]]
    actual = [p for p in find(path.star.planets.inner[0, 1], solar_system)]
    assert actual == expected


def test_list_planes_smaller_than_earth(solar_system):
    inner = solar_system["star"]["planets"]["inner"]
    expected = [inner[0], inner[1], inner[3]]
    actual = [p for p in find(path.star.planets.inner[wc][has(path["Equatorial diameter"] < 1)], solar_system)]
    assert actual == expected


def test_list_celestial_bodies_that_have_planets(solar_system):
    expected = ['Sun']
    actual = [p for p in find(path.rec[has(path.planets)].name, solar_system)]
    assert actual == expected


def test_func_get(solar_system):
    # get the star name from the solar_system
    sun = get(path.star.name, solar_system)
    assert sun == 'Sun'

    # When there is no match MatchNotFoundError is thrown
    try:
        get(path.star.human_population, solar_system)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # return a default value when match is not found
    human_population = get(path.star.human_population, solar_system, default=0)
    assert human_population == 0


def test_func_find(solar_system):
    # find returns an Iterator of all matches
    # Each match is found just in time
    inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system)]
    assert len(inner_planets) == 4


def test_func_get_match(solar_system):
    # get the star age.
    # get_match returns a match object, where get return the value
    # The match object tells us the age attribute exist but it value is None.
    # The match object lots of metadata about the match.
    match = get_match(path.star.age, solar_system)
    assert match is not None
    assert match.data is None

    # When there is no match MatchNotFoundError is thrown
    try:
        get_match(path.star.human_population, solar_system)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # get the sun from the solar_system
    match = get_match(path.star.human_population, solar_system, must_match=False)
    assert match is None


def test_func_find_matches(solar_system):
    # find_matches returns an Iterator of all matches
    # The match object knows its index
    for match in find_matches(path.star.planets.inner[wc], solar_system):
        assert match.data == solar_system["star"]["planets"]["inner"][match.data_name]


def test_func_nested_get_match(solar_system):
    # nested_get_match allows the next match to start the search relative from another match
    parent_match = get_match(path.star.planets.inner, solar_system)
    earth_match = nested_get_match(path[2].name, parent_match)
    assert earth_match.path == "$.star.planets.inner[2].name"
    assert earth_match.data == "Earth"

    # When there is no match MatchNotFoundError is thrown
    try:
        nested_get_match(path[5].name, parent_match)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # get the sun from the solar_system
    match = nested_get_match(path[5].name, parent_match, must_match=False)
    assert match is None


def test_func__nested_find_matches(solar_system):
    # find_matches returns an Iterator of all matches
    # The match object knows its index
    for planet_match in find_matches(path.star.planets.inner[wc], solar_system):
        name_match = nested_get_match(path.name, planet_match)
        assert name_match.data == solar_system["star"]["planets"]["inner"][name_match.parent.data_name]["name"]


def test_func_match_class(solar_system):
    match = get_match(path.star.name, solar_system)
    assert repr(match) == "$.star.name=Sun"
    assert match.path_as_list == [match.parent.parent, match.parent, match]
    assert match.path == "$.star.name"
    assert match.data_name == "name"
    assert match.data == "Sun"
    assert match.parent.path == "$.star"


def test_path_root(solar_system):
    pass


def test_path_keys(solar_system):
    pass


def test_path_keys_wildcard(solar_system):
    pass


def test_path_keys_special_characters(solar_system):
    pass


def test_path_list(solar_system):
    pass


def test_path_list_slice(solar_system):
    pass


def test_path_list_comma_delimited(solar_system):
    pass


def test_path_list_wildcard(solar_system):
    pass


def test_path_recursion(solar_system):
    pass


def test_path_filter(solar_system):
    pass


def test_path_filter_has(solar_system):
    pass


def test_path_filter_comparison_operators(solar_system):
    pass


def test_path_filter_comparison_type_conversion(solar_system):
    pass


def test_path_filter_customer_predicate(solar_system):
    pass
