import numpy as np
import pytest

from umami.calculations.metric.aggregate import _aggregate


def test_return_not_a_scalar():
    vals = np.random.randn(3, 4)
    with pytest.raises(ValueError):
        _aggregate(vals, "mean", axis=0)
