from landlab.components import ChiFinder, FlowAccumulator
from landlab.utils.flow__distance import calculate_flow__distance


def _create_landlab_components(
    grid, chi_finder_kwds=None, flow_accumulator_kwds=None
):
    # run FlowAccumulator
    kwds = flow_accumulator_kwds or {}
    fa = FlowAccumulator(grid, **kwds)
    fa.run_one_step()

    # Run ChiFinder
    kwds = chi_finder_kwds or {}
    cf = ChiFinder(grid, noclobber=False, **kwds)
    cf.calculate_chi()

    # run distance upstream.
    _ = calculate_flow__distance(grid, add_to_grid=True, noclobber=False)

    return fa, cf
