"""
Interacts with a redis cache
"""
import redis
import errors

FALSE, FIRST = [0, 0]

# {
#     'name': 'IMG_20210805_074634.jpg',
#     'path': '/opt/years-of-service-award/input/IMG_20210805_074634.jpg',
#     'hash': '1aa53ef6c16c9faf580383fed4e2ce81',
#     'inspect': '0',
#     'convert': '0',
#     'rotate': '0',
#     'resize': '0',
#     'crop': '0',
#     'overlay': '0',
#     'output': '0',
#     'error': '0',
# }

queue_names = [
    'triage',
    'convert',
    'rotate',
    'resize',
    'crop',
    'overlay',
    'output',
]

@errors.handle_redis_exceptions
def create_file_metadata(name, file_hash):
    """
    Generate a dict containing meta data about a filesystem file

    Parameters
    ----------
    name : str
    file_hash : str

    Returns
    -------
    file_data : dict
    """
    file_data = {
        'name': name,
        'hash': file_hash,
        'error': FALSE,
        'error_reason': '',
        'state': 'Getting picked up',
    }
    for queue_name in queue_names:
        file_data[queue_name] = FALSE
    return file_data

@errors.handle_redis_exceptions
def init_cache():
    """
    Initializes a connection to a Redis cache
    """
    cache = redis.Redis(host='localhost', port='6379', decode_responses=True)
    return cache

@errors.handle_redis_exceptions
def get_file_data(cache, key):
    """
    Retrieve meta data about a filesystem file using a hash key
    """
    data = cache.hgetall(key)
    return data

@errors.handle_redis_exceptions
def set_file_data(cache, key, data):
    """
    Store meta data about a filesystem file using a hash key
    """
    cache.hmset(key, data)

@errors.handle_redis_exceptions
def add_to_queue(cache, queue, data):
    """
    Push a data item into a Redis FIFO queue
    """
    cache.lpush(queue, data)

@errors.handle_redis_exceptions
def get_next_queue_item(cache, queue):
    """
    Get the next data item from a Redis FIFO queue
    """
    item = cache.rpop(queue)
    return item

@errors.handle_redis_exceptions
def flushall(cache):
    """
    Call flushall on a Redis cache
    """
    cache.flushall()

@errors.handle_queue_exceptions
def get_next_queue_name(current_name = None):
    """
    Get the next queue name based on the current
    """
    if not current_name:
        return queue_names[FIRST]
    index = queue_names.index(current_name)
    index += 1
    queue_name = queue_names[index]
    return queue_name
