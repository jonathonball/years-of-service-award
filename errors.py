"""
Handles exceptions for various modules
"""
import functools
import sys
import redis
from redis.exceptions import RedisError

FILE_ERROR_STATUS_CODE   = 1
PILLOW_ERROR_STATUS_CODE = 1
REDIS_ERROR_STATUS_CODE  = 1

def handle_file_exceptions(func):
    """
    Handle exceptions related to interacting with files in general
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotADirectoryError as not_a_dir_error:
            print(f"NotADirectoryError: {str(not_a_dir_error)}")
        except FileNotFoundError as file_not_found_error:
            print(f"FileNotFoundError: {str(file_not_found_error)}")
        except PermissionError as permission_error:
            print(f"PermissionError: {str(permission_error)}")
        except IOError as io_error:
            print(f"IOError: {str(io_error)}")
        sys.exit(FILE_ERROR_STATUS_CODE)
    return wrapper

def handle_pillow_exception(func):
    """
    A decorator that catches exceptions from the Pillow library and provides advice on how to
    handle them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IOError, ValueError) as exception:
            print(f"Error: {str(exception)}.")
            advice = get_advice_for_pillow_exception(exception)
            print(f"Advice: {advice}")
        sys.exit(PILLOW_ERROR_STATUS_CODE)
    return wrapper

def get_advice_for_pillow_exception(exception):
    """
    A function that provides advice on how to handle specific exceptions from the Pillow library.
    """
    if isinstance(exception, IOError):
        return "IOError occurred. Check that the file exists and is readable."
    if isinstance(exception, ValueError):
        return "ValueError occurred. Check that the image format is supported."
    return "Good luck!"

def handle_redis_exceptions(func):
    """
    Error handling for a Redis() conneciton
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RedisError as exception:
            print(f"Error: {str(exception)}.")
            advice = get_advice_for_redis_exception(exception)
            print(f"Advice: {advice}")
            sys.exit(REDIS_ERROR_STATUS_CODE)
    return wrapper

def get_advice_for_redis_exception(exception: RedisError):
    """
    Generate string with troubleshooting advice.
    """
    if isinstance(exception, redis.exceptions.ConnectionError):
        return "Check the Redis server is running and accessible."
    if isinstance(exception, redis.exceptions.AuthenticationError):
        return "Check the Redis server password and authentication settings."
    if isinstance(exception, redis.exceptions.TimeoutError):
        return "Check if Redis server under load or increase timeouts."
    if isinstance(exception, redis.exceptions.WatchError):
        return "Retry the transaction after handling the WatchError."
    return "Refer to the Redis documentation or seek support from Redis community for help."

def handle_queue_exceptions(func):
    """
    Handle exceptions related to interacting with files in general
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as exception:
            message = get_advice_for_queue_exception(exception)
            print(message)
            print(f"Error: {str(exception)}")
        sys.exit(REDIS_ERROR_STATUS_CODE)
    return wrapper

def get_advice_for_queue_exception(exception):
    """
    Generate string for a image processing queue error
    """
    if isinstance(exception, ValueError):
        return "Queue name does not exist"
    if isinstance(exception, IndexError):
        return "Queue out of bounds"
    return "Good luck!"
