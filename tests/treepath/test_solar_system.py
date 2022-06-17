from __future__ import annotations

import operator
import re
from functools import partial

import pytest

from tests.data.data import get_solar_system_json
from tests.utils.file_util import find_file
from tests.utils.readme_generator import Readme
from tests.utils.traverser_utils import gen_test_data, yria, yaia
from treepath import path, find, wc, set_, get, has, get_match, find_matches, pathd, wildcard, \
    MatchNotFoundError, Match, log_to, has_all, has_any, has_not, Document, attr, attr_typed, attr_iter_typed, \
    attr_list_typed, JsonArgTypes

read_me_file = find_file("README.md")
readme = Readme(read_me_file)

readme += """
# The **treepath** Package.

The **treepath** package offers a [declarative programming](https://en.wikipedia.org/wiki/Declarative_programming) 
approach to extracting data from a [json](https://docs.python.org/3/library/json.html) data structure.  The expressions 
are a [query language](https://en.wikipedia.org/wiki/Query_language) similar to
[jsonpath](https://goessner.net/articles/JsonPath/), and [Xpath](https://en.wikipedia.org/wiki/XPath), but are
written in native python syntax.

Note python 3.6 is supported in version earlier that 1.0.0.
"""


@readme.append_function
def test_quick_start(solar_system):
    """# Quick start"""

    # All of the treepath components should be imported as follows:
    # ```python
    # from treepath import path, find, wc, set_, get, has, get_match, find_matches, pathd, wildcard, \
    #     MatchNotFoundError, Match, log_to, has_all, has_any, has_not, pprop, mprop
    # ```

    # A treepath example that fetches the value 1 from data.
    data = {
        "a": {
            "b": [
                {
                    "c": 1
                },
                {
                    "c": 2
                }]
        }
    }
    value = get(path.a.b[0].c, data)
    assert value == 1

    # A treepath example that fetches the values 1 and 2 from data.
    value = [value for value in find(path.a.b[wc].c, data)]
    assert value == [1, 2]


readme += """
# Solar System Json Document

The examples shown in this README use the following json document.  It describes our solar system. Click to expand.  
<details><summary>solar_system = {...}</summary>
<p>

```json
"""
readme += get_solar_system_json()
readme += """
```

</p>
</details>
"""

readme += """
# Quick comparison between Imperative and Declarative Solution.

The following problem is solved using a Imperative Solution and a Declarative Solution to try to illustrate the 
differences between the two approaches.  

The problem is fetch the planet by name from the given solar system json document.  

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
| List first two inner planets                 | /star/planets.inner[position()<3]   | $.star.planets.inner[:2]                  | path.star.planets.inner[0:2]       |
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


readme += """# Traversal Functions"""


@readme.append_function
def test_traversal_function_get(solar_system):
    """## get"""

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

    # Or if preferred, a default value can be given.
    human_population = get(path.star.human_population, solar_system, default=0)
    assert human_population == 0

    # In addition to a constant, the default value may also be a callable
    def population():
        return 0

    human_population = get(path.star.human_population, solar_system, default=population)
    assert human_population == 0

    # The default value can be automatically injected in to json document
    human_population = get(path.star.human_population, solar_system, default=1, store_default=True)
    assert human_population == solar_system["star"]["human_population"]

    # The data source can be a json data structure or a Match object.
    parent_match = get_match(path.star.planets.inner, solar_system)
    name = get(path[2].name, parent_match)
    assert name == "Earth"


@readme.append_function
def test_traversal_function_set(solar_system):
    """## set_"""

    # The **set_** function modifies the json document.

    # Use the set_ function to modify the star name.
    sun = get(path.star.name, solar_system)
    assert sun == 'Sun'
    set_(path.star.name, "RedSun", solar_system)
    sun = get(path.star.name, solar_system)
    assert sun == 'RedSun'
    assert solar_system["star"]["name"] == 'RedSun'

    # Use the set_ to add planet9.   This example creates multiple objects in one step.
    name = get(path.star.planets.outer[4].name, solar_system, default=None)
    assert name is None
    planets_count = len(list(find(path.star.planets.wc[wc].name, solar_system)))
    assert planets_count == 8

    set_(path.star.planets.outer[4].name, 'planet9', solar_system, cascade=True)

    name = get(path.star.planets.outer[4].name, solar_system, default=None)
    assert name == 'planet9'
    planets_count = len(list(find(path.star.planets.wc[wc].name, solar_system)))
    assert planets_count == 9


