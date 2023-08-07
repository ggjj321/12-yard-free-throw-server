import redis
import time

red_server = redis.Redis(host='localhost', port=6379, decode_responses=True)

time.sleep(3)
red_server.set('shoot_time', 10)
