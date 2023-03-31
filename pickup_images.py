"""
Pickup images for processing by this application
"""
import time
import filesystem
import checksum
import cache

APPLICATION_SLEEP_INTERVAL = 1
dirs       = filesystem.get_app_dirs()
cache_conn = cache.init_cache()

while True:
    image_files = filesystem.get_image_file_list()
    for image_file in image_files:
        image_path = filesystem.get_file_input_path(image_file)
        IMAGE_HASH = checksum.calculate_file_md5(image_path)
        cache_data = cache.get_file_data(cache_conn, IMAGE_HASH)
        if not cache_data:
            print(f'{IMAGE_HASH}: Picked up {image_file}')
            file_data = cache.create_file_metadata(image_file, IMAGE_HASH)
            cache.set_file_data(cache_conn, IMAGE_HASH, file_data)
            QUEUE_NAME = cache.get_next_queue_name()
            cache.add_to_queue(cache_conn, QUEUE_NAME, IMAGE_HASH)
            print(f'{IMAGE_HASH}: Added to "{QUEUE_NAME}" queue')
    time.sleep(APPLICATION_SLEEP_INTERVAL)
