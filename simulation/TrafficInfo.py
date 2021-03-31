class TrafficInfo:

    def __init__(self, msg_id, state):
        self.msg_id = msg_id
        self.state = state

    def get_croses(self):
        dicts = {
            "id": self.msg_id,
            "crosses": [1, 4],
            "clearing_time": 7
        }
        return dicts
