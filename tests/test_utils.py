"""Testcases for pytemplator.utils modules."""

import builtins
from unittest import mock

from pytemplator.exceptions import UserCancellationError
from pytemplator.utils import check_if_new_dirs_can_be_created
from tests.utils import TmpdirTestCase


class CheckNewDirsCanBeCreatedTestCase(TmpdirTestCase):
    """TestCase for function check_if_new_dirs_can_be_created.

    WIP SECTION.
    """

    def test_directories_dont_exist_already(self):
        """Test it's true if there's no existing dir."""
        self.assertTrue(
            check_if_new_dirs_can_be_created(
                directories=[self.tmpdir / "dir{{solution}}"],
                context={"solution": 42},
                destination_dir=self.tmpdir,
            )
        )

    def test_directories_exist_user_overwrites(self):
        """
        Test it deletes the existing dir and returns true
        if the user accepts to overwrite.
        """
        existing_dir = self.tmpdir / "dir42"
        existing_dir.mkdir()
        existing_dir.resolve(strict=True)
        with mock.patch.object(builtins, "input", lambda _: "Y"):
            self.assertTrue(
                check_if_new_dirs_can_be_created(
                    directories=[self.tmpdir / "dir{{solution}}"],
                    context={"solution": 42},
                    destination_dir=self.tmpdir,
                )
            )
        with self.assertRaises(FileNotFoundError):
            existing_dir.resolve(strict=True)

    def test_directories_exist_user_cancels(self):
        """Test that an exception is thrown if user cancels."""
        existing_dir = self.tmpdir / "dir42"
        existing_dir.mkdir()
        with mock.patch.object(builtins, "input", lambda _: "N"):
            with self.assertRaises(UserCancellationError):
                check_if_new_dirs_can_be_created(
                    directories=[self.tmpdir / "dir{{solution}}"],
                    context={"solution": 42},
                    destination_dir=self.tmpdir,
                )
