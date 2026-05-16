import redis
import json
import os
redis_url = os.getenv("REDIS_URL")
r = redis.from_url(redis_url, decode_responses=True)
def get_cache(key):
    data = r.get(key)
    if data:
        return json.loads(data)
    return None
def set_cache(key, value, ttl=60):
    r.setex(key, ttl, json.dumps(value))
def delete_cache(pattern):
    for key in r.scan_iter(pattern):
        r.delete(key)

