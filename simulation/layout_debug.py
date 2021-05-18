from typing import Tuple, Optional, List

from game_objects import *
from traffic_light import *
from utils import *


class Layout:
    @staticmethod
    def load_intersection_layout(game):
        light_dict = {}

        def add_light(index, crossing, position, clearing_time=4.0):
            light_dict[index] = TrafficLight(index, crossing, clearing_time, "red", position, game)

        add_light(0, [1, 2, 3], (100, 550))
        add_light(1, [0, 2, 3], (350, 800))
        add_light(2, [0, 1, 3], (800, 300))
        add_light(3, [0, 1, 2], (300, 100))

        return light_dict


    @staticmethod
    def loads_roads(game):
        VC = Sensor.SensorType.VEHICLES_COMING
        VW = Sensor.SensorType.VEHICLES_WAITING

        roads = dict()
        road_conns = dict()

        def add_road(
                index: int,
                start: Tuple[int, int],
                end: Tuple[int, int],
                light_id: Optional[int],
                connection_ids: List[int],
                sensors: List[Tuple[Box, Sensor.SensorType]],
                bridge: bool = False
        ):
            light = game.state[light_id] if light_id is not None else None

            if bridge:
                road = Bridge(game, start, end, [], Box((2522, 276), (2700, 1167)), light)
            else:
                road = Road(game, start, end, [], light)

            roads[index] = road
            road_conns[index] = connection_ids

            for area, type in sensors: road.add_sensor(area, type)

        add_road(0, (0, 550), (1000, 550), 0, [], [(Box((0, 525), (100, 575)), VW)])
        add_road(1, (350, 1000), (350, 0), 1, [], [(Box((325, 1000), (375, 800)), VW)])
        add_road(2, (1000, 300), (0, 300), 2, [], [(Box((1000, 275), (800, 325)), VW)])
        add_road(3, (300, 0), (300, 1000), 3, [], [(Box((275, 0), (325, 100)), VW)])

        for i, connections_for_road in road_conns.items():
            roads[i].connections = [roads[j] for j in connections_for_road]

        return roads


    @staticmethod
    def load_spawnpoints(game):
        spawnpoints = [
            ('car', 0),
            ('car', 1),
            ('car', 2),
            ('car', 3)
        ]

        result = []
        for type, road_idx in spawnpoints:
            if type in ['man', 'bike']:
                speed = 15
            elif type in ['car', 'boat']:
                speed = 65
            else:
                raise NotImplementedError()

            result.append(SpawnPoint(game, type, game.roads[road_idx], speed))

        return result