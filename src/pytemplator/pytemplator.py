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
    generate_context_from_json,
    import_module_from_path,
    is_yes,
    render_templates,
)


class Templator:  # pylint: disable=too-many-instance-attributes
    """Main class creating a project from a template."""

    def __init__(
            self,
            base_dir: str = None,
            template_location: str = None,
            checkout_branch: str = 'master',
            destination_dir: str = None
    ):
        """Set up the attributes.

        template_location can be either a git repo, in which case we
        clone/pull and checkout, or a directory.

        We then call its initialize.py if it exists, otherwise we use
        the cookiecutter.json for context.
        """
        self.base_dir = Path(base_dir) if base_dir else Path.home() / '.pytemplator'
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.destination_dir = Path(destination_dir) if destination_dir else Path.cwd()
        self.destination_dir = self.destination_dir.resolve(strict=True)

        self.checkout_branch = checkout_branch
        if GIT_REGEX.match(template_location):
            template_name = template_location.replace('.git', '').strip('/').split('/')[-1]
            self.template_dir = self.base_dir / template_name
            self.get_git_template(template_location)
        else:
            self.template_dir = Path(template_location).resolve(strict=True)
        self.prepare_template_dir()
        self.context = {'cookiecutter': {}, 'pytemplator': {}}

    def get_git_template(self, url):
        """Get the template project from a Git repository."""
        try:
            with cd(self.template_dir):
                subprocess.run('git fetch -p', shell=True, check=True)
        except subprocess.CalledProcessError as error:
            use_old_repo = input(
                'Could not fetch from the repo url.\nDo you wish to continue '
                'using the version of the template already on file [Y]/N'
            ) or 'Y'
            if not is_yes(use_old_repo):
                raise UserCancellationError from error
        except FileNotFoundError:
            try:
                with cd(self.base_dir):
                    subprocess.run(f'git clone {url}', shell=True, check=True)
            except subprocess.CalledProcessError as error:
                raise BrokenTemplateError(
                    f'The template could not be cloned from {url}'
                ) from error

    def prepare_template_dir(self):
        """Make sure the template directory is in the expected state."""
        try:
            with cd(self.template_dir):
                subprocess.run(['git', 'checkout', self.checkout_branch], check=True)
        except subprocess.CalledProcessError:
            logger.info('The template is a standard directory, not a git repo.')

    def generate_context(self):
        """Generate the context for the `initialize` part of the template."""
        try:
            initializer = (self.template_dir / 'initialize.py').resolve(strict=True)
            initialize = import_module_from_path(initializer)
            self.context = initialize.generate_context()
            self.context.update(
                {'pytemplator': self.context, 'cookiecutter': self.context}
            )
        except AttributeError as error:
            raise BrokenTemplateError(
                'The `initialize.py` does not have a valid generate_context.'
            ) from error
        except FileNotFoundError:
            logger.warning(
                'The template does not have a valid initialize.py file'
                'Falling back to checking a cookiecutter.json definition file.'
            )
            try:
                self.context = generate_context_from_json(
                    json_file=(self.template_dir / 'cookiecutter.json').resolve(strict=True),
                    context=self.context,
                )
            except FileNotFoundError as error:
                raise BrokenTemplateError(
                    'The template is missing a valid initialize.py/cookiecutter.json.'
                ) from error

    def render(self):
        """Copy the folder/files with their names properly templated, then render them."""
        templates = self.template_dir / 'templates'
        try:
            templates = templates.resolve(strict=True)
            root_directories = [
                Path(f.path) for f in os.scandir(templates) if f.is_dir()
            ]
            render_templates(
                destination_dir=self.destination_dir,
                templates=templates,
                root_directories=root_directories,
                context=self.context,
            )
        except FileNotFoundError:
            root_directories = [
                Path(f.path) for f in os.scandir(self.template_dir)
                if f.is_dir() and f.name not in RESERVED_DIR_NAMES
            ]
            with tempfile.TemporaryDirectory() as templates:
                templates = Path(templates)
                # templates = Path.cwd() / 'test'
                # templates.mkdir()
                for directory in root_directories:
                    os.symlink(directory, templates / directory.name)
                render_templates(
                    destination_dir=self.destination_dir,
                    templates=templates,
                    root_directories=root_directories,
                    context=self.context,
                )
        self.finalize()

    def finalize(self):
        """Run the `finalize` part of the template."""

        try:
            finalizer = (self.template_dir / 'finalize.py').resolve(strict=True)
            final_script = import_module_from_path(finalizer)
            final_script.finalize(context=self.context, output_dir=self.destination_dir)
        except FileNotFoundError:
            return
