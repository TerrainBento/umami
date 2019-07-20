import numpy as np


def _aggregate(vals, method, **kwds):
    # inspect numpy namespace:
    function = np.__dict__[method]

    # calc value
    out = function(vals, **kwds)
    if np.isscalar(out):
        return out
    else:
        msg = ""
        raise ValueError("")


def aggregate(grid, field, method, **kwds):
    """Calculate an aggreggate value on a landlab grid field.

    ``aggregate`` calculates aggregate values on the core nodes of the model
    grid. It supports all methods in the numpy namespace that reduce an array
    to a scalar.

    Parameters
    ----------
    grid
    field : str
        An at-node landlab grid field that is present on the model grid.
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
    First an example that only uses the ``aggregate`` function.

    >>> from landlab import RasterModelGrid
    >>> from umami.calculations import aggregate
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node

    ``aggregate`` supports all functions in the ``numpy`` namespace. Here we
    show ``mean`` and ``percentile``. The latter of which takes an additional
    argument, *q*.

    >>> aggregate(grid, "topographic__elevation", "mean")
    9.0
    >>> aggregate(grid, "topographic__elevation", "percentile", q=10)
    5.0

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> file_like=StringIO('''
    ... me:
    ...     _func: aggregate
    ...     method: mean
    ...     field: topographic__elevation
    ... ep10:
    ...     _func: aggregate
    ...     method: percentile
    ...     field: topographic__elevation
    ...     q: 10
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_metrics_from_file(file_like)
    >>> metric.names
    odict_keys(['me', 'ep10'])
    >>> metric.calculate_metrics()
    >>> metric.values
    [9.0, 5.0]
    """
    vals = grid.at_node[field][grid.core_nodes]
    return _aggregate(vals, method, **kwds)