@readme.append_function
def test_traversal_function_find(solar_system):
    """## find"""

    # The **find** function returns an Iterator that iterates to each value the path leads to.  Each value is
    # determine on its iteration.

    # Find all of the planet names.
    inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']

    # The data source can be a json data structure or a Match object.
    parent_match = get_match(path.star.planets.inner, solar_system)
    inner_planets = [planet for planet in find(path[wc].name, parent_match)]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']


@readme.append_function
def test_traversal_function_get_match(solar_system):
    """## get_match"""

    # The **get_match** function returns the first Match the path leads to.

    # Get the star name from the solar_system
    match = get_match(path.star.name, solar_system)
    assert match.data == 'Sun'

    # When there is no match, MatchNotFoundError is thrown.
    try:
        get_match(path.star.human_population, solar_system)
        assert False, "Not expecting humans on the sun"
    except MatchNotFoundError:
        pass

    # Or if preferred, **None** is returned if must_match is set to False.
    match = get_match(path.star.human_population, solar_system, must_match=False)
    assert match is None

    # The data source can be a json data structure or a Match object.
    parent_match = get_match(path.star.planets.inner, solar_system)
    earth_match = get_match(path[2].name, parent_match)
    assert earth_match.path_as_str == "$.star.planets.inner[2].name"
    assert earth_match.data == "Earth"


@readme.append_function
def test_traversal_function_find_matches(solar_system):
    """## find_matches"""
    # The **find_matches** function returns an Iterator that iterates to each match the path leads to.  Each match is
    # determine on its iteration.

    # Find the path to each of the inner planets.
    for match in find_matches(path.star.planets.inner[wc], solar_system):
        assert match.path_as_str in [
            '$.star.planets.inner[0]',
            '$.star.planets.inner[1]',
            '$.star.planets.inner[2]',
            '$.star.planets.inner[3]',
        ]

    # The data source can be a json data structure or a Match object.
    parent_match = get_match(path.star.planets.inner, solar_system)
    for match in find_matches(path[wc], parent_match):
        assert match.path_as_str in [
            '$.star.planets.inner[0]',
            '$.star.planets.inner[1]',
            '$.star.planets.inner[2]',
            '$.star.planets.inner[3]',
        ]


@readme.append_function
def test_traversal_function_match_class(solar_system):
    """## The Match Class"""

    # The **Match** class provides metadata about the match.
    match = get_match(path.star.name, solar_system)

    # The explicit path to the match
    explicit_path = match.path
    assert explicit_path == path.star.name

    # The string representation of the match including the value: "path=value"
    assert repr(match) == "$.star.name=Sun"
    assert str(match) == "$.star.name=Sun"

    # The string representation of the match, but with just the path component.
    assert match.path_as_str == "$.star.name"

    # A list containing each match in the path.
    assert match.path_match_list == [match.parent.parent, match.parent, match]

    # The key that points to the match value.  The data_name is a dictionary key if the parent is a dict or an index if
    # the parent is a list.
    assert match.data_name == "name" and match.parent.data[match.data_name] == match.data

    # The value the path matched.
    assert match.data == "Sun"

    # The parent match.
    assert match.parent.path_as_str == "$.star"

    # The match can modify the value
    match.data = "Soleil"
    assert repr(match) == "$.star.name=Soleil"
    del match.data
    assert repr(match) == "$.star.name=None"
    match.data = "Sun"
    assert repr(match) == "$.star.name=Sun"
    match.pop()
    assert repr(match) == "$.star.name=None"


@readme.append_function
def test_tracing(solar_system):
    """## Tracing Debugging"""

    # All of the functions: get, find, get_match and find_matchesm, support tracing.   An option, when enabled,
    # records the route the algorithm takes to determine a match.

    # This example logs the route the algorithm takes to find the inner planets.  The **print**
    # function is give to capture the logs, but any single argument function can be used.
    inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system, trace=log_to(print))]
    assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']

    # The results
    """
    at $.star got {'name': 'Sun', 'dia...
    at $.star.planets got {'inner': [{'name': ...
    at $.star.planets.inner got [{'name': 'Mercury',...
    at $.star.planets.inner[*] got {'name': 'Mercury', ...
    at $.star.planets.inner[0].name got 'Mercury'
    at $.star.planets.inner[*] got {'name': 'Venus', 'N...
    at $.star.planets.inner[1].name got 'Venus'
    at $.star.planets.inner[*] got {'name': 'Earth', 'N...
    at $.star.planets.inner[2].name got 'Earth'
    at $.star.planets.inner[*] got {'name': 'Mars', 'Nu...
    at $.star.planets.inner[3].name got 'Mars'
    """


