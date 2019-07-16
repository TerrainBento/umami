import numpy as np


def count_equal(grid, field, value):
    """
    """
    vals = grid.at_node[field][grid.core_nodes]
    return np.sum(vals == value)
