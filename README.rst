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

Example
~~~~~~~

See this `project example`_ to get an idea of an actual pytemplator template.

.. _`project example`: https://github.com/arnaudblois/pypi-package-template

General idea
~~~~~~~~~~~~

A typical Pytemplator template project can live either as a local directory or as a Git repo.
It relies on three elements:
- a `templates` folder where all folders and files to be templated should be placed.
Under the hood, pytemplator relies on jinja2.
- an `initialize.py` at the root level with a function "generate_context". More details below.
- a `finalize.py` whose `finalize` function is run after the templating.


The `generate_context` function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `generate_context` function should return a dictionary mapping the variables in the
template to their values. The idea is to use the extra flexibility to offer sensible default
values to make the user experience smoother.

`generate_context` must accept `no_input` as argument. This tells what should happen in purely
programmatic environment. It is up to you how you'd like to address this, you can provide default values
if this makes sense and choose not to handle it, in which case a NoInputOptionNotHandledByTemplateError
will be raised.

There are several utility classes to help, `Context` and `Question`.

The following code illustrates how they can be used::

  import datetime

  from pytemplator.utils import Question as Q, Context

  def generate_context(no_input, *args, **kwargs):
      """Generate context."""

      context = Context()

      context.questions = [
          Q("pypi_name", ask="Name of the package on Pypi"),
          Q("module_name", ask=False, default=lambda: context["pypi_name"].replace("-","_").lower()),
          Q("year", default=date.today().year, ask=False),
      ]
      context.resolve(no_input)
      return context.as_dict()

A `Question` takes several arguments:
- the key that will be put in the context, required.
- `ask` is the prompt displayed to the user, a default inferred from the key is
displayed if this is left to None. Set this to False to take the default without
asking the user.
- `default` is the value by default. This can be either a value or a callable.
The latter allows for lazy evaluation, especially useful to look into the context
to use answers from previous questions.
- `no_input_default` is the value used when `no_input` is True. If None, `default`
is used.


Contributing
------------

All help is much appreciated and credit is always given.
Please consult CONTRIBUTING.rst for details on how to assist me.


Credits
-------

This package is inspired from the excellent `CookieCutter package`_ and `audreyr/cookiecutter-pypackage`_ project template.


.. _`CookieCutter package`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
