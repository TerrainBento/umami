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
