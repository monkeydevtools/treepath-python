from tests.utils.traverser_utils import gen_test_data, naia, yaia
from treepath import path, find, wc


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
