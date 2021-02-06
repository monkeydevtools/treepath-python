import pytest

from tests.data.data import get_keys, get_three_dimensional_list, get_a_k_k_a_k_k_k_a, get_k_a_a_k_a_a_a_k, \
    get_all_data_types, get_dash


@pytest.fixture
def dash() -> dict:
    return get_dash()

@pytest.fixture
def keys() -> dict:
    return get_keys()


@pytest.fixture
def three_dimensional_list() -> list:
    return get_three_dimensional_list()


@pytest.fixture
def a_k_k_a_k_k_k_a() -> list:
    return get_a_k_k_a_k_k_k_a()


@pytest.fixture
def k_a_a_k_a_a_a_k() -> dict:
    return get_k_a_a_k_a_a_a_k()

@pytest.fixture
def all_data_types() -> dict:
    return get_all_data_types()
