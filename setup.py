#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

from src.pytemplator import __version__

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = [
    'jinja2', 'loguru',
]
SETUP_REQUIREMENTS = ['pytest-runner', 'wheel']
TEST_REQUIREMENTS = ['pytest>=3', ]

setup(
    author="Arnaud Blois",
    author_email='a.blois@ucl.ac.uk',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description=(
        'Pytemplator aims to streamline the creation of dynamic templates. It '
        'is inspired from the excellent cookiecutter package but offers more '
        'customization.'
    ),
    entry_points={
        'console_scripts': [
            'pytemplate=pytemplator.cli:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license="Apache Software License 2.0",
    long_description=README + '\n\n' + HISTORY,
    include_package_data=True,
    keywords='pytemplator',
    name='pytemplator',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    url='https://github.com/arnaudblois/pytemplator',
    version=__version__,
    zip_safe=False,
)
