"""Utility scripts used for the tests."""

from pathlib import Path


def get_fixture_path():
    """Return the absolute path to the required fixture."""
    print("X", Path(__file__).parent)