readme += """# Path"""


@readme.append_function
def test_path_root(solar_system):
    """## The root"""
    # The **path** point to root of the tree.
    match = get_match(path, solar_system)

    assert match.data == solar_system

    # In a filter path point to the current element.
    match = get_match(path.star.name[has(path == 'Sun')], solar_system)

    assert match.data == 'Sun'


readme += """## Dictionaries"""


@readme.append_function
def test_path_keys(solar_system):
    """### Keys"""

    # The dictionary keys are referenced as dynamic attributes on a path.
    inner_from_attribute = get(path.star.planets.inner, solar_system)
    inner_from_string_keys = get(path["star"]["planets"]["inner"], solar_system)

    assert inner_from_attribute == inner_from_string_keys == solar_system["star"]["planets"]["inner"]


@readme.append_function
def test_path_keys_special_characters(solar_system):
    """### Keys With Special Characters"""

    # Dictionary keys that are not valid python syntax can be referenced as double quoted strings.
    sun_equatorial_diameter = get(path.star.planets.inner[0]["Number of Moons"], solar_system)

    assert sun_equatorial_diameter == solar_system["star"]["planets"]["inner"][0]["Number of Moons"]

    # Dictionaries that have alot of keys with a dash in the name can can use **pathd** instead.  It will interpret
    # path attributes with underscore as dashes.
    mercury_has_moons = get(pathd.star.planets.inner[0].has_moons, solar_system)

    assert mercury_has_moons == solar_system["star"]["planets"]["inner"][0]["has-moons"]


@readme.append_function
def test_path_keys_wildcard(solar_system):
    """### Wildcard as a Key."""

    # The **wildcard** attribute specifies all sibling keys.   It is useful for iterating over attributes.
    star_children = [child for child in find(path.star.wildcard, solar_system)]
    assert star_children == [solar_system["star"]["name"],
                             solar_system["star"]["diameter"],
                             solar_system["star"]["age"],
                             solar_system["star"]["planets"], ]

    # The **wc** is the short version of wildcard.
    star_children = [child for child in find(path.star.wc, solar_system)]
    assert star_children == [solar_system["star"]["name"],
                             solar_system["star"]["diameter"],
                             solar_system["star"]["age"],
                             solar_system["star"]["planets"], ]


@readme.append_function
def test_path_keys_comma_delimited(solar_system):
    """### Comma Delimited Keys"""

    # Multiple dictionary keys can be specified using a comma delimited list.
    last_and_first = [planet for planet in find(path.star["diameter", "name"], solar_system)]
    assert last_and_first == [1391016, "Sun"]


readme += """## List"""


@readme.append_function
def test_path_list(solar_system):
    """### Indexes"""

    # List can be access using index.
    earth = get(path.star.planets.inner[2], solar_system)
    assert earth == solar_system["star"]["planets"]["inner"][2]

    # List the third inner and outer planet.
    last_two = [planet for planet in find(path.star.wc.wc[2].name, solar_system)]
    assert last_two == ['Earth', 'Uranus']


@readme.append_function
def test_path_list_slice(solar_system):
    """### Slices"""

    # List can be access using slices.

    # List the first two planets.
    first_two = [planet for planet in find(path.star.planets.outer[:2].name, solar_system)]
    assert first_two == ["Jupiter", "Saturn"]

    # List the last two planets.
    last_two = [planet for planet in find(path.star.planets.outer[-2:].name, solar_system)]
    assert last_two == ["Uranus", "Neptune"]

    # List all outer planets in reverse.
    last_two = [planet for planet in find(path.star.planets.outer[::-1].name, solar_system)]
    assert last_two == ["Neptune", "Uranus", "Saturn", "Jupiter"]

    # List the last inner and outer planets.
    last_two = [planet for planet in find(path.star.wc.wc[-1:].name, solar_system)]
    assert last_two == ["Mars", "Neptune"]


