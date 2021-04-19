"""
# The **treepath** Package

**treepath** uses [declarative programming](https://en.wikipedia.org/wiki/Declarative_programming) approach for
extracting data from a [json](https://docs.python.org/3/library/json.html) data structure.  The expressions are a
[query language](https://en.wikipedia.org/wiki/Query_language) similar to
[jsonpath](https://goessner.net/articles/JsonPath/), and [Xpath](https://en.wikipedia.org/wiki/XPath), but are
written in native python syntax.

# Quick start

```python
    from treepath import path, get
    data = {
        "a": {
            "b": {
                "c": 1
            }
        }
    }
    value = get(path.a.b.c, data)
    assert value == 1
```
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

path = RootPathBuilder()
pathd = DashPathRoot()
