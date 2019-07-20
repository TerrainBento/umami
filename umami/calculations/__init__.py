"""All of this will be expanded through development here and where more appropriate in Landlab.
 Width function,
 hack exponents.

 """

from .metric import (
    aggregate,
    chi_gradient,
    chi_intercept,
    count_equal,
    hypsometric_integral,
    watershed_aggregation,
)
from .residual import (
    discretized_misfit,
    joint_density_misfit,
    kstest,
    kstest_watershed,
)

__all__ = [
    "aggregate",
    "chi_intercept",
    "chi_gradient",
    "count_equal",
    "hypsometric_integral",
    "watershed_aggregation",
    "discretized_misfit",
    "joint_density_misfit",
    "kstest",
    "kstest_watershed",
]
