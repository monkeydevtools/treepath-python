from treepath.path.builder.dash_path_builder import DashPathRoot
from treepath.path.builder.patch_constants import recursive as _recursive
from treepath.path.builder.patch_constants import wildcard as _wildcard
from treepath.path.builder.root_path_builder import RootPathBuilder
from treepath.path.traverser.traverser_functions import find as _find
from treepath.path.traverser.traverser_functions import find_matches as _find_matches
from treepath.path.traverser.traverser_functions import get as _get
from treepath.path.traverser.traverser_functions import get_match as _get_match
from treepath.path.traverser.traverser_functions import has as _has

path = RootPathBuilder()
expd = DashPathRoot()

wildcard = _wildcard
wc = wildcard
recursive = _recursive
rec = recursive

get = _get
find = _find
get_match = _get_match
find_matches = _find_matches
has = _has
