import redis
import json

r = redis.Redis(host="localhost", port=6379)

def get_cache(query):
    result = r.get(query)
    if result:
        return json.loads(result)

    return None

def set_cache(query, answer):
    r.set(query, json.dumps(answer))