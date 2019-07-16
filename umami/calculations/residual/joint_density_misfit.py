def joint_density_misfit(
    data_grid,
    model_grid,
    field_1,
    field_2,
    field_1_percentile_edges,
    field_2_percentile_edges,
):
    """
    """

    f1 = grid.at_node[field_1]
    f2 = grid.at_node[field_2]

    # first bin by field 1, then within field_1, bin by field_2
    is_core = np.zeros_like(f1, dtype=bool)
    is_core[grid.core_nodes] = True

    # calc the percentiles of the field 1 distribution
    f1_edges = np.percentile(f1[is_core], field_1_percentile_edges)

    def _calc_channel_chi_distribution(self):
        """"""
        # calc on DEM
        self._density_chi, xedges, yedges = np.histogram2d(
            self.z, self.chi, bins=(self._xedges, self._yedges), normed=True
        )

    def density_chi(self):
        """"""
        return self._density_chi
