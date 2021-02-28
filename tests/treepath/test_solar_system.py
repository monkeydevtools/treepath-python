from tests.utils.traverser_utils import gen_test_data, yria, yaia
from treepath import path, find, wc, get, has


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
