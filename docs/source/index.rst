
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

Check out the example notebooks `housed on Binder`_ to get a sense of how umami
can be used.

.. _housed on Binder: https://mybinder.org/v2/gh/TerrainBento/umami/master?filepath=notebooks%2FWelcome.ipynb

Get Help
--------

To get help or ask questions, please `make an issue on GitHub`_.

.. _make an issue on GitHub: https://github.com/TerrainBento/umami/issues

Installation Instructions
-------------------------

Installation is described on `GitHub`_.

.. _GitHub: https://github.com/TerrainBento/umami#where-to-get-it

Contributing
------------

All contributions are welcome. Please read the
:ref:`development practices <development_practices>` page for more information.

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
