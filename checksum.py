"""
Functions for dealing with checksums
"""
import hashlib

def calculate_file_md5(filename):
    """
    Calculate md5sum of a file, reading it 4K bytes at a time
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
