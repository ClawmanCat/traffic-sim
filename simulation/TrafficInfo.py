class TrafficInfo:

    def __init__(self, msg_id, crosses, clearing_time):
        self.msg_id = msg_id
        self.crosses = crosses
        self.clearing_time = clearing_time

    def get_croses(self):
        dicts = {
            "id": self.msg_id,
            "crosses": self.crosses,
            "clearing_time": self.clearing_time + 1
        }
        return dicts
