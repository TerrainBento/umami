import pytest

from umami.calculations.metric.chi_intercept_gradient import (
    _validate_chi_finder,
)


def test_bad_input():
    with pytest.raises(ValueError):
        _validate_chi_finder("spam")
