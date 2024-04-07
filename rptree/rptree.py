"""This module supplies the RP Tree main module."""

import os
import pathlib
from functions import FileObject, DirectoryObject, file_hash

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root_dir, hash_type='sha256'):
        """
        This method requires the filepath to the root directory where the
        DirectoryTree will begin. This is a required parameter, but it
        may be a relative path instead of an absolute path.

        Parameter, hash_type, is the type of hash to perform on items found
        in the directory.

        :param root_dir: str of a filepath
        :param hash_type: str, name of the hash algorithm to use to build
            the hash list of all files in the directory, defaults to 'sha256'.
        """
        # Make sure root_dir is a directory and it exists.
        if not os.path.exists(root_dir):
            error_msg = (f"DirectoryTree.__init__(): root_dir, {root_dir}, "
                         f"does not exist.")
            raise OSError(error_msg)
        elif not os.path.isdir(root_dir):
            error_msg = (f"DirectoryTree.__init__(): root_dir, {root_dir}, is "
                         f"not a directory. Only an actual directory is"
                         f"acceptable.")
            raise OSError(error_msg)
        else:
            self._diagram_generator = _TreeDiagramGenerator(root_dir)
            self.tree = []
            self.root_dir = root_dir
            self.hash_type = hash_type
            root = DirectoryObject(name=root_dir, parent=None)
            self.tree.append(root)

    def generate(self):
        """This method prints out the directory tree to STDIO"""
        tree = self._diagram_generator.build_tree()
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
        """
        This method creates the header of the diagram. All actions take place
        on the diagram itself.
        :return: None
        """
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        """
        This method creates the body of the diagram. All action takes place
        on the object itself. directory is a required argument and is the
        directory that this method will traverse.
        :param directory: str, directory name
        :param prefix: str, allows the addition of spacers to the program.
        :return: None
        """
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)
        for idx, entry in enumerate(entries):
            connector = ELBOW if idx == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, idx, entries_count, prefix,
                                    connector)
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, idx: int, count: int,
                       prefix: str, connector: str):
        """
        This method recursively traverses the tree below directory by calling
        _tree_body again..
        :param directory: filepath of this directory to be added
        :param idx: int, current index of this director in its parent
            directory
        :param count: int: total number of entries in its parent directory
        :param prefix: str: the graphical string to prepend before the
            connector string when displaying this directory in its parent
        :param connector: str: the graphical string to prepend when connecting
            it to its parent directory
        :return: None, all action takes place internally
        """
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if idx != count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory=directory, prefix=prefix)

    def _add_file(self, file_entry, prefix, connector):
        """
        This method adds the filename to the directory tree structure and
        diagram.
        :param file_entry: relative filepath to this file
        :param prefix: str, graphical representation of the spacing to the
            connector to the file's parent directory
        :param connector: str, graphical representation of the connection to
            the file's parent directory
        :return: None, all action takes place internally
        """
        self._tree.append(f"{prefix}{connector} {file_entry.name}")
