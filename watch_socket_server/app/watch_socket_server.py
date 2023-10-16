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
        r = f'finish'
        await websocket.send(r)
        # time.sleep(2)
        # r = f'finish'
        # await websocket.send(r)
        # print(f'Server Sent: {r}')

start_server = websockets.serve(hello, "0.0.0.0", 2222)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()