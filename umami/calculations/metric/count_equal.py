import numpy as np


def count_equal(grid, field, value):
    """Sum the number of array elements equal to a value.

    ``count_equal`` calculates number of values in the core nodes of the model
    grid that are equal to the input *value*.

    Parameters
    ----------
    grid : Landlab model grid
    field : str
        An at-node Landlab grid field that is present on the model grid.
    value : float
        The value to identify within the field.

    Returns
    -------
    out : float
        The number of elements in the field array equal to value.

    Examples
    --------
    First an example that only uses the ``count_equal`` function.

    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import count_equal
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node
    >>> fa = FlowAccumulator(grid)
    >>> fa.run_one_step()
    >>> count_equal(grid, "topographic__elevation", 4)
    3
    >>> count_equal(grid, "drainage_area", 1)
    8

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> file_like=StringIO('''
    ... elev4:
    ...     _func: count_equal
    ...     field: topographic__elevation
    ...     value: 4
    ... num_headwater_nodes:
    ...     _func: count_equal
    ...     field: drainage_area
    ...     value: 1
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_from_file(file_like)
    >>> metric.names
    ['elev4', 'num_headwater_nodes']
    >>> metric.calculate()
    >>> metric.values
    [3, 8]
    """
    vals = grid.at_node[field][grid.core_nodes]
    return np.sum(vals == value)
