import redis
import sys

def init_cache():
  try:
    cache = redis.Redis(host='localhost', port='6379', decode_responses=True)
  except Exception as e:
    print(f'Cannot open connection to redis cache: "{str(e)}"')
    sys.exit(1)
  return cache

def get_file_data(cache, hash):
  try:
    data = cache.hgetall(hash)
  except Exception as e:
    print(f'Unable to query cache: "{str(e)}"')
    sys.exit(1)
  return data

def set_file_data(cache, hash, data):
  try:
    cache.hmset(hash, data)
  except Exception as e:
    print(f'Unable to set cache item: "{str(e)}"')
    sys.exit(1)

def create_file_data(name, path):
  return {
    'name': name,
    'path': path,
    'processed': 0
  }

def add_to_queue(cache, queue, data):
  try:
    cache.rpush(queue, data)
  except Exception as e:
    print(f'Cannot add item to {queue}: {data}')
    sys.exit(1)

def get_next_queue_item(cache, queue):
  try:
    item = cache.rpop(queue)
  except Exception as e:
    print(f'Cannot retrieve queue item from {queue}')
    sys.exit(1)
  return item
