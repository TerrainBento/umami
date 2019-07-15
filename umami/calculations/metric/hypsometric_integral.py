import numpy as np


def hypsometric_integral(grid):
    """
    """
    # Get just those elevation values that are within the watershed
    vals = grid.at_node[field][grid.core_nodes]

    # Get min and max
    min_val = np.amin(vals)
    max_val = np.amax(vals)

    # Calc and return hyps int
    return np.mean(wshed_val - min_val) / (max_val - min_val)
