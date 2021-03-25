from treepath import path, get_match


def test_eq_identical_match(solar_system):
    match = get_match(path.star.name, solar_system)
    assert match == match


def test_eq_simular_match(solar_system):
    match1 = get_match(path.star.name, solar_system)
    match2 = get_match(path.star.name, solar_system)
    assert match1 == match2


def test_ne_match(solar_system):
    match1 = get_match(path.star.name, solar_system)
    match2 = get_match(path.star, solar_system)
    assert match1 != match2
