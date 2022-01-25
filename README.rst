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
- In a shell::

  $ pytemplate <target>

Where `<target>` can be either a local path to the directory of a Pytemplator template
or the url to a git repo.

There are options to specify which branch should be used for templating,
the output directory and the config directory. More details can be obtained with::

  $ pytemplate --help



For template developers
-----------------------

See this `example`_ to get an idea of an actual pytemplator template.

.. _`example`: https://github.com/arnaudblois/pypi-package-template


A typical Pytemplator template project can live either as a local directory or as a Git repo.
It relies on three elements:
- a `templates` folder where all folders and files to be templated should be placed.
Under the hood, pytemplator relies on jinja2.
- an `initialize.py` at the root level with a function "generate_context". More details below.
- a `finalize.py` which is run after the templating.



Contributing
------------

All help is much appreciated and credit is always given.
Please consult CONTRIBUTING.rst for details on how to assist me.


Credits
-------

This package is inspired from the excellent `CookieCutter package`_ and `audreyr/cookiecutter-pypackage`_ project template.


.. _`CookieCutter package`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
