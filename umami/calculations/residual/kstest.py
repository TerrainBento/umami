import numpy as np
from landlab.utils import get_watershed_mask
from scipy.stats import ks_2samp


def kstest(model_grid, data_grid, field):
    """Calculate an Kolmogorov-Smirnov test for a Landlab grid field.

    ``kstest`` calculates the Kolmogorov-Smirnov test for goodness of fit
    using the function ``ks_2samp`` from ``scipy.stats``.

    Parameters
    ----------
    model_grid : Landlab model grid
    data_grid : Landlab model grid
    field : str
        An at-node Landlab grid field that is present on both grids.

    Returns
    -------
    out : float
        The KS test statistic

    Examples
    --------
    First an example that only uses the ``kstest`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from umami.calculations import kstest
    >>> np.random.seed(42)
    >>> model = RasterModelGrid((10, 10))
    >>> z_model = model.add_zeros("node", "topographic__elevation")
    >>> z_model += model.x_of_node + model.y_of_node
    >>> data = RasterModelGrid((10, 10))
    >>> z_data = data.add_zeros("node", "topographic__elevation")
    >>> z_data +=  data.x_of_node + data.y_of_node
    >>> z_data[data.core_nodes] += np.random.random(data.core_nodes.shape)
    >>> np.round(kstest(model, data, "topographic__elevation"), decimals=3)
    0.125

    Next, the same calculations are shown as part of an umami ``Residual``.

    >>> from io import StringIO
    >>> from umami import Residual
    >>> file_like=StringIO('''
    ... ks:
    ...     _func: kstest
    ...     field: topographic__elevation
    ... ''')
    >>> residual = Residual(model, data)
    >>> residual.add_from_file(file_like)
    >>> residual.names
    ['ks']
    >>> residual.calculate()
    >>> residual.values
    [0.125]
    """
    model_vals = model_grid.at_node[field][model_grid.core_nodes]
    data_vals = data_grid.at_node[field][data_grid.core_nodes]

    d, _ = ks_2samp(model_vals, data_vals)
    return d


def kstest_watershed(model_grid, data_grid, field, outlet_id):
    """Calculate an Kolmogorov-Smirnov test for a watershed.

    ``kstest_watershed`` calculates the Kolmogorov-Smirnov test for
    goodness of fit using the function ``ks_2samp`` from ``scipy.stats``.

    Given an *outlet_id* it identifes a watershed mask for the *data_grid*. It
    then uses that mask on both the *data_grid* and the *model_grid*.

    If the field is "flow__distance", then this performs a KS test of the width
    function.

    Parameters
    ----------
    model_grid : Landlab model grid
    data_grid : Landlab model grid
    field : str
        An at-node Landlab grid field that is present on both grids.
    outlet_id : int

    Returns
    -------
    out : float
        The KS test statistic

    Examples
    --------
    First an example that only uses the ``kstest`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import kstest_watershed
    >>> np.random.seed(42)
    >>> model = RasterModelGrid((10, 10))
    >>> z_model = model.add_zeros("node", "topographic__elevation")
    >>> z_model += model.x_of_node + model.y_of_node
    >>> data = RasterModelGrid((10, 10))
    >>> z_data = data.add_zeros("node", "topographic__elevation")
    >>> z_data +=  data.x_of_node + data.y_of_node
    >>> z_data[data.core_nodes] += np.random.random(data.core_nodes.shape)
    >>> data_fa = FlowAccumulator(data)
    >>> data_fa.run_one_step()
    >>> model_fa = FlowAccumulator(model)
    >>> model_fa.run_one_step()
    >>> np.round(
    ...     kstest_watershed(
    ...         model,
    ...         data,
    ...         "topographic__elevation",
    ...         outlet_id=1),
    ...     decimals=3)
    0.5

    Next, the same calculations are shown as part of an umami ``Residual``.

    >>> from io import StringIO
    >>> from umami import Residual
    >>> file_like=StringIO('''
    ... ksw:
    ...     _func: kstest_watershed
    ...     outlet_id: 1
    ...     field: topographic__elevation
    ... ''')
    >>> residual = Residual(model, data)
    >>> residual.add_from_file(file_like)
    >>> residual.names
    ['ksw']
    >>> residual.calculate()
    >>> np.round(residual.values, decimals=3)
    array([ 0.5])
    """
    mask = get_watershed_mask(data_grid, outlet_id)
    model_vals = model_grid.at_node[field][mask]
    data_vals = data_grid.at_node[field][mask]

    d, _ = ks_2samp(model_vals, data_vals)
    return d
