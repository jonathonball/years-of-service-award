import os
import filesystem
import hash
import cache

# Generate a list of dirs used by this app
dirs = filesystem.get_app_dirs()

# Start cache service
cache_conn = cache.init_cache()

# Iterate through image files
extensions = ('.png', '.jpg', '.jpeg')
image_files = [ f for f in os.listdir(dirs['input']) if f.lower().endswith(extensions) ]
for image_file in image_files:
  # Generate full path to image
  image_path = os.path.join(dirs['input'], image_file)
  # Calculate image checksum
  image_hash = hash.calculate_file_md5(image_path)
  # Fetch image data from cache
  cache_data = cache.get_file_data(cache_conn, image_hash)
  # Pickup new images
  if not cache_data:
    cache_data = cache.create_file_data(image_file, image_path)
    cache.set_file_data(cache_conn, image_hash, cache_data)
    print(f'Picked up {str(image_hash)} ({str(image_file)})')
