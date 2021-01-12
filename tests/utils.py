"""Utility scripts used for the tests."""

import filecmp
from pathlib import Path
import tempfile
from unittest import TestCase


def get_fixture_path():
    """Return the absolute path to the required fixture."""
    return (Path(__file__).parent / 'fixtures').resolve(strict=True)


def are_identical_dirs(dir1: Path, dir2: Path) -> bool:
    """Compare two directories recursively, including file content."""
    dir1, dir2 = Path(dir1).resolve(strict=True), Path(dir2).resolve(strict=True)
    dirs_cmp = filecmp.dircmp(dir1, dir2)
    if dirs_cmp.left_only or dirs_cmp.right_only or dirs_cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    if mismatch or errors:
        return False
    for common_dir in dirs_cmp.common_dirs:
        if not are_identical_dirs(dir1 / common_dir, dir2 / common_dir):
            return False
    return True


class TmpdirTestCase(TestCase):
    """TestCase setting automatically a temporary directory."""

    def setUp(self):
        """Set up a temp directory and locate the fixture."""
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmpdir.name)
        self.fixture_dir = get_fixture_path()

    def tearDown(self):
        """Delete the temp directory."""
        self._tmpdir.cleanup()
