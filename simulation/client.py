# WS client example

import asyncio
import websockets
import json


async def hello():
    uri = "ws://localhost:6968"
    async with websockets.connect(uri) as websocket:
        print("connected!")
        jn = {
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
        name = json.dumps(jn)

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hello())
