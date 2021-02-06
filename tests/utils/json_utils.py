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


def query(json_dict, json_path: str, must_be_found=True):
    """
    Utility method for querying json dict using JSONPATH.
    The JSONPATH must be structure to only find a single item.
    :param json_dict: - the dict to query
    :param json_path: - the JSONPATH query string
    :param must_be_found: boolean that specifies if a JSONPathQueryError is raised if the json_path does not map to a
    value in the specified json_dict
    :return: The value that the json_path maps too.
    :raises: JSONPathQueryError if there are either too many or no matches
    """
    pass


def query_generator(json_dict, json_path):
    """
    This method performs a tree traversal reporting each value the json_path maps too.
    It uses Python Generators to report each result.

    Example

    {
      "store":{
        "book":[
          {
            "category":"reference",
            "author":"Nigel Rees",
            "title":"Sayings of the Century",
            "price":8.95
          },
          {
            "category":"fiction",
            "author":"Evelyn Waugh",
            "title":"Sword of Honour",
            "price":12.99
          }
       ]
      }
    }

    for match in query_generator(json_dict, “"$.book.title"):
        print(“match = “, match)

    result:
      match = Sayings of the Century"
      match = Sword of Honour

    :param json_dict: - the dict to query
    :param json_path: - the JSONPATH query string
    :return:
    """
    pass
