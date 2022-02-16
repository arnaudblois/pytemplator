#!/usr/bin/env python

"""Tests for `pytemplator` package."""
import shutil
import subprocess
from unittest.mock import patch

from jinja2 import Template

from pytemplator import __version__
from pytemplator.pytemplator import Templator
from tests.utils import TmpdirTestCase, are_identical_dirs


class PytemplatorFullScaleTestCase(TmpdirTestCase):
    """End-to-end testing."""

    def run_test_on_template_fixture(self, number):
        """Template the specified fixture and compare to expected result."""
        template = (self.fixture_dir / f"test_template_{number}").resolve(strict=True)
        output_dir = self.tmpdir / "output_dir"
        output_dir.mkdir(exist_ok=True)
        tmp_template_dir = self.tmpdir / "templates" / f"test_template_{number}"
        # We copy the template out of the Pytemplator project
        # otherwise the git commands will start picking up its configuration
        # as they go check into the parent directories.
        shutil.copytree(template, tmp_template_dir)
        template = tmp_template_dir.resolve(strict=True)

        # Calling the pytemplate command as a user would.
        subprocess.run(
            [
                "pytemplate",
                "-b",
                str(self.tmpdir),
                "--no-input",
                "-d",
                str(output_dir),
                str(template),
            ],
            check=True,
            capture_output=True,
        )
        # In the fixtures expected results .pytemplator.yml, the pytemplator
        # version and tmp file path are left as jinja variables to template
        # since these can vary from test to test.
        # We template it in the following.
        expected_result = self.fixture_dir / f"expected_test_template_{number}_result"
        shutil.copytree(expected_result, self.tmpdir / "expected")
        expected_result = self.tmpdir / "expected"
        with open(
            expected_result / ".pytemplator.yml", "r", encoding="UTF-8"
        ) as yml_file:
            content = Template(yml_file.read()).render(
                {"current_version": __version__, "test_dir": str(template)}
            )
        with open(
            expected_result / ".pytemplator.yml", "w", encoding="UTF-8"
        ) as yml_file:
            yml_file.write(content)
            yml_file.write("\n\n")
        # Finally we can compare the output with its expected result
        self.assertTrue(are_identical_dirs(output_dir, expected_result))

    def test_template_cli_1(self):
        """Run the test on the test template 1.

        - Context from initialize.py
        - no finalize
        - template directory present (folders outside should be ignored)
        """
        self.run_test_on_template_fixture(number=1)

    def test_template_cli_2(self):
        """Run the test on the test template 2.

        - Context from initialize.py
        - finalize.py provided
        """
        self.run_test_on_template_fixture(number=2)

    def test_template_cli_3(self):
        """Run the test on the test template 3.

        - Context from initialize.py
        - finalize.py provided
        - a cookiecutter.json is present and should be ignored.
        """
        self.run_test_on_template_fixture(number=3)

    def test_template_cli_4(self):
        """Run the test on the test template 4.

        - Context from cookiecutter.json as there is no initialize.py.
        """
        self.run_test_on_template_fixture(number=4)

    def test_template_cli_5(self):
        """Run the test on the test template 5.

        - The initialize.py doesn't cater for no-input, raise exception.
        """
        with self.assertRaises(subprocess.CalledProcessError) as error:
            self.run_test_on_template_fixture(number=5)
        self.assertIn(
            "NoInputOptionNotHandledByTemplateError", error.exception.stderr.decode()
        )


@patch.object(Templator, "get_git_template")
@patch.object(Templator, "prepare_template_dir")
class PytemplatorInitTestCase(TmpdirTestCase):
    """TestCase for the init function of Templators."""

    def test_remote_url_makes_preparation_remote(
        self, mocked_prepare_dir, mocked_get_git
    ):
        """Test that passing a remote repo calls the right methods."""
        output_dir = self.tmpdir / "output_dir"
        output_dir.mkdir(exist_ok=True)
        Templator(
            base_dir=self.tmpdir,
            template_location="https://github.com/some-repo",
            destination_dir=output_dir,
        )
        mocked_get_git.assert_called_once()
        mocked_prepare_dir.assert_called_once()

    def test_local_path_preparation_is_not_remote(
        self, mocked_prepare_dir, mocked_get_git
    ):
        """Test that passing a local path doesn't call git-related methods."""
        output_dir = self.tmpdir / "output_dir"
        output_dir.mkdir(exist_ok=True)
        some_local_path = self.tmpdir / "location42"
        some_local_path.mkdir(exist_ok=True)
        Templator(
            base_dir=self.tmpdir,
            template_location=str(some_local_path),
            destination_dir=output_dir,
        )
        mocked_get_git.assert_not_called()
        mocked_prepare_dir.assert_not_called()
