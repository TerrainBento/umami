
"""
"""

class Residual(object):
    """
    """

    _required_fields = ["topographic__elevation"]

    def __init__(data,
                 model,
                 chi_percentiles=[0, 5, 20, 50, 100],
                 elev_percentiles=[0, 20, 40, 60, 80, 100]):
        """

        could do.

        Residual(model=Terrain(grid), data=Terrain.from_dict(stuff))

        """
        # assert that the model grids have the same x_of_node and y_of_node.
        assert_array_equal(data.grid.x_of_node, model.grid.x_of_node)
        assert_array_equal(data.grid.y_of_node, model.grid.y_of_node)

        self.data = data
        self.model = model

    def _chi_cat_categories(self):
        # first bin by chi, then within chi, bin by elevation
        is_core = np.zeros_like(z)
        is_core[grid.core_nodes] = True
        chi_percentiles = [0, 5, 20, 50, 100]
        elev_percentiles = [0, 20, 40, 60, 80, 100]

        # calc the percentiles of the chi distribution
        chi_edges = np.percentile(ch.chi[is_core==True], chi_percentiles)

        # work through each bin and label them.
        cat = np.zeros_like(z)
        H = np.zeros((len(chi_percentiles)-1, len(elev_percentiles)-1))
        val = 1

        cat_bin = np.zeros_like(z)

        f, axarr = plt.subplots(len(chi_edges)-1, figsize = (4, 16), dpi=300)
        for i in range(len(chi_edges) - 1):

            cat_plot = np.zeros_like(z)

            # selected nodes
            x_min = chi_edges[i]
            x_max = chi_edges[i+1]

            if i != len(chi_edges) - 2:
                x_sel = (ch.chi >= x_min) & (ch.chi < x_max) & (is_core==True)
            else:
                x_sel = (ch.chi >= x_min) & (is_core==True)

            # get the edges for this particular part of chi-space
            z_sel = z[x_sel]
            elev_edges = np.percentile(z_sel, elev_percentiles)
            for j in range(len(elev_edges) - 1):

                elev_min = elev_edges[j]
                elev_max = elev_edges[j+1]

                if j != len(elev_edges) - 2:
                    y_sel = (z >= elev_min) & (z < elev_max) & (x_sel)
                else:
                    y_sel = (z >= elev_min) & (x_sel)

                sel_nodes = np.where(y_sel)[0]

                H[i,j] = int(len(sel_nodes))
                #sel_nodes = grid.core_nodes
                if len(sel_nodes) > 0:
                    cat[sel_nodes] = val
                    cat_bin[sel_nodes] = len(sel_nodes)
                    cat_plot[sel_nodes] = cat[sel_nodes]
                    val +=1
