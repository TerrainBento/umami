import numpy as np


def _aggregate(vals, method, **kwds):
    # inspect numpy namespace:
    function = np.__dict__[method]

    # calc value
    try:
        out = function(vals, **kwds)
        assert isinstance(out, scalar)
    except:
        raise ValueError()
    return out


def aggregate(grid, field, method, **kwds):
    vals = grid.at_node[field][grid.core_nodes]

    return _aggregate(vals, method, **kwds)
