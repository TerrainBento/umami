import numpy as np

from landlab.utils import get_watershed_mask

from .aggregate import _aggregate


def watershed_aggregation(grid, field, outlet_id, method, **kwds):
    """
    """
    mask = get_watershed_mask(grid, outlet_id)
    vals = grid.at_node[field][mask]
    return _aggregate(vals, method, **kwds)
