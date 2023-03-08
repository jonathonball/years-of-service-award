import os
from memoize import memoize

extensions = ('.png', '.jpg', '.jpeg')

@memoize
def get_app_dirs():
  work_dir = os.environ.get('YOSA_WORK_DIR')
  if not work_dir or not os.path.isdir(work_dir):
    work_dir = os.path.dirname(os.path.abspath(__file__))
  input_dir = os.path.join(work_dir, 'input')
  return {
    'work': work_dir,
    'input': input_dir
  }

def get_image_full_path(image_file):
  dirs = get_app_dirs()
  return os.path.join(dirs['input'], image_file)

def get_image_files():
  dirs = get_app_dirs()
  return [ f for f in os.listdir(dirs['input']) if f.lower().endswith(extensions) ]
