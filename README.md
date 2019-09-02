[![Documentation Status](https://readthedocs.org/projects/umami/badge/?version=latest)](https://umami.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/TerrainBento/umami.svg?branch=master)](https://travis-ci.org/TerrainBento/umami)
[![Build status](https://ci.appveyor.com/api/projects/status/0ehba569dttgsuyv?svg=true)](https://ci.appveyor.com/project/kbarnhart/umami)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/TerrainBento/umami/master)
[![Coverage Status](https://coveralls.io/repos/github/TerrainBento/umami/badge.svg?branch=master)](https://coveralls.io/github/TerrainBento/umami?branch=master)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/umami/badges/installer/conda.svg)](https://conda.anaconda.org/conda-forge)

# What is it?

Umami calculates topographic metrics for use in assessing model-data fit. To
get a sense of how it is meant to be used, check out the notebooks

# Where to get it

To install the release version of umami (this is probably what you want) we support conda and pip package management.

## Using conda

Open a terminal and execute the following:

```
conda config --add channels conda-forge
conda install umami
```

## Using pip

Open a terminal and execute the following:

```
pip install umami
```

## From source code

The source code is housed on [GitHub](https://github.com/TerrainBento/umami).
To install the umami from source code we recommend creating a conda environment.

```
git clone https://github.com/TerrainBento/umami.git
cd umami
conda env create -f environment-dev.yml
conda activate umami-dev
python setup.py install
```

If you are interested in developing umami, please check out the
[development practices]() page.

# Documentation
Documentation is housed on [ReadTheDocs]().

# License
[MIT](https://github.com/TerrainBento/umami/blob/master/LICENSE)

# Getting help

# Contributing to umami
Contributors and maintainers to this project are are expected to abide the [Contributor Code of Conduct](https://github.com/TerrainBento/umami/blob/master/CODE_OF_CONDUCT.md).


# Citing umami
A Journal of Open Source Software submission is planned. When it is finalized, a link and citation will be found here.
