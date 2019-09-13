import numpy as np
from landlab.utils import get_watershed_mask


def hypsometric_integral(grid, outlet_id):
    """Calculate the hypsometric integral for the model grid.

    The hypsometric integral :math:`I` is defined as

    .. math::

        I = \\frac{\\frac{1}{N} \\sum_{i=0}^{N}
        \\left( z - \\min \\left( z\\right) \\right)}
        {\\max \\left(z\\right) - \\min \\left( z \\right)}

    Where :math:`z` is the set of elevation values, and :math:`N` is the number
    of elevation values.

    Parameters
    ----------
    grid : Landlab model grid
    outlet_id : int
        Outlet id of the watershed.

    Returns
    -------
    I : float
        The hypsometric integral.

    Examples
    --------
    First an example that only uses the ``hypsometric_integral`` function.

    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import hypsometric_integral
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node
    >>> fa = FlowAccumulator(grid)
    >>> fa.run_one_step()
    >>> hypsometric_integral(grid, 1)
    0.5

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> file_like=StringIO('''
    ... hi:
    ...     _func: hypsometric_integral
    ...     outlet_id: 1
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_from_file(file_like)
    >>> metric.names
    ['hi']
    >>> metric.calculate()
    >>> metric.values
    [0.5]
    """
    # Get just those elevation values that are within the watershed
    mask = get_watershed_mask(grid, outlet_id)
    vals = grid.at_node["topographic__elevation"][mask]

    # Get min and max
    min_val = np.amin(vals)
    max_val = np.amax(vals)

    # Calc and return the hypsometric_integral
    return np.mean(vals - min_val) / (max_val - min_val)
