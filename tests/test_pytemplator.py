#!/usr/bin/env python

"""Tests for `pytemplator` package."""

import shutil
import subprocess

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
        expected_result = self.fixture_dir / f"expected_test_template_{number}_result"
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
        )
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
