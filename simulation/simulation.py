import websockets
import asyncio
import json
import time
import socket
import copy
from trafficLight import TrafficLight
import sys

simulation_state = {
    1: TrafficLight([2, 3], 10, "green"),
    2: TrafficLight([1, 3], 10, "red"),
    3: TrafficLight([1, 2], 10, "red"),
    4: TrafficLight([5], 3, "green"),
    5: TrafficLight([4], 4, "green"),
}

message_layout = {
    "msg_type": "notify_sensor_change",
    "data": []
}
# Only send a new message if at least 3 seconds have elapsed since the last one.
last_state_change = 0


def parse_sim_data():
    message = copy.deepcopy(message_layout)
    for key, traffic_light in simulation_state.items():
        data = {
            "id": key,
            "state": traffic_light.state
        }
        message['data'].append(data)
    print(message)
    return message


async def send_state(ws):
    global last_state_change
    if time.time() - last_state_change < 3.0: return

    await ws.send(json.dumps(parse_sim_data()))
    last_state_change = time.time()


async def receive_traffic_lights_state(ws):
    async for message in ws:
        for crossing_state in message['data']:
            simulation_state[crossing_state['id']].state = crossing_state['state']
        print(f'Received new state:\n{message}')


async def on_client_connected(ws, path):
    print(f'Client connected from {ws.remote_address[0]}')

    try:
        while True:
            send_task = asyncio.ensure_future(send_state(ws))
            recv_task = asyncio.ensure_future(receive_traffic_lights_state(ws))

            done, pending = await asyncio.wait([send_task, recv_task], return_when=asyncio.FIRST_COMPLETED)
            for task in pending: task.cancel()

            # Unpack exceptions from future so they can be caught.
            f, = done
            e = f.exception()
            if e is not None: raise e
    except Exception as e:
        print(f'Error occurred in connection with {ws.remote_address[0]}: {e}')

# Note: connect with local ip, (e.g. 192.168.*.*:6969) or normal IP if portforwarding is enabled.
# localhost and loopback address are unlikely to work.

local_ip = socket.gethostbyname(socket.gethostname())
server_fn = websockets.serve(on_client_connected, local_ip, 6969)

asyncio.get_event_loop().run_until_complete(server_fn)
asyncio.get_event_loop().run_forever()
