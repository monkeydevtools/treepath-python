**treepath** is a [query language](https://en.wikipedia.org/wiki/Query_language) for selecting 
[nodes](https://en.wikipedia.org/wiki/Node_(computer_science)) from a 
[json](https://docs.python.org/3/library/json.html) data-structure. The query expressions are similar to 
[jsonpath](https://goessner.net/articles/JsonPath/) and  
[Xpath](https://en.wikipedia.org/wiki/XPath),  but are written in python syntax.  


### Solar System Sample Data
The sample data use by the examples in this README.  
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

When working with json data-structures, there is a need to fetch specific pieces of data deep in the tree.   A common 
approach to this problem is writing structural code.  This approach can become quite complex depending on the json 
structure and search criteria.   

A more declarative approach would be to use a query language which does a better job communicating the intent of what 
is being searched for.  

Here are two examples that fetched the planet Earth from the sample solar-system data defined above.   One is 
structural code, and the other is using a treepath query.  

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

Both examples will return the follwing results; however, the treepath example uses only one line of code to construct 
the same search algorithm.  

```python
{'name': 'Earth', 'Equatorial diameter': 1.0, 'has-moons': True}
```


## Summary example.  

 
| question                                     | Xpath                               | jsonpath                                  | treepath                           |
|----------------------------------------------|-------------------------------------|-------------------------------------------|------------------------------------|
| Find planet earth.                           | /star/planets/inner[name='Earth']   | $.star.planets.inner[?(@.name=='Earth')]  | path.star.planets.inner[wc][has(path.name == 'Earth')]   |
| List the names of the inner planets.         | /star/planets/inner[*].name         | $.star.planets.inner[*].name              | path.star.planets.inner[wc].name   |
| List the names of all planets.               | /star/planets/*/name                | $.star.planets.[*].name                   | path.star.planets.wc[wc].name      |
| List the names of all the celestial bodies.  | //name                              | $..name                                   | path.rec.name                      |  