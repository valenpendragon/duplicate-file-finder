import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="tree",
        description="RP Tree directory tree generator",
        epilog="RP Tree Help"
    )
    parser.version = f"RP Tree v{__version__}"
    parser.add_argument("-v", "--version",
                        action="version")
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default='.',
        help="Create a full directory tree at ROOT_DIR."
    )
    return parser.parse_args()


def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        error_msg = (f"{args.root_dir}, does not exist or is not "
                     f"a directory. ROOT_DIR must be a directory.")
        print(error_msg)
        sys.exit()
    tree = DirectoryTree(root_dir)
    tree.generate()
