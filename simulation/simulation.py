import websockets
import asyncio
import json
import time


dummy_message = {
    "msg_type": "notify_state_change",
    "msg_id": 0,
    "data": [
        {
            "id": 0,
            "crosses": [1],
            "clearing_time": 3.0
        },
        {
            "id": 1,
            "crosses": [0],
            "clearing_time": 6.0
        }
    ]
}


# Only send a new message if at least 3 seconds have elapsed since the last one.
last_state_change = 0

async def notify_state_change(ws):
    global last_state_change
    if time.time() - last_state_change < 3.0: return
    
    await ws.send(json.dumps(dummy_message))
    last_state_change = time.time()
    
    
async def on_state_change_received(ws):
    async for message in ws:
        print(f'Received new state:\n{message}')


async def on_client_connected(ws, path):
    print(f'Client connected from {ws.remote_address[0]}')

    while True:
        try:
            send_task = asyncio.ensure_future(notify_state_change(ws))
            recv_task = asyncio.ensure_future(on_state_change_received(ws))
            
            done, pending = await asyncio.wait([send_task, recv_task], return_when = asyncio.FIRST_COMPLETED)
            for task in pending: task.cancel()
        except Exception as e:
            print(f'Error: {e}')
            return
    

server_fn = websockets.serve(on_client_connected, "localhost", 6969)

asyncio.get_event_loop().run_until_complete(server_fn)
asyncio.get_event_loop().run_forever()