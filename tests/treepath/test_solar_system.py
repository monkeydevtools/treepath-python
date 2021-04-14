"""**treepath** uses [declarative programming](https://en.wikipedia.org/wiki/Declarative_programming) approach for
extracting data from a [json](https://docs.python.org/3/library/json.html) data structure.  The expressions are a
[query language](https://en.wikipedia.org/wiki/Query_language) similar to
[jsonpath](https://goessner.net/articles/JsonPath/), and [Xpath](https://en.wikipedia.org/wiki/XPath), but are
written in native python syntax.
"""
import inspect
import os
import re
import textwrap

from tests.utils.traverser_utils import gen_test_data, yria, yaia
from treepath import path, find, wc, get, has, get_match, find_matches, pathd, wildcard, \
    MatchNotFoundError, Match


class Readme:

    def __init__(self, readme_file: str):
        self._readme_file = open(readme_file, 'w')

    def append(self, data):
        self._readme_file.write(data)

    def append_doc(self, data):
        dedent_data = textwrap.dedent(data)
        self.append(f"{os.linesep}{dedent_data}")

    def append_python_src(self, python_src):
        dedent_python_src = textwrap.dedent(python_src)
        self.append(f"{os.linesep}```python{os.linesep}{dedent_python_src}```")

    @staticmethod
    def extract_doc_string(python_entity):
        doc_string = python_entity.__doc__
        return doc_string

    def extract_python_src(self, python_entity):
        doc_string = python_entity.__doc__
        source = inspect.getsource(python_entity)

        index_of_doc = source.index(doc_string)
        source_start = index_of_doc + len(doc_string) + 3
        python_src = source[source_start:]

        return python_src

    def process_python_src(self, python_src: str):
        dedent_python_src = textwrap.dedent(python_src)
        lines_itr = iter(dedent_python_src.splitlines(keepends=True))
        line = next(lines_itr)
        self.process_python_src_segment(line, lines_itr)

    def process_python_src_segment(self, line, lines_itr):
        buffer = line
        for line in lines_itr:
            if not line.startswith('#'):
                buffer += line
            else:
                if not buffer.isspace():
                    self.append_python_src(buffer)
                self.process_comment_segment(line, lines_itr)
                return
        self.append_python_src(buffer)

    def process_comment_segment(self, line, lines_itr):
        buffer = line[1:]
        for line in lines_itr:
            if line.startswith('#'):
                buffer += line[1:]
            elif not line.strip():
                buffer += line
            else:
                self.append_doc(buffer)
                self.process_python_src_segment(line, lines_itr)
                return
        self.append_doc(buffer)

    def append_function(self, function):
        doc_string = self.extract_doc_string(function)
        self.append_doc(doc_string)

        python_src = self.extract_python_src(function)
        self.process_python_src(python_src)

        return function

    def __iadd__(self, p2):
        dedent_txt = textwrap.dedent(p2)
        self.append(dedent_txt)
        return self


readme = Readme("/tmp/README.md")

readme += __doc__

readme += """
# Quick comparison between Imperative and Declarative Solution

To understand how treepath can differs from Imperative solution, here is an example problem showing both an Imperative
and declarative solution.

The problem is:  given the solar system json document fetch the planet by name.

The example solar system json document can be found [Here](# Solar System Json document)
"""


@readme.append_function
def test_get_earth_imperative_solution(solar_system):
    """
    ## Imperative Solution

    The first example uses flow control statements to define a
    [Imperative Solution]( https://en.wikipedia.org/wiki/Imperative_programming).   This is a
    very common approach to solving problems.
    """

    def get_planet_by_name(name, the_solar_system):
        try:
            planets = the_solar_system['star']['planets']
            for arc in planets.values():
                for planet in arc:
                    if name == planet.get('name', None):
                        return planet
        except KeyError:
            pass
        return None

    actual = get_planet_by_name('Earth', solar_system)
    expected = {'Number of Moons': '1', 'diameter': 12756, 'has-moons': True, 'name': 'Earth'}
    assert actual == expected


@readme.append_function
def test_get_earth_declarative_solution(solar_system):
    """
    ## Declarative  Solution

    The second example uses treepath to define a
    [declarative solution](https://en.wikipedia.org/wiki/Declarative_programming).
    It solves the same problem without defining any flow control statements.    This keeps the Cyclomatic and
    Cognitive Complexity low.
    """

    def get_planet_by_name(name: str, the_solar_system):
        return get(
            path.star.planets.wc[wc][has(path.name == name)],
            the_solar_system,
            default=None
        )

    actual = get_planet_by_name('Earth', solar_system)
    expected = {'Number of Moons': '1', 'diameter': 12756, 'has-moons': True, 'name': 'Earth'}
    assert actual == expected


