import redis
import time

red_server = redis.Redis(host='redis', port=6379, decode_responses=True)

time.sleep(3)

grid_shoot_data = red_server.hgetall("grid_shoot_data")
grid_shoot_data[1] = 9
grid_shoot_data[2] = 1
red_server.hmset('grid_shoot_data', grid_shoot_data)

red_server.set('shoot_time', 10)
