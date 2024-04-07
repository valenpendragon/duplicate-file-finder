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
        This method requires the filepath to the root directory where the
        DirectoryTree will begin. This is a required parameter, but it
        may be a relative path instead of an absolute path.
        :param root_dir: str of a filepath
        """
        self._generator = _TreeDiagramGenerator(root_dir)

    def generate(self):
        """This method prints out the directory tree to STDIO"""
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeDiagramGenerator:
    def __init__(self, root_dir):
        """
        This method requires the filepath to the root directory where the
        _TreeGenerator will begin. This is a required parameter, but it
        may be a relative path instead of an absolute path. This class adds
        an important attribute to DirectoryTree.
        :param root_dir: str of a filepath
        """
        self._root_dir = pathlib.Path(root_dir)
        self._tree = []

    def build_tree(self):
        """
        This method builds the tree structure for a DirectoryTree, storing it
        in the internal attributes of this object as well as returning the
        structure to make it available to other classes.
        :return: _tree, a nested list of nodes forming the directory tree.
        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, root_dir):
        pass