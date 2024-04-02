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

    Unlike Node, tag is a required parameter. It is the name of the
    directory. The path-to-directory will be stored in data. Also
    unlike Node, data cannot be specified as a parameter.
    :param tag: str (filepath)
    :param identifier: unique key, usually assigned by the parent
        class to the actual system identifier in memory.
    :param expanded: bool, defaults to True
    """
    def __init__(self, tag, identifier=None,
                 expanded=True, data=None):
        print(f"DirectoryObject: tag: {tag}")
        if not (os.path.exists(tag) and os.path.isdir(tag)):
            error_msg = f"{tag} must be an actual directory."
            raise TypeError(error_msg)
        data = os.path.dirname(tag)
        print(f"FileObject: data: {data}")

        super().__init__(tag=os.path.basename(tag),
                         identifier=identifier,
                         expanded=expanded, data=data)


class FileObject(Node):
    """
    This class allows us to differentiate between a file node and a
    directory node in the tree. It also adds a new attribute,
    hash_value, which stores the result of a file_hash run on the
    file to find duplicates.

    Tree.leaves() does not differentiate between empty directories and
    files.

    Unlike Node, tag is a required parameter. It is the filename for
    actual file. The directory it is stored in will stored in data.
    Also unlike Node, data cannot be specified as a parameter.

    DirectoryTree will have an override parameter which will not
    allow another Node-based object to be connected to a FileObject.

    :param tag: str (filepath)
    :param identifier: unique key, usually assigned by the parent
        class to the actual system identifier in memory.
    :param expanded: bool, defaults to True
    """
    def __init__(self, tag, identifier=None, expanded=True):
        print(f"FileObject: tag: {tag}")
        if os.path.exists(tag) and os.path.isfile(tag):
            self.file_hash = file_hash(tag)
        else:
            error_msg = f"{tag} must be an actual file."
            raise TypeError(error_msg)
        data = os.path.dirname(tag)
        print(f"FileObject: data: {data}")

        super().__init__(tag=os.path.basename(tag),
                         identifier=identifier,
                         expanded=expanded, data=data)
