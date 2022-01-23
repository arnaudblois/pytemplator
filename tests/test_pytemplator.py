#!/usr/bin/env python

"""Tests for `pytemplator` package."""

import subprocess

from tests.utils import TmpdirTestCase, are_identical_dirs


class PytemplatorFullScaleTestCase(TmpdirTestCase):
    """End-to-end testing."""

    def run_test_on_template_fixture(self, number):
        """Template the specified fixture and compare to expected result."""
        template = (self.fixture_dir / f"test_template_{number}").resolve(strict=True)
        output_dir = self.tmpdir / "output_dir"
        output_dir.mkdir(exist_ok=True)
        expected_result = self.fixture_dir / f"expected_test_template_{number}_result"
        subprocess.run(
            [
                "pytemplate",
                "-b",
                str(self.tmpdir),
                "-d",
                str(output_dir),
                str(template),
            ],
            check=True,
        )
        self.assertTrue(are_identical_dirs(output_dir, expected_result))

    def test_template_cli_1(self):
        """Run the test on the test template 1.

        - Complete generation of a template from an initialize
        - no finalize
        - template directory present (folders outside should be ignore)
        """
        self.run_test_on_template_fixture(number=1)

    def test_template_cli_2(self):
        """Run the test on the test template 2.

        - Complete generation of a template from an initialize
        - finalize provided
        """
        self.run_test_on_template_fixture(number=2)

    def test_template_cli_3(self):
        """Run the test on the test template 3.

        - Complete generation of a template from an initialize
        - finalize provided
        """
        self.run_test_on_template_fixture(number=2)

    # def test_template_cli_2(self):
    #     template = (self.fixture_dir / 'test_template_2').resolve(strict=True)
    #     output_dir = self.tmpdir / 'output_dir'
    #     output_dir.mkdir(exist_ok=True)
    #     expected_result = self.fixture_dir / 'expected_test_template_2_result'
    #     subprocess.run([
    #         'pytemplate', '-b', str(self.tmpdir), '-d', str(output_dir),
    #         str(template)
    #     ])
    #
    #     self.assertTrue(are_identical_dirs(output_dir, expected_result))
