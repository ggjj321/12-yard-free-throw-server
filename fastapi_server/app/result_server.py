from fastapi import FastAPI
import time
import redis
import json

from .firebase_data_process import *
from .suggest import *

app = FastAPI()
red_server = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.get("/get_shoot_result/{total_shoot_time}/{shoot_target}")
def read_root(total_shoot_time : int, shoot_target : int):
    grid_shoot_data = {}
    for grid_index in range(12):
        grid_shoot_data[str(grid_index)] = 0
    
    red_server.set('shoot_time', 0)
    red_server.set('is_shoot_time', "True")
    grid_shoot_data_json = json.dumps(grid_shoot_data)   
    red_server.set("grid_shoot_data", grid_shoot_data_json)
    
    while int(red_server.get("shoot_time")) < int(total_shoot_time):
        time.sleep(0.05)

    grid_shoot_data_json = red_server.get("grid_shoot_data")
    grid_shoot_data = json.loads(grid_shoot_data_json)

    convert_grid_shoot_data = {}

    for i in range(1, 13):
        convert_grid_shoot_data[i] = grid_shoot_data[str(i - 1)]

    suggest_result = suggest(int(shoot_target), int(total_shoot_time), convert_grid_shoot_data)
    save_data_to_firebase_db(convert_grid_shoot_data, suggest_result["percentage"], suggest_result["pivot_foot_bias"], suggest_result["hit_pos"])
                                         
    return "success"
