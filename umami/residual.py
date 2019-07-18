""""""

from .metric import Metric


class Residual(object):
    """"""

    _required_fields = ["topographic__elevation"]
    _required_fields_by_func = {"ks_width_function": "flow__distance"}

    _all_residuals = []

    _simple_difference = []  # those metrics that can take a simple difference.

    def __init__(data, model, metrics=None, **kwargs):
        """"""
        # assert that the model grids have the same x_of_node and y_of_node.
        assert_array_equal(data.grid.x_of_node, model.grid.x_of_node)
        assert_array_equal(data.grid.y_of_node, model.grid.y_of_node)

        # validate

        # calculate 
        self.data = Metric(data)
        self.model = Metric(model, **kwargs)
