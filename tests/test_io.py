import pytest
import yaml
from numpy.testing import assert_array_equal

from umami import Metric


@pytest.fixture()
def test_read_file(tmpdir, grid_with_z, input_yaml):
    with tmpdir.as_cwd():
        with open("params.yml", "w") as fp:
            fp.write(input_yaml)
        metric = Metric(grid_with_z)
        metric.add_metrics_from_file("params.yml")
        metric.calculate_metrics()
        assert_array_equal(
            list(metric.names), ["me", "ep10", "oid1_mean", "sn1"]
        )
        assert_array_equal(metric.values, [9.0, 5.0, 5.0, 8])
    return metric


def test_write_file(tmpdir, test_read_file):
    metric = test_read_file
    fout = "output.txt"
    with tmpdir.as_cwd():
        metric.write_metrics_to_file(fout, style="yaml")

        with open(fout, "r") as f:
            out = yaml.safe_load(f)

    correct = {"me": 9.0, "ep10": 5.0, "oid1_mean": 5.0, "sn1": 8}

    for key, val in correct.items():
        assert key in out
        assert out[key] == val
