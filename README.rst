===========
Pytemplator
===========


.. image:: https://img.shields.io/pypi/v/pytemplator.svg
        :target: https://pypi.python.org/pypi/pytemplator


.. image:: https://pyup.io/repos/github/arnaudblois/pytemplator/shield.svg
     :target: https://pyup.io/repos/github/arnaudblois/pytemplator/
     :alt: Updates



Pytemplator aims to streamline the creation of dynamic templates.
It supports the format from `CookieCutter package`_ but also offers the option
to generate the context using Python, which in practice provides a better user
experience and more flexibility.


* Free software: Apache Software License 2.0
* Documentation: https://arnaudblois.github.io/pytemplator/.

How to use
----------

- Install the package `pytemplator` using pip or poetry.
-


For template developers
-----------------------

See `example`_

.. _`example`: https://github.com/arnaudblois/pypi-package-template


A typical Pytemplator template project can live either as a local directory or as a Git repo.
It relies on three elements:
- a `templates` folder where all folders and files to be templated should be placed
- an `initialize.py` at the root level with a function "generate_context". More details below.
- a `finalize.py` which is run after


Contributing
------------


Credits
-------

This package is inspired from the excellent `CookieCutter package`_ and `audreyr/cookiecutter-pypackage`_ project template.


.. _`CookieCutter package`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