def test_solar_system_json(solar_system_json):
    global readme
    readme += """
    # Solar System Json document
    
    The examples shown in this README use the following json document.  It describes our solar system.
    <details><summary>solar_system = {...}</summary>
    <p>

    ```json
    """
    readme += solar_system_json
    readme += """
    ```

    </p>
    </details>
    """


readme += """
# query examples.

| Description                                 | Xpath                               | jsonpath                                  | treepath                            |
|----------------------------------------------|-------------------------------------|-------------------------------------------|------------------------------------|
| Find planet earth.                           | /star/planets/inner[name='Earth']   | $.star.planets.inner[?(@.name=='Earth')]  | path.star.planets.inner[wc][has(path.name == 'Earth')]   |
| List the names of all inner planets.         | /star/planets/inner[*].name         | $.star.planets.inner[*].name              | path.star.planets.inner[wc].name   |
| List the names of all planets.               | /star/planets/*/name                | $.star.planets.[*].name                   | path.star.planets.wc[wc].name      |
| List the names of all celestial bodies       | //name                              | $..name                                   | path.rec.name                      |  
| List all nodes in the tree Preorder          | //*                                 | $..                                       | path.rec                           |
| Get the third rock from the sun              | /star/planets/inner[3]              | $.star.planets.inner[2]                   | path.star.planets.inner[2]         |
| List first two inner planets                 | /star/plnaets.inner[position()<3]   | $.star.planets.inner[:2]                  | path.star.planets.inner[0:2]       |
|                                              |                                     | $.star.planets.inner[0, 1]                | path.star.planets.inner[0, 2]      |
| List planets smaller than earth              | /star/planets/inner[Equatorial_diameter < 1]   | $.star.planets.inner[?(@.['Equatorial diameter'] < 1)]              | path.star.planets.inner[wc][has(path["Equatorial diameter"] < 1)]       |
| List celestial bodies that have planets.     | //*[planets]/name                   | $..*[?(@.planets)].name                   | path.rec[has(path.planets)].name       |
"""


def test_query_examples_list_the_names_of_all_inner_planets(solar_system):
    inner_planets = [p for p in find(path.star.planets.inner[wc].name, solar_system)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']


def test_query_examples_list_the_names_of_all_planets(solar_system):
    all_planets = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


def test_query_examples_list_the_names_of_all_celestial_bodies(solar_system):
    all_celestial_bodies = [p for p in find(path.rec.name, solar_system)]
    assert all_celestial_bodies == ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                    'Neptune']


def test_query_examples_list_all_nodes_in_the_tree_preorder(solar_system):
    expected = [ss for _, ss in gen_test_data(solar_system, yria, yaia, yaia, yaia, yaia, yaia)]
    actual = [p for p in find(path.rec, solar_system)]
    assert actual == expected


def test_query_examples_get_third_rock_from_the_sun(solar_system):
    earth = get(path.star.planets.inner[2], solar_system)
    assert earth == solar_system["star"]["planets"]["inner"][2]


def test_query_examples_list_first_two_inner_planets(solar_system):
    expected = [solar_system["star"]["planets"]["inner"][0],
                solar_system["star"]["planets"]["inner"][1]]
    first_two_planets = [p for p in find(path.star.planets.inner[0:2], solar_system)]
    assert first_two_planets == expected

    first_two_planets = [p for p in find(path.star.planets.inner[0, 1], solar_system)]
    assert first_two_planets == expected


def test_query_examples_list_planets_smaller_than_earth(solar_system):
    planets_smaller_than_earth = [p for p in
                                  find(path.star.planets.inner[wc][has(path.diameter < 12756)], solar_system)]
    assert planets_smaller_than_earth == [solar_system["star"]["planets"]["inner"][0],
                                          solar_system["star"]["planets"]["inner"][1],
                                          solar_system["star"]["planets"]["inner"][3]]


def test_query_examples_list_celestial_bodies_that_have_planets(solar_system):
    sun = [p for p in find(path.rec[has(path.planets)].name, solar_system)]
    assert sun == ['Sun']


readme += """
# Traversal Functions

"""


