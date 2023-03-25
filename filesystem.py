"""
Interacts with the local filesystem
"""
import os
from memoize import memoize
import errors
import chardet

FILE_EXTENSIONS = ('.png', '.jpg', '.jpeg')
ENV_PREFIX = 'YOSA'
ENV_SUFFIX = 'DIR'

@errors.handle_file_exceptions
def validate_dir(path):
    """
    Validate path is a dir
    """
    return path and os.path.isdir(path)

@errors.handle_file_exceptions
def get_dir_path(dir_name):
    """
    Resolve the path of a directory
    """
    envvar_name = '_'.join([ENV_PREFIX, dir_name.upper(), ENV_SUFFIX])
    dir_path    = os.getenv(envvar_name)
    if validate_dir(dir_path):
        return dir_path
    script_path = os.path.dirname(os.path.abspath(__file__))
    dir_path    = os.path.join(script_path, dir_name)
    if validate_dir(dir_path):
        return dir_path
    print(f"Unabled to load {dir_name}: {dir_path}")
    raise NotADirectoryError(f"'{dir_path} is not a directory")

@memoize
def get_app_dirs():
    """
    Return a dict of resolved and validated paths used by this application
    """
    input_dir  = get_dir_path('input')
    output_dir = get_dir_path('output')
    return {
        'input':  input_dir,
        'output': output_dir,
    }

def get_file_input_path(file):
    """
    Get path for input image
    """
    dirs = get_app_dirs()
    return os.path.join(dirs['input'], file)

@errors.handle_file_exceptions
def get_image_file_list():
    """
    Get a list of images in a directory by file extension
    """
    dirs     = get_app_dirs()
    filelist = os.listdir(dirs['input'])
    return [ f for f in filelist if f.lower().endswith(FILE_EXTENSIONS) ]

@errors.handle_file_exceptions
def get_file_contents(file_path):
    """
    Reads a file into memory
    """
    data = None
    with open(file_path, 'rb') as file_handle:
        data = file_handle.read()
    return data

@errors.handle_file_exceptions
def remove_file(file_path):
    """
    Remove a file from the filesystem
    """
    os.remove(file_path)

def get_file_encoding(image_data):
    """
    Gets the encoding of a file
    """
    encoding = chardet.detect(image_data)['encoding']
    return encoding
