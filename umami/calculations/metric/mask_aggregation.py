import numpy as np

from .aggregate import _aggregate


def mask_aggregation(grid, field, mask, method, **kwds):
    """Aggregate a field value masked by a boolean field.

    ``mask_aggregation`` calculates aggregate values on a field masked by a
    second, boolean field. It supports all methods in the `numpy`_ namespace
    that reduce an array to a scalar.

    .. _numpy: https://numpy.org

    Parameters
    ----------
    grid : Landlab model grid
    field : str
        An at-node Landlab grid field that is present on the model grid.
    mask : str
        An at-node Landlab grid field of boolean type. Aggregation is done
        where the masked value is True.
    method : str
        The name of a numpy namespace method.
    **kwds
        Any additional keyword arguments needed by the method.

    Returns
    -------
    out : float
        The aggregate value.

    Examples
    --------
    First an example that only uses the ``mask_aggregation`` function.

    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import mask_aggregation
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node

    Create a boolean mask and add it to the grid.

    >>> mask = grid.add_field("mask", z > 11, at="node")

    ``mask_aggregation`` supports all functions in the `numpy`_ namespace.
    Here we show `mean`_ and `percentile`_. The latter of which takes an
    additional argument, *q*.

    .. _numpy: https://numpy.org
    .. _mean: https://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    .. _percentile: https://docs.scipy.org/doc/numpy/reference/generated/numpy.percentile.html


    >>> mask_aggregation(grid, "topographic__elevation", "mask",  "mean")
    14.0
    >>> mask_aggregation(
    ... grid,
    ... "topographic__elevation",
    ... "mask",
    ... "percentile",
    ... q=10)
    12.0

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> file_like=StringIO('''
    ... mask_mean:
    ...     _func: mask_aggregation
    ...     mask: mask
    ...     method: mean
    ...     field: topographic__elevation
    ... mask_10thptile:
    ...     _func: mask_aggregation
    ...     mask: mask
    ...     method: percentile
    ...     field: topographic__elevation
    ...     q: 10
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_from_file(file_like)
    >>> metric.names
    ['mask_mean', 'mask_10thptile']
    >>> metric.calculate()
    >>> metric.values
    [14.0, 12.0]
    """
    masked = grid.at_node[mask]
    vals = grid.at_node[field][masked]
    return _aggregate(vals, method, **kwds)
