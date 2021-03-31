import pygame
# WS server example

import asyncio
import websockets
from TrafficInfo import TrafficInfo
import json


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
            traffic = TrafficInfo(data['id'], data['state'],)
            crosses.append(traffic.get_croses())
        traffics['data'] = crosses
        await websocket.send(json.dumps(traffics))


start_server = websockets.serve(server, "localhost", 6969)

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
