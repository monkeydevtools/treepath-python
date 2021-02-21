from treepath.path.builder.dash_path_builder import DashRoot
from treepath.path.builder.patch_constants import recursive as _recursive
from treepath.path.builder.patch_constants import wildcard as _wildcard
from treepath.path.builder.root_path_builder import Root
from treepath.path.util.function import find as _find
from treepath.path.util.function import get as _get
from treepath.path.util.function import has as _has
from treepath.path.util.function import match as _match
from treepath.path.util.function import match as _match
from treepath.path.util.function import match_all as _match_all

exp = Root()
expd = DashRoot()

wildcard = _wildcard
wc = wildcard
recursive = _recursive
rec = recursive

get = _get
find = _find
match = _match
match_all = _match_all
has = _has
