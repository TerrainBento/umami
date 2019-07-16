"""The umami Metric class calculates metrics on terrain."""
from collections import OrderedDict
from io import StringIO

import yaml

import umami.calculations.metric as calcs
from landlab import RasterModelGrid
from landlab.components import ChiFinder, FlowAccumulator

# google "register as plugins" and consider alowing these to be plugins
# instead of fuunctions only in this module.


def _read_input(file):
    if isinstance(file, (str, StringIO)):
        stream = file
    else:
        with open(file, "r") as f:
            stream = f.readlines()
    return OrderedDict(yaml.safe_load(stream))


class Metric(object):
    """Create a Metric class based on a Landlab grid.

    Examples
    --------

    >>> from io import StringIO
    >>> from landlab import RasterModelGrid
    >>> from landlab.components import FlowAccumulator, ChiFinder
    >>> from umami import Metric

    >>> grid = RasterModelGrid((10, 10))
    >>> z = grid.add_zeros("node", "topographic__elevation")
    >>> z += grid.x_of_node + grid.y_of_node
    >>> fa = FlowAccumulator(grid)
    >>> fa.run_one_step()
    >>> cf = ChiFinder(grid)
    >>> cf.calculate_chi()

    >>> file_like=StringIO('''
    ... hi:
    ...     _func: hypsometric_integral
    ... me:
    ...     _func: aggregate
    ...     method: mean
    ...     field: topographic__elevation
    ... ve:
    ...     _func: variance
    ...     field: topographic__elevation
    ... ms:
    ...     _func: mean
    ...     field: topographic__steepest_slope
    ... vs:
    ...     _func: variance
    ...     field: topographic__steepest_slope
    ... ci:
    ...     _func: chi_intercept
    ... cg:
    ...     _func: chi_gradient
    ... ep10:
    ...     _func: percentile
    ...     field: topographic__elevation
    ...     percentile: 10
    ... wshd_mean:
    ...     _func : watershed_aggregation
    ...     field: cumulative_elevation
    ...     method: mean
    ...     outlet_id: 2
    ... sn1:
    ...     _func: count_equal
    ...     field: drainage_area
    ...     value: 1
    ... jdm:
    ...     field_1 : channel__chi_index
    ...     field_2 : topographic__elevation
    ...     field_1_percentile_edges:
    ...         - 0
    ...         - 5
    ...         - 20
    ...         - 40
    ...         - 100
    ...     field_2_percentile_edges:
    ...         - 0
    ...         - 25
    ...         - 50
    ...         - 75
    ...         - 100
    ... dm:
    ...     misfit_field: topographic__elevation
    ...     field_1 : channel__chi_index
    ...     field_2 : topographic__elevation
    ...     field_1_percentile_edges:
    ...         - 0
    ...         - 5
    ...         - 20
    ...         - 40
    ...         - 100
    ...     field_2_percentile_edges:
    ...         - 0
    ...         - 25
    ...         - 50
    ...         - 75
    ...         - 100
    ... ''')
    >>> metric = Metric(grid)
    >>> metric.add_metrics_from_file(file_like)
    >>> metric.names
    odict_keys(['hi', 'me', 've', 'ms', 'vs', 'ci', 'cg', 'ep10', 'wshd_mean', 'sn1', 'jdm', 'dm'])
    """

    _required_fields = [
        "topographic__elevation",
        "channel__chi_index",
        "flow__link_to_receiver_node",
        "drainage_area",
        "flow__upstream_node_order",
    ]

    _default_metrics = OrderedDict()

    @classmethod
    def from_dict(params):
        """"""
        # TODO ordered dictionary

        # create grid
        grid = create_grid(params.pop("grid"))

        # run FlowAccumulator
        fa = FlowAccumulator(
            self.grid, **params.pop("flow_accumulator_kwds", {})
        )
        self.fa.run_one_step()

        # Run ChiFinder
        self.chi_finder = ChiFinder(self.grid, **params.pop("chi_kwds", {}))

        # remaining params has metrics.
        return cls(grid, **params)

    @classmethod
    def from_file(file):
        """"""
        params = _read_input(file)
        return cls.from_dict(params)

    def __init__(self, grid, metrics=None):
        """
        Parameters
        ----------

        """
        # determine which metrics are desired.
        self._validate_metrics(metrics)
        self._metrics = metrics or self._default_metrics

        # verify that apppropriate fields are present.
        for field in self._required_fields:
            if field not in grid.at_node:
                msg = ""
                raise ValueError(msg)

        # look at field required by metrics. test if they are all present.

        # look at all _funcs, ensure that they are valid for

        # save a reference to the grid.
        self.grid = grid

    def _validate_metrics(self, metrics):
        """"""
        pass

    def add_metrics_from_file(self, file):
        """"""
        params = _read_input(file)
        self.add_metrics_from_dict(params)

    def add_metrics_from_dict(self, params):
        """"""
        self._validate_metrics(params)
        for key in params:
            self._metrics[key] = params[key]

    @property
    def names(self):
        return self._metrics.keys()

    def calculate_metrics():
        """"""
        self.metric_order = []
        self.metrics = {}

        for metric in self._metrics:
            self.metric_order.append(name)
            # get _function, apply  with inspect.
            # save value.
