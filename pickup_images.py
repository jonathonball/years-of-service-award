"""
Pickup images for processing by this application
"""
import time
import filesystem
import checksum
import cache

dirs       = filesystem.get_app_dirs()
cache_conn = cache.init_cache()

while True:
    image_files = filesystem.get_image_files()
    for image_file in image_files:
        image_path = filesystem.get_image_input_path(image_file)
        IMAGE_HASH = checksum.calculate_file_md5(image_path)
        cache_data = cache.get_file_data(cache_conn, IMAGE_HASH)
        if not cache_data:
            file_data = filesystem.get_file_contents(image_path)
            cache_data = cache.create_file_data(image_file, file_data)
            cache.set_file_data(cache_conn, IMAGE_HASH, cache_data)
            print(f'Picked up {str(IMAGE_HASH)} ({str(image_file)})')
            QUEUE_NAME = cache.get_first_queue_name()
            cache.add_to_queue(cache_conn, QUEUE_NAME, IMAGE_HASH)
            print(f'Image {IMAGE_HASH} added to "{QUEUE_NAME}" queue')
            filesystem.remove_file(image_path)
            print(f'Image file removed: {image_path}')
    time.sleep(1)
