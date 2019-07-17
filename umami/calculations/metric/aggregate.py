import numpy as np

def _aggregate(vals, method, **kwds):
    # inspect numpy namespace:
    function = np.__dict__[method]

    # calc value
    out = function(vals, **kwds)
    if np.isscalar(out):
        return out
    else:
        raise ValueError()


def aggregate(grid, field, method, **kwds):
    vals = grid.at_node[field][grid.core_nodes]

    return _aggregate(vals, method, **kwds)
