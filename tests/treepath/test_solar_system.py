from tests.utils.traverser_utils import gen_test_data, naia, yaia
from treepath import exp, find, wc


def test_names_of_planets_that_orbit_the_sun(solar_system):
    expected = [expected_value["name"] for expected_path, expected_value in
                gen_test_data(solar_system, naia, naia, yaia)]
    actual = [p for p in find(exp.star.planets[wc].name, solar_system)]
    assert actual == expected
