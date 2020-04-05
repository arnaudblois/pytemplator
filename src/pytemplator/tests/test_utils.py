"""Testcases for pytemplator.utils modules."""

import tempfile
import shutil
from unittest import mock, TestCase


class CheckNewDirsCanBeCreatedTestCase(TestCase):
    """"""

    def setUp(self):
        """"""
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """"""
        shutil.rmtree(self.tempdir)

    def test_directories_dont_exist_already(self):
        """"""

    def test_directories_exist_user_overwrites(self):
        """"""

    def test_directories_exist_user_cancels(self):
        """"""
        self.assertTrue(True)


class GenerateContextTestCase(TestCase):
    """"""

    def setUp(self):
        """"""
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """"""
        shutil.rmtree(self.tempdir)

    def test_initialize_is_run(self):
        """"""


class RenderTemplatesTestCase(TestCase):
    """"""
