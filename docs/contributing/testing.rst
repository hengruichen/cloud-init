.. _testing:

=================
Testing
=================

Cloud-init uses `Tox`_ to run tests against multiple Python
versions and platforms. To run the tests, use the following
command:

.. code-block:: bash

    tox

Tox will create a virtual environment for each Python version and
platform, and then run the tests in that environment. The results of
the tests will be displayed in the terminal.

To run the tests for a specific Python version or platform, use the
following command:

.. code-block:: bash

    tox -e <environment>

Where `<environment>` is the name of the environment you want to run
the tests in. For example, to run the tests for Python 3.10 on Ubuntu
22.04, use the following command:

.. code-block:: bash

    tox -e py310-ubuntu-22.04

Tox will create a virtual environment for the specified Python
version and platform, and then run the tests in that environment.

Tox will also create a `coverage report`_ for the tests. The
coverage report will be displayed in the terminal and will be saved
to the `coverage.xml`_ file.

.. _Tox: https://tox.wiki/en/latest/
.. _coverage report:***REDACTED***@lists.canonical.com>`_.

