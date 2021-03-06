from tests.utils.traverser_utils import gen_test_data, yria, yaia
from treepath import path, find, wc, get, has, get_match, find_matches, nested_get_match, pathd, wildcard
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.traverser.match import Match


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

    earth = get(path.star.planets.inner[wc][has(path.name == 'Earth')], solar_system)
    assert earth == get_planet('Earth', solar_system)


def test_list_names_of_all_inner_planets(solar_system):
    inner_planets = [p for p in find(path.star.planets.inner[wc].name, solar_system)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']


def test_preorder_tree_traversal(solar_system):
    expected = [ss for _, ss in gen_test_data(solar_system, yria, yaia, yaia, yaia, yaia, yaia)]
    actual = [p for p in find(path.rec, solar_system)]
    assert actual == expected


def test_third_rock_from_the_sun(solar_system):
    earth = get(path.star.planets.inner[2], solar_system)
    assert earth == solar_system["star"]["planets"]["inner"][2]


def test_list_first_two_inner_planets(solar_system):
    first_two_planets = [p for p in find(path.star.planets.inner[0, 1], solar_system)]
    assert first_two_planets == [solar_system["star"]["planets"]["inner"][0],
                                 solar_system["star"]["planets"]["inner"][1]]


def test_list_planets_smaller_than_earth(solar_system):
    planets_smaller_than_earth = [p for p in
                                  find(path.star.planets.inner[wc][has(path.diameter < 12756)], solar_system)]
    assert planets_smaller_than_earth == [solar_system["star"]["planets"]["inner"][0],
                                          solar_system["star"]["planets"]["inner"][1],
                                          solar_system["star"]["planets"]["inner"][3]]


def test_list_celestial_bodies_that_have_planets(solar_system):
    sun = [p for p in find(path.rec[has(path.planets)].name, solar_system)]
    assert sun == ['Sun']


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

    # The string representation of match = [path=value]
    assert repr(match) == "$.star.name=Sun"

    # A list containing each match in the path
    assert match.path_as_list == [match.parent.parent, match.parent, match]

    # The string representation of path the match represents
    assert match.path == "$.star.name"

    # Key that points to the match value.  Key can be index if the parent is a list
    assert match.data_name == "name" and match.parent.data[match.data_name] == match.data

    # the value match path maps to.
    assert match.data == "Sun"

    # The parent of this match
    assert match.parent.path == "$.star"


def test_path_root(solar_system):
    # path  point to root of the tree
    match = get_match(path, solar_system)

    assert match.data == solar_system

    # In a filter path point to the current element
    match = get_match(path.star.name[has(path == 'Sun')], solar_system)

    assert match.data == 'Sun'


def test_path_keys(solar_system):
    # dict key are dynamic attribute on a path
    inner_from_attribute = get(path.star.planets.inner, solar_system)
    inner_from_string_keys = get(path["star"]["planets"]["inner"], solar_system)

    assert inner_from_attribute == inner_from_string_keys == solar_system["star"]["planets"]["inner"]


def test_path_keys_special_characters(solar_system):
    # dick keys that are not valid python syntax can be referenced as strings
    sun_equatorial_diameter = get(path.star.planets.inner[0]["Number of Moons"], solar_system)

    assert sun_equatorial_diameter == solar_system["star"]["planets"]["inner"][0]["Number of Moons"]

    # dick keys that are not valid python syntax can be referenced as strings
    mercury_has_moons = get(path.star.planets.inner[0]["has-moons"], solar_system)

    assert mercury_has_moons == solar_system["star"]["planets"]["inner"][0]["has-moons"]

    # If the json has a lots of attributes with dashes, pathd can be use to interpret underscore as dashes
    # in attribute names.
    mercury_has_moons = get(pathd.star.planets.inner[0].has_moons, solar_system)

    assert mercury_has_moons == solar_system["star"]["planets"]["inner"][0]["has-moons"]


def test_path_keys_wildcard(solar_system):
    # wildcard is useful for iterating over attributes
    star_children = [child for child in find(path.star.wildcard, solar_system)]
    assert star_children == [solar_system["star"]["name"],
                             solar_system["star"]["diameter"],
                             solar_system["star"]["age"],
                             solar_system["star"]["planets"], ]

    # wc for short
    star_children = [child for child in find(path.star.wc, solar_system)]
    assert star_children == [solar_system["star"]["name"],
                             solar_system["star"]["diameter"],
                             solar_system["star"]["age"],
                             solar_system["star"]["planets"], ]


def test_path_list(solar_system):
    # list can be access using index
    earth = get(path.star.planets.inner[2], solar_system)
    assert earth == solar_system["star"]["planets"]["inner"][2]


def test_path_list_slice(solar_system):
    # list can be access using slices
    # first to planets
    first_two = [planet for planet in find(path.star.planets.outer[:2].name, solar_system)]
    assert first_two == ["Jupiter", "Saturn"]

    # last to planets
    last_two = [planet for planet in find(path.star.planets.outer[-2:].name, solar_system)]
    assert last_two == ["Uranus", "Neptune"]

    # all outer planets reversed
    last_two = [planet for planet in find(path.star.planets.outer[::-1].name, solar_system)]
    assert last_two == ["Neptune", "Uranus", "Saturn", "Jupiter"]

    # The last inner planet and the last outer planet
    # The inner and outer list are still treated a separate list
    # notice the wildcard
    last_two = [planet for planet in find(path.star.wc.wc[-1:].name, solar_system)]
    assert last_two == ["Mars", "Neptune"]


def test_path_list_comma_delimited(solar_system):
    # comma delimited index work too.
    last_and_first = [planet for planet in find(path.star.planets.outer[3, 0].name, solar_system)]
    assert last_and_first == ["Neptune", "Jupiter"]


def test_path_list_wildcard(solar_system):
    # wildcard can be used as a list index
    all_outer = [planet for planet in find(path.star.planets.outer[wildcard].name, solar_system)]
    assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

    # wc for short
    all_outer = [planet for planet in find(path.star.planets.outer[wc].name, solar_system)]
    assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

    # combine dict wildcard and list wildcard
    all_planets = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


def test_path_recursion(solar_system):
    # using recursive search to find all the planet names
    all_planets = [p for p in find(path.star.planets.recursive.name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # rec for short
    all_planets = [p for p in find(path.star.planets.rec.name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # using recursive search to find all the celestial bodies names
    all_celestial_bodies = [p for p in find(path.rec.name, solar_system)]
    assert all_celestial_bodies == ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                    'Neptune']


def test_path_filter_has(solar_system):
    # filters can be used filter on attribute existence
    # celestial bodies that have planets
    sun = get(path.rec[has(path.planets)].name, solar_system)
    assert sun == "Sun"

    # filter all celestial bodies that have a has-moon attribute
    all_celestial_bodies_moon_attribute = [planet for planet in find(path.rec[has(pathd.has_moons)].name, solar_system)]
    assert all_celestial_bodies_moon_attribute == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                                   'Neptune']

    # filter all celestial bodies that have a moons
    all_celestial_bodies_moon_attribute = [planet for planet in
                                           find(path.rec[has(pathd.has_moons == True)].name, solar_system)]
    assert all_celestial_bodies_moon_attribute == ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


def test_path_filter_comparison_operators(solar_system):
    # filters with comparison operators
    earth = [planet for planet in find(path.rec[has(path.diameter == 12756)].name, solar_system)]
    assert earth == ['Earth']

    earth = [planet for planet in find(path.rec[has(path.diameter != 12756)].name, solar_system)]
    assert earth == ['Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    earth = [planet for planet in find(path.rec[has(path.diameter > 12756)].name, solar_system)]
    assert earth == ['Sun', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    earth = [planet for planet in find(path.rec[has(path.diameter >= 12756)].name, solar_system)]
    assert earth == ['Sun', 'Earth', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    earth = [planet for planet in find(path.rec[has(path.diameter < 12756)].name, solar_system)]
    assert earth == ['Mercury', 'Venus', 'Mars']

    earth = [planet for planet in find(path.rec[has(path.diameter <= 12756)].name, solar_system)]
    assert earth == ['Mercury', 'Venus', 'Earth', 'Mars']


def test_path_filter_comparison_type_conversion(solar_system):
    # sometimes the value is the wrong type
    # like here the number of moons are strings
    planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > "5")].name, solar_system)]
    assert planets == ['Jupiter', 'Saturn']

    # convert the number of moon to in and get a different answer
    planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > 5, int)].name, solar_system)]
    assert planets == ['Jupiter', 'Saturn', 'Uranus', 'Neptune']


def test_path_filter_customer_predicate(solar_system):
    # write your own operator
    def smaller_than_earth(value):
        return value < 12756

    earth = [planet for planet in find(path.rec[has(path.diameter, smaller_than_earth)].name, solar_system)]
    assert earth == ['Mercury', 'Venus', 'Mars']

    # write your own predicate
    def my_neighbor_is_earth(match: Match):
        i_am_planet = nested_get_match(path.parent.parent.parent.planets, match, must_match=False)
        if not i_am_planet:
            return False

        index_before_planet = match.data_name - 1
        before_planet = nested_get_match(path[index_before_planet][has(path.name == "Earth")], match.parent,
                                         must_match=False)
        if before_planet:
            return True

        index_after_planet = match.data_name + 1
        before_planet = nested_get_match(path[index_after_planet][has(path.name == "Earth")], match.parent,
                                         must_match=False)
        if before_planet:
            return True

        return False


    earth = [planet for planet in find(path.rec[my_neighbor_is_earth].name, solar_system)]
    assert earth == ['Venus', 'Mars']
