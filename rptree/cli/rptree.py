"""
This module provides the RP tree main module.
"""

import os
import pathlib

# Constants needed to generate the tree appearance in the CLI.
PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    """
    This class stores a directory tree structure. It requires an
    internal class, _TreeGenerator.
    """
    def __init__(self, root_dir):
        """
        DirectoryTree requires a root directory to begin building
        a tree from the files and subdirectories in the root
        directory. root_dir must be a filepath, but it can be a
        relative filepath. It also requires the internal class
        _TreeGenerator.
        :param root_dir: filepath
        """
        self._generator = _TreeGenerator(root_dir)

        def generate(self):
            """
            This method generates the tree using the property
            build_tree() of the internal _TreeGenerator class.
            :return: None. All activity appears in STDIO.
            """
            tree = self._generator.build_tree()
            for entry in tree:
                print(entry)

class _TreeGenerator:
    pass