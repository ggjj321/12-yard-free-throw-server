import redis
import asyncio
import websockets
import time

# 接受客戶端連接

red_server = redis.Redis(host='redis', port=6379, decode_responses=True)

print("socket start")

async def hello(websocket):
    while True:
        data = await websocket.recv()
        if data == "start shoot":
            red_server.set('is_shoot_time', "True")
            r = f'success'
            await websocket.send(r)
        while red_server.get("is_shoot_time") == "True":
            time.sleep(0.05)

        shoot_time = red_server.get("shoot_time")
        total_shoot_time = red_server.get("total_shoot_time")

        preesent_shoot_field = red_server.get("preesent_shoot_field")
        
        print(total_shoot_time, preesent_shoot_field)

        if shoot_time == red_server.get("total_shoot_time"):
            shoot_time = "compelete"

        if preesent_shoot_field != "not_set":
            r = f'{shoot_time} {preesent_shoot_field}'
            await websocket.send(r)

start_server = websockets.serve(hello, "0.0.0.0", 2222)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()