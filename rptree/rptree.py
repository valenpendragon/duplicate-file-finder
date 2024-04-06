"""This module supplies the RP Tree main module."""

import os
import pathlib

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root_dir):
        """
        This method requires the path to the root directory where the
        DirectoryTree will begin. This is a required parameeter, but it
        may be a relative path instead of an absolute path.
        :param root_dir: filepath
        """
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        """This method prints out the directory tree to STDIO"""
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)



class _TreeGenerator:
    pass