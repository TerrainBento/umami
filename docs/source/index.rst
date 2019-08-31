
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
`terrainbento`_.

TODO: put a link to the source code here. 

.. _Landlab Toolkit: https://landlab.github.io
.. _terrainbento: https://terrainbento.readthedocs.io/en/latest/

Organization of Software
------------------------
.. toctree::
    :maxdepth: 1

    umami.residual
    umami.metric

.. toctree::
    :maxdepth: 1

    umami.calculations

Example Usage
-------------

.. toctree::
    :maxdepth: 1

    umami.example_usage

Get Help
--------
TODO


Installation Instructions
-------------------------
TODO

Contributing
------------
TODO

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
