import hashlib
import os
import glob


def file_hash(filename, algorithm='sha256'):
    """
    file_hash does a binary read of the file defined by filename,
    builds a file_digest, using the specified algorithm string.
    :param filename: filename (str)
    :param algorithm: str
    :return: str (hexadecimal hash string)
    """
    # Create a hash object to store the digest.
    hash_object = hashlib.sha256()
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
    for filename in glob.glob(search_str):
        print(f"{filename}: {file_hash(filename)}")