@readme.append_function
def test_path_list_comma_delimited(solar_system):
    """### Comma Delimited Indexes."""

    # List indexes can be specified as a comma delimited list.
    last_and_first = [planet for planet in find(path.star.planets.outer[3, 0].name, solar_system)]
    assert last_and_first == ["Neptune", "Jupiter"]


@readme.append_function
def test_path_list_wildcard(solar_system):
    """### Wildcard as an Index."""

    # The **wildcard** word can be used as a list index.   It is useful for iterating over attributes.
    all_outer = [planet for planet in find(path.star.planets.outer[wildcard].name, solar_system)]
    assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

    # The **wc** is the short version of wildcard.
    all_outer = [planet for planet in find(path.star.planets.outer[wc].name, solar_system)]
    assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

    # The dictionary wildcard is given as dot notation and cannot be used to iterator over a list.  The list wildcard
    # is given as an index and cannot be used to iterate over dictionary keys.
    all_planets = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


@readme.append_function
def test_path_recursion(solar_system):
    """## Recursion"""

    # The **recursive** word implies recursive search.  It executes a preorder tree traversal.  The search algorithm
    # descends the tree hierarchy evaluating the path on each vertex until a match occurs.  On each iteration it
    # continues where it left off. This is an example that finds all the planets names.
    all_planets = [p for p in find(path.star.planets.recursive.name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # The **rec** is the short version of recursive.
    all_planets = [p for p in find(path.star.planets.rec.name, solar_system)]
    assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # Here is another example that finds all the celestial bodies names.
    all_celestial_bodies = [p for p in find(path.rec.name, solar_system)]
    assert all_celestial_bodies == ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                    'Neptune']


readme += """## Filters

Filters are use to add additional search criteria.
"""


@readme.append_function
def test_path_has_filter(solar_system):
    """### has filter"""

    # The **has** function is a filter that evaluates a branched off path relative to its parent path.  This example
    # finds all celestial bodies that have planets.
    sun = get(path.rec[has(path.planets)].name, solar_system)
    assert sun == "Sun"

    # This search finds all celestial bodies that have a has-moons attribute.
    all_celestial_bodies_moon_attribute = [planet for planet in find(path.rec[has(pathd.has_moons)].name, solar_system)]
    assert all_celestial_bodies_moon_attribute == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                                   'Neptune']

    # This search finds all celestial bodies that have moons. Note the **operator.truth** is used to exclude planets
    # that don't have moons.
    all_celestial_bodies_moon_attribute = [planet for planet in
                                           find(path.rec[has(pathd.has_moons, operator.truth)].name, solar_system)]
    assert all_celestial_bodies_moon_attribute == ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


@readme.append_function
def test_path_has_filter_comparison_operators(solar_system):
    """### has filter comparison operators"""

    # Filters can be specified with a comparison operator.
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


@readme.append_function
def test_path_has_filter_type_conversion(solar_system):
    """### has filter type conversion"""

    # Sometimes the value is the wrong type for the comparison operator. In this example the attribute
    # "Number of Moons" is str type.
    planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > "5")].name, solar_system)]
    assert planets == ['Jupiter', 'Saturn']

    # This is how to convert the type to an int before applying the comparison operator.
    planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > 5, int)].name, solar_system)]
    assert planets == ['Jupiter', 'Saturn', 'Uranus', 'Neptune']


@readme.append_function
def test_path_has_filter_operators_as_single_argument_functions(solar_system):
    """### has filter comparison operators as single argument functions"""

    # A filter operator can be specified as a single argument function.  Here an example that searches for planets that
    # have the same diameter as earth.
    earths_diameter = partial(operator.eq, 12756)
    earth = [planet for planet in find(path.rec[has(path.diameter, earths_diameter)].name, solar_system)]
    assert earth == ['Earth']

    # Any single argument function can be used as an operator.  This example uses a Regular Expression to finds
    # planets that end with s.
    name_ends_with_s = re.compile(r"\w+s").match
    earth = [planet for planet in find(path.rec[has(path.name, name_ends_with_s)].name, solar_system)]
    assert earth == ['Venus', 'Mars', 'Uranus']

    # This example uses a closure to find planets that have the same diameter as earth.
    def smaller_than_earth(value):
        return value < 12756

    earth = [planet for planet in find(path.rec[has(path.diameter, smaller_than_earth)].name, solar_system)]
    assert earth == ['Mercury', 'Venus', 'Mars']


