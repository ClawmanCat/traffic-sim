import websockets
import asyncio
import json
import time
import socket
import copy
from trafficLight import TrafficLight
import sys

first_message = 1
counter = 0
simulation_state = {
    1: TrafficLight([2, 3], 10, "green"),
    2: TrafficLight([1, 3], 10, "red"),
    3: TrafficLight([1, 2], 10, "red"),
    4: TrafficLight([5], 3, "green"),
    5: TrafficLight([4], 4, "green"),
}

message_layout = {
    "msg_type": "notify_sensor_change",
    'msg_id' : 0,
    "data": []
}
# Only send a new message if at least 3 seconds have elapsed since the last one.
last_state_change = 0


def create_init_message():
    global counter
    message = copy.deepcopy(message_layout)
    message['msg_type'] = "initialization"

    counter += 1
    message['msg_id'] = counter
    for key, traffic_light in simulation_state.items():
        data = {
            "id": key,
            "crosses": traffic_light.crossing,
            "clearing_time": traffic_light.clearing_time,
        }
        message['data'].append(data)
    return message


def parse_sim_data():
    global counter
    message = copy.deepcopy(message_layout)
    counter += 1
    message['msg_id'] = counter
    for key, traffic_light in simulation_state.items():
        data = {
            "id": key,
            "vehicles_waiting": traffic_light.vehicles_waiting,
            "vehicles_coming": traffic_light.vehicles_waiting,
            "emergency_vehicle": traffic_light.vehicles_waiting,

        }
        message['data'].append(data)
    return message


async def send_state(ws):
    global last_state_change
    global first_message
    if time.time() - last_state_change < 3.0: return

    if first_message:
        await ws.send(json.dumps(create_init_message()))
        first_message = False
    else:
        await ws.send(json.dumps(parse_sim_data()))
    last_state_change = time.time()


async def receive_traffic_lights_state(ws):
    async for message in ws:
        json_message = ''
        try:
            message = json.loads(message)
        except Exception as e:
            print(f"json error: {e}")

        for crossing_state in message['data']:
            traffic_light = simulation_state[crossing_state['id']]
            traffic_light.state = crossing_state['state']
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
