#!/usr/bin/env python3
""" Writing strings to Redis """
import uuid
from redis import Redis
from typing import Union
UnionOfTypes = Union[str, bytes, int, float]
from functools import wraps


def count_calls(method):
    """ Counter of cache """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f'count:{method.__qualname__}'
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    """ History of cache """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method):
    """ Display the history of calls of a particular function. """
    input_key = f'{method.__qualname__}:inputs'
    output_key = f'{method.__qualname__}:outputs'
    count_key = f'count:{method.__qualname__}'
    count = method.__self__._redis.get(count_key)
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)
    print(f'{method.__qualname__} was called {count} times:')
    for input_, output in zip(inputs, outputs):
        print(f'{method.__qualname__}(*{input_}) -> {output}')


class Cache:
    """ Writing strings to Redis """
    def __init__(self):
        """ Store an instance of the Redis client """
        self._redis = Redis()
        self._redis.flushdb()


    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """ Takes a data argument and returns a string """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key


    def get(self, key: str,
            fn: Optional[Callable] = None) -> UnionOfTypes:
        """  convert the data back to the desired format. """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data


    def get_str(self, key: str) -> Optional[str]:
        """ automatically parametrize Cache.get with the
        correct conversion function. """
        return self.get(key, fn=lambda d: d.decode('utf-8'))


    def get_int(self, key: str) -> Optional[int]:
        """ automatically parametrize Cache.get with the
        correct conversion function. """
        return self.get(key, fn=int)
