#!/usr/bin/env python3
""" Writing strings to Redis """
import uuid
from redis import Redis
from typing import Union
UnionOfTypes = Union[str, bytes, int, float]


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
