import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def get_cache(key):
    return r.get(key)

def set_cache(key, value):
    r.setex(key, 60, value)