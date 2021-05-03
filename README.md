
# The **treepath** Package.

The **treepath** package offers a [declarative programming](https://en.wikipedia.org/wiki/Declarative_programming) 
approach to extracting data from a [json](https://docs.python.org/3/library/json.html) data structure.  The expressions 
are a [query language](https://en.wikipedia.org/wiki/Query_language) similar to
[jsonpath](https://goessner.net/articles/JsonPath/), and [Xpath](https://en.wikipedia.org/wiki/XPath), but are
written in native python syntax.

Note python 3.6 is supported in version earlier that 1.0.0.

# Quick start
All of the treepath components should be imported as follows:
```python
from treepath import path, find, wc, get, has, get_match, find_matches, pathd, wildcard, \
    MatchNotFoundError, Match, log_to, has_all, has_any, has_not
```

A treepath example that fetches the value 1 from data.

```python
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

```
A treepath example that fetches the values 1 and 2 from data.

```python
value = [value for value in find(path.a.b[wc].c, data)]
assert value == [1, 2]
```

# Solar System Json Document

The examples shown in this README use the following json document.  It describes our solar system. Click to expand.  
<details><summary>solar_system = {...}</summary>
<p>

```json

{
  "star": {
    "name": "Sun",
    "diameter": 1391016,
    "age": null,
    "planets": {
      "inner": [
        {
          "name": "Mercury",
          "Number of Moons": "0",
          "diameter": 4879,
          "has-moons": false
        },
        {
          "name": "Venus",
          "Number of Moons": "0",
          "diameter": 12104,
          "has-moons": false
        },
        {
          "name": "Earth",
          "Number of Moons": "1",
          "diameter": 12756,
          "has-moons": true
        },
        {
          "name": "Mars",
          "Number of Moons": "2",
          "diameter": 6792,
          "has-moons": true
        }
      ],
      "outer": [
        {
          "name": "Jupiter",
          "Number of Moons": "79",
          "diameter": 142984,
          "has-moons": true
        },
        {
          "name": "Saturn",
          "Number of Moons": "82",
          "diameter": 120536,
          "has-moons": true
        },
        {
          "name": "Uranus",
          "Number of Moons": "27",
          "diameter": 51118,
          "has-moons": true
        },
        {
          "name": "Neptune",
          "Number of Moons": "14",
          "diameter": 49528,
          "has-moons": true
        }
      ]
    }
  }
}


```

</p>
</details>


# Quick comparison between Imperative and Declarative Solution.

The following problem is solved using a Imperative Solution and a Declarative Solution to try to illustrate the 
differences between the two approaches.  

The problem is fetch the planet by name from the given solar system json document.  



## Imperative Solution

The first example uses flow control statements to define a
[Imperative Solution]( https://en.wikipedia.org/wiki/Imperative_programming).   This is a
very common approach to solving problems.

```python


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
```

## Declarative  Solution

The second example uses treepath to define a
[declarative solution](https://en.wikipedia.org/wiki/Declarative_programming).
It solves the same problem without defining any flow control statements.    This keeps the Cyclomatic and
Cognitive Complexity low.

```python


def get_planet_by_name(name: str, the_solar_system):
    return get(
        path.star.planets.wc[wc][has(path.name == name)],
        the_solar_system,
        default=None
    )

actual = get_planet_by_name('Earth', solar_system)
expected = {'Number of Moons': '1', 'diameter': 12756, 'has-moons': True, 'name': 'Earth'}
assert actual == expected
```

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

# Traversal Functions
## get
The **get** function returns the first value the path leads to.

Get the star name from the solar_system

```python
sun = get(path.star.name, solar_system)
assert sun == 'Sun'

```
When there is no match, MatchNotFoundError is thrown.

```python
try:
    get(path.star.human_population, solar_system)
    assert False, "Not expecting humans on the sun"
except MatchNotFoundError:
    pass

```
Or if preferred, a default value can be given.

```python
human_population = get(path.star.human_population, solar_system, default=0)
assert human_population == 0

```
The data source can be a json data structure or a Match object.

```python
parent_match = get_match(path.star.planets.inner, solar_system)
name = get(path[2].name, parent_match)
assert name == "Earth"
```
## find
The **find** function returns an Iterator that iterates to each value the path leads to.  Each value is
determine on its iteration.

Find all of the planet names.

```python
inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system)]
assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']

```
The data source can be a json data structure or a Match object.

```python
parent_match = get_match(path.star.planets.inner, solar_system)
inner_planets = [planet for planet in find(path[wc].name, parent_match)]
assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']
```
## get_match
The **get_match** function returns the first Match the path leads to.

Get the star name from the solar_system

```python
match = get_match(path.star.name, solar_system)
assert match.data == 'Sun'

```
When there is no match, MatchNotFoundError is thrown.

```python
try:
    get_match(path.star.human_population, solar_system)
    assert False, "Not expecting humans on the sun"
except MatchNotFoundError:
    pass

```
Or if preferred, **None** is returned if not must_match is given.

```python
match = get_match(path.star.human_population, solar_system, must_match=False)
assert match is None

```
The data source can be a json data structure or a Match object.

```python
parent_match = get_match(path.star.planets.inner, solar_system)
earth_match = get_match(path[2].name, parent_match)
assert earth_match.path == "$.star.planets.inner[2].name"
assert earth_match.data == "Earth"
```
## find_matches
The **find_matches** function returns an Iterator that iterates to each match the path leads to.  Each match is
determine on its iteration.

Find the path to each of the inner planets.

```python
for match in find_matches(path.star.planets.inner[wc], solar_system):
    assert match.path in [
        '$.star.planets.inner[0]',
        '$.star.planets.inner[1]',
        '$.star.planets.inner[2]',
        '$.star.planets.inner[3]',
    ]

```
The data source can be a json data structure or a Match object.

```python
parent_match = get_match(path.star.planets.inner, solar_system)
for match in find_matches(path[wc], parent_match):
    assert match.path in [
        '$.star.planets.inner[0]',
        '$.star.planets.inner[1]',
        '$.star.planets.inner[2]',
        '$.star.planets.inner[3]',
    ]
```
## The Match Class
The **Match** class provides metadata about the match.

```python
match = get_match(path.star.name, solar_system)

```
The string representation of match = [path=value].

```python
assert repr(match) == "$.star.name=Sun"

```
A list containing each match in the path.

```python
assert match.path_as_list == [match.parent.parent, match.parent, match]

```
The string representation of match path.

```python
assert match.path == "$.star.name"

```
The key that points to the match value.  The data_name is a dictionary key if the parent is a dict or an index if
the parent is a list.

```python
assert match.data_name == "name" and match.parent.data[match.data_name] == match.data

```
The value the path matched.

```python
assert match.data == "Sun"

```
The parent match.

```python
assert match.parent.path == "$.star"
```
## Tracing Debugging
All of the functions: get, find, get_match and find_matchesm, support tracing.   An option, when enabled,
records the route the algorithm takes to determine a match.

This example logs the route the algorithm takes to find the inner planets.  The **print**
function is give to capture the logs, but any single argument function can be used.

```python
inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system, trace=log_to(print))]
assert inner_planets == ['Mercury', 'Venus', 'Earth', 'Mars']

```
The results

```python
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
```
# Path
## The root
The **path** point to root of the tree.

```python
match = get_match(path, solar_system)

assert match.data == solar_system

```
In a filter path point to the current element.

```python
match = get_match(path.star.name[has(path == 'Sun')], solar_system)

assert match.data == 'Sun'
```
## Dictionaries
### Keys
The dictionary keys are referenced as dynamic attributes on a path.

```python
inner_from_attribute = get(path.star.planets.inner, solar_system)
inner_from_string_keys = get(path["star"]["planets"]["inner"], solar_system)

assert inner_from_attribute == inner_from_string_keys == solar_system["star"]["planets"]["inner"]
```
### Keys With Special Characters
Dictionary keys that are not valid python syntax can be referenced as double quoted strings.

```python
sun_equatorial_diameter = get(path.star.planets.inner[0]["Number of Moons"], solar_system)

assert sun_equatorial_diameter == solar_system["star"]["planets"]["inner"][0]["Number of Moons"]

```
Dictionaries that have alot of keys with a dash in the name can can use **pathd** instead.  It will interpret
path attributes with underscore as dashes.

```python
mercury_has_moons = get(pathd.star.planets.inner[0].has_moons, solar_system)

assert mercury_has_moons == solar_system["star"]["planets"]["inner"][0]["has-moons"]
```
### Wildcard as a Key.
The **wildcard** attribute specifies all sibling keys.   It is useful for iterating over attributes.

```python
star_children = [child for child in find(path.star.wildcard, solar_system)]
assert star_children == [solar_system["star"]["name"],
                         solar_system["star"]["diameter"],
                         solar_system["star"]["age"],
                         solar_system["star"]["planets"], ]

```
The **wc** is the short version of wildcard.

```python
star_children = [child for child in find(path.star.wc, solar_system)]
assert star_children == [solar_system["star"]["name"],
                         solar_system["star"]["diameter"],
                         solar_system["star"]["age"],
                         solar_system["star"]["planets"], ]
```
### Comma Delimited Keys
Multiple dictionary keys can be specified using a comma delimited list.

```python
last_and_first = [planet for planet in find(path.star["diameter", "name"], solar_system)]
assert last_and_first == [1391016, "Sun"]
```
## List
### Indexes
List can be access using index.

```python
earth = get(path.star.planets.inner[2], solar_system)
assert earth == solar_system["star"]["planets"]["inner"][2]

```
List the third inner and outer planet.

```python
last_two = [planet for planet in find(path.star.wc.wc[2].name, solar_system)]
assert last_two == ['Earth', 'Uranus']
```
### Slices
List can be access using slices.

List the first two planets.

```python
first_two = [planet for planet in find(path.star.planets.outer[:2].name, solar_system)]
assert first_two == ["Jupiter", "Saturn"]

```
List the last two planets.

```python
last_two = [planet for planet in find(path.star.planets.outer[-2:].name, solar_system)]
assert last_two == ["Uranus", "Neptune"]

```
List all outer planets in reverse.

```python
last_two = [planet for planet in find(path.star.planets.outer[::-1].name, solar_system)]
assert last_two == ["Neptune", "Uranus", "Saturn", "Jupiter"]

```
List the last inner and outer planets.

```python
last_two = [planet for planet in find(path.star.wc.wc[-1:].name, solar_system)]
assert last_two == ["Mars", "Neptune"]
```
### Comma Delimited Indexes.
List indexes can be specified as a comma delimited list.

```python
last_and_first = [planet for planet in find(path.star.planets.outer[3, 0].name, solar_system)]
assert last_and_first == ["Neptune", "Jupiter"]
```
### Wildcard as an Index.
The **wildcard** word can be used as a list index.   It is useful for iterating over attributes.

```python
all_outer = [planet for planet in find(path.star.planets.outer[wildcard].name, solar_system)]
assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

```
The **wc** is the short version of wildcard.

```python
all_outer = [planet for planet in find(path.star.planets.outer[wc].name, solar_system)]
assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]

```
The dictionary wildcard is given as dot notation and cannot be used to iterator over a list.  The list wildcard
is given as an index and cannot be used to iterate over dictionary keys.

```python
all_planets = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
```
## Recursion
The **recursive** word implies recursive search.  It executes a preorder tree traversal.  The search algorithm
descends the tree hierarchy evaluating the path on each vertex until a match occurs.  On each iteration it
continues where it left off. This is an example that finds all the planets names.

```python
all_planets = [p for p in find(path.star.planets.recursive.name, solar_system)]
assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

```
The **rec** is the short version of recursive.

```python
all_planets = [p for p in find(path.star.planets.rec.name, solar_system)]
assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

```
Here is another example that finds all the celestial bodies names.

```python
all_celestial_bodies = [p for p in find(path.rec.name, solar_system)]
assert all_celestial_bodies == ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                'Neptune']
```
## Filters

Filters are use to add additional search criteria.

### has filter
The **has** function is a filter that evaluates a branched off path relative to its parent path.  This example
finds all celestial bodies that have planets.

```python
sun = get(path.rec[has(path.planets)].name, solar_system)
assert sun == "Sun"

```
This search finds all celestial bodies that have a has-moons attribute.

```python
all_celestial_bodies_moon_attribute = [planet for planet in find(path.rec[has(pathd.has_moons)].name, solar_system)]
assert all_celestial_bodies_moon_attribute == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus',
                                               'Neptune']

```
This search finds all celestial bodies that have moons. Note the **operator.truth** is used to exclude planets
that don't have moons.

```python
all_celestial_bodies_moon_attribute = [planet for planet in
                                       find(path.rec[has(pathd.has_moons, operator.truth)].name, solar_system)]
assert all_celestial_bodies_moon_attribute == ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
```
### has filter comparison operators
Filters can be specified with a comparison operator.

```python
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
```
### has filter type conversion
Sometimes the value is the wrong type for the comparison operator. In this example the attribute
"Number of Moons" is str type.

```python
planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > "5")].name, solar_system)]
assert planets == ['Jupiter', 'Saturn']

```
This is how to convert the type to an int before applying the comparison operator.

```python
planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > 5, int)].name, solar_system)]
assert planets == ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
```
### has filter comparison operators as single argument functions
A filter operator can be specified as a single argument function.  Here an example that searches for planets that
have the same diameter as earth.

```python
earths_diameter = partial(operator.eq, 12756)
earth = [planet for planet in find(path.rec[has(path.diameter, earths_diameter)].name, solar_system)]
assert earth == ['Earth']

```
Any single argument function can be used as an operator.  This example uses a Regular Expression to finds
planets that end with s.

```python
name_ends_with_s = re.compile(r"\w+s").match
earth = [planet for planet in find(path.rec[has(path.name, name_ends_with_s)].name, solar_system)]
assert earth == ['Venus', 'Mars', 'Uranus']

```
This example uses a closure to find planets that have the same diameter as earth.

```python
def smaller_than_earth(value):
    return value < 12756

earth = [planet for planet in find(path.rec[has(path.diameter, smaller_than_earth)].name, solar_system)]
assert earth == ['Mercury', 'Venus', 'Mars']
```
### logical and, or and not filters
#### has_all
A regular express to test if second letter in the value is an a.

```python
second_letter_is_a = re.compile(r".a.*").fullmatch

```
The **has_all** function evaluates as the logical **and** operator.   It is equivalent to: (arg1 and arg2 and ...)

```python
found = [planet for planet in find(
    path.rec[has_all(path.diameter < 10000, (path.name, second_letter_is_a))].name,
    solar_system)
         ]
assert found == ['Mars']

```
#### has_any
The **has_any** function evaluates as the logical **or** operator.   It is equivalent to: (arg1 and arg2 and ...)

```python
found = [planet for planet in find(
    path.rec[has_any(path.diameter < 10000, (path.name, second_letter_is_a))].name,
    solar_system)
         ]
assert found == ['Mercury', 'Earth', 'Mars', 'Saturn']

```
#### has_not
The **has_not** function evaluates as the logical **not** operator.   It is equivalent to: (not arg)
This example find all the planets names not not equal to Earth.  Note the double nots.

```python
found = [planet for planet in find(
    path.rec[has_not(path.name != 'Earth')].name,
    solar_system)
         ]
assert found == ['Earth']

```
#### Combining has, has_all, has_any, and has_not filters.
Each of the **has** function can be passed as arguments to any of the other **has** function to construct complex
boolean equation.  This example is equivalent to:
(10000 > diameter  or diameter > 20000) and second_letter_is_a(name))

```python
found = [planet for planet in find(
    path.rec[has_all(has_any(path.diameter < 10000, path.diameter > 20000), (path.name, second_letter_is_a))].name,
    solar_system)
         ]
assert found == ['Mars', 'Saturn']

```
#### has.these
The decorator **has.these** can be used to construct the boolean equations more explicitly.  This example shows
to use python built in and, or and not operators.

```python
@has.these(path.diameter < 10000, path.diameter > 20000, (path.name, second_letter_is_a))
def predicate(parent_match: Match, small_diameter, large_diameter, name_second_letter_is_a):
    return (small_diameter(parent_match) or large_diameter(parent_match)) and name_second_letter_is_a(parent_match)

found = [planet for planet in find(path.rec[predicate].name, solar_system)]
assert found == ['Mars', 'Saturn']
```
### A custom filter.
A predicate is a single argument function that returns anything. The argument is the current match.   The has
function is a fancy predicate.

This example writes a custom predicate that find all of Earth's neighbours.

```python
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
```
