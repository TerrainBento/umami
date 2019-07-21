# #TODO put simple calculations with known answers here.
# import numpy as np
# from landlab import RasterModelGrid
# from landlab.components import FlowAccumulator
# from umami.calculations import joint_density_misfit
# model = RasterModelGrid((10, 10))
# z_model = model.add_zeros("node", "topographic__elevation")
# z_model += model.x_of_node + model.y_of_node
# data = RasterModelGrid((10, 10))
# z_data = data.add_zeros("node", "topographic__elevation")
# z_model += 2 * model.x_of_node + 2 * model.y_of_node
#
# data_fa = FlowAccumulator(data)
# data_fa.run_one_step()
# model_fa = FlowAccumulator(model)
# model_fa.run_one_step()
#
# oint_density_misfit(
#             model,
#             data,
#             "topographic__elevation",
#             "drainage_area",
#             [0, 0.25, 0.5, 0.75, 1.0],
#             [0, 0.2, 0.4, 0.6, 0.8, 1.0]),
#         decimals=3)
