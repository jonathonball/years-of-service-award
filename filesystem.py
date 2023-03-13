"""
Interacts with the local filesystem
"""
import os
from memoize import memoize

EXTENSIONS = ('.png', '.jpg', '.jpeg')
ENV_PREFIX = 'YOSA'
ENV_SUFFIX = 'DIR'

def validate_dir(path):
    """
    Validate path is a dir
    """
    return path and os.path.isdir(path)

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

# change this method to indicate it's for input only or refactor
def get_image_input_path(image_file):
    """
    Get path for input image
    """
    dirs = get_app_dirs()
    return os.path.join(dirs['input'], image_file)

def get_image_files():
    """
    Get a list of images in a directory by file extension
    """
    dirs     = get_app_dirs()
    filelist = os.listdir(dirs['input'])
    return [ f for f in filelist if f.lower().endswith(EXTENSIONS) ]
