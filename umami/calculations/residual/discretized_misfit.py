def discretized_misfit(
    data_grid,
    model_grid,
    misfit_field,
    field_1,
    field_2,
    field_1_percentile_edges,
    field_2_percentile_edges,
):
    """
    """
    category = _get_category_labels(
        data_grid,
        misfit_field,
        field_1,
        field_2,
        field_1_percentile_edges,
        field_2_percentile_edges,
    )


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
    category = np.zeros_like(vals)

    val = 1
    for i in range(len(f1_edges) - 1):

        # selected nodes
        f1_min = f1_edges[i]
        f1_max = f1_edges[i + 1]

        if i != len(f1_edges) - 2:
            f1_sel = (field_1 >= f1_min) & (field_1 < f1_max) & (is_core)
        else:
            f1_sel = (field_1 >= f1_min) & (is_core)

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
