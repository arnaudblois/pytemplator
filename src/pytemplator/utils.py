"""Utility functions for the Templator."""

from collections import OrderedDict
from contextlib import contextmanager
import importlib
import json
import os
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger

from pytemplator.constants import YES_SET
from pytemplator.exceptions import UserCancellationError


@contextmanager
def cd(new_dir):  # pylint: disable=invalid-name
    """Cd into the directory.

    Used as context manager to avoid side-effects if
    something goes wrong.
    See SO #24176022
    """
    previous_dir = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(previous_dir)


def is_yes(reply):
    """Handle human-readable replies."""
    return reply.lower() in YES_SET


def import_module_from_path(path):
    """Import and execute a module in a safer way.

    Recipe taken from importlib doc at
    https://docs.python.org/3/library/importlib.html
    """
    path = Path(path).resolve(strict=True)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generate_context_from_json(json_file, context):
    """Generate the context from a json file.

    Same behavior as cookiecutter.
    """
    with open(json_file) as file:
        questions = json.load(file, object_pairs_hook=OrderedDict)
    for key, value in questions.items():
        question = key.replace('-', ' ').replace('_', ' ')
        default_value = Template(str(value)).render(context)
        answer = input(f'{question} [{default_value}] ') or default_value
        context['pytemplator'][key] = context['cookiecutter'][key] = context[key] = answer
    print('context', context)
    return context


def check_if_new_dirs_can_be_created(directories, context, destination_dir):
    """Check if any of the templated directories already exist.

    If so, offer the user to overwrite them.
    """
    existing_target_dirs = []
    for directory in directories:
        new_dir_name = Template(directory.name).render(context)
        new_dir_path = destination_dir / new_dir_name
        if new_dir_path.exists():
            existing_target_dirs.append(new_dir_path)
    if not existing_target_dirs:
        return True
    logger.warning('\nThe following directories already exist:\n\t{}'.format(
        '\n\t'.join(str(dir) for dir in existing_target_dirs)
    ))
    overwrite = input('Overwrite those directories y/[N] ') or False
    if is_yes(overwrite):
        for directory in existing_target_dirs:
            shutil.rmtree(directory)
        return True
    raise UserCancellationError


def render_templates(templates, root_directories, context, destination_dir):
    """Render the templated directories/files into the current location."""
    with cd(destination_dir):
        print("cwd", Path.cwd())
        check_if_new_dirs_can_be_created(
            directories=root_directories,
            context=context,
            destination_dir=destination_dir,
        )
        print('starting env')
        print('templates are', templates)
        jinja_env = Environment(
            loader=FileSystemLoader(str(templates), followlinks=True),
            keep_trailing_newline=True,
        )

        for template in jinja_env.list_templates():
            print('templaring', template)
            new_file = Path(Template(template).render(context))
            new_file.parents[0].mkdir(parents=True, exist_ok=True)
            template = jinja_env.get_template(template)
            content = template.render(context)
            with open(new_file, 'w') as templated_file:
                templated_file.write(content)
