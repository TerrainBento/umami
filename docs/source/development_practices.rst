.. _development_practices:

Development Practices
=====================

All contributions to umami are welcome. If you are considering developing with
umami, we recommend you read this page. All developers and maintainers are
expecte to abide by the `Code of Conduct`_.

.. _Code of Conduct: https://github.com/TerrainBento/umami/blob/master/CODE_OF_CONDUCT.md

Contribution Guidelines
-----------------------

To contribute to umami, please fork the repository and make modifications on a
development branch. If you have any questions about how to get started,
`make an issue on GitHub`_.

Umami strives for a meaningful 100% code coverage through docstring and unit
tests, adherence to `PEP8`_, low lint levels using `Flake8`_, and
`Black style`_. Many of these standards are enforced by continuous integration
tests and the development team will help you bring contributions into
compliance.

.. _make an issue on GitHub: https://github.com/TerrainBento/umami/issues
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _Black style: https://black.readthedocs.io/en/stable/
.. _Flake8: http://flake8.pycqa.org/en/latest/#

Developer Install instructions
------------------------------

After forking the repository, install using a conda environment.::

    git clone https://github.com/<your user name>/umami.git
    cd umami
    conda env create -f environment-dev.yml
    conda activate umami-dev
    python setup.py develop

You will need to run ``conda activate umami-dev`` each time you start a new
terminal session.

When using this conda environment, you will have all of the tools you need to
format files and run the tests.

Unit and Docstring Tests
------------------------

Umami uses `pytest`_ to discover and run tests of the codebase. We have two
types of tests that serve two complimentary purposes. Docstring tests are
examples within the code that provide context in the API documentation. Unit
tests live in in the ``test`` folder and provide additional tests that are
extraneous to the API documentation but important for ensuring that umami is
fully tested. The tests use small examples so that known answers can be used.

.. _pytest: https://pytest.org/en/latest/

To run the tests, navigate to the top level ``umami`` directory and run::

  pytest

You can also assess how well the tests cover the code base.::

  pytest umami tests/ --doctest-modules --cov=umami --cov-report term-missing -vvv

Convenience Functions
---------------------

There are a few convienience commands available through the Makefile to assist
with formatting and checking for lint. From the top level of the umami source
code directory you can type ``make pretty`` to format all the files. You can
type ``make lint`` to check for lint. Finally, the command ``make docs`` will
make the docs with `sphinx`_ and open the local copy in a web browser.

.. _sphinx: https://www.sphinx-doc.org/en/master/
