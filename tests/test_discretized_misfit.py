from collections import OrderedDict

import numpy as np
import pytest

from landlab import RasterModelGrid
from umami.calculations import discretized_misfit
from umami.calculations.residual.discretized_misfit import _get_category_labels


def test_correct_category_labels(category_grid):
    category = _get_category_labels(
        category_grid, "f1", "f2", [0, 25, 50, 75, 100], [0, 25, 50, 75, 100]
    )

    correct = np.zeros((6, 6))
    correct[1:-1, 1:-1] = np.arange(1, 17).reshape((4, 4))

    np.testing.assert_array_equal(category, correct.flatten())


def test_no_misfit(category_grid):
    model_grid = RasterModelGrid((6, 6))
    data_grid = category_grid

    vals = np.arange(36)
    _ = model_grid.add_field("node", "misfit_field", vals)
    _ = data_grid.add_field("node", "misfit_field", vals)

    out = discretized_misfit(
        model_grid,
        data_grid,
        "misfit_field",
        "f1",
        "f2",
        [0, 25, 50, 75, 100],
        [0, 25, 50, 75, 100],
    )

    assert isinstance(out, OrderedDict) == True
    assert len(out) == 16
    for key in out:
        np.testing.assert_array_equal(out[key], 0.0)


def test_known_misfit(category_grid):
    model_grid = RasterModelGrid((6, 6))
    data_grid = category_grid

    vals = np.arange(36)
    _ = model_grid.add_field("node", "misfit_field", vals)
    _ = data_grid.add_field("node", "misfit_field", 2.0 * vals)

    out = discretized_misfit(
        model_grid,
        data_grid,
        "misfit_field",
        "f1",
        "f2",
        [0, 25, 50, 75, 100],
        [0, 25, 50, 75, 100],
    )

    core_vals = (vals.reshape((6, 6))[1:-1, 1:-1]).flatten()
    assert isinstance(out, OrderedDict) == True
    assert len(out) == 16
    for key in out:
        np.testing.assert_array_equal(out[key], core_vals[key - 1])
