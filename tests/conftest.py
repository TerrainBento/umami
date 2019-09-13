import numpy as np
import pytest
from landlab import RasterModelGrid


@pytest.fixture()
def grid():
    grid = RasterModelGrid((10, 10))
    return grid


@pytest.fixture()
def grid_with_z(grid):
    z = grid.add_zeros("node", "topographic__elevation")
    z += grid.x_of_node + grid.y_of_node
    return grid


@pytest.fixture()
def input_yaml():
    file_like = """
    me:
      _func: aggregate
      method: mean
      field: topographic__elevation
    ep10:
      _func: aggregate
      method: percentile
      field: topographic__elevation
      q: 10
    oid1_mean:
      _func: watershed_aggregation
      field: topographic__elevation
      method: mean
      outlet_id: 1
    sn1:
      _func: count_equal
      field: drainage_area
      value: 1
    """
    return file_like


@pytest.fixture()
def category_grid():
    grid = RasterModelGrid((6, 6))
    f1 = np.vstack(
        (
            1 * np.ones((2, 6)),
            2 * np.ones((1, 6)),
            3 * np.ones((1, 6)),
            4 * np.ones((2, 6)),
        )
    )

    f2 = f1 + np.hstack(
        (
            1 * np.ones((6, 2)),
            2 * np.ones((6, 1)),
            3 * np.ones((6, 1)),
            4 * np.ones((6, 2)),
        )
    )
    _ = grid.add_field("node", "f1", f1)
    _ = grid.add_field("node", "f2", f2)
    return grid
