"""The umami Metric class calculates metrics on terrain."""
from collections import OrderedDict
from copy import deepcopy
from io import StringIO

import yaml

import umami.calculations.metric as calcs
from landlab import RasterModelGrid
from landlab.components import ChiFinder, FlowAccumulator
from landlab.utils.flow__distance import calculate_flow__distance

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


    """

    # only build fields if they are required...
    _required_fields = ["topographic__elevation"]

# ,
# "channel__chi_index",
# "flow__link_to_receiver_node",
# "drainage_area",
# "flow__upstream_node_order",
#flow__distance

    _required_fields_by_func = {"hypsometric_integral": ("flow__receiver_node", "flow__upstream_node_order"),
                                "watershed_aggregation": ("flow__receiver_node", "flow__upstream_node_order")}

    _default_metrics = OrderedDict()

    @classmethod
    def from_dict(params):
        """"""
        # create grid
        grid = create_grid(params.pop("grid"))

        return cls(grid, **params)

    @classmethod
    def from_file(file):
        """"""
        params = _read_input(file)
        return cls.from_dict(params)

    def __init__(self, grid, flow_accumulator_kwds=None, chi_finder_kwds=None, metrics=None):
        """
        Parameters
        ----------
        grid
        flow_accumulator_kwds
        chi_finder_kwds
        metrics

        Attributes
        ----------
        grid
        names
        values

        Functions
        ---------
        add_metrics_from_dict
        add_metrics_from_file
        calculate_metrics
        write_metrics_to_file

        Examples
        --------

        >>> from io import StringIO
        >>> from landlab import RasterModelGrid
        >>> from umami import Metric

        >>> grid = RasterModelGrid((10, 10))
        >>> z = grid.add_zeros("node", "topographic__elevation")
        >>> z += grid.x_of_node + grid.y_of_node

        >>> file_like=StringIO('''
        ... me:
        ...     _func: aggregate
        ...     method: mean
        ...     field: topographic__elevation
        ... ep10:
        ...     _func: aggregate
        ...     method: percentile
        ...     field: topographic__elevation
        ...     q: 10
        ... watershed_aggregation:
        ...     _func: watershed_aggregation
        ...     field: topographic__elevation
        ...     method: mean
        ...     outlet_id: 1
        ... sn1:
        ...     _func: count_equal
        ...     field: drainage_area
        ...     value: 1
        ... ''')

        >>> metric = Metric(grid)
        >>> metric.add_metrics_from_file(file_like)
        >>> metric.names
        odict_keys(['me', 'ep10', 'watershed_aggregation', 'sn1'])
        >>> metric.calculate_metrics()
        >>> metric.values
        [9.0, 5.0, 5.0, 8]
        """
        # verify that apppropriate fields are present.
        for field in self._required_fields:
            if field not in grid.at_node:
                msg = ""
                raise ValueError(msg)

        # save a reference to the grid.
        self._grid = grid

        # run FlowAccumulator
        kwds = flow_accumulator_kwds or {}
        self._fa = FlowAccumulator( grid, **kwds)
        self._fa.run_one_step()

        # Run ChiFinder
        kwds = flow_accumulator_kwds or {}
        self._cf = ChiFinder(grid, **kwds)

        # run distance upstream.
        _ = calculate_flow__distance(grid, add_to_grid=True, noclobber=False)

        # determine which metrics are desired.
        self._metrics = OrderedDict(metrics or {})
        self._validate_metrics(self._metrics)

    @property
    def grid(self):
        """ """
        return self._grid

    @property
    def names(self):
        """
        """
        return self._metrics.keys()

    @property
    def values(self):
        """
        """
        return [self._metric_values[key] for key in self._metrics.keys()]

    def _validate_metrics(self, metrics):
        """"""
        # look at field required by metrics. test if they are all present.
        field_locs = ["field_1", "field_2", "field"]

        # look at all _funcs, ensure that they are valid
        for key in metrics:
            info = metrics[key]

            # Function is defined
            if "_func" not in info:
                msg = ""
                raise ValueError(msg)

            # Function is supported
            func = info["_func"]
            if func not in calcs.__dict__:
                msg = ""
                raise ValueError(msg)

            # Fields required by function are present.
            if func in self._required_fields_by_func:
                fields = self._required_fields_by_func[func]
                for field in fields:
                    if field not in self._grid.at_node:
                        msg = ""
                        raise ValueError(msg)

            for fl in field_locs:
                if fl in info:
                    if info[fl] not in self._grid.at_node:
                        msg = ""
                        raise ValueError(msg)

    def add_metrics_from_file(self, file):
        """"""
        params = _read_input(file)
        self.add_metrics_from_dict(params)

    def add_metrics_from_dict(self, params):
        """"""
        new_metrics = OrderedDict(params)
        self._validate_metrics(new_metrics)
        for key in new_metrics:
            self._metrics[key] = new_metrics[key]

    def calculate_metrics(self):
        """"""
        self._metric_values = OrderedDict()

        for key in self._metrics.keys():
            info = deepcopy(self._metrics[key])
            _func = info.pop("_func")
            function = calcs.__dict__[_func]

            if _func in ("chi_gradient", "chi_intercept"):
                self._metric_values[key] = function(self._cf)
            else:
                self._metric_values[key] = function(self._grid, **info)

    def write_metrics_to_file(self, path):
        """

        Styles: Yaml, Dakota

        """
        pass
