from pdx.cache.in_memory_cache import InMemoryCache
from functools import wraps


def agent_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Access self properties here
        _agent_cache = args[0]._cache
        print(f"Inside the decorator, before func call.")
        _func_return = func(*args, **kwargs)
        print(f"Inside the decorator, after func call.")
        return _func_return
    return wrapper
