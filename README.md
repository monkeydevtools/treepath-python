**treepath** is a [query language](https://en.wikipedia.org/wiki/Query_language) for selecting 
[nodes](https://en.wikipedia.org/wiki/Node_(computer_science)) from a 
[json](https://docs.python.org/3/library/json.html) data-structure. The query expressions are similar to 
[jsonpath](https://goessner.net/articles/JsonPath/) and 
[Xpath](https://en.wikipedia.org/wiki/XPath),  but are written in python syntax.  

https://jsonpath.herokuapp.com
http://xpather.com

### Solar System Sample Data
Sample data used by the examples in this README.  
<details><summary>solar_system = {  ... }</summary>
<p>

```json
{
  "star": {
    "name": "Sun",
    "Equatorial diameter": 109.168,
    "planets": {
      "inner": [
        {
          "name": "Mercury",
          "Equatorial diameter": 0.383,
          "has-moons": false
        },
        {
          "name": "Venus",
          "Equatorial diameter": 0.949,
          "has-moons": false
        },
        {
          "name": "Earth",
          "Equatorial diameter": 1.000,
          "has-moons": true
        },
        {
          "name": "Mars",
          "Equatorial diameter": 0.532,
          "has-moons": true
        }
      ],
      "outer": [
        {
          "name": "Jupiter",
          "Equatorial diameter": 11.209,
          "has-moons": true
        },
        {
          "name": "Saturn",
          "Equatorial diameter": 9.449,
          "has-moons": true
        },
        {
          "name": "Uranus",
          "Equatorial diameter": 4.007,
          "has-moons": true
        },
        {
          "name": "Neptune",
          "Equatorial diameter": 3.883,
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

When working with json data-structures, there is a need to fetch specific pieces of data in the tree.   A common 
approach to this problem is to write structural code.  This approach can become quite complex depending on the json 
structure and search criteria.   

A more declarative approach is to use a query language as it does a better job at communicating the intent of what 
is being searched for.  

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
### get
```python


```

### find
### get_match
### find_matches
### match result

# Expressions
## root
## keys
### wildcard
### special characters
## arrays
### index
### slice
### comma delimited
### wildcard
## recursion
## filters
### has
### Comparison Operators
### type conversion
### write a customer predicate


