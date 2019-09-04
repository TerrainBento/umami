import numpy as np
from landlab.utils import get_watershed_mask

from .aggregate import _aggregate


def watershed_aggregation(grid, field, outlet_id, method, **kwds):
    """Aggregate a field value over a watershed.

    ``watershed_aggregation`` calculates aggregate values on the nodes in a
    watershed that drain to *outlet_id*. It supports all methods in the
    `numpy`_ namespace that reduce an array to a scalar.

    .. _numpy: https://numpy.org

    Parameters
    ----------
    grid : Landlab model grid
    field : str
        An at-node Landlab grid field that is present on the model grid.
    outlet_id : int
        Outlet id of the watershed.
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
    First an example that only uses the ``watershed_aggregation`` function.

    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import watershed_aggregation
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node
    >>> fa = FlowAccumulator(grid)
    >>> fa.run_one_step()

    ``watershed_aggregation`` supports all functions in the `numpy`_ namespace.
    Here we show `mean`_ and `percentile`_. The latter of which takes an
    additional argument, *q*.

    .. _numpy: https://numpy.org
    .. _mean: https://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    .. _percentile: https://docs.scipy.org/doc/numpy/reference/generated/numpy.percentile.html


    >>> watershed_aggregation(grid, "topographic__elevation", 1,  "mean")
    5.0
    >>> watershed_aggregation(
    ... grid,
    ... "topographic__elevation",
    ... 1,
    ... "percentile",
    ... q=10)
    1.8

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> file_like=StringIO('''
    ... oid1_mean:
    ...     _func: watershed_aggregation
    ...     outlet_id: 1
    ...     method: mean
    ...     field: topographic__elevation
    ... oid1_10thptile:
    ...     _func: watershed_aggregation
    ...     outlet_id: 1
    ...     method: percentile
    ...     field: topographic__elevation
    ...     q: 10
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_from_file(file_like)
    >>> metric.names
    ['oid1_mean', 'oid1_10thptile']
    >>> metric.calculate()
    >>> metric.values
    [5.0, 1.8]
    """
    mask = get_watershed_mask(grid, outlet_id)
    vals = grid.at_node[field][mask]
    return _aggregate(vals, method, **kwds)
