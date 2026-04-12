import redis

r = redis.Redis(host="redis", port=6379)

def get_cache(key):
    try:
        val = r.get(key)
        return val.decode() if val else None
    except:
        return None

def set_cache(key, value):
    try:
        r.set(key, value)
    except:
        pass
