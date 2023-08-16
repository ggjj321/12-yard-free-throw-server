from fastapi import FastAPI
import time
import redis

app = FastAPI()

@app.get("/get_shoot_result/{total_shoot_time}/{shoot_target}")
def read_root(total_shoot_time : int, shoot_target : int):
    red_server = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    grid_shoot_data = {}
    for grid_index in range(12):
        grid_shoot_data[grid_index] = 0
    
    red_server.set('shoot_time', 0)
    red_server.set('is_shoot_time', True)
    red_server.hmset('grid_shoot_data', grid_shoot_data)
    
    while int(red_server.get("shoot_time")) < int(total_shoot_time):
        time.sleep(0.05)

    grid_shoot_data = red_server.hgetall("grid_shoot_data")
    hit_rate = int(grid_shoot_data[str(shoot_target)]) / total_shoot_time
    hit_rate = str(int(hit_rate * 100)) + '%'
    offset_of_supporting_leg = "No Need"
    offset_of_shoot_point = "No Need"
                                         
    return {'grid_shoot_data' : red_server.hgetall("grid_shoot_data"),
            'hit_rate' : hit_rate,
            'offset_of_supporting_leg' : offset_of_supporting_leg,
            'offset_of_shoot_point' : offset_of_shoot_point
            }
