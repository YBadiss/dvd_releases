from datetime import timedelta
import logging
import os

from redis import Redis

from secret import REDIS_PWD

logger = logging.getLogger()

ENV_NAME = os.environ.get("ENV_NAME")


def cached_call(key, func, serialize, deserialize, ttl=None):
    ttl = ttl if ttl is not None else timedelta(hours=2)
    cache = __get_cache()
    full_key = "{}.{}".format(ENV_NAME, key)
    cached_value = cache.get(full_key)
    if cached_value is None:
        value = func()
        logger.info("{}: saving value in cache".format(func.__name__))
        cache.setex(full_key, serialize(value), ttl)
    else:
        logger.info("{}: retrieved value from cache".format(func.__name__))
        value = deserialize(cached_value)
    return value


def cache_it(key, serialize, deserialize, ttl=None):
    def cache_decorator(func):
        def wrapper():
            return cached_call(key, func, serialize, deserialize, ttl)
        return wrapper
    return cache_decorator


def __get_cache():
    return Redis(host="redis-16045.c3.eu-west-1-2.ec2.cloud.redislabs.com",
                 port=16045,
                 password=REDIS_PWD)

