import pytest

from umami import Metric


def test_no_required_field(grid):
    with pytest.raises(ValueError):
        Metric(grid)


def test_metric_specific_field_absent(grid_with_z):
    metrics = {"ag": {"_func": "aggregate", "field": "spam", "method": "mean"}}
    with pytest.raises(ValueError):
        Metric(grid_with_z, metrics=metrics)


def test_func_not_in_info(grid_with_z):
    metrics = {"ce": {"spam": "eggs"}}
    with pytest.raises(ValueError):
        Metric(grid_with_z, metrics=metrics)


def test_bad_func_in_info(grid_with_z):
    metrics = {"ce": {"_func": "eggs"}}
    with pytest.raises(ValueError):
        Metric(grid_with_z, metrics=metrics)
