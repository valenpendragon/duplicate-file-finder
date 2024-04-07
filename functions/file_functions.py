import hashlib
import os
import glob
from collections import namedtuple


FileObject = namedtuple('File_Object',
                        ['name', 'parent', 'hash', 'hash_type'])
DirectoryObject = namedtuple('DirectoryObject',
                             ['name', 'parent'])


def file_hash(filename, algorithm='sha256'):
    """
    file_hash does a binary read of the file defined by filename,
    builds a file_digest, using the specified algorithm string.
    Valid algorithms are: sha224, sha256, sha384, sha512, sha3_224
    sha3_256, sha3_384, and sha3_512. sha1 collisions have been
    discovered. So, it is not included. Setting algorithm to an
    algorithm that has not been implemented results in a
    NotImplementedError.
    :param filename: filename (str)
    :param algorithm: str
    :return: str (hexadecimal hash string)
    """
    # Create a hash object to store the digest.
    match algorithm:
        case 'sha224':
            hash_object = hashlib.sha224()
        case 'sha256':
            hash_object = hashlib.sha256()
        case 'sha384':
            hash_object = hashlib.sha384()
        case 'sha512':
            hash_object = hashlib.sha512()
        case 'sha3_224':
            hash_object = hashlib.sha3_224()
        case 'sha3_256':
            hash_object = hashlib.sha3_256()
        case 'sha3_384':
            hash_object = hashlib.sha3_384()
        case 'sha3_512':
            hash_object = hashlib.sha3_512()
        case _ :
            error_msg = f"Algorithm, {algorithm}, has not been implemented."
            raise NotImplementedError(error_msg)

    # Open the file and start pulling in blocks of data.
    with open(filename, 'rb') as f:
        # Read a 64k data block and update the digest each block.
        file_end = False
        while not file_end:
            data = f.read(65536)
            file_end = not data
            if not file_end:
                hash_object.update(data)

    # Return hexadecimal digest string.
    return hash_object.hexdigest()


if __name__ == "__main__":
    path = '../data'
    print(f"path: {path}")
    search_str = f"{path}/*.*"
    for alg in ['sha224', 'sha256', 'sha384', 'sha512',
                'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512']:
        print(f"Performing algorithm, {alg}, on files in {path}.")
        for filename in glob.glob(search_str):
            print(f"{filename}: {file_hash(filename, alg)}")