"""The umami Metric class calculates metrics on terrain."""
from landlab import RasterModelGrid
from landlab.components import ChiFinder, FlowAccumulator


class Metric(object):
    """Create a Metric class based on a Landlab grid.


    longest_channel_slope_area

    Examples
    --------

    >>> from six import StringIO
    >>> input=StringIO('''
    ... grid: # create grid
    ... flow_accumulator_kwargs:
    ...     kwd: val
    ... chi_kwargs:
    ...     kwd: val
    ... metrics:
    ...     - hypsometric_integral
    ...     - mean_elevation
    ...     - variance_elevation
    ...     - mean_slope
    ...     - variance_slope
    ...     - chi_intercept
    ...     - chi_gradient
    ...     - elev_percentile:
    ...         - 10
    ...         - 50
    ...         - 90
    ...     - area_percentile:
    ...         - 10
    ...         - 50
    ...         - 90
    ...     - source_nodes:
    ...         - 1
    ...         - 2
    ...         - 3
    ...     - chi_elev_distribution:
    ...         chi_percentile_edges:
    ...             - 0
    ...             - 5
    ...             - 20
    ...             - 40
    ...             - 100
    ...         elev_percentile_edges:
    ...             - 0
    ...             - 25
    ...             - 50
    ...             - 75
    ...             - 100
    ...     - chi_elev_categories:
    ...         chi_percentile_edges:
    ...             - 0
    ...             - 5
    ...             - 20
    ...             - 40
    ...             - 100
    ...         elev_percentile_edges:
    ...             - 0
    ...             - 25
    ...             - 50
    ...             - 75
    ...             - 100'''

    """

    _required_fields = ["topographic__elevation"]
    _default_metrics = []

    def __init__(
        grid,
        chi_kwargs=None,
        flow_accumulator_kwargs=None,
        metrics=None
    ):
        """
        Parameters
        ----------



        """

        # chi_distribution_xedges=None,
        # chi_distribution_yedges=None,
        # area_percentiles=[10, 30, 50, 70, 90],
        # elevation_percentiles=[10, 30, 50, 70, 90],

        # determine which metrics are desired.
        metrics = metrics or self._all_metrics

        # get the correct kwargs
        chi_kwargs = chi_kwargs or {}
        flow_accumulator_kwargs = flow_accumulator_kwargs or {}

        # save a reference to the grid.
        self.grid = grid

        # route flow on the grid. Use steepest and DepressionFinderAndRouter as
        # defaults.
        self.fa = FlowAccumulator(self.grid, **flow_accumulator_kwargs)
        self.fa.run_one_step()

        # Instantiate a ChiFinder for chi-index
        self.chi_finder = ChiFinder(self.grid, **chi_kwargs)

        # Calc slopes
        self._calc_slope()

        # calc chi intercepts
        self._calc_chi_index()

        # Remember a few at-node fields
        self.z = grid.grid.at_node["topographic__elevation"]
        self.area = self.grid.at_node["drainage_area"]
        self.slope = self.grid.at_node["topographic__steepest_slope"]
        self.chi = self.grid.at_node["channel__chi_index"]

        # set the chi-distribution x and y edges.
        self._xedges = chi_distribution_xedges or np.arrange(
            self.z.min(), self.z.max(), 10
        )
        self._yedges = chi_distribution_yedges or np.arrange(
            self.chi.min(), self.chi.max(), 10
        )

        # calculate desired percentiles in elevation and area.
        for pct in elevation_percentiles:
            name = "elevation_percentiles_" + str(pct)
            self._attrs[name] = self._calc_elevation_percentile(percentile=pct)

        for pct in area_percentiles:
            name = "area_percentiles_" + str(pct)
            self._attrs[name] = self._calc_area_percentile(percentile=pct)

    @property
    def longest_channel_slope_area(self):
        """ """

    @property
    def hypsometric_integral(self):
        """Hypsometric integral."""
        return self._hypsometric_integral

    def _hypsometric_integral(self):
        # Get just those elevation values that are within the watershed
        wshed_elevs = self.z[self.grid.core_nodes]

        # Get min and max
        min_elev = np.amin(wshed_elevs)
        max_elev = np.amax(wshed_elevs)

        # Calc and return hyps int
        return np.mean(wshed_elevs - min_elev) / (max_elev - min_elev)

    @property
    def mean_elevation(self):
        """Mean of elevation."""
        return self._mean_elevation

    def _mean_elevation(self):
        return np.mean(self.z[self.grid.core_nodes])

    @property
    def mean_slope(self):
        """Mean slope."""
        return self._mean_slope

    def _mean_slope(self):
        return np.mean(self._slope)

    @property
    def variance_elevation(self):
        """Mean of elevation."""
        return self._variance_elevation

    def _variance_elevation(self):
        return np.var(self.z[self.grid.core_nodes])

    @property
    def variance_slope(self):
        """Mean slope."""
        return self._variance_slope

    def _variance_slope(self):
        return np.var(self._slope)

    def _calc_slope(self):
        # calc the gradient at links
        grad = self.grid.calc_grad_at_link(self.z)

        # Find IDs of nodes that have four active links
        active_links_at_node = self.grid.links_at_node * np.abs(
            self.grid.active_link_dirs_at_node
        )
        nodes = np.where(np.amin(active_links_at_node, axis=1) > 0)

        # Get the x and y components of slope at each of these.
        # We're assuming we're dealing with raster grids, in which columns
        # 0 and 2 of the links_at_node array contain east-west links, and
        # columns 1 and 3 contain north-south links. We take the average in
        # each direction.
        if isinstance(self.grid, RasterModelGrid):
            grad_x = 0.5 * (
                grad[self.grid.links_at_node[nodes, 0]]
                + grad[self.grid.links_at_node[nodes, 2]]
            )
            grad_y = 0.5 * (
                grad[self.grid.links_at_node[nodes, 1]]
                + grad[self.grid.links_at_node[nodes, 3]]
            )

            # Combine them to get the slope magnitude
            self._slope = np.sqrt(grad_x ** 2 + grad_y ** 2)

    def _calc_chi_index(self):
        """calc and return coefficients of chi plot."""
        self.chi_finder.calc_chi()
        (self._chi_gradient, self._chi_intercept) = self.calc_chi_index()

    @property
    def chi_intercept(self):
        """"""
        return self._chi_intercept

    @property
    def chi_gradient(self):
        """"""
        return self._chi_gradient

    def _calc_channel_chi_distribution(self):
        """"""
        # calc on DEM
        self._density_chi, xedges, yedges = np.histogram2d(
            self.z, self.chi, bins=(self._xedges, self._yedges), normed=True
        )

    def density_chi(self):
        """"""
        return self._density_chi

    def _calc_number_source_nodes(self, factor=1.0):
        """calc and return number of nodes below a given threshold.

        Parameters
            factor, float, default

        Threshold given by cell area x factor
        """
        single_cell_area = factor * (self.grid.dx ** 2.0)

        source_nodes = np.sum(
            self.area[self.grid.core_nodes] <= single_cell_area
        )

        return source_nodes

    @property
    def one_cell_nodes(self):
        """"""
        return self._calc_number_source_nodes(factor=1.0)

    @property
    def two_cell_nodes(self):
        """"""
        return self._calc_number_source_nodes(factor=2.0)

    @property
    def three_cell_nodes(self):
        """"""
        return self._calc_number_source_nodes(factor=3.0)

    @property
    def four_cell_nodes(self):
        """"""
        return self._calc_number_source_nodes(factor=4.0)

    def _calc_area_percentile(self, percentile=50):
        """"""
        return np.percentile(self.area[self.grid.core_nodes], percentile)

    def _calc_elevation_percentile(self, percentile=50):
        """"""
        return np.percentile(self.z[self.grid.core_nodes], percentile)
