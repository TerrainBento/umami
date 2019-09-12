import numpy as np


def joint_density_misfit(
    model_grid,
    data_grid,
    field_1,
    field_2,
    field_1_percentile_edges,
    field_2_percentile_edges,
):
    """Calculate the joint-density misfit on a Landlab grid field.

    Density bounds are calculated with the data grid.

    Parameters
    ----------
    model_grid : Landlab model grid
    data_grid : Landlab model grid
    field_1 : str
        An at-node Landlab grid field that is present on the model grid.
    field_2 : str
        An at-node Landlab grid field that is present on the model grid.
    field_1_percentile_edges : list
        A list of percentile edges applied to ``field_1``. For example,
        ``[0, 60, 100]`` specifies splitting ``field_1`` into two parts,
        separated at the 60th percentile.
    field_2_percentile_edges : list
        A list of percentile edges applied to ``field_2``. For example,
        ``[0, 60, 100]`` specifies splitting ``field_2`` into two parts,
        separated at the 60th percentile.

    Returns
    -------
    out : float
        The misfit

    Examples
    --------
    First an example that only uses the ``joint_density_misfit`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import joint_density_misfit
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
    >>> np.isclose(
    ...     joint_density_misfit(
    ...         model,
    ...         data,
    ...         "topographic__elevation",
    ...         "drainage_area",
    ...         [0, 25, 50, 75, 100],
    ...         [0, 20, 40, 60, 80, 100]),
    ...         0.056599, atol=1e-03)
    True

    Next, the same calculations are shown as part of an umami ``Residual``.

    >>> from io import StringIO
    >>> from umami import Residual
    >>> file_like=StringIO('''
    ... jdm:
    ...     _func: joint_density_misfit
    ...     field_1: topographic__elevation
    ...     field_2: drainage_area
    ...     field_1_percentile_edges:
    ...         - 0
    ...         - 25
    ...         - 50
    ...         - 75
    ...         - 100
    ...     field_2_percentile_edges:
    ...         - 0
    ...         - 20
    ...         - 40
    ...         - 60
    ...         - 80
    ...         - 100
    ... ''')
    >>> residual = Residual(model, data)
    >>> residual.add_from_file(file_like)
    >>> residual.names
    ['jdm']
    >>> residual.calculate()
    >>> np.round(residual.values, decimals=3)
    array([ 0.057])
    """

    f1_data = data_grid.at_node[field_1][data_grid.core_nodes]
    f2_data = data_grid.at_node[field_2][data_grid.core_nodes]

    f1_model = model_grid.at_node[field_1][model_grid.core_nodes]
    f2_model = model_grid.at_node[field_2][model_grid.core_nodes]

    # calc the percentiles of each_distribution.
    f1_edges = np.percentile(f1_data, field_1_percentile_edges)
    f2_edges = np.percentile(f2_data, field_2_percentile_edges)

    # calculate the densities for model and data
    data_count, _, _ = np.histogram2d(
        f1_data, f2_data, bins=(f1_edges, f2_edges), density=False
    )

    model_count, _, _ = np.histogram2d(
        f1_model, f2_model, bins=(f1_edges, f2_edges), density=False
    )

    data_density = data_count / data_count.sum()

    if model_count.sum() == 0:
        model_density = model_count
    else:
        model_density = model_count / model_count.sum()

    sq_resid = np.power(model_density - data_density, 2.0)
    misfit = np.sqrt(np.mean(sq_resid))

    return misfit
