from fastapi import FastAPI
import time
from soccer_detect_calculate import *
import redis

app = FastAPI()

@app.get("/get_shoot_result/{total_shoot_time}")
def read_root(total_shoot_time : int):
    red_server = redis.Redis(host='localhost', port=6379, decode_responses=True)
    red_server.set('shoot_time', 0)
    while int(red_server.get("shoot_time")) < int(total_shoot_time):
        time.sleep(0.05)
    return {"message": "Hello, FastAPI!"}
