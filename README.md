[![Documentation Status](https://readthedocs.org/projects/umami/badge/?version=latest)](https://umami.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/TerrainBento/umami.svg?branch=master)](https://travis-ci.org/TerrainBento/umami)
[![Build status](https://ci.appveyor.com/api/projects/status/0ehba569dttgsuyv?svg=true)](https://ci.appveyor.com/project/kbarnhart/umami)


# Umami

Umami calculates topographic metrics for use in assessing model-data fit.

It is presently under construction.

There will eventually be a binder link here to some notebooks that provide introductory examples.

# Getting Help

Use the [Issues Page]() to ask questions and get help. Please search open and closed issues to identify if a question has already been asked. We welcome all questions.

# Contributing

User contributions are welcome pull requests on a development branch. Umami strives for a meaningful 100% code coverage, adherence to [PEP8](), low lint levels using [Flake8](), and [Black style](). Many of these standards are enforced by continuous integration tests and the development team will help you bring contributions into compliance. Please see the [Development Practices]() page for more information.

# Installation instructions

**WARNING: conda and pip distributions are not presently active**
Before installing umami you will need a python distribution. We recommend that you use the [Anaconda python distribution](https://www.anaconda.com/download/). Unless you have a specific reason to want Python 2.7 we strongly suggest that you install Python 3.7 (or the current 3.* version provided by Anaconda).

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

To install the umami source code version of umami we recommend creating a conda environment for umami.

```
git clone https://github.com/TerrainBento/umami.git
cd umami
cconda env create -f environment-dev.yml
conda activate umami-dev
python setup.py install
```

#### A note to developers

If you plan to develop with umami, please fork umami, clone the forked repository, and replace `python setup.py install` with `python setup.py develop`. We recommend developing new features on a development branch.


# How to cite

This repository will be submitted to JOSS.
