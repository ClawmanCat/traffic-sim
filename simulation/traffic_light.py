class TrafficLight:
    def __init__(self, crossings, clearing_time,state,coordinates):
        self.crossing = crossings  # cant go on green
        self.clearing_time = clearing_time
        self.vehicles_waiting = False
        self.vehicles_coming = False
        self.emergency_vehicle = False
        self.state = state
        self.coordinates = coordinates

    def __str__(self):
        return self.state
