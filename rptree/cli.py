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
    parser.add_argument("--version",
                        action="version")
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default='.',
        help="Create a full directory tree at ROOT_DIR."
    )
    parser.add_argument(
        "-t",
        "--hash-type",
        action="store",
        default='sha256',
        choices=['sha224', 'sha256', 'sha384', 'sha512',
                 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512'],
        help="Determines which safe SHA algorithm to use. Defaults to sha256."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Controls display of file and directory being examined. Defaults to False, "
             "suppressing such output."
    )
    parser.add_argument(
        "-o",
        "--output-file",
        action="store",
        default=None,
        help="Writes output of directory tree to a file."
    )
    parser.add_argument(
        "-f",
        "--file-type",
        action="store",
        default="txt",
        choices=["txt", 'md'],
        help="Determines type of output displays or written to screen. "
             "Only supports txt and md currently."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--list-duplicates",
        action="store_true",
        default=False,
        help="Finds file duplicates and lists them by filename "
             "with full directory info."
    )
    group.add_argument(
        "-s",
        "--suppress-hash",
        action="store_true",
        default=False,
        help="Controls display of file hashes, but does not suppress the performance"
             "of hash algorithm on files. Defaults is False, displaying hash results."
    )
    group.add_argument(
        "-d",
        "--dir_only",
        action="store_true",
        help="Generator directory-only tree."
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
    # print(f"rptree cli: args: {args}")
    tree = DirectoryTree(root_dir,
                         dir_only=args.dir_only,
                         hash_type=args.hash_type,
                         suppress_hash=args.suppress_hash,
                         verbose=args.verbose,
                         output_file=args.output_file,
                         file_type=args.file_type,
                         list_duplicates=args.list_duplicates)
    tree.generate()
    tree.print_tree()
    if args.list_duplicates:
        duplicate_files = tree.find_duplicates()