@readme.append_function
def test_traversal_function_get(solar_system):
    """
    ## get
    """

    # The **get** function returns the first value the path leads to.

    # Get the star name from the solar_system
    sun = get(path.star.name, solar_system)
    assert sun == 'Sun'

    # When there is no match, MatchNotFoundError is thrown.
    try:
        get(path.star.human_population, solar_system)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # Return a default value when match is not found.
    human_population = get(path.star.human_population, solar_system, default=0)
    assert human_population == 0

    # The data source can be a json data structure or a [Match](#The-Match-class).
    parent_match = get_match(path.star.planets.inner, solar_system)
    name = get(path[2].name, parent_match)
    assert name == "Earth"


@readme.append_function
def test_traversal_function_find(solar_system):
    """
    ## find
    """

    # The **find** function returns an Iterator that iterates to each value the path leads to.  Each value is
    # determine on its iteration.

    # Find all of the planet names.
    inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']

    # The data source can be a json data structure or a [Match](#The-Match-class).
    parent_match = get_match(path.star.planets.inner, solar_system)
    inner_planets = [planet for planet in find(path[wc].name, parent_match)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']


@readme.append_function
def test_traversal_function_get_match(solar_system):
    """
    ## get_match
    """

    # The **get_match** function returns the first [Match](#The-Match-class) the path leads to.

    # Get the star name from the solar_system
    match = get_match(path.star.name, solar_system)
    assert match.data == 'Sun'

    # When there is no match, MatchNotFoundError is thrown.
    try:
        get_match(path.star.human_population, solar_system)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # Return a None when match is not found.
    match = get_match(path.star.human_population, solar_system, must_match=False)
    assert match is None

    # The data source can be a json data structure or a [Match](#The-Match-class).
    parent_match = get_match(path.star.planets.inner, solar_system)
    earth_match = get_match(path[2].name, parent_match)
    assert earth_match.path == "$.star.planets.inner[2].name"
    assert earth_match.data == "Earth"


@readme.append_function
def test_traversal_function_find_matches(solar_system):
    """
    ## find_matches
    """
    # The **find_matches** function returns an Iterator that iterates to each match the path leads to.  Each match is
    # determine on its iteration.

    # Find the path to each of the inner planets.
    for match in find_matches(path.star.planets.inner[wc], solar_system):
        assert match.path in [
            '$.star.planets.inner[0]',
            '$.star.planets.inner[1]',
            '$.star.planets.inner[2]',
            '$.star.planets.inner[3]',
        ]

    # The data source can be a json data structure or a [Match](#The-Match-class).
    parent_match = get_match(path.star.planets.inner, solar_system)
    for match in find_matches(path[wc], parent_match):
        assert match.path in [
            '$.star.planets.inner[0]',
            '$.star.planets.inner[1]',
            '$.star.planets.inner[2]',
            '$.star.planets.inner[3]',
        ]


@readme.append_function
def test_traversal_function_match_class(solar_system):
    """
    ## The Match class
    """
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
    # dict keys that are not valid python syntax can be referenced as strings
    sun_equatorial_diameter = get(path.star.planets.inner[0]["Number of Moons"], solar_system)

    assert sun_equatorial_diameter == solar_system["star"]["planets"]["inner"][0]["Number of Moons"]

    # dict keys that are not valid python syntax can be referenced as strings
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

    # comma delimited keys works too.
    last_and_first = [planet for planet in find(path.star["diameter", "name"], solar_system)]
    assert last_and_first == [1391016, "Sun"]


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
        i_am_planet = get_match(path.parent.parent.parent.planets, match, must_match=False)
        if not i_am_planet:
            return False

        index_before_planet = match.data_name - 1
        before_planet = get_match(path[index_before_planet][has(path.name == "Earth")], match.parent,
                                         must_match=False)
        if before_planet:
            return True

        index_after_planet = match.data_name + 1
        before_planet = get_match(path[index_after_planet][has(path.name == "Earth")], match.parent,
                                         must_match=False)
        if before_planet:
            return True

        return False

    earth = [planet for planet in find(path.rec[my_neighbor_is_earth].name, solar_system)]
    assert earth == ['Venus', 'Mars']


def test_path_filter_regex(solar_system):
    # match values by regular expression
    # Find the planets that end with s
    pattern = re.compile(r"\w+s")
    earth = [planet for planet in find(path.rec[has(path.name, pattern.match)].name, solar_system)]
    assert earth == ['Venus', 'Mars', 'Uranus']
