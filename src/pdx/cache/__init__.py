from pdx.cache.in_memory_cache import InMemoryCache
from functools import wraps


def agent_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Access self properties here
        _agent_cache = args[0]._cache
        if _agent_cache == None:
            _func_return = func(*args, **kwargs)
            return _func_return
        else:
            _agent_id = args[0]._agent_id
            if len(args) >= 2:
                _agent_request = args[1]
            else:
                _agent_request = kwargs.get('request', {})

            _cached_response = _agent_cache.lookup(
                agent_id=_agent_id, agent_request=_agent_request)
            if _cached_response:
                return _cached_response
            else:
                _func_return = func(*args, **kwargs)
                _agent_cache.update(
                    agent_id=_agent_id, agent_request=_agent_request, agent_response=_func_return)
                return _func_return
    return wrapper


def aagent_cache(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Access self properties here
        _agent_cache = args[0]._cache
        if _agent_cache == None:
            _func_return = await func(*args, **kwargs)
            return _func_return
        else:
            _agent_id = args[0]._agent_id
            if len(args) >= 2:
                _agent_request = args[1]
            else:
                _agent_request = kwargs.get('request', {})

            _cached_response = _agent_cache.lookup(
                agent_id=_agent_id, agent_request=_agent_request)
            if _cached_response:
                return _cached_response
            else:
                _func_return = await func(*args, **kwargs)
                _agent_cache.update(
                    agent_id=_agent_id, agent_request=_agent_request, agent_response=_func_return)
                return _func_return
    return wrapper
