"""Main module."""


import os
from pathlib import Path
import subprocess
import tempfile

from loguru import logger

from pytemplator.constants import (
    GIT_REGEX, RESERVED_DIR_NAMES,
)
from pytemplator.exceptions import (
    BrokenTemplateError,
    UserCancellationError,
)
from pytemplator.utils import (
    cd,
    import_module_from_path,
    is_yes,
    render_templates,
)


class Templator:
    """Main class creating a project from a template."""

    def __init__(
            self,
            base_dir: str = None,
            template_location: str = None,
            checkout_branch: str = 'master',
    ):
        """Set up the attributes."""
        self.base_dir = Path(base_dir) if base_dir else Path.home() / '.pytemplator'
        self.base_dir.mkdir(parents=True, exist_ok=True)

        if GIT_REGEX.match(template_location):
            template_name = template_location.replace('.git', '').strip('/').split('/')[-1]
            self.template_dir = self.base_dir / template_name
            self.checkout_branch = checkout_branch
            self.get_git_template(template_location)
        else:
            self.template_dir = Path(template_location).resolve(strict=True)

        self.context = None
        try:
            self.initializer = (self.template_dir / 'initialize.py').resolve(strict=True)
            self.initializer_style = 'pytemplator'
        except FileNotFoundError:
            logger.warning(
                'The template does not have a valid initialize.py file'
                'Falling back to checking a cookiecutter.json definition file.'
            )
            try:
                self.initializer = (self.template_dir / 'cookiecutter.json').resolve(strict=True)
                self.initializer_style = 'cookiecutter'
            except FileNotFoundError:
                raise BrokenTemplateError(
                    'The template is missing a valid initialize.py/cookiecutter.json.'
                )

        try:
            self.finalizer = (self.template_dir / 'finalize.py').resolve(strict=True)
        except FileNotFoundError:
            self.finalizer = None

    def get_git_template(self, url):
        """Get the template project from a Git repository."""
        try:
            with cd(self.template_dir):
                subprocess.run(['git', 'fetch', '-p'], shell=True)
        except subprocess.CalledProcessError:
            use_old_repo = input(
                'Could not fetch from the repo url.\nDo you wish to continue '
                'using the version of the template already on file [Y]/N'
            ) or 'Y'
            if not is_yes(use_old_repo):
                raise UserCancellationError
        except FileNotFoundError:
            try:
                with cd(self.base_dir):
                    subprocess.run(['git', 'clone', url], shell=True)
            except subprocess.CalledProcessError:
                raise BrokenTemplateError(
                    f'The template could not be cloned from {url}'
                )

        with cd(self.template_dir):
            subprocess.run(['git', 'checkout', self.checkout_branch])

    def generate_context(self):
        """Generate the context for the `initialize` part of the template."""
        initialize = import_module_from_path(self.initializer)
        self.context = initialize.generate_context()
        self.context.update(
            {"pytemplator": self.context, "cookiecutter": self.context}
        )

    def render(self):
        """Copy the folder/files with templated names, then template them."""
        templates = self.template_dir / 'templates'
        try:
            templates = templates.resolve(strict=True)
            root_directories = [
                Path(f.path) for f in os.scandir(templates) if f.is_dir()
            ]
            render_templates(
                templates=templates,
                root_directories=root_directories,
                context=self.context,
            )
        except FileNotFoundError:
            root_directories = (
                Path(f.path) for f in os.scandir(self.template_dir)
                if f.is_dir() and f.name not in RESERVED_DIR_NAMES
            )
            with tempfile.TemporaryDirectory() as templates:
                templates = Path(templates)
                for directory in root_directories:
                    os.symlink(directory, templates / directory.name)
                render_templates(
                    templates=templates,
                    root_directories=root_directories,
                    context=self.context,
                )

    def finalize(self):
        """Run the `finalize` part of the template."""
        if not self.finalizer:
            return
        final_script = import_module_from_path(self.finalizer)
        final_script.finalize()
