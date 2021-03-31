import pygame
# WS server example

import asyncio
import websockets
from TrafficInfo import TrafficInfo
import json
import time

dump_array = {
    "msg_type": "notify_state_change",
    "msg_id": 1, "data":
        [
            {"id": 1, "crosses": [5, 3], "clearing_time": 9},
            {"id": 2, "crosses": [2, 4], "clearing_time": 9}
        ]
}
PORT = 6968


async def send_state_message(ws, send_all: bool):
    await ws.send(json.dumps(dump_array))


def change_light_states(json):
    x = {
        "msg_type": "state_change",
        "msg_id": 1, "data":
            [
                {"id": 1, "crosses": [1, 4], "clearing_time": 7},
                {"id": 2, "crosses": [1, 4], "clearing_time": 7}
            ]
    }
    return x


async def server_fn(ws, path):
    async def send_updates():
        nonlocal ws

        try:
            first = True
            while True:
                time.sleep(1)
                await send_state_message(ws, first)
                first = False
        except Exception as e:
            print(f'Connection errored: {e}')

    future = asyncio.create_task(send_updates())

    try:
        while True:
            update = await ws.recv()
            change_light_states(update)
    except Exception as e:
        print(f'Connection errored: {e}')

    await future


start_server = websockets.serve(server_fn, "localhost", 6968)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

"""
async def server(websocket, path):
    async for message in websocket:
        traffic_json = json.loads(message)
        traffic_data = traffic_json['data']
        traffics = {
            "msg_type": "state_change",
            "msg_id": 1,
            "data": []
        }
        crosses = []
        for data in traffic_data:
            traffic = TrafficInfo(data['id'], data['state'], )
            crosses.append(traffic.get_croses())
        traffics['data'] = crosses
        await websocket.send(json.dumps(traffics))

    print("test")
    time.sleep(1)
    await websocket.send(dump_array)


start_server = websockets.serve(server, "localhost", PORT)
print(f"server runs on port: {PORT}")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

# pygame.init()
# screen = pygame.display.set_mode((700, 500))
# pygame.display.set_caption("trafic simulation")
# run = True
# while run:
#     for event in pygame.event.get():
#         print(event)
#         if event.type == 256:  # quit event
#             run = False
#         screen.fill((50, 50, 50))
#         pygame.display.flip()
"""
