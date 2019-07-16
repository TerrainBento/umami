"""
"""


def chi_intercept(chi_finder):
    """"""
    slp, incp = chi_finder.best_fit_chi_elevation_gradient_and_intercept()
    return incp


def chi_gradient(self):
    """"""
    slp, incp = chi_finder.best_fit_chi_elevation_gradient_and_intercept()
    return slp
