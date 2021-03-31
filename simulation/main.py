import asyncio
import json
import logging
import websockets

logging.basicConfig()
web_dump = {
            "msg_type": "state_change",
            "msg_id": 0,
            "data": [
                {
                    "id": 1,
                    "crosses": [1, 2],
                    "clearing_time": 3
                },
                {
                    "id": 2,
                    "crosses": [3, 6],
                    "clearing_time": 6
                }

            ]
        }
STATE = {"value": 0}

USERS = set()


def state_event():
    return json.dumps(
        {
            "msg_type": "state_change",
            "msg_id": 0,
            "data": [
                {
                    "id": 1,
                    "crosses": [4, 5],
                    "clearing_time": 6
                },
                {
                    "id": 2,
                    "crosses": [1, 3],
                    "clearing_time": 8
                }

            ]
        }
    )


async def register(websocket):
    await websocket.send(json.dumps(web_dump))
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            print(data)
    finally:
        await unregister(websocket)


start_server = websockets.serve(counter, "localhost", 6969)

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
