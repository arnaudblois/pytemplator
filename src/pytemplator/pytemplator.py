"""Main module."""

import os
import subprocess
import tempfile
from functools import cached_property
from pathlib import Path

import yaml
from loguru import logger

from pytemplator import __version__
from pytemplator.constants import GIT_REGEX, RESERVED_DIR_NAMES
from pytemplator.exceptions import (
    BrokenTemplateError,
    InvalidInputError,
    UserCancellationError,
)
from pytemplator.utils import (
    cd,
    generate_context_from_json,
    import_module_from_path,
    is_yes,
    render_templates,
)


class Templator:  # pylint: disable=too-many-instance-attributes, too-many-arguments
    """Main class creating a project from a template."""

    def __init__(
        self,
        base_dir: str = None,
        template_location: str = None,
        checkout_branch: str = "main",
        destination_dir: str = None,
        no_input: bool = False,
    ):
        """Set up the attributes.

        template_location can be either a remote git repo, in which case we
        clone/pull and checkout, or a directory on the local file system.

        Important note: the local directory is treated as-is, i.e. even if it
        is a valid git repo, the checkout-branch will be ignored and nothing
        will be touched. Earlier versions of PyTemplator were altering the
        local repo, dogfooding showed it was a very confusing experience.

        We then call its initialize.py if it exists, otherwise we use
        the cookiecutter.json for context.
        """
        self.base_dir = Path(base_dir) if base_dir else Path.home() / ".pytemplator"
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.destination_dir = Path(destination_dir) if destination_dir else Path.cwd()
        self.destination_dir = self.destination_dir.resolve(strict=True)

        self.checkout_branch = checkout_branch
        self.template_location = template_location
        if GIT_REGEX.match(template_location):
            template_name = (
                template_location.replace(".git", "").strip("/").split("/")[-1]
            )
            self.template_dir = self.base_dir / template_name
            self.get_git_template(template_location)
            self.prepare_template_dir()
        else:
            self.template_dir = Path(template_location).resolve(strict=True)
        self.context = {"cookiecutter": {}, "pytemplator": {}}
        self.no_input = no_input

    def get_git_template(self, url):
        """Get the template project from a Git repository."""
        try:
            with cd(self.template_dir):
                subprocess.run("git fetch -p", shell=True, check=True)
        except subprocess.CalledProcessError as error:
            if self.no_input:
                logger.warning("Couldn't fetch repo, using cached version")
                use_old_repo = "Y"
            else:
                use_old_repo = (
                    input(
                        "Could not fetch from the repo url.\nDo you wish to continue "
                        "using the version of the template already on file [Y]/N"
                    )
                    or "Y"
                )
            if not is_yes(use_old_repo):
                raise UserCancellationError from error
        except FileNotFoundError:
            try:
                with cd(self.base_dir):
                    subprocess.run(f"git clone {url}", shell=True, check=True)
            except subprocess.CalledProcessError as error:
                raise BrokenTemplateError(
                    f"The template could not be cloned from {url}"
                ) from error

    def prepare_template_dir(self):
        """Make sure the template directory is in the expected state."""
        with cd(self.template_dir):
            try:
                subprocess.run(
                    ["git", "checkout", self.checkout_branch],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                # If the cached repo has been edited somehow, the index might
                # be corrupted so we do a hard reset to unblock things.
                try:
                    subprocess.run(
                        ["git", "reset", "--hard", f"origin/{self.checkout_branch}"],
                        check=True,
                        capture_output=True,
                    )
                    subprocess.run(
                        ["git", "checkout", self.checkout_branch],
                        check=True,
                        capture_output=True,
                    )
                except subprocess.CalledProcessError as error:
                    logger.error("The specified branch to checkout does not exist.")
                    raise InvalidInputError from error

    @cached_property
    def last_commit_hash(self):
        """Return the hash of the latest commit.

        This is recorded in the .pytemplator.yml file to allow for
        further re-templating in the future.

        This is kept separate from the prepare_template_dir as unlike the
        checkout logic, storing the commit for a git repo on the filesystem
        is something useful which doesn't lead to unexpected side-effects.
        """
        with cd(self.template_dir):
            try:
                return subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
            except subprocess.CalledProcessError:
                return None

    def generate_context(self):
        """Generate the context for the `initialize` part of the template."""
        try:
            initializer = (self.template_dir / "initialize.py").resolve(strict=True)
            initialize = import_module_from_path(initializer)
            self.context = initialize.generate_context(self.no_input)
            # This allows the user to call the variables {{ cookiecutter.var }} or
            # {{ pytemplator.var }} in the template for convenience.
            self.context.update(
                {"pytemplator": self.context, "cookiecutter": self.context}
            )
        except AttributeError as error:
            raise BrokenTemplateError(
                "The `initialize.py` does not have a valid generate_context."
            ) from error
        except FileNotFoundError:
            logger.warning(
                "The template does not have a valid initialize.py file\n"
                "Falling back to checking a cookiecutter.json definition file."
            )
            try:
                self.context = generate_context_from_json(
                    json_file=(self.template_dir / "cookiecutter.json").resolve(
                        strict=True,
                    ),
                    context=self.context,
                    no_input=self.no_input,
                )
            except FileNotFoundError as error:
                raise BrokenTemplateError(
                    "The template is missing a valid initialize.py/cookiecutter.json."
                ) from error

    def render(self):
        """Copy the folder/files with their names properly templated, then render them."""
        templates = self.template_dir / "templates"
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
                no_input=self.no_input,
            )
        except FileNotFoundError:
            root_directories = [
                Path(f.path)
                for f in os.scandir(self.template_dir)
                if f.is_dir() and f.name not in RESERVED_DIR_NAMES
            ]
            with tempfile.TemporaryDirectory() as templates:
                templates = Path(templates)
                for directory in root_directories:
                    os.symlink(directory, templates / directory.name)
                render_templates(
                    destination_dir=self.destination_dir,
                    templates=templates,
                    root_directories=root_directories,
                    context=self.context,
                    no_input=self.no_input,
                )
        self.finalize()
        self.add_pytemplator_yaml()

    def finalize(self):
        """Run the `finalize` part of the template."""

        try:
            finalizer = (self.template_dir / "finalize.py").resolve(strict=True)
            final_script = import_module_from_path(finalizer)
            final_script.finalize(context=self.context, output_dir=self.destination_dir)
        except FileNotFoundError:
            return

    def add_pytemplator_yaml(self):
        """Add a `.pytemplator.yml` config file.

        This allows for future automated boilerplate update to follow
        the latest version of the template.
        """
        with open(
            self.destination_dir / ".pytemplator.yml", "w", encoding="UTF-8"
        ) as conf_file:
            conf_file.write(
                "# This is an automated file generated by the PyTemplator package.\n"
                "# It is used to update the boilerplate to follow the latest\n"
                "# version of the template.\n\n"
            )
            context = dict(self.context)
            context.pop("pytemplator", None)
            context.pop("cookiecutter", None)
            yaml.dump(
                {
                    "pytemplator_version": __version__,
                    "template_location": self.template_location,
                    "checkout_branch": self.checkout_branch,
                    "template_commit": self.last_commit_hash,
                    "context": context,
                },
                conf_file,
            )
            conf_file.write("\n")
