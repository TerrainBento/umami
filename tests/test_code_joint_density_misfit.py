import numpy as np
import pytest
from landlab import RasterModelGrid

from umami.calculations import joint_density_misfit


def test_perfect_misfit(category_grid):
    model_grid = RasterModelGrid((6, 6))
    data_grid = category_grid
    data_grid.at_node["f2"] -= data_grid.at_node["f1"]
    _ = model_grid.add_field("node", "f1", np.zeros((6, 6)))
    _ = model_grid.add_field("node", "f2", np.zeros((6, 6)))

    out = joint_density_misfit(
        model_grid,
        data_grid,
        "f1",
        "f2",
        [0, 25, 50, 75, 100],
        [0, 25, 50, 75, 100],
    )

    np.testing.assert_array_equal(out, 1 / 16)
