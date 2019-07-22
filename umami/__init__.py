from ._version import get_versions
from .metric import Metric
from .residual import Residual

__all__ = ["Metric", "Residual"]

__version__ = get_versions()["version"]
del get_versions
