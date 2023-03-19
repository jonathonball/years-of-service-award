"""
Handles exceptions for various modules
"""
import functools
import sys

FILE_ERROR_STATUS_CODE = 1

def handle_file_exceptions(func):
    """
    Handle exceptions related to interacting with files in general
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotADirectoryError as nadr:
            print(f"NotADirectoryError: {nadr}")
        except FileNotFoundError as fnfe:
            print(f"FileNotFoundError: {fnfe}")
        except PermissionError as pex:
            print(f"PermissionError: {pex}")
        except IOError as ioe:
            print(f"IOError: {ioe}")
        sys.exit(FILE_ERROR_STATUS_CODE)
    return wrapper
