from treepath.path.builder.symbol import Symbol

# wildcard path constants.  When included in the path, the traversal algorithm applies the path to each sibling
# tree node.  It stops each time a successful match occurs.   The [wildcard] defines iterator that will only iterate
# over a list, while path.wildcard defines an iterator that will only iterate over dictionary keys.
# Examples:   path.wildcard, path[wildcard] path.a.wildcard, path.a[wildcard], path.wildcard.b, path[wildcard].b
# path.a.wildcard.b, path.a[wildcard].b
wildcard = Symbol("wildcard")

# wc is short version of wildcard
# Examples:   path.wc, path[wc] path.a.wc, path.a[wc], path.wc.b, path[wc].b
# path.a.wc.b, path.a[wc].b
wc = wildcard

# generic wildcard path constants.  When included in the path, the traversal algorithm applies the path to each sibling
# tree node.  It stops each time a successful match occurs. The generic_wildcard is agnostic of collection type.  It
# It will iterate over either type.
# Examples:   path.generic_wildcard, path[generic_wildcard] path.a.generic_wildcard, path.a[generic_wildcard],
# path.generic_wildcard.b, path[generic_wildcard].b
# path.a.generic_wildcard.b, path.a[generic_wildcard].b
generic_wildcard = Symbol("generic_wildcard")

# gwc is short version of generic_wildcard
# Examples:   path.gwc, path[gwc] path.a.gwc, path.a[gwc], path.gwc.b, path[gwc].b
# path.a.gwc.b, path.a[gwc].b
gwc = generic_wildcard

# recursive path constants.  When included in the path, the traversal algorithm applies the path to each node in the
# in the tree in pre-order traversal.  It stops each time a successful match occurs.
# Examples:   path.recursive, path.a.recursive,  path.recursive.b, path.a.recursive.b
recursive = Symbol("recursive")

# rec is short version of recursive
# Examples:   path.recursive, path.a.recursive,  path.recursive.b, path.a.recursive.b
rec = recursive
