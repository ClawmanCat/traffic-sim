import copy
import json
import time
from threading import Lock

message_template = {
    "msg_type": "notify_sensor_change",
    'msg_id' : 0,
    "data": []
}

message_interval_s = 3.0


class Connection:
    def __init__(self, ws):
        self.ws = ws
        self.msg_count = 0
        self.initialized = False
        self.last_message_time = 0.0


    async def send_state(self, state):
        if time.time() - self.last_message_time < message_interval_s: return


        message = copy.deepcopy(message_template)

        message['msg_id'] = self.msg_count
        self.msg_count += 1


        if not self.initialized:
            message['msg_type'] = 'initialization'

            for key, light in state.items():
                if not light.sync: continue

                data = {"id": key, "crosses": light.crossing, "clearing_time": light.clearing_time}
                message['data'].append(data)

            self.initialized = True
        else:
            for key, light in state.items():
                if not light.dirty or not light.sync: continue
                light.dirty = False

                data = {
                    "id": key,
                    "vehicles_waiting":  light.vehicles_waiting,
                    "vehicles_coming":   light.vehicles_coming,
                    "emergency_vehicle": light.emergency_vehicle,

                }

                message['data'].append(data)

        if len(message['data']) > 0:
            print(f'Sending state for { len(message["data"]) } traffic lights.')
            await self.ws.send(json.dumps(message))

        self.last_message_time = time.time()


    async def recv_state(self, state):
        async for message in self.ws:
            try:
                json_message = json.loads(message)
            except Exception as e:
                print(f"Failed to parse JSON: {e}")
                return

            print(f'Received state for { len(json_message["data"]) } traffic lights.')

            for crossing_state in json_message['data']:
                traffic_light = state[crossing_state['id']]
                print(f'Light {traffic_light.id}: {traffic_light.state} => {crossing_state["state"]}')

                traffic_light.state = crossing_state['state']