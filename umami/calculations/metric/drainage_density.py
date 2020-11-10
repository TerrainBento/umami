"""
"""
from landlab.components import DrainageDensity


def _validate_drainage_density(drainage_density):
    if not isinstance(drainage_density, DrainageDensity):
        msg = "umami: A valid instance of a DrainageDensity is required."
        raise ValueError(msg)


def drainage_density(drainage_density):
    r"""Return the drainage density.

    This is a loose wrapper around the Landlab function
    `DrainageDensity.calculate_drainage_density`_.

    .. _DrainageDensity.calculate_drainage_density:

    Parameters
    ----------
    drainage_density : an instance of a `DrainageDensity`_


    .. _DrainageDensity:


    Returns
    -------
    out : float
        The drainage density.

    Examples
    --------
    First an example that only uses the ``calculate_drainage_density`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator, DrainageDensity
    >>> from umami.calculations import drainage_density
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node**2 + grid.y_of_node**2
    >>> fa = FlowAccumulator(grid)
    >>> fa.run_one_step()

    The Landlab ``DrainageDensity`` component can be initialized with either
    an area exponent and coefficient, a slope exponent and coefficient, and a
    threshold, OR a mask. Umami can support either of these options.

    >>> dd = DrainageDensity(grid, )
    >>> drainage_density = dd.calculate_drainage_density()
    >>> np.round(drainage_density(dd), decimals=1)
    -4.0

    Next, the same calculations are shown as part of an umami ``Metric``.

    >>> from io import StringIO
    >>> from umami import Metric
    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node**2 + grid.y_of_node**2
    >>> file_like=StringIO('''
    ... dd:
    ...     _func: drainage_density
    ... ''')
    >>> metric = Metric(
    ...     grid,
    ...     drainage_density_kwds={"min_drainage_area": 1.0})
    >>> metric.add_from_file(file_like)
    >>> metric.names
    ['dd']
    >>> metric.calculate()
    >>> np.round(metric.values, decimals=0)
    array([-4.])
    """
    _validate_drainage_density(drainage_density)
    dd = drainage_density.calculate_drainage_density()
    return dd
