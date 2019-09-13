"""The ``umami.Metric`` class calculates metrics on a Landlab model grid."""
from collections import OrderedDict
from copy import deepcopy

import numpy as np
import yaml
from landlab import RasterModelGrid, create_grid

import umami.calculations.metric as calcs
from umami.utils.create_landlab_components import _create_landlab_components
from umami.utils.io import _read_input, _write_output
from umami.utils.validate import _validate_fields, _validate_func

_VALID_FUNCS = calcs.__dict__


class Metric(object):
    """Create a ``Metric`` class based on a Landlab model grid."""

    _required_fields = ["topographic__elevation"]

    def __init__(
        self,
        grid,
        flow_accumulator_kwds=None,
        chi_finder_kwds=None,
        metrics=None,
    ):
        """
        Parameters
        ----------
        grid : Landlab model grid
        flow_accumulator_kwds : dict
            Parameters to pass to the Landlab ``FlowAccumulator`` to specify
            flow direction and accumulation.
        chi_finder_kwds : dict
            Parameters to pass to the Landlab ``ChiFinder`` to specify optional
            arguments.    `
        metrics : dict
            A dictionary of desired metrics to calculate. See examples for
            required format.

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
        ... oid1_mean:
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
        >>> metric.add_from_file(file_like)
        >>> metric.names
        ['me', 'ep10', 'oid1_mean', 'sn1']
        >>> metric.calculate()
        >>> metric.value('me')
        9.0
        >>> metric.values
        [9.0, 5.0, 5.0, 8]
        """
        # verify that apppropriate fields are present.
        for field in self._required_fields:
            if field not in grid.at_node:
                msg = "umami: Required field: {field} is missing.".format(
                    field=field
                )
                raise ValueError(msg)

        # save a reference to the grid.
        self._grid = grid

        # run FlowAccumulator and ChiFinder
        self._fa, self._cf = _create_landlab_components(
            self._grid,
            chi_finder_kwds=chi_finder_kwds,
            flow_accumulator_kwds=flow_accumulator_kwds,
        )

        # determine which metrics are desired.
        self._metrics = OrderedDict(metrics or {})
        self._validate_metrics(self._metrics)

    @property
    def names(self):
        """Names of metrics in metric order."""
        self._names = [key for key in self._metrics]
        return self._names

    def value(self, name):
        """Get a specific metric value.

        Parameters
        ----------
        name: str
            Name of desired metric.
        """
        return self._values[name]

    @property
    def values(self):
        """Metric values in metric order."""
        return [self._values[key] for key in self._metrics.keys()]

    def add_from_file(self, file):
        """Add metrics to an ``umami.Metric`` from a file.

        Parameters
        ----------
        file_like : file path or StringIO
            File will be parsed by ``yaml.safe_load`` and converted to an
            ``OrderedDict``.
        """
        params = _read_input(file)
        self.add_from_dict(params)

    def add_from_dict(self, params):
        """Add metrics to an ``umami.Metric`` from a dictionary.

        Adding metrics through this method does not overwrite already existing
        metrics. New metrics are appended to the existing metric list.

        Parameters
        ----------
        params : dict or OrderedDict
            Keys are metric names and values are a dictionary describing
            the creation of the metric. It will be convereted to an OrderedDict
            before metrics are added so as to preserve metric order.
        """
        new_metrics = OrderedDict(params)
        self._validate_metrics(new_metrics)
        for key in new_metrics:
            self._metrics[key] = new_metrics[key]

    def calculate(self):
        """Calculate metric values.

        Calculated metric values are stored in the attribute
        ``Metric.values``.
        """
        self._values = OrderedDict()

        for key in self._metrics.keys():
            info = deepcopy(self._metrics[key])
            _func = info.pop("_func")
            function = calcs.__dict__[_func]

            if _func in ("chi_gradient", "chi_intercept"):
                self._values[key] = function(self._cf)
            else:
                self._values[key] = function(self._grid, **info)

    def write_metrics_to_file(self, path, style, decimals=3):
        """Write metrics to a file.

        Parameters
        ----------
        path :
        style : str
            yaml, dakota
        decimals: int
            Number of decimals to round output to.

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
        ... oid1_mean:
        ...     _func: watershed_aggregation
        ...     field: topographic__elevation
        ...     method: mean
        ...     outlet_id: 1
        ... sn1:
        ...     _func: count_equal
        ...     field: drainage_area
        ...     value: 1
        ... ''')

        First we ouput in *dakota* style, in which each metric is listed on
        its own line with its name as a comment.

        >>> metric = Metric(grid)
        >>> metric.add_from_file(file_like)
        >>> metric.calculate()
        >>> out = StringIO()
        >>> metric.write_metrics_to_file(out, style="dakota")
        >>> file_contents = out.getvalue().splitlines()
        >>> for line in file_contents:
        ...     print(line.strip())
        9.0 # me
        5.0 # ep10
        5.0 # oid1_mean
        8 # sn1

        Next we output in *yaml* style, in which each metric is serialized in
        YAML format.

        >>> out = StringIO()
        >>> metric.write_metrics_to_file(out, style="yaml")
        >>> file_contents = out.getvalue().splitlines()
        >>> for line in file_contents:
        ...     print(line.strip())
        me: 9.0
        ep10: 5.0
        oid1_mean: 5.0
        sn1: 8
        """
        if style == "dakota":
            stream = "\n".join(
                [
                    str(np.round(val, decimals=decimals)) + " # " + str(key)
                    for key, val in self._values.items()
                ]
            )
        if style == "yaml":
            stream = "\n".join(
                [
                    str(key) + ": " + str(np.round(val, decimals=decimals))
                    for key, val in self._values.items()
                ]
            )

        _write_output(path, stream)

    @classmethod
    def from_dict(cls, params):
        """Create an umami ``Metric`` from a dictionary.

        Parameters
        ----------
        params : dict or OrderedDict
            This dict must contain a key *grid*, the values of which will be
            passed to the `Landlab` function ``create_grid`` to create the
            model grid. It will be convereted to an OrderedDict before metrics
            are added so as to preserve metric order.

        Examples
        --------
        >>> from io import StringIO
        >>> from umami import Metric
        >>> params = {
        ...     "grid": {
        ...         "RasterModelGrid": [
        ...             [10, 10],
        ...             {
        ...                 "fields": {
        ...                     "node": {
        ...                         "topographic__elevation": {
        ...                             "plane": [
        ...                                 {"point": [0, 0, 0]},
        ...                                 {"normal": [-1, -1, 1]},
        ...                             ]
        ...                         }
        ...                     }
        ...                 }
        ...             },
        ...         ]
        ...     },
        ...     "metrics": {
        ...         "me": {
        ...             "_func": "aggregate",
        ...             "method": "mean",
        ...             "field": "topographic__elevation",
        ...         },
        ...         "ep10": {
        ...             "_func": "aggregate",
        ...             "method": "percentile",
        ...             "field": "topographic__elevation",
        ...             "q": 10,
        ...         },
        ...         "oid1_mean": {
        ...             "_func": "watershed_aggregation",
        ...             "field": "topographic__elevation",
        ...             "method": "mean",
        ...             "outlet_id": 1,
        ...         },
        ...         "sn1": {
        ...             "_func": "count_equal",
        ...             "field": "drainage_area",
        ...             "value": 1,
        ...         },
        ...     },
        ... }
        >>> metric = Metric.from_dict(params)
        >>> metric.names
        ['me', 'ep10', 'oid1_mean', 'sn1']
        >>> metric.calculate()
        >>> metric.value('me')
        9.0
        >>> metric.values
        [9.0, 5.0, 5.0, 8]
        """
        # create grid
        grid = create_grid(params.pop("grid"))
        return cls(grid, **params)

    @classmethod
    def from_file(cls, file_like):
        """Create an umami ``Metric`` from a file-like object.

        Parameters
        ----------
        file_like : file path or StringIO
            File will be parsed by ``yaml.safe_load`` and converted to an
            ``OrderedDict``.

        Returns
        -------
        umami.Metric

        Examples
        --------
        >>> from io import StringIO
        >>> from umami import Metric
        >>> file_like=StringIO('''
        ... grid:
        ...     RasterModelGrid:
        ...         - [10, 10]
        ...         - fields:
        ...               node:
        ...                   topographic__elevation:
        ...                       plane:
        ...                           - point: [0, 0, 0]
        ...                           - normal: [-1, -1, 1]
        ... metrics:
        ...     me:
        ...         _func: aggregate
        ...         method: mean
        ...         field: topographic__elevation
        ...     ep10:
        ...         _func: aggregate
        ...         method: percentile
        ...         field: topographic__elevation
        ...         q: 10
        ...     oid1_mean:
        ...         _func: watershed_aggregation
        ...         field: topographic__elevation
        ...         method: mean
        ...         outlet_id: 1
        ...     sn1:
        ...         _func: count_equal
        ...         field: drainage_area
        ...         value: 1
        ... ''')
        >>> metric = Metric.from_file(file_like)
        >>> metric.names
        ['me', 'ep10', 'oid1_mean', 'sn1']
        >>> metric.calculate()
        >>> metric.value('me')
        9.0
        >>> metric.values
        [9.0, 5.0, 5.0, 8]
        """
        params = _read_input(file_like)
        return cls.from_dict(params)

    def _validate_metrics(self, metrics):
        # look at all _funcs, ensure that they are valid
        for key in metrics:
            info = metrics[key]
            _validate_func(key, info, _VALID_FUNCS)
            _validate_fields(self._grid, info)