@readme.append_function
def test_path_filter_has_all(solar_system):
    """### logical and, or and not filters"""

    # #### has_all
    # A regular express to test if second letter in the value is an a.
    second_letter_is_a = re.compile(r".a.*").fullmatch

    # The **has_all** function evaluates as the logical **and** operator.   It is equivalent to: (arg1 and arg2 and ...)
    found = [planet for planet in find(
        path.rec[has_all(path.diameter < 10000, (path.name, second_letter_is_a))].name,
        solar_system)
             ]
    assert found == ['Mars']

    # #### has_any
    # The **has_any** function evaluates as the logical **or** operator.   It is equivalent to: (arg1 and arg2 and ...)
    found = [planet for planet in find(
        path.rec[has_any(path.diameter < 10000, (path.name, second_letter_is_a))].name,
        solar_system)
             ]
    assert found == ['Mercury', 'Earth', 'Mars', 'Saturn']

    # #### has_not
    # The **has_not** function evaluates as the logical **not** operator.   It is equivalent to: (not arg)
    # This example find all the planets names not not equal to Earth.  Note the double nots.
    found = [planet for planet in find(
        path.rec[has_not(path.name != 'Earth')].name,
        solar_system)
             ]
    assert found == ['Earth']

    # #### Combining has, has_all, has_any, and has_not filters.
    # Each of the **has** function can be passed as arguments to any of the other **has** function to construct complex
    # boolean equation.  This example is equivalent to:
    # (10000 > diameter  or diameter > 20000) and second_letter_is_a(name))
    found = [planet for planet in find(
        path.rec[has_all(has_any(path.diameter < 10000, path.diameter > 20000), (path.name, second_letter_is_a))].name,
        solar_system)
             ]
    assert found == ['Mars', 'Saturn']

    # #### has.these
    # The decorator **has.these** can be used to construct the boolean equations more explicitly.  This example shows
    # to use python built in and, or and not operators.
    @has.these(path.diameter < 10000, path.diameter > 20000, (path.name, second_letter_is_a))
    def predicate(parent_match: Match, small_diameter, large_diameter, name_second_letter_is_a):
        return (small_diameter(parent_match) or large_diameter(parent_match)) and name_second_letter_is_a(parent_match)

    found = [planet for planet in find(path.rec[predicate].name, solar_system)]
    assert found == ['Mars', 'Saturn']


@readme.append_function
def test_path_filter_customer_predicate(solar_system):
    """### A custom filter."""

    # A predicate is a single argument function that returns anything. The argument is the current match.   The has
    # function is a fancy predicate.

    # This example writes a custom predicate that find all of Earth's neighbours.
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


readme += """# Class Descriptors"""


@readme.append_function
def test_path_descriptor(solar_system):
    """### basic path descriptor"""

    # paths can be added as properties to a class using the path_descriptor function.
    planets = path.star.planets.wc[wc]

    class SolarSystem(Document):
        jupiter_name = attr(path.star.planets.outer[0].name)
        saturn_name = attr(path.star.planets.outer[1].name)
        big_planets = attr(planets[has(path.diameter > 25000)].name, getter=find)
        small_planets = attr(planets[has(path.diameter <= 25000)].name, getter=find, to_wrapped_value=list)
        number_of_planets = attr(planets, getter=find, to_wrapped_value=lambda itr: len(list(itr)))

    # The property support both gets and sets and dels
    ss = SolarSystem(solar_system)
    assert ss.jupiter_name == 'Jupiter'
    assert ss.saturn_name == 'Saturn'

    # Rename Jupiter to Planet 5
    ss.jupiter_name = 'Planet 5'
    assert ss.jupiter_name == 'Planet 5'

    # The assignment operation alters the original document.
    assert solar_system["star"]["planets"]["outer"][0]["name"] == 'Planet 5'

    # remove Jupiter's name
    del ss.jupiter_name
    with pytest.raises(MatchNotFoundError):
        print(ss.jupiter_name)
    assert "name" not in solar_system["star"]["planets"]["outer"][0]

    # There are still 8 planets because only Jupiter's name was delete
    assert ss.number_of_planets == 8

    # list all the big planets.  Remember Jupiter was deleted.
    big_planets = [name for name in ss.big_planets]
    assert big_planets == ['Saturn', 'Uranus', 'Neptune']

    # list all the small planets.
    assert ss.small_planets == ['Mercury', 'Venus', 'Earth', 'Mars']


