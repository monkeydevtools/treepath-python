import pkgutil

from tests.utils.json_utils import json_to_dict, json_to_list


def get_dash_json() -> str:
    data = pkgutil.get_data(__name__, "dash.json")
    data = data.decode()
    return data


def get_dash() -> dict:
    data = get_dash_json()
    data_dict = json_to_dict(data)
    return data_dict

def get_keys_json() -> str:
    data = pkgutil.get_data(__name__, "keys.json")
    data = data.decode()
    return data


def get_keys() -> dict:
    data = get_keys_json()
    data_dict = json_to_dict(data)
    return data_dict



def get_three_dimensional_list_json() -> str:
    data = pkgutil.get_data(__name__, "three_dimensional_list.json")
    data = data.decode()
    return data


def get_three_dimensional_list() -> list:
    data = get_three_dimensional_list_json()
    data_list = json_to_list(data)
    return data_list


def get_a_k_k_a_k_k_k_a_json() -> str:
    data = pkgutil.get_data(__name__, "a_k_k_a_k_k_k_a.json")
    data = data.decode()
    return data


def get_a_k_k_a_k_k_k_a() -> list:
    data = get_a_k_k_a_k_k_k_a_json()
    data_dict = json_to_list(data)
    return data_dict


def get_k_a_a_k_a_a_a_k_json() -> str:
    data = pkgutil.get_data(__name__, "k_a_a_k_a_a_a_k.json")
    data = data.decode()
    return data


def get_k_a_a_k_a_a_a_k() -> dict:
    data = get_k_a_a_k_a_a_a_k_json()
    data_list = json_to_dict(data)
    return data_list


def get_all_data_types_json() -> str:
    data = pkgutil.get_data(__name__, "all_data_types.json")
    data = data.decode()
    return data


def get_all_data_types() -> dict:
    data = get_all_data_types_json()
    data_list = json_to_dict(data)
    return data_list


