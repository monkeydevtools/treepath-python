**treepath** is a [query language](https://en.wikipedia.org/wiki/Query_language) for selecting 
[nodes](https://en.wikipedia.org/wiki/Node_(computer_science)) from a [json]() tree data structure. The syntax for 
defining a query is similar to [jsonpath](https://goessner.net/articles/JsonPath/) or 
[Xpath](https://en.wikipedia.org/wiki/XPath) but written in pure python.


## Simple Example

Here is a simple json document that defines our solar system:   
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

To fetch the Earth from the document 

```python
solar_system = json.loads(...)

earth 
```


| Python       | JSON  |   
|--------------|-------|
|  dict        | object      |
|  list, tuple | array      | 
|    str|string|
|  int, float, int- & float-derived Enums            | number      |
|  True| true|
|  False|false
|  None | null|