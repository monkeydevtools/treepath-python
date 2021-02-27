from tests.utils.traverser_utils import gen_test_data, naia, yaia
from treepath import path, find, wc, get, has


def test_get_earth(solar_system):
    def get_planet(name, solar_system):
        star = solar_system.get('star', {})
        planets = star.get('planets', [])
        inner = planets.get('inner', [])
        for planet in inner:
            if name == planet.get('name', None):
                return planet
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


def test_list_names_of_all_planets_rec(solar_system):
    expected = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    actual = [p for p in find(path.star.planets.rec.name, solar_system)]
    assert actual == expected


def test_names_of_all_the_celestial_bodies(solar_system):
    expected = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    actual = [p for p in find(path.rec.name, solar_system)]
    assert actual == expected
