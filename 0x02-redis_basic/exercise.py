#!/usr/bin/env python3
""" Writing strings to Redis """
import uuid
from redis import Redis
from typing import Union


class Cache:
    """ Writing strings to Redis """
    def __init__(self):
        """ Store an instance of the Redis client """
        self._redis = Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Takes a data argument and returns a string """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
