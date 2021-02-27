########
# Copyright (C) 2018 Bell Canada.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
from json import JSONDecodeError


def json_to_obj(json_str: str):
    """
    Transforms the json string into tree made up of dictionaries and list.
    :param json_str: The json string to transform
    :return: the dict or list
    """
    return json.loads(json_str)


def obj_to_json(json_obj, sort_keys=True, indent=None) -> str:
    """
    Transforms a tree made up of dictionaries and list into json string.
    :param  json_dict: the dict to transform
    :return: the json string
    """
    return json.dumps(json_obj, sort_keys=sort_keys, indent=indent)


def json_to_dict(json_str: str) -> dict:
    """
    Transforms the json string into tree made up of dictionaries and list.
    :param json_str: The json string to transform
    :return: the dict
    """
    if not re.match(r'\s*{', json_str):
        raise JSONDecodeError(
            "Unexpected character.  For the root object to be a dict the json string must start with",
            json_str,
            0)
    return json.loads(json_str)


def dict_to_json(json_dict: dict, sort_keys=True, indent=None) -> str:
    """
    Transforms a tree made up of dictionaries and list into json string.
    :param  json_dict: the dict to transform
    :return: the json string
    """
    return json.dumps(json_dict, sort_keys=sort_keys, indent=indent)


def json_to_list(json_str: str) -> list:
    """
    Transforms the json string into tree made up of dictionaries and list.
    :param json_str: The json string to transform
    :return: the list
    """
    if not re.match(r'\s*\[', json_str):
        raise JSONDecodeError(
            "Unexpected character.  For the root object to be a list the json string must start with",
            json_str,
            0)
    return json.loads(json_str)


def list_to_json(json_list: list, sort_keys=True, indent=None) -> str:
    """
    Transforms a tree made up of dictionaries and list into json string.
    :param  json_list: the list to transform
    :return: the json string
    """
    return json.dumps(json_list, sort_keys=sort_keys, indent=indent)


