"""
Interacts with a redis cache
"""
import sys
import redis
from redis.exceptions import RedisError

FALSE, FIRST = [0, 0]
REDIS_ERROR_RETURN_CODE = 1

queue_names = [
    'inspect',
    'convert',
    'rotate',
    'resize',
    'crop',
    'overlay',
    'output'
]

def handle_redis_exceptions(func):
    """
    Error handling for a Redis() conneciton
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RedisError as exception:
            print(f"Error: {str(exception)}.")
            advice = get_advice_for_exception(exception)
            print(f"Advice: {advice}")
            sys.exit(REDIS_ERROR_RETURN_CODE)
    return wrapper

def get_advice_for_exception(exception: RedisError):
    """
    Generate string with troubleshooting advice.
    """
    if isinstance(exception, redis.exceptions.ConnectionError):
        return "Check the Redis server is running and accessible."
    if isinstance(exception, redis.exceptions.AuthenticationError):
        return "Check the Redis server password and authentication settings."
    if isinstance(exception, redis.exceptions.TimeoutError):
        return "Check if there is a firewall between this app and the Redis server or increase timeouts."
    if isinstance(exception, redis.exceptions.WatchError):
        return "Retry the transaction after handling the WatchError."
    return "Refer to the Redis documentation or seek support from Redis community for help."

def create_file_data(name, path):
    """
    Generate a dict containing meta data about a filesystem file
    """
    file_data = {
      'name': name,
      'path': path
    }
    for queue_name in queue_names:
        file_data[queue_name] = FALSE
    return file_data

@handle_redis_exceptions
def init_cache():
    """
    Initializes a connection to a Redis cache
    """
    cache = redis.Redis(host='localhost', port='6379', decode_responses=True)
    return cache

@handle_redis_exceptions
def get_file_data(cache, key):
    """
    Retrieve meta data about a filesystem file using a hash key
    """
    data = cache.hgetall(key)
    return data

@handle_redis_exceptions
def set_file_data(cache, key, data):
    """
    Store meta data about a filesystem file using a hash key
    """
    cache.hmset(key, data)

@handle_redis_exceptions
def add_to_queue(cache, queue, data):
    """
    Push a data item into a Redis FIFO queue
    """
    cache.lpush(queue, data)

@handle_redis_exceptions
def get_next_queue_item(cache, queue):
    """
    Get the next data item from a Redis FIFO queue
    """
    item = cache.rpop(queue)
    return item

@handle_redis_exceptions
def flushall(cache):
    """
    Call flushall on a Redis cache
    """
    cache.flushall()

def get_first_queue_name():
    """
    Get the name of the initial redis queue
    """
    return queue_names[FIRST]

def get_next_queue_name(current_name):
    """
    Get the next queue name based on the current
    """
    try:
        index = queue_names.index(current_name)
        index += 1
        try:
            queue_name = queue_names[index]
        except IndexError as exception:
            print(f'Queue name error: {str(exception)}')
            sys.exit(REDIS_ERROR_RETURN_CODE)
    except ValueError as exception:
        print(f'Queue name error: {str(exception)}')
        sys.exit(REDIS_ERROR_RETURN_CODE)
    return queue_name
