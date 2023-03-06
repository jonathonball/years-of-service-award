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
