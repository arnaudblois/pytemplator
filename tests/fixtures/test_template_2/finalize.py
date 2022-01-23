"""Finalization script run after the templating"""

import os
from pathlib import Path


def finalize(context: dict, output_dir: Path):
    """Do some final adjustment to the templated files."""
    if context.get("remove_test1_file"):
        os.remove(str(output_dir / context["main_folder_name"] / "test1"))
