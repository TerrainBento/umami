""""""
from collections import OrderedDict
from copy import deepcopy

import numpy as np
import yaml
from numpy.testing import assert_array_equal

import umami.calculations.metric as metric_calcs
import umami.calculations.residual as residual_calcs
from landlab import RasterModelGrid, create_grid
from umami.metric import Metric
from umami.utils.create_landlab_components import _create_landlab_components
from umami.utils.io import _read_input, _write_output
from umami.utils.validate import _validate_fields, _validate_func

_VALID_FUNCS = {}
_VALID_FUNCS.update(residual_calcs.__dict__)
_VALID_FUNCS.update(metric_calcs.__dict__)


class Residual(object):
    """Create a ``Residual`` class based on a model and data Landlab grid."""

    _required_fields = ["topographic__elevation"]

    def __init__(
        self,
        model,
        data,
        flow_accumulator_kwds=None,
        chi_finder_kwds=None,
        residuals=None,
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
        residuals : dict
            A dictionary of desired residuals to calculate. See examples for
            required format.

        Attributes
        ----------
        names
        values

        Functions
        ---------
        add_residuals_from_dict
        add_residuals_from_file
        calculate_residuals
        write_residuals_to_file

        Examples
        --------
        >>> import numpy as np
        >>> from io import StringIO
        >>> from landlab import RasterModelGrid
        >>> from umami import Residual

        >>> np.random.seed(42)

        >>> model = RasterModelGrid((10, 10))
        >>> z_model = model.add_zeros("node", "topographic__elevation")
        >>> z_model += model.x_of_node + model.y_of_node

        >>> data = RasterModelGrid((10, 10))
        >>> z_data = data.add_zeros("node", "topographic__elevation")
        >>> z_data +=  data.x_of_node + data.y_of_node
        >>> z_data[data.core_nodes] += np.random.random(data.core_nodes.shape)

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

        >>> residual = Residual(model, data)
        >>> residual.add_residuals_from_file(file_like)
        >>> residual.names
        odict_keys(['me', 'ep10', 'oid1_mean', 'sn1'])
        >>> residual.calculate_residuals()
        >>> np.testing.assert_array_almost_equal(
        ...     np.round(residual.values, decimals=3),
        ...     np.array([ -0.467,  -0.151,   3.313, -18.   ]))
        """
        # assert that the model grids have the same x_of_node and y_of_node.
        assert_array_equal(data.x_of_node, model.x_of_node)
        assert_array_equal(data.y_of_node, model.y_of_node)

        self._data_grid = data
        self._model_grid = model

        # verify that apppropriate fields are present.
        for field in self._required_fields:
            if (field not in model.at_node) or (field not in data.at_node):
                msg = ""
                raise ValueError(msg)

        # run FlowAccumulator and ChiFinder
        self._data_fa, self._data_cf = _create_landlab_components(
            self._data_grid,
            chi_finder_kwds=chi_finder_kwds,
            flow_accumulator_kwds=flow_accumulator_kwds,
        )

        self._model_fa, self._model_cf = _create_landlab_components(
            self._model_grid,
            chi_finder_kwds=chi_finder_kwds,
            flow_accumulator_kwds=flow_accumulator_kwds,
        )

        # determine which residuals are desired.
        self._residuals = OrderedDict(residuals or {})
        self._validate_residuals(self._residuals)
        self._distinguish_metric_from_resid()

        # calculate
        self._data_metric = Metric(
            data,
            flow_accumulator_kwds=flow_accumulator_kwds,
            chi_finder_kwds=chi_finder_kwds,
            metrics=self._metrics,
        )
        self._model_metric = Metric(
            model,
            flow_accumulator_kwds=flow_accumulator_kwds,
            chi_finder_kwds=chi_finder_kwds,
            metrics=self._metrics,
        )

    @classmethod
    def from_dict(cls, params):
        """Create an umami ``Residual`` from a dictionary.

        Parameters
        ----------
        params : dict or OrderedDict
            This dict must contain a key *grid*, the values of which will be
            passed to the `Landlab` function ``create_grid`` to create the
            model grid. It will be convereted to an OrderedDict before residuals
            are added so as to preserve residual order.

        Examples
        --------
        >>> import numpy as np
        >>> from io import StringIO
        >>> from umami import Residual

        >>> np.random.seed(42)

        >>> params = {
        ...     "model": {
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
        ...     "data": {
        ...         "RasterModelGrid": [
        ...             [10, 10],
        ...             {
        ...                 "fields": {
        ...                     "node": {
        ...                         "topographic__elevation": {
        ...                             "plane": [
        ...                                 {"point": [0, 0, 0]},
        ...                                 {"normal": [-1, -1, 1]},
        ...                             ],
        ...                             "random" : [
        ...                                 {"where": "CORE_NODE"},
        ...                                 {"distribution": "standard_normal"},
        ...                             ]
        ...                         }
        ...                     }
        ...                 }
        ...             },
        ...         ]
        ...     },
        ...     "residuals": {
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

        >>> residual = Residual.from_dict(params)
        >>> residual.names
        odict_keys(['me', 'ep10', 'oid1_mean', 'sn1'])
        >>> residual.calculate_residuals()
        >>> np.testing.assert_array_almost_equal(
        ...     np.round(residual.values, decimals=3),
        ...     np.array([  0.158,   0.67 ,   4.138, -20.   ]))
        """
        model = create_grid(params.pop("model"))
        data = create_grid(params.pop("data"))

        return cls(model, data, **params)

    @classmethod
    def from_file(cls, file_like):
        """Create an umami ``Residual`` from a file-like object.

        Parameters
        ----------
        file_like : file path or StringIO
            File will be parsed by ``yaml.safe_load`` and converted to an
            ``OrderedDict``.

        Returns
        -------
        umami.Residual

        Examples
        --------
        >>> import numpy as np
        >>> from io import StringIO
        >>> from umami import Residual

        >>> np.random.seed(42)

        >>> file_like=StringIO('''
        ... model:
        ...     RasterModelGrid:
        ...         - [10, 10]
        ...         - fields:
        ...               node:
        ...                   topographic__elevation:
        ...                       plane:
        ...                           - point: [0, 0, 0]
        ...                           - normal: [-1, -1, 1]
        ... data:
        ...     RasterModelGrid:
        ...         - [10, 10]
        ...         - fields:
        ...               node:
        ...                   topographic__elevation:
        ...                       plane:
        ...                           - point: [0, 0, 0]
        ...                           - normal: [-1, -1, 1]
        ...                       random:
        ...                          distribution: standard_normal
        ...                          where: CORE_NODE
        ... residuals:
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

        >>> residual = Residual.from_file(file_like)
        >>> residual.names
        odict_keys(['me', 'ep10', 'oid1_mean', 'sn1'])
        >>> residual.calculate_residuals()
        >>> np.testing.assert_array_almost_equal(
        ...     np.round(residual.values, decimals=3),
        ...     np.array([  0.191,   0.426,   3.252, -20.   ]))
        """
        params = _read_input(file_like)
        return cls.from_dict(params)

    @property
    def names(self):
        """"""
        return self._residuals.keys()

    @property
    def values(self):
        """"""
        return [self._residual_values[key] for key in self._residuals.keys()]

    def _distinguish_metric_from_resid(self):
        self._metrics = {}
        for key, info in self._residuals.items():
            func = info["_func"]
            if func in metric_calcs.__dict__:
                self._metrics[key] = info

    def _validate_residuals(self, residuals):
        """"""
        for key in residuals:
            info = residuals[key]
            _validate_func(info, _VALID_FUNCS)
            _validate_fields(self._data_grid, info)
            _validate_fields(self._model_grid, info)

    def add_residuals_from_file(self, file):
        """Add residuals to an ``umami.Residual`` from a file.

        Parameters
        ----------
        file_like : file path or StringIO
            File will be parsed by ``yaml.safe_load`` and converted to an
            ``OrderedDict``.
        """
        params = _read_input(file)
        self.add_residuals_from_dict(params)

    def add_residuals_from_dict(self, params):
        """Add residuals to an ``umami.Residual`` from a dictionary.

        Adding residuals through this method does not overwrite already existing
        residuals. New residuals are appended to the existing residual list.

        Parameters
        ----------
        params : dict or OrderedDict
            Keys are residual names and values are a dictionary describing
            the creation of the residual. It will be convereted to an OrderedDict
            before residuals are added so as to preserve residual order.
        """
        new_residuals = OrderedDict(params)
        self._validate_residuals(new_residuals)
        for key in new_residuals:
            self._residuals[key] = new_residuals[key]
        self._distinguish_metric_from_resid()

        new_metrics = {}
        for name, info in self._metrics.items():
            if name not in self._data_metric._metrics:
                new_metrics[name] = info
        if len(new_metrics) > 0:
            self._data_metric.add_metrics_from_dict(new_metrics)
            self._model_metric.add_metrics_from_dict(new_metrics)

    def calculate_residuals(self):
        """Calculate residual values.

        Calculated residual values are stored in the attribute
        ``Residual.values``.
        """
        self._residual_values = OrderedDict()

        self._model_metric.calculate_metrics()
        self._data_metric.calculate_metrics()

        for key in self._residuals.keys():
            info = deepcopy(self._residuals[key])
            _func = info.pop("_func")

            if key in self._metrics:

                resid = (
                    self._model_metric._metric_values[key]
                    - self._data_metric._metric_values[key]
                )
            else:

                function = residual_calcs.__dict__[_func]
                resid = function(self._model_grid, self._data_grid, **info)

            self._residual_values[key] = resid

    def write_residuals_to_file(self, path, style, decimals=3):
        """Write residuals to a file.

        Parameters
        ----------
        path :
        style : str
            yaml, dakota
        decimals: int
            Number of decimals to round output to.

        Examples
        --------
        >>> import numpy as np
        >>> from io import StringIO
        >>> from landlab import RasterModelGrid
        >>> from umami import Residual

        >>> np.random.seed(42)

        >>> model = RasterModelGrid((10, 10))
        >>> z_model = model.add_zeros("node", "topographic__elevation")
        >>> z_model += model.x_of_node + model.y_of_node

        >>> data = RasterModelGrid((10, 10))
        >>> z_data = data.add_zeros("node", "topographic__elevation")
        >>> z_model += data.x_of_node + data.y_of_node
        >>> z_data[data.core_nodes] += np.random.random(data.core_nodes.shape)


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

        >>> residual = Residual(model, data)
        >>> residual.add_residuals_from_file(file_like)
        >>> residual.calculate_residuals()

        >>> out = StringIO()
        >>> residual.write_residuals_to_file(out, style="dakota", decimals=3)
        >>> out.getvalue()
        '17.533 # me\\n9.909 # ep10\\n9.813 # oid1_mean\\n-41 # sn1'
        >>> out = StringIO()
        >>> residual.write_residuals_to_file(out, style="yaml", decimals=3)
        >>> out.getvalue()
        'me: 17.533\\nep10: 9.909\\noid1_mean: 9.813\\nsn1: -41'
        """
        if style == "dakota":
            stream = "\n".join(
                [
                    str(np.round(val, decimals=decimals)) + " # " + str(key)
                    for key, val in self._residual_values.items()
                ]
            )
        if style == "yaml":
            stream = "\n".join(
                [
                    str(key) + ": " + str(np.round(val, decimals=decimals))
                    for key, val in self._residual_values.items()
                ]
            )

        _write_output(path, stream)