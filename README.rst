========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/mfs/badge/?style=flat
    :target: https://readthedocs.org/projects/mfs
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/miroag/mfs.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/miroag/mfs

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/miroag/mfs?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/miroag/mfs

.. |requires| image:: https://requires.io/github/miroag/mfs/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/miroag/mfs/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/miroag/mfs/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/miroag/mfs

.. |version| image:: https://img.shields.io/pypi/v/mfs.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/mfs

.. |commits-since| image:: https://img.shields.io/github/commits-since/miroag/mfs/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/miroag/mfs/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mfs.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/mfs

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mfs.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/mfs

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mfs.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/mfs


.. end-badges

mfs is a set of utilities to ease image download from some Russian modelling forums

* Free software: MIT license

Installation
============

::

    pip install mfs

Documentation
=============

https://mfs.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
