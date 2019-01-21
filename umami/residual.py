
""""""

from .metric import Metric
class Residual(object):
    """"""

    _required_fields = ["topographic__elevation"]

    _all_metrics = []

    def __init__(
        data,
        model,
        chi_percentiles=[0, 5, 20, 50, 100],
        elev_percentiles=[0, 20, 40, 60, 80, 100],
        metrics=None,
        **kwargs
    ):
        """could do.

        Residual(model=Terrain(grid), data=Terrain.from_dict(stuff))
        """
        # assert that the model grids have the same x_of_node and y_of_node.
        assert_array_equal(data.grid.x_of_node, model.grid.x_of_node)
        assert_array_equal(data.grid.y_of_node, model.grid.y_of_node)

        self.data = Metric(data, **kwargs)
        self.model = Metric(model, **kwargs)

        self._chi_percentiles = chi_percentiles
        self._elev_percentiles = elevation_percentiles

    def _chi_cat_categories(self):
        """ """
        # first bin by chi, then within chi, bin by elevation
        is_core = np.zeros_like(self.data.z)
        is_core[self.data.grid.core_nodes] = True

        # calc the percentiles of the chi distribution
        chi_edges = np.percentile(self.data.chi[is_core is True],
                                  self._chi_percentiles)

        # work through each bin and label them.
        self._chi_elev_category = np.zeros_like(z)

        val = 1
        for i in range(len(chi_edges) - 1):

            # selected nodes
            x_min = chi_edges[i]
            x_max = chi_edges[i + 1]

            if i != len(chi_edges) - 2:
                x_sel = (
                    (ch.chi >= x_min) & (ch.chi < x_max) & (is_core is True)
                )
            else:
                x_sel = (ch.chi >= x_min) & (is_core is True)

            # get the edges for this particular part of chi-space
            z_sel = self.data.z[x_sel]
            elev_edges = np.percentile(z_sel, self._elev_percentiles)

            for j in range(len(elev_edges) - 1):

                elev_min = elev_edges[j]
                elev_max = elev_edges[j + 1]

                if j != len(elev_edges) - 2:
                    y_sel = (z >= elev_min) & (z < elev_max) & (x_sel)
                else:
                    y_sel = (z >= elev_min) & (x_sel)

                sel_nodes = np.where(y_sel)[0]

                if len(sel_nodes) > 0:
                    self._chi_elev_category[sel_nodes] = val
                    val += 1
