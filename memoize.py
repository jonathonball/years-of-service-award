"""
Functions wrappers to cache results between calls
"""

def memoize(func):
  """
  Place function results into a dict and return it if called again
  """
  cache = {}

  def wrapper():
    if () not in cache:
      cache[()] = func()
    return cache[()]

  return wrapper
