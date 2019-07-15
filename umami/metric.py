"""The umami Metric class calculates metrics on terrain."""
import yaml

import umami.calculations.metric as calcs
from landlab import RasterModelGrid
from landlab.components import ChiFinder, FlowAccumulator

# google "register as plugins" and consider alowing these to be plugins
# instead of fuunctions only in this module.

class Metric(object):
    """Create a Metric class based on a Landlab grid.

    Examples
    --------

    >>> from six import StringIO
    >>> from umami import Metric
    >>> input=StringIO(
    ... '''
    ... grid: # create grid
    ... flow_accumulator_kwds:
    ...     kwd: val
    ... chi_kwds:
    ...     kwd: val
    ... metrics: # read in as ordered dictionary
    ...     hi:
    ...         _func: hypsometric_integral
    ...     me:
    ...         _func: aggregate # on core nodes...
    ...         method: mean
    ...         field: topographic__elevation
    ...     ve:
    ...         _func: variance
    ...         field: topographic__elevation
    ...     ms:
    ...         _func: mean
    ...         field: topographic__steepest_slope
    ...     vs:
    ...         _func: variance
    ...         field: topographic__steepest_slope
    ...     ci:
    ...         _func: chi_intercept
    ...     cg:
    ...         _func: chi_gradient
    ...     ep10:
    ...         _func: percentile:
    ...         field: topographic__elevation
    ...         percentile: 10
    ...     basin_1_average:
    ...         _func : watershed_aggregation
    ...         field: cumulative_elevation
    ...         outlet_id: 12234
    ...     sn1:
    ...         _func: count_equal
    ...         field: drainage_area
    ...         value: 1
    ...     joint_density_misfit:
    ...         field_1 : channel__chi_index
    ...         field_2 : topographic__elevation
    ...         field_1_percentile_edges:
    ...             - 0
    ...             - 5
    ...             - 20
    ...             - 40
    ...             - 100
    ...         field_2_percentile_edges:
    ...             - 0
    ...             - 25
    ...             - 50
    ...             - 75
    ...             - 100
    ...     discretized_misfit:
    ...         misfit_field: topographic__elevation
    ...         field_1 : channel__chi_index
    ...         field_2 : topographic__elevation
    ...         field_1_percentile_edges:
    ...             - 0
    ...             - 5
    ...             - 20
    ...             - 40
    ...             - 100
    ...         field_2_percentile_edges:
    ...             - 0
    ...             - 25
    ...             - 50
    ...             - 75
    ...             - 100
    ... ''')

    """

    _required_fields = ["topographic__elevation", "channel__chi_index", "drainage_area",] # TODO remaining flow requirements.
    _default_metrics = []

    @classmethod
    def from_dict(params):
        """
        """
        #TODO ordered dictionary

        # create grid
        grid = create_grid(params.pop("grid"))

        # run FlowAccumulator
        fa = FlowAccumulator(self.grid, **params.pop("flow_accumulator_kwds", {}))
        self.fa.run_one_step()

        # Run ChiFinder
        self.chi_finder = ChiFinder(self.grid, **params.pop("chi_kwds", {}))

        # remaining params has metrics.
        return cls(grid, **params)

    @classmethod
    def from_file(file):
        """
        """
        with open(file, 'r') as f:

            #TOdo ordered dictionary
            params = yaml.save_load(f)

        return cls.from_dict(params)

    def __init__(
        grid,
        metrics=None
    ):
        """
        Parameters
        ----------

        """
        # determine which metrics are desired.
        self._metrics = metrics or self._all_metrics

        # verify that apppropriate fields are present.
        for field in self._required_fields:
            if field not in  grid.at_node:
                msg = ""
                raise ValueError(msg)

        # look at field required by metrics. test if they are all present.


        # look at all funcs, ensure that they are valid for


        # save a reference to the grid.
        self.grid = grid


    def add_metrics_from_file(self, file):
        """
        """

    def add_metrics_from_dict(self, params):
        """
        """

    def calculate_metrics():
        """  """
        self.metric_order = []
        self.metrics = {}

        for metric in self._metrics:

            self.metric_order.append(name)
            # get function, apply  with inspect.
            # save value.
