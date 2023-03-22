"""
Interacts with a redis cache
"""
import redis
import errors

FALSE, FIRST = [0, 0]

queue_names = [
    'inspect',
    'convert',
    'rotate',
    'resize',
    'crop',
    'overlay',
    'output',
]

@errors.handle_redis_exceptions
def create_file_data(name, data):
    """
    Generate a dict containing meta data about a filesystem file
    """
    file_data = {
      'name': name,
      'data': data,
    }
    for queue_name in queue_names:
        file_data[queue_name] = FALSE
    file_data['error'] = FALSE
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
def get_first_queue_name():
    """
    Get the name of the initial redis queue
    """
    return queue_names[FIRST]

@errors.handle_queue_exceptions
def get_next_queue_name(current_name):
    """
    Get the next queue name based on the current
    """
    index = queue_names.index(current_name)
    index += 1
    queue_name = queue_names[index]
    return queue_name
