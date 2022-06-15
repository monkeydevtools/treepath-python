from treepath.path.traverser.match import Match
from treepath.path.builder.path_builder import PathBuilder
from treepath.path.builder.root_path_builder import RootPathBuilder


def match_to_path(match: Match) -> PathBuilder:
    """
    Converts a match to a Path
    """
    path_as_list = match.path_match_list
    path = RootPathBuilder()
    for match in path_as_list[1:]:
        data_name = match.data_name
        path = path[data_name]
    return path
