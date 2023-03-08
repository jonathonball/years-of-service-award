def memoize(func):
  cache = {}

  def wrapper():
    if () not in cache:
      cache[()] = func()
    return cache[()]

  return wrapper
