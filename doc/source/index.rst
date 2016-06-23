photon
======

A data driven tool to deploy fusion.

Usage
-----

Display upgrade steps of entity ``foo`` az ``bar``

.. code-block:: bash

	$ photon --az foo/bar --action upgrade

Display upgrade steps of entity ``foo`` az ``bar`` on the controllers

.. code-block:: bash

	$ photon --az foo/bar --action upgrade --target 'mcp'

Display upgrade steps of entity ``foo`` az ``bar`` on mcp1

.. code-block:: bash

	$ photon --az foo/bar --action upgrade --target 'mcp[0]'

Display restart steps of entity ``foo`` az ``bar``

.. code-block:: bash

	$ photon --az foo/bar --action restart

Perform the action(s) to be executed

Decided to pipe the commands into a shell, instead of implementing a
a streaming stdout subprocess iterator.

.. code-block:: bash

	$ photon --az $az --action $action 2>/dev/null | sh

Testing
-------

Requirements:

* Tox

Execute unit tests:

.. code-block:: bash

	$ tox

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
