import pytest

from umami import Residual


def test_no_required_field(grid):
    with pytest.raises(ValueError):
        Residual(grid, grid)
