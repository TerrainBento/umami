from collections import OrderedDict

import numpy as np


def discretized_misfit(
    model_grid,
    data_grid,
    name,
    misfit_field,
    field_1,
    field_2,
    field_1_percentile_edges,
    field_2_percentile_edges,
):
    """Calculate a discretized misfit on a landlab grid field.

    density bounds calculated with the data grid.

    # TODO:
    ALSO FIX how these get named.


    Parameters
    ----------
    model_grid : Landlab model grid
    data_grid : Landlab model grid
    name
    misfit_field
    field_1
    field_2
    field_1_percentile_edges
    field_2_percentile_edges

    Returns
    -------
    OrderedDict

    Examples
    --------
    First an example that only uses the ``discretized_misfit`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import discretized_misfit
    >>> np.random.seed(42)
    >>> model = RasterModelGrid((50, 50))
    >>> z_model = model.add_zeros("node", "topographic__elevation")
    >>> z_model += model.x_of_node + model.y_of_node
    >>> data = RasterModelGrid((50, 50))
    >>> z_data = data.add_zeros("node", "topographic__elevation")
    >>> z_data +=  data.x_of_node + data.y_of_node
    >>> z_data[data.core_nodes] += np.random.random(data.core_nodes.shape)
    >>> data_fa = FlowAccumulator(data)
    >>> data_fa.run_one_step()
    >>> model_fa = FlowAccumulator(model)
    >>> model_fa.run_one_step()

    >>> cat, out = discretized_misfit(
    ...     model,
    ...     data,
    ...     "da_{field_1_level}_z_{field_2_level}",
    ...     "topographic__elevation",
    ...     "drainage_area",
    ...     "topographic__elevation",
    ...     [0, 50, 100],
    ...     [0, 30, 60, 100])
    >>> for key, value in out.items():
    ...     print(key, np.round(value, decimals=3))
    da_0_z_0 0.713
    da_0_z_1 0.711
    da_0_z_2 0.712
    da_1_z_0 0.414
    da_1_z_1 0.441
    da_1_z_2 0.432
    >>> cat[:5]
    array([0, 0, 0, 0, 0])

    Next, the same calculations are shown as part of an umami ``Residual``.

    >>> from io import StringIO
    >>> from umami import Residual
    >>> file_like=StringIO('''
    ... dm:
    ...     _func: discretized_misfit
    ...     name: da_{field_1_level}_z_{field_2_level}
    ...     misfit_field: topographic__elevation
    ...     field_1: drainage_area
    ...     field_2: topographic__elevation
    ...     field_1_percentile_edges:
    ...         - 0
    ...         - 50
    ...         - 100
    ...     field_2_percentile_edges:
    ...         - 0
    ...         - 30
    ...         - 60
    ...         - 100
    ... ''')
    >>> residual = Residual(model, data)
    >>> residual.add_from_file(file_like)
    >>> residual.names
    ['da_0_z_0', 'da_0_z_1', 'da_0_z_2', 'da_1_z_0', 'da_1_z_1', 'da_1_z_2']
    >>> residual.calculate()
    >>> for key, value in zip(residual.names, residual.values):
    ...     print(key, np.round(value, decimals=3))
    da_0_z_0 0.713
    da_0_z_1 0.711
    da_0_z_2 0.712
    da_1_z_0 0.414
    da_1_z_1 0.441
    da_1_z_2 0.432
    >>> residual.category[:5]
    array([0, 0, 0, 0, 0])
    """
    category = _get_category_labels(
        data_grid,
        field_1,
        field_2,
        field_1_percentile_edges,
        field_2_percentile_edges,
    )

    difference = (
        model_grid.at_node[misfit_field] - data_grid.at_node[misfit_field]
    )

    n_f1_levels = np.size(field_1_percentile_edges) - 1
    n_f2_levels = np.size(field_2_percentile_edges) - 1

    out = OrderedDict()
    for c in range(0, np.max(category)):
        f1l, f2l = np.unravel_index(c, (n_f1_levels, n_f2_levels))
        n = name.format(field_1_level=f1l, field_2_level=f2l)

        loc = category == (c + 1)
        sq_resids = np.power(difference[loc], 2.0)
        misfit = np.sqrt(np.mean(sq_resids))
        out[n] = misfit
    return category, out


def _get_category_labels(
    grid, field_1, field_2, field_1_percentile_edges, field_2_percentile_edges
):

    f1 = grid.at_node[field_1]
    f2 = grid.at_node[field_2]

    # first bin by field 1, then within field_1, bin by field_2
    is_core = np.zeros_like(f1, dtype=bool)
    is_core[grid.core_nodes] = True

    # calc the percentiles of the field 1 distribution
    f1_edges = np.percentile(f1[is_core], field_1_percentile_edges)

    # work through each bin and label them.
    category = np.zeros_like(f1, dtype=np.int)

    val = 1
    for i in range(len(f1_edges) - 1):

        # selected nodes
        f1_min = f1_edges[i]
        f1_max = f1_edges[i + 1]

        if i != len(f1_edges) - 2:
            f1_sel = (f1 >= f1_min) & (f1 < f1_max) & (is_core)
        else:
            f1_sel = (f1 >= f1_min) & (is_core)

        # get the f2 edges for this particular part of f1-space.
        vals_sel = f2[f1_sel]
        f2_edges = np.percentile(vals_sel, field_2_percentile_edges)

        for j in range(len(f2_edges) - 1):

            f2_min = f2_edges[j]
            f2_max = f2_edges[j + 1]

            if j != len(f2_edges) - 2:
                f2_sel = (f2 >= f2_min) & (f2 < f2_max) & (f1_sel)
            else:
                f2_sel = (f2 >= f2_min) & (f1_sel)

            sel_nodes = np.nonzero(f2_sel)[0]

            if len(sel_nodes) > 0:
                category[sel_nodes] = val

            val += 1  # increment no matter what for consistency of naming.

    return category
