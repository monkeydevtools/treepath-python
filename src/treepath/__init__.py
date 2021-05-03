"""
See README.md  for details
"""
from treepath.path.builder.dash_path_builder import DashPathRoot
from treepath.path.builder.patch_constants import rec
from treepath.path.builder.patch_constants import recursive
from treepath.path.builder.patch_constants import wc
from treepath.path.builder.patch_constants import wildcard
from treepath.path.builder.root_path_builder import RootPathBuilder
from treepath.path.exceptions.infinite_loop_detected import InfiniteLoopDetected
from treepath.path.exceptions.match_not_found_error import MatchNotFoundError
from treepath.path.exceptions.nested_match_not_found_error import NestedMatchNotFoundError
from treepath.path.exceptions.path_syntax_error import PathSyntaxError
from treepath.path.exceptions.stop_traversing import StopTraversing
from treepath.path.exceptions.traversing_error import TraversingError
from treepath.path.exceptions.treepath_exception import TreepathException
from treepath.path.traverser.match import Match
from treepath.path.traverser.trace import Trace
from treepath.path.traverser.trace import log_to
from treepath.path.traverser.traverser_functions import find
from treepath.path.traverser.traverser_functions import find_matches
from treepath.path.traverser.traverser_functions import get
from treepath.path.traverser.traverser_functions import get_match
from treepath.path.traverser.traverser_functions import has
from treepath.path.traverser.traverser_functions import has_all
from treepath.path.traverser.traverser_functions import has_any
from treepath.path.traverser.traverser_functions import has_not
from treepath.path.traverser.traverser_functions import nested_find_matches
from treepath.path.traverser.traverser_functions import nested_get_match

# path is a global object for dynamically declaring a query to extract data from a json data structure.
#     # A treepath example that fetches the value 1 from data.
#     data = {
#         "a": {
#             "b": [
#                 {
#                     "c": 1
#                 },
#                 {
#                     "c": 2
#                 }]
#         }
#     }
#     value = get(path.a.b[0].c, data)
#     assert value == 1
#
#     # A treepath example that fetches the values 1 and 2 from data.
#     value = [value for value in find(path.a.b[wc].c, data)]
#     assert value == [1,2]
# See the README.md for example on how to use the path object.
path = RootPathBuilder()

# pathd is similar to path, but with the augmentation to translate underscores into dashes.  It provides a convenient
# way of working with json documents that has a lot of keys with dashes in the names as dashes are not valid python
# attribute names.  For example pathd.a_a  is equivalent to data["a-a"]
pathd = DashPathRoot()
