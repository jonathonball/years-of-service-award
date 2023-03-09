import filesystem
import hash
import cache

dirs       = filesystem.get_app_dirs()
cache_conn = cache.init_cache()

image_files = filesystem.get_image_files()
for image_file in image_files:
  image_path = filesystem.get_image_full_path(image_file)
  image_hash = hash.calculate_file_md5(image_path)
  cache_data = cache.get_file_data(cache_conn, image_hash)
  if not cache_data:
    cache_data = cache.create_file_data(image_file, image_path)
    cache.set_file_data(cache_conn, image_hash, cache_data)
    print(f'Picked up {str(image_hash)} ({str(image_file)})')
    cache.add_to_queue(cache_conn, 'rotate', image_hash)
