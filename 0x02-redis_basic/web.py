#!/usr/bin/env python3
""" web.py """
import requests
from redis import Redis

redis = Redis()


def get_page(url: str) -> str:
    """ Implementing an expiring web cache and tracker """
    count_key = f'count:{url}'
    cache_key = f'cache:{url}'
    redis.incr(count_key)
    content = redis.get(cache_key)
    if content is None:
        response = requests.get(url)
        content = response.text
        redis.setex(cache_key, 10, content)
    return content
