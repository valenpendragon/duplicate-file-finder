from treelib import Node, Tree
import os
import pathlib


class DirectoryObject(Node):
    """
    This class allows us to differentiate between a file node and a
    directory node in the tree. This is important because a directory
    can be a leaf object when it is empty. Tree.leaves() in treelib
    returns all leaf objects, but treats all nodes as possibly having
    children.

    Only a Directory Node will allow other Nodes to be added to it.
    """
    pass


class FileObject(Node):
    """
    This class allows us to differentiate between a file node and a
    directory node in the tree. It also adds a new attribute,
    hash_value, which stores the result of a file_hash run on the
    file to find duplicates.

    Tree.leaves() does not differentiate between empty directories and
    files.

    This object will not allow another node to be added to it.
    """
    pass

