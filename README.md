[![Documentation Status](https://readthedocs.org/projects/umami/badge/?version=latest)](https://umami.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/TerrainBento/umami.svg?branch=master)](https://travis-ci.org/TerrainBento/umami)
[![Build status](https://ci.appveyor.com/api/projects/status/0ehba569dttgsuyv?svg=true)](https://ci.appveyor.com/project/kbarnhart/umami)
[![Coverage Status](https://coveralls.io/repos/github/TerrainBento/umami/badge.svg?branch=master)](https://coveralls.io/github/TerrainBento/umami?branch=master)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/umami/badges/installer/conda.svg)](https://conda.anaconda.org/conda-forge)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TerrainBento/umami/master?filepath=notebooks%2FWelcome.ipynb)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.01776/status.svg)](https://doi.org/10.21105/joss.01776)


# What is it?

Umami is a package for calculating objective functions or objective function
components for Earth surface dynamics modeling. It was designed to work well
with
[terrainbento](https://github.com/TerrainBento/terrainbento) and other models built with the
[Landlab Toolkit](https://github.com/landlab/landlab). Examples can be
found in the `notebooks` directory (or on Binder
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TerrainBento/umami/master?filepath=notebooks%2FWelcome.ipynb)
).

Umami offers two primary classes:
* a [`Residual`](https://umami.readthedocs.io/en/latest/umami.residual.html#Residual),
which represents the difference between model and data, and
* a [`Metric`](https://umami.readthedocs.io/en/latest/umami.metric.html),
which is a calculated value on either model or data.

The set of currently supported calculations are found in the [`umami.calculations`](https://umami.readthedocs.io/en/latest/umami.calculations.html) submodule.

# What does it do well?

Umami was designed to provide an input-file based interface for calculating
single-value landscape metrics for use in model analysis. This supports
reproducible analysis and systematic variation in metric construction. When
used with `terrainbento` one input file can describe the model run, and one
input file can describe the model assessment or model-data comparison. This
streamlines model analysis applications. Umami also provides multiple output
formats (YAML and Dakota), the latter of which is designed to interface with
Sandia National Laboratory's [Dakota package](https://dakota.sandia.gov).

To get a sense of how it is meant to be used, check out the
[notebooks on Binder](https://mybinder.org/v2/gh/TerrainBento/umami/master?filepath=notebooks%2FWelcome.ipynb)
and the [API documentation](https://umami.readthedocs.io/en/latest/).

# Where to get it

To install the release version of umami (this is probably what you want) we
support [conda](https://anaconda.org/conda-forge/umami) and
[pip](https://pypi.org/project/umami/) package management.

## Using conda

Open a terminal and execute the following:

```
$ conda config --add channels conda-forge
$ conda install umami
```

## Using pip

Open a terminal and execute the following:

```
$ pip install umami
```

## From source code

The source code is housed on [GitHub](https://github.com/TerrainBento/umami).
To install the umami from source code we recommend creating a conda environment.

```
$ git clone https://github.com/TerrainBento/umami.git
$ cd umami
$ conda env create -f environment-dev.yml
$ conda activate umami-dev
$ python setup.py install
```

If you are interested in developing umami, please check out the
[development practices](https://umami.readthedocs.io/en/latest/development_practices.html)
page.

# Read the documentation

Documentation is housed on [ReadTheDocs](https://umami.readthedocs.io).

# License

[MIT](https://github.com/TerrainBento/umami/blob/master/LICENSE)

# Report issues and get help

Umami uses Github Issue as a single point of contact for users and developers.
To ask a question, report a bug, make a feature request, or to get in touch for
any reason, please make [an Issue](https://github.com/TerrainBento/umami/issues).

# Contribute to umami

All contributions are welcome and appreciated. Feel free to:

- Make [an issue](https://github.com/TerrainBento/umami/issues) to ask a
  question. Your question will help others in the future.
- Make [an issue](https://github.com/TerrainBento/umami/issues) to report a
  bug or a potential improvement. We will work to fix it. If you have an idea
  about how to fix it, please feel free to propose it, or make a Pull Request.  
- [Fork the repository](https://help.github.com/en/articles/fork-a-repo), make
  changes to the source code on a
  [development branch](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow),
  and submit a Pull Request to have your changes brought into the umami
  repository. **No contribution to the code base or documentation is too small.**

Contributors and maintainers to this project are are expected to abide the [Contributor Code of Conduct](https://github.com/TerrainBento/umami/blob/master/CODE_OF_CONDUCT.md).

# Cite umami
[![DOI](https://joss.theoj.org/papers/10.21105/joss.01776/status.svg)](https://doi.org/10.21105/joss.01776)

Umami is described by a Journal of Open Source Software paper. If you use umami in your research, please cite it. 
