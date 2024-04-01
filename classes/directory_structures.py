from treelib import Node, Tree
from functions import file_hash
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
    def __init__(self, tag, identifier=None,
                 expanded=True, data=None):
        super().__init__(self, tag=tag, identifier=identifier,
                         expanded=expanded, data=data)

        if not (os.path.exists(self.tag) and os.path.isdir(self.tag)):
            error_msg = f"{self.tag} must be an actual directory."
            raise TypeError(error_msg)


class FileObject(Node):
    """
    This class allows us to differentiate between a file node and a
    directory node in the tree. It also adds a new attribute,
    hash_value, which stores the result of a file_hash run on the
    file to find duplicates.

    Tree.leaves() does not differentiate between empty directories and
    files.

    Unlike Node, tag is a required parameter.

    DirectoryTree will have an override parameter which will not
    allow another Node-based object to be connected to a FileObject.

    :param tag: str, filepath
    """
    def __init__(self, tag, identifier=None,
                 expanded=True, data=None):
        super().__init__(self, tag=tag, identifier=identifier,
                         expanded=expanded, data=data)
        if os.path.exists(self.tag) and os.path.isfile(self.tag):
            self.file_hash = file_hash(self.tag)
        else:
            error_msg = f"{self.tag} must be an actual file."
            raise TypeError(error_msg)
