---
title: 'umami: A Python package for Earth surface dynamics objective function construction'
tags:
  - Python
  - landscape evolution
  - geomorphology
  - hydrology
  - surface processes
  - calibration
  - validation
  - model analysis
  - model-data comparison
  - objective function
authors:
  - name: Katherine R. Barnhart
    orcid: 0000-0001-5682-455X
    affiliation: 1, 2
  - name: Eric Hutton
    orcid: 0000-0002-5864-6459
    affiliation: 3, 4
  - name: Gregory E. Tucker
    orcid: 0000-0003-0364-5800
    affiliation: 1, 2, 3
affiliations:
  - name: University of Colorado at Boulder, Department of Geological Sciences
    index: 1
  - name: University of Colorado at Boulder, Cooperative Institute for Research in Environmental Sciences
    index: 2
  - name: University of Colorado at Boulder, Community Surface Dynamics Modeling System Integration Facility
    index: 3
  - name: University of Colorado at Boulder, Institute for Arctic and Alpine Research
    index: 4
date: 4 September 2019
bibliography: paper.bib
---

# Summary

Models of Earth's surface dynamics are typically designed to simulate timescales that range from years to geologic epochs ($10^6$+ years). They represent and evolve a primary state variable, Earth's surface. Some applications may use other state variables (e.g., soil thickness). A diverse array of physical and chemical processes may be present. For example, the making and moving of water; the creation of soil and sediment from bedrock; the transport of mobile material due to hillslope processes, river erosion, and landslides; and the deposition of that material into the geologic archive. These models are used for applications as diverse as understanding the limit to the hight of mountain ranges and predicting the erosion, transport, and fate of contaminated material on human timescales.

A diversity of data is used to compare models with observations. These data serve as "simulated equivalents", quantities with which to assess model performance. A common observable compared with model output is topography. High resolution topography, occasionally at two points in time, provides a dataset rich in the spatial dimension and sparse in the temporal. However, because model initial condition topography is not often known, we do not often expect modeled and observed topography to line up exactly. Thus, statistical derivatives of topography are often used. Other data sources (e.g., cosmogenic radionuclide derived erosion rates) provide time and space integrated measures.

There is, however, no clear consensus regarding which set of simulated equivalents is most appropriate or most sucessful for assessing the performance of Earth surface dynamics models. This presents a challenge when this type of model is used in formal model analysis efforts. For example, calibration requires a formal objective function. Under these circumstances, there is a need for generic tools that facilitate exploration and usage of many plausibly successful simulated equivalents. This is the need that the umami package was designed to address.

# Description of umami

Umami is a package for calculating objective functions or objective function components for Earth surface dynamics modeling. It was designed to work well with models built with the Landlab Toolkit [@hobley2017creative] or with the `terrainbento` multi-model analysis [@barnhart2019terrain]. Umami is complementary to existing topographic analysis tools such as LSDTopoTools [@mudd2014statistical; @club2017geomorphometric], TopoToolbox [@schwanghart2010topo; @schwanghart2014topo] and the Topographic Analysis Kit [@forte2019tak]. Rather than performing topographic analysis, umami is used to distill model output into a form usable by model analysis methods such as sensitivity analysis, calibration, and validation.  

Umami offers two primary classes: a [`Residual`](https://umami.readthedocs.io/en/latest/umami.residual.html#Residual)
which represents the difference between model and data, and a [`Metric`](https://umami.readthedocs.io/en/latest/umami.metric.html)
which is a calculated value on either model or data. The set of currently supported calculations are found in the [`umami.calculations`](https://umami.readthedocs.io/en/latest/umami.calculations.html) submodule. Both the `Metric` and `Residual` classes are designed to be fully specified through a YAML-style input-file or python Dictionary interface. Many different calculations can be accomplished through parameter specification. This supports reproducible analysis and systematic variation in metric construction. For example, when used with `terrainbento` one input file can describe the model run, and one input file can describe the model assessment or model-data comparison. This streamlines model analysis applications by making driver files more re-usable and by placing the code that accomplished calculations in the umami package rather than within the driver file. Umami also provides multiple output formats (YAML and Dakota), the latter of which is designed to interface with Sandia National Laboratory's Dakota package [@adams2019dakota].

The novel contribution of the umami package is not primarily found in the specific calculations accomplished (e.g., some of them are as straightforward as the mean of a state variable). Instead it is the flexible and extensible nature of the input file format and the `Metric` and `Residual` classes. Additionally, the package can be extended through the addition of new calculation methods.

Two model-data comparison metrics in umami are novel. First, the `joint_density_misfit` provides a misfit metric of the joint density of two state variables. This comparison measure was inspired by the use of channel $\chi$ index value [@perron2013integral] and topographic elevation to assess river channel long profiles ($\chi$-z plots). While it is not clear how to best quantify the difference between a modeled and observed $\chi$-z plot, it is straightforward to calculate the sum of squared residuals between the joint density of $\chi$ and topographic elevation for a modeled and observed landscape. In umami, this comparison is generalized to the joint density of two state variables.

Second, the `discretized_misfit` calculation seeks to reduce the dimension of a state variable misfit. In some applications it is appropriate to make a direct comparison between a measured and modeled state variable (e.g., difference measured and modeled topography). However, if an application uses a model domain with tens of thousands of grid cells a user is faced with a challenging choice: either treat each residual as an individual observation or reduce all residuals to a single value through a sum of squared residuals (or other norm). The `discretized_misfit` calculation permits the identification of consistent "categories" of grid cells based on other grid fields. A sum of squared residuals is then calculated within each of these categories.

# Acknowledgements

Support for this work was provided by an NSF EAR  Postdoctoral Fellowship to Barnhart (NSF Award Number 1725774). Funding for Landlab was provided by NSF (NSF Award Numbers 1147454 and 1450409). Landlab is additionally supported by the Community Surface Dynamics Modeling System (NSF Award Number 1226297 and 1831623).

# References
