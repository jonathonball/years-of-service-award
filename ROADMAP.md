# Planned Application Flow
- pickup_images.py
    - monitor input directory
    - finds supported image files
    - calculates checksum
    - check redis for checksums of found files
    - check redis if file needs processed
    - checks file validity
    - if image is jpg, queue convert job
    - if image is png, queue overlay job
- convert_images.py
    - monitors convert queue