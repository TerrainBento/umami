# Getting Help

Use the [Issues Page]() to ask questions and get help. Please search open and closed issues to identify if a question has already been asked. We welcome all questions.


# Installation instructions

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
conda env create -f environment-dev.yml
conda activate umami-dev
python setup.py install
```

#### A note to developers

If you plan to develop with umami, please fork umami, clone the forked repository, and replace `python setup.py install` with `python setup.py develop`. We recommend developing new features on a development branch.


# How to cite

This repository will be submitted to JOSS.
