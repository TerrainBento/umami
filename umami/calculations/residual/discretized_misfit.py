from collections import OrderedDict

import numpy as np


def discretized_misfit(
    model_grid,
    data_grid,
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
    model_grid
    data_grid
    misfit_field
    field_1
    field_2
    field_1_percentile_edges
    field_2_percentile_edges

    Returns
    -------


    Examples
    --------
    First an example that only uses the ``discretized_misfit`` function.

    >>> import numpy as np
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator
    >>> from umami.calculations import discretized_misfit
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

    >>> discretized_misfit(
    ...     model,
    ...     data,
    ...     "topographic__elevation",
    ...     "topographic__elevation",
    ...     "drainage_area",
    ...     [0, 50, 100],
    ...     [0, 60, 100]) # doctest: +NORMALIZE_WHITESPACE
    OrderedDict([(1, 0.52883662950630161), (2, 0.54198190529674906), (3, 0.51940386248902548)])

    Next, the same calculations are shown as part of an umami ``Residual``.

    >>> from io import StringIO
    >>> from umami import Residual
    >>> file_like=StringIO('''
    ... dm:
    ...     _func: discretized_misfit
    ...     misfit_field: topographic__elevation
    ...     field_1: topographic__elevation
    ...     field_2: drainage_area
    ...     field_1_percentile_edges:
    ...         - 0
    ...         - 50
    ...         - 100
    ...     field_2_percentile_edges:
    ...         - 0
    ...         - 60
    ...         - 100
    ... ''')
    >>> residual = Residual(model, data)
    >>> residual.add_residuals_from_file(file_like)
    >>> residual.names
    odict_keys(['dm'])
    >>> residual.calculate_residuals()
    >>> residual.values
    [OrderedDict([(1, 0.52883662950630161), (2, 0.54198190529674906), (3, 0.51940386248902548)])]
    """

    category = _get_category_labels(
        data_grid,
        misfit_field,
        field_1,
        field_2,
        field_1_percentile_edges,
        field_2_percentile_edges,
    )

    difference = (
        model_grid.at_node[misfit_field] - data_grid.at_node[misfit_field]
    )

    out = OrderedDict()
    for c in range(1, np.max(category)):

        sq_resids = np.power(difference[category == c], 2.0)
        misfit = np.sqrt(np.mean(sq_resids))
        out[c] = misfit
    return out


def _get_category_labels(
    grid,
    misfit_field,
    field_1,
    field_2,
    field_1_percentile_edges,
    field_2_percentile_edges,
):

    vals = grid.at_node[misfit_field]
    f1 = grid.at_node[field_1]
    f2 = grid.at_node[field_2]

    # first bin by field 1, then within field_1, bin by field_2
    is_core = np.zeros_like(vals, dtype=bool)
    is_core[grid.core_nodes] = True

    # calc the percentiles of the field 1 distribution
    f1_edges = np.percentile(f1[is_core], field_1_percentile_edges)

    # work through each bin and label them.
    category = np.zeros_like(vals, dtype=np.int)

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
        vals_sel = vals[f1_sel]
        f2_edges = np.percentile(vals_sel, field_2_percentile_edges)

        for j in range(len(f2_edges) - 1):

            f2_min = f2_edges[j]
            f2_max = f2_edges[j + 1]

            if j != len(f2_edges) - 2:
                f2_sel = (vals >= f2_min) & (vals < f2_max) & (f1_sel)
            else:
                f2_sel = (vals >= f2_min) & (f1_sel)

            sel_nodes = np.nonzero(f2_sel)[0]

            if len(sel_nodes) > 0:
                category[sel_nodes] = val
                val += 1

    return category
