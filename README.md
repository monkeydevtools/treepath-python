**treepath** is a [query language](https://en.wikipedia.org/wiki/Query_language) for selecting
[nodes](https://en.wikipedia.org/wiki/Node_(computer_science)) from a
[json](https://docs.python.org/3/library/json.html) data-structure. The query expressions are similar to
[jsonpath](https://goessner.net/articles/JsonPath/) and
[Xpath](https://en.wikipedia.org/wiki/XPath), but are written in python syntax.

### Solar System Sample Data

Sample data used by the examples in this README.
<details><summary>solar_system = {  ... }</summary>
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

## Typical example.

When working with json data-structures, there is a need to fetch specific pieces of data in the tree. A common approach
to this problem is to write structural code. This approach can become quite complex depending on the json structure and
search criteria.

A more declarative approach is to use a query language.   It does a better job at communicating the intent of what is
being searched for.

Here are two examples that fetched the planet Earth from the sample solar-system data.

<table>
<tr>
<th>Structured Python Syntax</th>
<th>declarative Python Syntax Using treepath</th>
</tr>
<tr>
<td>

```python
def get_planet(name, the_solar_system):
    try:
        inner = the_solar_system['star']['planets']['inner']
        for planet in inner:
            if name == planet.get('name', None):
                return planet
    except KeyError:
        pass
    raise Exception(f"The planet {name} not found")


earth = get_planet('Earth', solar_system)
```

</td>
<td>

```python
earth = get(path.star.planets.inner[wc][has(path.name == 'Earth')], solar_system)










```

</td>
</tr>
</table>

Both examples will return the following results; however, the declarative approach uses only one line of code to
construct the same search algorithm.

```python
{'name': 'Earth', 'Equatorial diameter': 1.0, 'has-moons': True}
```

## query example.

| Description                                 | Xpath                               | jsonpath                                  | treepath                            |
|----------------------------------------------|-------------------------------------|-------------------------------------------|------------------------------------|
| Find planet earth.                           | /star/planets/inner[name='Earth']   | $.star.planets.inner[?(@.name=='Earth')]  | path.star.planets.inner[wc][has(path.name == 'Earth')]   |
| List the names of the inner planets.         | /star/planets/inner[*].name         | $.star.planets.inner[*].name              | path.star.planets.inner[wc].name   |
| List the names of all planets.               | /star/planets/*/name                | $.star.planets.[*].name                   | path.star.planets.wc[wc].name      |
| List the names of all the celestial bodies.  | //name                              | $..name                                   | path.rec.name                      |  
| List all nodes in the tree Preorder          | //*                                 | $..                                       | path.rec                           |
| Get the third rock from the sun              | /star/planets/inner[3]              | $.star.planets.inner[2]                   | path.star.planets.inner[2]         |
| List first two inner planets                 | /star/plnaets.inner[position()<3]   | $.star.planets.inner[:2]                  | path.star.planets.inner[0:2]       |
|                                              |                                     | $.star.planets.inner[0, 1]                | path.star.planets.inner[0, 2]      |
| List planets smaller than earth              | /star/planets/inner[Equatorial_diameter < 1]   | $.star.planets.inner[?(@.['Equatorial diameter'] < 1)]              | path.star.planets.inner[wc][has(path["Equatorial diameter"] < 1)]       |
| List celestial bodies that have planets.     | //*[planets]/name                   | $..*[?(@.planets)].name                   | path.rec[has(path.planets)].name       |

# Search Function

## get

Get the star name from the solar_system.
```python
sun = get(path.star.name, solar_system)
assert sun == 'Sun'
```

When there is no match,  a MatchNotFoundError is thrown
```python
try:
    get(path.star.human_population, solar_system)
    assert False, "Not expecting humans on the sun"
except MatchNotFoundError:
    pass
```

Return a default value when match is not found.
```python
human_population = get(path.star.human_population, solar_system, default=0)
assert human_population == 0
```

## find

Find all the inner planet names. 
Each match is found just in time.
```python
inner_planets = [planet for planet in find(path.star.planets.inner[wc].name, solar_system)]
assert len(inner_planets) == 4
```

## get_match

Get the star age.
The get_match function returns a match object, where get function returns the value
The match object tells us the age attribute exist when its value is null.
```python
match = get_match(path.star.age, solar_system)
assert match is not None
assert match.data is None
```

When there is no match, the  MatchNotFoundError is thrown.
```python
try:
    get_match(path.star.human_population, solar_system)
    assert False, "Not expecting humans on the sun"
except MatchNotFoundError:
    pass
```

Return a None when match is not found.
```python
match = get_match(path.star.human_population, solar_system, must_match=False)
assert match is None
```

## find_matches

The find_matches function returns an Iterator of all matches.
The match object remembers its index.  
```python
for match in find_matches(path.star.planets.inner[wc], solar_system):
    assert match.data == solar_system["star"]["planets"]["inner"][match.data_name]
```

## nested_get_match

The nested_get_match function allows the next match to start the search relative from another match.
```python
parent_match = get_match(path.star.planets.inner, solar_system)
earth_match = nested_get_match(path[2].name, parent_match)
assert earth_match.path == "$.star.planets.inner[2].name"
assert earth_match.data == "Earth"
```

When there is no match, MatchNotFoundError is thrown.
```python
try:
    nested_get_match(path[5].name, parent_match)
    assert False, "Not expecting humans on the sun"
except MatchNotFoundError:
    pass
```

Return a None when match is not found.
```python
match = nested_get_match(path[5].name, parent_match, must_match=False)
assert match is None
```

## nested_find_matches

The find_matches function returns an Iterator of all matches.
```python
for planet_match in find_matches(path.star.planets.inner[wc], solar_system):
    name_match = nested_get_match(path.name, planet_match)
    assert name_match.data == solar_system["star"]["planets"]["inner"][name_match.parent.data_name]["name"]
```

## match_class
The match object has metadata about the match.  
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

The string representation of the path the match represents.
```python
assert match.path == "$.star.name"
```

Key that points to the match value.  Key can be index if the parent is a list
```python
assert match.data_name == "name" and match.parent.data[match.data_name] == match.data
```

The value the match's path maps to.
```python
assert match.data == "Sun"
```

The parent of the match.
```python
assert match.parent.path == "$.star"
```

# path

## root

The path word point to root of the tree.
```python
match = get_match(path, solar_system)

assert match.data == solar_system
```

In a filter path point to the current element.
```python
match = get_match(path.star.name[has(path == 'Sun')], solar_system)

assert match.data == 'Sun'
```

## key

The path uses dynamic attributes so dict keys do not need to double quotes.
```python
inner_from_attribute = get(path.star.planets.inner, solar_system)
inner_from_string_keys = get(path["star"]["planets"]["inner"], solar_system)

assert inner_from_attribute == inner_from_string_keys == solar_system["star"]["planets"]["inner"]
```

## keys with special characters

The dict keys that are not valid python syntax can be referenced as strings.
```python
sun_equatorial_diameter = get(path.star.planets.inner[0]["Number of Moons"], solar_system)

assert sun_equatorial_diameter == solar_system["star"]["planets"]["inner"][0]["Number of Moons"]
```

If the json has lots of attributes with dashes, pathd can be used to interpret all underscore as dashes.
```python
mercury_has_moons = get(pathd.star.planets.inner[0].has_moons, solar_system)

assert mercury_has_moons == solar_system["star"]["planets"]["inner"][0]["has-moons"]
```

## wildcard keys

The wildcard word is useful for iterating over attributes
```python
star_children = [child for child in find(path.star.wildcard, solar_system)]
assert star_children == [solar_system["star"]["name"],
                         solar_system["star"]["diameter"],
                         solar_system["star"]["age"],
                         solar_system["star"]["planets"], ]
```

The wc word is the short version.  
```python
star_children = [child for child in find(path.star.wc, solar_system)]
assert star_children == [solar_system["star"]["name"],
                         solar_system["star"]["diameter"],
                         solar_system["star"]["age"],
                         solar_system["star"]["planets"], ]
```


## key comma delimited

The dict key can be access using comma delimited list.
```python
last_and_first = [planet for planet in find(path.star["diameter", "name"], solar_system)]
assert last_and_first == [1391016, "Sun"]
```

## list

The list can be access using index.
```python
earth = get(path.star.planets.inner[2], solar_system)
assert earth == solar_system["star"]["planets"]["inner"][2]
```

## list slice

The list can be access using slices.  This example finds the first to planets.
```python
first_two = [planet for planet in find(path.star.planets.outer[:2].name, solar_system)]
assert first_two == ["Jupiter", "Saturn"]
```

Finds the last two planets.
```python
last_two = [planet for planet in find(path.star.planets.outer[-2:].name, solar_system)]
assert last_two == ["Uranus", "Neptune"]
```

Finds all outer planets in reverse.
```python
last_two = [planet for planet in find(path.star.planets.outer[::-1].name, solar_system)]
assert last_two == ["Neptune", "Uranus", "Saturn", "Jupiter"]
```

Find the last inner planet, and the last outer planet.  
The inner and outer list are still treated as separate list. 
The wildcard is used to search both of these list.  
```python
last_two = [planet for planet in find(path.star.wc.wc[-1:].name, solar_system)]
assert last_two == ["Mars", "Neptune"]
```

## list comma delimited

The list can be access using comma delimited list.  This example finds the fourth and first planet.
```python
last_and_first = [planet for planet in find(path.star.planets.outer[3, 0].name, solar_system)]
assert last_and_first == ["Neptune", "Jupiter"]
```


## list wildcard

The wildcard word can be used as a list index.
```python
all_outer = [planet for planet in find(path.star.planets.outer[wildcard].name, solar_system)]
assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]
```

The wc word for short version.
```python
all_outer = [planet for planet in find(path.star.planets.outer[wc].name, solar_system)]
assert all_outer == ["Jupiter", "Saturn", "Uranus", "Neptune"]
```

The dict wildcard and list wildcard can be combined. 
```python
all_planets = [p for p in find(path.star.planets.wc[wc].name, solar_system)]
assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
```

## recursion

The recursive word applies the query to every vertex in the subtree.  This is an example the finds all the planets names.
```python
all_planets = [p for p in find(path.star.planets.recursive.name, solar_system)]
assert all_planets == ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
```

The rec word for short version.
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

## filter has

Filters can be used add additional search criteria.  This search finds all celestial bodies that have planets
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

This search finds all celestial bodies that have moons. 
```python
all_celestial_bodies_moon_attribute = [planet for planet in
                                       find(path.rec[has(pathd.has_moons == True)].name, solar_system)]
assert all_celestial_bodies_moon_attribute == ['Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
```

## filter comparison operators

Filters can be specified with comparison operator.  
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

## filter comparison operators with type conversion

Sometimes the value is the wrong type for the comparison operator. In this example the attribute "Number of Moons" is 
str type. 
```python
planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > "5")].name, solar_system)]
assert planets == ['Jupiter', 'Saturn']
```

This is how to convert the type to an int before applying the comparison operator.  
```python
planets = [planet for planet in find(path.rec[has(path["Number of Moons"] > 5, int)].name, solar_system)]
assert planets == ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
```

## filer regular expression
Regular Expression can be used as a way to match values. This example finds the planets that end with s.  
```python
pattern = re.compile(r"\w+s")
earth = [planet for planet in find(path.rec[has(path.name, pattern.match)].name, solar_system)]
assert earth == ['Venus', 'Mars', 'Uranus']
```

## filter as a function

A filter is just a single argument function that returns anything.  Here is another way to do a comparison operator.
```python
def smaller_than_earth(value):
    return value < 12756


earth = [planet for planet in find(path.rec[has(path.diameter, smaller_than_earth)].name, solar_system)]
assert earth == ['Mercury', 'Venus', 'Mars']

```

## predicate as a filter

A predicate is a single argument function that returns anything. The  argument is the current match.   The has 
function is a fancy predicate.  

This example writes a custom predicate that find earths neighbours.  
```python
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
```

