"""This module supplies the RP Tree main module."""

import os
import pathlib
import sys
import copy
from itertools import cycle
from time import sleep
from collections import namedtuple

from functions import FileObject, DirectoryObject, file_hash

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(self, root_dir,
                 hash_type='sha256',
                 dir_only=False,
                 suppress_hash=False,
                 verbose=False,
                 output_file=None,
                 file_type='txt',
                 list_duplicates=False):
        """
        This method requires the filepath to the root directory where the
        DirectoryTree will begin. This is x required parameter, but it
        may be x relative path instead of an absolute path.

        Parameter, hash_type, is the type of hash to perform on items found
        in the directory.

        :param root_dir: str of x filepath
        :param hash_type: str, name of the hash algorithm to use to build
            the hash list of all files in the directory, defaults to 'sha256'.
        :param dir_only: bool, defaults to False, used to create a directory only listing
        :param suppress_hash: bool, defaults to False, suppresses hash output in the
            directory tree printout
        :param verbose: bool, defaults to False, allows extra messages to appear as the
            program performs its work
        :param output_file: str, filepath to an output file
        :param file_type: str, either 'txt' for ASCII text or 'md' for Markdown which
            uses UTF-8 encoding, anything else default to 'txt', will be ignored if
            output_file is None
        :param list_duplicates: bool, defaults to False, determines if this program attempt
            to find duplicate files in the tree after it has traversed it.
        """
        # Make sure root_dir is x directory and it exists.
        if not os.path.exists(root_dir):
            error_msg = (f"DirectoryTree.__init__(): root_dir, {root_dir}, "
                         f"does not exist.")
            raise OSError(error_msg)
        elif not os.path.isdir(root_dir):
            error_msg = (f"DirectoryTree.__init__(): root_dir, {root_dir}, is "
                         f"not x directory. Only an actual directory is"
                         f"acceptable.")
            raise OSError(error_msg)
        else:
            self._diagram_generator = _TreeDiagramGenerator(root_dir,
                                                            dir_only=dir_only,
                                                            hash_type=hash_type,
                                                            suppress_hash=suppress_hash,
                                                            verbose=verbose)
            self.tree = []
            self.root_dir = root_dir
            self.hash_type = hash_type
            self._dir_only = dir_only
            self._suppress_hash = suppress_hash
            self._verbose = verbose
            self._output_file = output_file
            self._list_duplicates = list_duplicates
            if self._output_file:
                if file_type == 'md':
                    self._file_type = 'md'
                else:
                    self._file_type = 'txt'
                self.output_stream = open(self._output_file, mode='w', encoding='UTF-8')
            else:
                self._file_type = None
                self.output_stream = sys.stdout
            print(self)

    def __str__(self):
        s = (f"DirectoryTree: \n"
             f"root_dir: {self.root_dir}. hash_type: {self.hash_type}\n."
             f"_dir_only: {self._dir_only}. _suppress_hash: {self._suppress_hash}\n."
             f"_verbose: {self._verbose}. _list_duplicates: {self._list_duplicates}.\n"
             f"_output_file: {self._output_file}.\n"
             f"_file_type: {self._file_type}.\n"
             f"tree: {self.tree}\n."
             f"_diagram_generator: {self._diagram_generator}\n"
             f"End of DirectoryTree.")
        return s

    def generate(self):
        """
        This method generates the tree from _TreeDiagramGenerator.
        :return:
        """
        print(f"Using algorithm {self.hash_type} for the hash values displayed.")
        if self._suppress_hash:
            print("Files hash output has been suppressed.")
        print("Building directory tree.")
        self.tree = self._diagram_generator.build_tree()

    def print_tree(self):
        """This method prints out the tree to either a file or
        to stdout."""
        if self._file_type == 'md':
            # Wrap the tree in a markdown code block.
            self.tree.insert(0, "```")
            self.tree.append("```")

        if self.output_stream == sys.stdout:
            print("Printing the completed directory tree.")
            for entry in self.tree:
                print(entry)
        else:
            print(f"Printing the completed directory tree to {self._output_file}.")
            for entry in self.tree:
                print(entry, file=self.output_stream)
            if not self._list_duplicates:
                self.output_stream.close()

    def find_duplicates(self):
        """
        This method searches self._tree to find files with matching
        file_hashes and prints out a report detailing this information,
        either to the output_file or stdout.
        :return:
        """
        duplicate_files = []       # Stores the actual duplicate files.
        previous_path = []         # Stores the path to a file.
        files_with_full_data = []  # Stores the file list with hash and filepath.
        dir_end = False            # Flag to set when a directory end is reached.
        previous_path.append(str(self.root_dir))
        for item in self.tree:
            if self.tree.index(item) == 0:
                # Skip the root directory.
                continue
            elif item == PIPE:
                # Skip the first PIPE.
                continue
            # Now, we need to disassemble the item to get the
            # path to the item.
            depth_ctr = 0
            while PIPE in item:
                # Remove all PIPE_PREFIX strings and track the number.
                depth_ctr += 1
                item = item[len(PIPE_PREFIX):]
            if TEE in item:
                # Remove TEE since it is the middle of a directory, regardless of whether
                # the item is really a file or a directory.
                item = item.replace(f"{TEE} ", '')
                dir_end = False
            if ELBOW in item:
                # This marks the end of the directory.
                dir_end = True
                item = item.replace(f"{ELBOW} ", '')
            if item[-1] == os.sep or item[-2:] == os.sep:
                # item is a directory name.
                if depth_ctr < len(previous_path):
                    # Remove one level due to an empty directory.
                    previous_path.pop()
                previous_path.append(item)
                continue
            else: # item is a file.
                filename, hash_val = tuple(item.split('\t\t'))
                dir_path = "".join(str(directory) for directory in previous_path)
                f = FileObject(
                    name=filename,
                    parent=dir_path,
                    hash=hash_val,
                    hash_type=self.hash_type
                )
                files_with_full_data.append(f)
                if dir_end:
                    # Remove the last directory added to it.
                    if len(previous_path) != 0:
                        previous_path.pop()
        temp_list = copy.deepcopy(files_with_full_data)
        for f1 in files_with_full_data:
            # Remove the redundant item.
            if f1 is None:
                continue
            duplicates = []
            for f2 in temp_list:
                if f2 is None:
                    continue

                if f1 == f2:
                    temp_list[temp_list.index(f2)] = None
                    continue

                if f1.hash == f2.hash:
                    dupe = temp_list[temp_list.index(f2)]
                    temp_list[temp_list.index(f2)] = None
                    files_with_full_data[files_with_full_data.index(f2)] = None
                    duplicates.append(dupe)
            if duplicates != []:
                duplicate_files.append((f1, duplicates))
        if duplicate_files == []:
            print("No duplicate files found.", file=self.output_stream)
        else:
            if self.output_stream != sys.stdout:
                for f, l in duplicate_files:
                    print(f"\n\nFile, {f.name}, with hash, {f.hash}, in directory, {f.parent}, has the "
                          f"following duplicates:", file=self.output_stream)
                    for item in l:
                        print(f"{item.parent}{os.sep}{item.name} with hash {item.hash}",
                              file=self.output_stream)
                print(f"Duplicate report completed.", file=self.output_stream)
                self.output_stream.close()
                print(f"Report completed and printed to {self._output_file}.")
            else:
                for f, l in duplicate_files:
                    print(f"File, {f.name}, with hash, {f.hash}, in directory, {f.parent}, has the "
                          f"following duplicates:")
                    for item in l:
                        print(f"{item.parent}{os.sep}{item.name} with hash {item.hash}")
                    print(f"Duplicate report completed.")


