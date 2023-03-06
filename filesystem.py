import os

def get_app_dirs():
  work_dir = os.environ.get('YOSA_WORK_DIR')
  if not work_dir or not os.path.isdir(work_dir):
    work_dir = os.path.dirname(os.path.abspath(__file__))
  input_dir = os.path.join(work_dir, 'input')
  return {
    'work': work_dir,
    'input': input_dir
  }
