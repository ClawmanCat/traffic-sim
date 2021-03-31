# WS client example

import asyncio
import websockets
import json


async def hello():
    uri = "ws://localhost:6964"
    async with websockets.connect(uri) as websocket:
        print("connected!")
        x = await websocket.recv()
        print(f"< {x}")
        jn = {
            "msg_type": "perform_state_change",
            "msg_id": 0,
            "data": [
                {
                    "id": 1,
                    "state": 'green'
                },
                {
                    "id": 2,
                    'state': 'green'
                }

            ]
        }
        name = json.dumps(jn)
        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")


asyncio.get_event_loop().run_until_complete(hello())
