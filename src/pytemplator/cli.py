"""Console script for pytemplator."""

import argparse
from pathlib import Path
import sys

from loguru import logger
from pytemplator.pytemplator import Templator


def main():
    """Console script for pytemplator."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--base-dir', default=str(Path.home() / '.pytemplator'),
        help=(
            'The directory which pytemplator can use to store its config files '
            'and downloaded templates'
        ),
    )
    parser.add_argument(
        '-c', '--checkout-branch', default='master',
        help=(
            'Which ref to checkout if using a repo-based template'
        ),
    )
    parser.add_argument(
        'template_location',
        help=(
            'The location of the template to use, can be either a repo url or '
            'its path on the filesystem.'
        )
    )
    args = parser.parse_args()

    templator = Templator(**vars(args))
    templator.generate_context()
    templator.render()
    logger.info("\nSuccess!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
