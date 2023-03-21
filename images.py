"""
Functions for working with images
"""
from PIL import Image, ExifTags
from memoize import memoize
import errors

@errors.handle_pillow_exception
def open_image(file_path):
    """
    Open an image file
    """
    image = Image.open(file_path)
    return image

@memoize
def get_orientation_exif_key():
    """
    Determine the key related to exif orientation
    """
    orientation_key = None
    for orientation_key in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation_key]=='Orientation':
            break
    if orientation_key is None:
        raise ValueError("Cannot determine exif orientation on this system")
    return orientation_key

@errors.handle_pillow_exception
def get_orientation_correction(image):
    """
    Determine how many degrees an image must be rotated
    """
    orientation_key = get_orientation_exif_key()
    try:
        exif_data       = image.getexif()
        orientation     = exif_data[orientation_key]
        if orientation == 3:
            correction_degrees = 180
        elif orientation == 6:
            correction_degrees = 270
        elif orientation == 8:
            correction_degrees = 90
        else:
            correction_degrees = 0
    except (AttributeError, KeyError, ValueError):
        correction_degrees = 0
    return correction_degrees
