"""Finalization script run after the templating"""

import pathlib


def finalize(context, current_dir):
    """Do some final adjustment to the templated files."""
    if context.get("delete_test2_file"):
        shutil.rm(pathlilb.Path())
