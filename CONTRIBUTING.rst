.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/arnaudblois/pytemplator/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

pytemplator could always use more documentation, whether as part of the
official pytemplator docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/arnaudblois/pytemplator/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Sponsor the project
~~~~~~~~~~~~~~~~~~~

If you or your company would like to contribute to the development of this package,
or simply as a nice thank you, feel free to `buy me a coffee`_


.. _`buy me a coffee`: https://www.buymeacoffee.com/arnaudblois



Get Started!
------------

Ready to contribute? Here's how to set up `pytemplator` for local development.

1. Fork the `pytemplator` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pytemplator.git

3. Install the local package and dependencies using Poetry::

    $ cd pytemplator/
    $ poetry install

4. Activate your shell::

    $ poetry shell

5. Install the pre-commits hooks::

    $ pre-commit install && pre-commit install --hook-type commit-msg

6. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

7. When you're done making changes, check that your changes pass flake8 and the
   tests with `pytest`.


8. Commit your changes and push your branch to GitHub, remember that the commit
name must follow the semantic convention::

    $ git add .
    $ git commit -m "fix: title for commit" -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.



Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).

Be sure everything is pushed and merged to main, then cut a tag corresponding to
the new version. The Github actions will then automatically upload to Pypi
