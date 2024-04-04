from treelib import Node, Tree
from functions import file_hash
import os
import pathlib


class MultipleRootError(Exception):
    pass


class DuplicateNodeIdError(Exception):
    pass


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
            raise OSError(error_msg)
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
            raise OSError(error_msg)
        data = os.path.dirname(tag)
        print(f"FileObject: data: {data}")

        super().__init__(tag=os.path.basename(tag),
                         identifier=identifier,
                         expanded=expanded, data=data)


class DirectoryTree(Tree):
    """
    This class allows us to create a directory tree with built-in
    validation. DirectoryObject and FileObject ensure that directories
    and files are assigned to the correct objects, but they cannot
    determine if a FileObject or a DirectoryObject are contained in an
    existing DirectoryObject in the tree before adding it to the node.
    This class can look at an existing nodes data to see if contains
    the new using its filepath.

    DirectoryObject and FileObject exist to allows the leaves() method
    to produce a list of objects that can be differentiated as files
    or empty directories.

    This class differs from the original in that node_class will be
    set to 'directory tree'. This ensure that tree adds must be the
    same type before pasting. The bool, deep, is automatically set to
    True, since directory structures should be deep copied to avoid
    errors. Only tree is an optional str value.

    The __init__ method needs to force the node_class attribute to
    the value 'directory tree'. That will keep it from adding nodes for
    trees that are not files or directories. However, the add_node needs
    to be altered to check for DirectoryObject and FileObject nodes.
    This class cannot use inheritance for this method.

    The create_node method needs an additional parameter to ensure
    that the correct type of node is created (directory or file).
    """
    def __init__(self, tree=None):
        """
        The only unset parameter, tree, is an optional str indicating
        the unique identifier of a existing Tree object. deep is set
        to True to ensure that deep copies are made and stored.
        node_class is set to 'directory tree' to ensure that only
        other DirectoryTree objects are allows to paste to or be
        copied into this new object.

        :param tree: str or None, optional
        """
        deep = True
        node_class = 'directory tree'
        if tree is not None:
            if not isinstance(tree, DirectoryTree):
                error_msg = (f"DirectoryTree: {tree} must be "
                             f"DirectoryTree type.")
                raise TypeError(error_msg)
        super().__init__(tree=tree, deep=deep, node_class=None)
        self.node_class = node_class

    def add_node(self, node, parent=None):
        """
        This method adds a new node to the DirectoryTree. The node_class
        must be either DirectoryObject or FileObject. If the tree is
        empty, the new node must be DirectoryObject type. If the tree
        is not empty, then the parent must be DirectoryObject type.
        :param node: instance of Class::Node
        :param parent: instance of Class::Node that will contain the
            new node, default to None (adding a root node)
        :return: None, all changes within the tree object
        """
        # The node_class is 'directory tree'. In practical terms, that
        # means that nodes can have two types: DirectoryObject and
        # FileObject. This is why we could not use the original method
        # which checks node_class for a single type.
        if not (isinstance(node, DirectoryObject)
                or isinstance(node, FileObject)):
            error_msg = (f"DirectoryTree: node must be one of the following "
                         f"types derived from Class::Node - DirectoryObject "
                         f"or FileObject.")
            raise OSError(error_msg)

        # Node identifiers cannot appear more than once in a tree.
        if node.identifier in self.nodes:
            error_msg = (f"DirectoryTree: Node, {node} has a Node ID, "
                         f"{node.identifier}, which already appears in "
                         f"this tree.")
            raise DuplicateNodeIdError(error_msg)

        # We have to verity that new root is a DirectoryObject
        # before adding it as root. We also need to make sure that
        # more than root is not being added.
        if parent is None:
            if self.root is not None:
                error_msg = (f"DirectoryTree: {self.root} has already been set"
                             f"as root. Tree objects cannot have multiple"
                             f"roots.")
                raise MultipleRootError(error_msg)
            else:
                if not isinstance(node, DirectoryObject):
                    error_msg = (f"DirectoryTree: Node {node} is "
                                 f"type {type(node)}. A root node "
                                 f"must be type DirectoryObject.")
                    TypeError(error_msg)
                else:
                    self.root = node.identifier

        else:
            # Parent must be a directory object to contain other
            # nodes.
            if not isinstance(parent, DirectoryObject):
                error_msg = (f"DirectoryTree: Parent node, {parent}, "
                             f"is type {type(parent)}. In directory"
                             f"trees, only DirectoryObjects can"
                             f"contain other objects.")
                raise OSError(error_msg)
            else:
                parent = Node.sanitize_id(parent)

        self.nodes.update({node.identifier: node})
        self.__update_fpointer(parent, node.identifier, Node.ADD)
        node.bpointer = parent



