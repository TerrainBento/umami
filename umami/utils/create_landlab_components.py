from landlab.components import ChiFinder, FlowAccumulator


def _create_landlab_components(
    grid, chi_finder_kwds=None, flow_accumulator_kwds=None
):

    # run FlowAccumulator
    kwds = flow_accumulator_kwds or {}
    fa = FlowAccumulator(grid, **kwds)
    fa.run_one_step()

    # Run ChiFinder
    kwds = chi_finder_kwds or {}
    cf = ChiFinder(grid, **kwds)
    cf.calculate_chi()

    return fa, cf
