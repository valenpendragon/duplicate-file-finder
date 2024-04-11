import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree
from functions import file_hash


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
    parser.add_argument(
        "-d",
        "--dir_only",
        action="store_true",
        help="Generator directory-only tree."
    )
    parser.add_argument(
        "-t",
        "--hash-type",
        action="store",
        default='sha256',
        choices=['sha224', 'sha256', 'sha384', 'sha512',
                 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']
    )
    parser.add_argument(
        "-s",
        "--suppress-hash",
        action="store_true",
        default=False
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
    print(f"rptree cli: args: {args}")
    tree = DirectoryTree(root_dir, dir_only=args.dir_only, hash_type=args.hash_type,
                         suppress_hash=args.suppress_hash)
    tree.generate()
