
Welcome to the Umami documentation!
===================================

Introduction and Purpose
------------------------

Umami is a package for calculating objective functions or objective function
components for landscape evolution modeling. It was designed to work well with
`terrainbento`_ and other models built with the `Landlab Toolkit`_. Examples
can be found in the notebooks on Binder (or in the ``notebooks`` directory).

Umami offers two primary classes: a :py:class:`Residual`,
which represents the difference between model and data, and a
:py:class:`Metric`,
which is a calculated value on either model or data. The set of currently
supported calculations can be found in the
:py:mod:`umami.calculations`
submodule.

Umami was designed to provide an input-file based interface for calculating
single-value landscape metrics for use in model analysis. This supports
reproducible analysis and systematic variation in metric construction. When
used with ``terrainbento``, one input file can describe the model run, and
another input file can describe the model assessment or model-data comparison.
This streamlines model analysis applications. Umami also provides multiple
output formats (YAML and Dakota), the latter of which is designed to interface
with Sandia National Laboratory's `Dakota package`_.

The source code is housed on `GitHub`_.

.. _Landlab Toolkit: https://landlab.github.io
.. _terrainbento: https://terrainbento.readthedocs.io/en/latest/
.. _GitHub: https://github.com/TerrainBento/umami
.. _Dakota package: https://dakota.sandia.gov

Getting Started
---------------

Check out the example notebooks `housed on Binder`_ to get a sense of how umami
can be used.

.. _housed on Binder: https://mybinder.org/v2/gh/TerrainBento/umami/master?filepath=notebooks%2FWelcome.ipynb

Get Help
--------

To get help or ask questions, please make an `issue on GitHub`_.

.. _issue on GitHub: https://github.com/TerrainBento/umami/issues

Installation Instructions
-------------------------

Installation is described on `this`_ section of the README.

.. _this: https://github.com/TerrainBento/umami#where-to-get-it

Contributing
------------

All contributions are welcome. Make an `issue on GitHub`_ to file a bug report.

If you are planning to contribute to the source code, please read the following
page for more information.

.. toctree::
    :maxdepth: 1

    development_practices

API Documentation
-----------------

.. toctree::
    :maxdepth: 1

    umami.residual
    umami.metric

.. toctree::
    :maxdepth: 1

    umami.calculations

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
