
Welcome to the Umami documentation!
===================================

Introduction and Purpose
------------------------
Umami is a package for calculating objective functions or objective function
components for landscape evolution modeling. TODO: add more purpose here.

Umami offers two primary classes a :py:class:`Residual` which represents the
difference between model and data, and :py:class:`Metric` which is a calculated
value on either model or data. A set of currently supported calculations are
found in the :py:mod:`umami.calculations` submodule.

Umami is built on top of the `Landlab Toolkit`_ and designed to work well with
`terrainbento`_. The source code is housed on `GitHub`_.

.. _Landlab Toolkit: https://landlab.github.io
.. _terrainbento: https://terrainbento.readthedocs.io/en/latest/
.. _GitHub: https://github.com/TerrainBento/umami

Getting Started
---------------

.. toctree::
    :maxdepth: 1

    umami.getting_started

Get Help
--------
TODO

Installation Instructions
-------------------------
TODO

Contributing
------------
TODO

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
