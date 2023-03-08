import os
from memoize import memoize
import sys

extensions = ('.png', '.jpg', '.jpeg')
env_prefix = 'YOSA'
env_suffix = 'DIR'

def validate_dir(path):
  return path and os.path.isdir(path)

def get_dir_path(dir_name):
  envvar_name = '_'.join([env_prefix, dir_name.upper(), env_suffix])
  dir_path = os.getenv(envvar_name)
  if validate_dir(dir_path):
    return dir_path
  script_path = os.path.dirname(os.path.abspath(__file__))
  dir_path = os.path.join(script_path, dir_name)
  if validate_dir(dir_path):
    return dir_path
  print(f"Unabled to load {dir_name}: {dir_path}")

@memoize
def get_app_dirs():
  input_dir = get_dir_path('input')
  output_dir = get_dir_path('output')
  return {
    'input': input_dir,
    'output': output_dir
  }

def get_image_full_path(image_file):
  dirs = get_app_dirs()
  return os.path.join(dirs['input'], image_file)

def get_image_files():
  dirs = get_app_dirs()
  filelist = os.listdir(dirs['input'])
  return [ f for f in filelist if f.lower().endswith(extensions) ]