@readme.append_function
def test_path_descriptor_adaptor_types(solar_system):
    """### document typed path descriptor"""

    # A descriptor support wrapping json types with an adaptor class. This example wraps the json that represents a
    # planet with the planet class.   The Planet class extends the Document class which provides the marshalling
    # methods.
    class Planet(Document):
        name = attr(path=path.name)

    class SolarSystem(Document):
        jupiter = attr_typed(Planet, path.star.planets.outer[0])
        planets = attr_iter_typed(Planet, path.star.planets.wc[wc])
        outer_planets = attr_list_typed(Planet, path.star.planets.outer)

    # The getter returns the planet type
    ss = SolarSystem(solar_system)
    planet = ss.jupiter
    assert planet.name == 'Jupiter'

    # rename Jupiter to Planet 5
    planet.name = 'Planet 5'
    assert planet.name == 'Planet 5'

    # The assignment operation alters the original document.
    assert solar_system["star"]["planets"]["outer"][0]["name"] == 'Planet 5'

    # Jupiter can be renamed by replacing the planet with an imposter.
    impostor_planet = Planet({})
    impostor_planet.name = 'Imposter Jupiter'
    ss.jupiter = impostor_planet
    assert ss.jupiter.name == 'Imposter Jupiter'

    # The imposter planet also alters the original document.
    assert solar_system["star"]["planets"]["outer"][0]["name"] == 'Imposter Jupiter'

    # An attribute descriptor can return an iterator where each element is converted to the correct type.
    planets = [planet.name for planet in ss.planets]
    assert planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Imposter Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # An attribute descriptor can return an list where each element is converted to the correct type.
    assert ss.outer_planets[0].name == 'Imposter Jupiter'

    # The list can be modified and the underline document is modified too.
    jupiter = Planet({})
    jupiter.name = 'Jupiter'
    ss.outer_planets[0] = jupiter
    planets = [planet.name for planet in ss.planets]
    assert planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


@readme.append_function
def test_path_descriptor_custom_types(solar_system):
    """### custom typed path descriptor"""

    # A descriptor support wrapping json types with an adaptor class. This example wraps the json that represents a
    # planet with the planet class.   This Planet class defines its own marshalling methods.
    class Planet:
        def __init__(self, name: str = None):
            self._name = name

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, name: str):
            self._name = name

        @staticmethod
        def to_wrapped_value(json_: JsonArgTypes) -> Planet:
            return Planet(json_["name"])

        @staticmethod
        def to_json_value(planet_: Planet) -> JsonArgTypes:
            return {"name": planet_.name}

    class SolarSystem(Document):
        jupiter = attr_typed(Planet, path.star.planets.outer[0],
                             to_wrapped_value=Planet.to_wrapped_value,
                             to_json_value=Planet.to_json_value)
        planets = attr_iter_typed(Planet, path.star.planets.wc[wc],
                                  to_wrapped_value=Planet.to_wrapped_value)
        outer_planets = attr_list_typed(Planet, path.star.planets.outer,
                                        to_wrapped_value=Planet.to_wrapped_value,
                                        to_json_value=Planet.to_json_value)

    # The getter returns the planet type
    ss = SolarSystem(solar_system)
    planet = ss.jupiter
    assert planet.name == 'Jupiter'

    # rename Jupiter to Planet 5
    planet.name = 'Planet 5'
    assert planet.name == 'Planet 5'

    # Jupiter can be renamed by replacing the planet with an imposter.
    impostor_planet = Planet()
    impostor_planet.name = 'Imposter Jupiter'
    ss.jupiter = impostor_planet
    assert ss.jupiter.name == 'Imposter Jupiter'

    # The imposter planet also alters the original document.
    assert solar_system["star"]["planets"]["outer"][0]["name"] == 'Imposter Jupiter'

    # An attribute descriptor can return an iterator where each element is converted to the correct type.
    planets = [planet.name for planet in ss.planets]
    assert planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Imposter Jupiter', 'Saturn', 'Uranus', 'Neptune']

    # An attribute descriptor can return an list where each element is converted to the correct type.
    assert ss.outer_planets[0].name == 'Imposter Jupiter'

    # The list can be modified and the underline document is modified too.
    jupiter = Planet()
    jupiter.name = 'Jupiter'
    ss.outer_planets[0] = jupiter
    planets = [planet.name for planet in ss.planets]
    assert planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