class _TreeDiagramGenerator:
    def __init__(self, root_dir, dir_only=False, hash_type='she256',
                 suppress_hash=False, verbose=False):
        """
        This method requires the filepath to the root directory where the
        _TreeGenerator will begin. This is x required parameter, but it
        may be x relative path instead of an absolute path. This class adds
        an important attribute to DirectoryTree.
        :param root_dir: str of x filepath
        :param dir_only: bool, defaults to False, used to generate directory only
            listing
        :param hash_type: str, type of hash algorithm to use on the files
            See file_hash in functions for details on supported algorithms.
        :param suppress_hash: bool, defaults to False, suppresses hash output in the
            directory tree output
        :param verbose: bool, defaults to False, allows extra messages to appear as the
            program performs its work
        """
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._hash_type = hash_type
        self._suppress_hash = suppress_hash
        self._verbose = verbose
        self._tree = []
        print(self)

    def __str__(self):
        s = (f"_TreeDiagramGenerator:\n"
             f"_root_dir: {self._root_dir}. _dir_only: {self._dir_only}.\n"
             f"_hash_type: {self._hash_type}. _suppress_hash: {self._suppress_hash}\n"
             f"_verbose: {self._verbose}.\n"
             f"_tree: {self._tree}\n"
             f"End of _TreeDiagramGenerator")
        return s

    @staticmethod
    def _spin_clock():
        for frame in cycle(r'-\|/'):
            print('\r', frame, sep='', end='', flush=True)
            sleep(0.2)

    def build_tree(self):
        """
        This method builds the tree structure for x DirectoryTree, storing it
        in the internal attributes of this object as well as returning the
        structure to make it available to other classes.
        :return: _tree, x nested list of nodes forming the directory tree.
        """
        print(f"Added root directory, {self._root_dir}, to tree.")
        self._tree_head()
        print(f"Recursing subdirectories collecting data:", flush=True)
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
        on the object itself. directory is x required argument and is the
        directory that this method will traverse.
        :param directory: str, directory name
        :param prefix: str, allows the addition of spacers to the program.
        :return: None
        """
        print(f"Searching {directory}...", flush=True)
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for idx, entry in enumerate(entries):
            connector = ELBOW if idx == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(entry, idx, entries_count, prefix, connector)
            else:
                if self._suppress_hash:
                    hash_val = None
                else:
                    hash_val = file_hash(entry)
                self._add_file(entry, prefix, connector, hash_val)

    def _prepare_entries(self, directory):
        """
        This internal method applies filters to the tree content based
        on boolean attributes of _TreeDiagramGenerator.
        :param directory: filepath
        :return: list of filepaths
        """
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        # _dir_only is the default of False.
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries

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
        if self._verbose:
            print(f"_TreeDiagramGenerator._add_directory: Working on directory, {directory}.")
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if idx != count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(directory=directory, prefix=prefix)

    def _add_file(self, file_entry, prefix, connector, hash_value=None):
        """
        This method adds the filename to the directory tree structure and
        diagram.
        :param file_entry: relative filepath to this file
        :param prefix: str, graphical representation of the spacing to the
            connector to the file's parent directory
        :param connector: str, graphical representation of the connection to
            the file's parent directory
        :param hash_value: str, hash value for the file, defaults to None
        :return: None, all action takes place internally
        """
        if self._verbose:
            print(f"_TreeDiagramGenerator._add_file: Working on file, {file_entry}.")
        if hash_value:
            self._tree.append(f"{prefix}{connector} {file_entry.name}\t\t{hash_value}")
        else:
            self._tree.append(f"{prefix}{connector} {file_entry.name}")
