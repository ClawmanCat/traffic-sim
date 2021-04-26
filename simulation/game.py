from typing import Tuple, Optional, List

import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight
from utils import *
from game_objects import Vehicle, SpawnPoint, Road, Sensor


def load_intersection_layout(game):
    light_dict = {}

    def add_light(index, crossing, position, clearing_time=4.0):
        light_dict[index] = TrafficLight(crossing, clearing_time, "red", position, game)

    # add_light(1, [30, 31, 35], (530, 520), 4)
    # add_light(2, [30, 31, 35], (488, 613), 4)
    # add_light(3, [21, 22, 23, 24], (512, 739), 4)
    # add_light(4, [21, 22, 23, 24], (486, 923), 4)
    # add_light(5, [30, 31, 35], (510, 520), 4)
    # add_light(6, [24, 28, 34], (759, 1118), 4)
    # add_light(7, [24, 28, 34], (940, 1097), 4)
    # add_light(8, [25, 26, 27], (1040, 1095), 4)
    # add_light(9, [25, 26, 27], (1075, 1124), 4)
    # add_light(10, [24, 28, 34], (680, 1095), 4)
    # add_light(11, [22, 23, 27, 33], (1225, 925), 10)
    # add_light(12, [22, 23, 27, 33], (1275, 850), 3)
    # add_light(13, [29, 30, 31, 32], (1249, 723), 4)
    # add_light(14, [29, 30, 31, 32], (1276, 536), 4)
    # add_light(15, [22, 23, 27, 33], (1250, 925), 10)
    # add_light(16, [21, 25, 32], (1081, 391), 4)
    # add_light(17, [21, 25, 32], (1003, 338), 4)
    # add_light(18, [33, 34, 35], (819, 363), 4)
    # add_light(19, [33, 34, 35], (688, 336), 4)
    # add_light(20, [21, 25, 32], (1081, 365), 4)
    # add_light(21, [16, 17, 20, 29, 30, 31, 32], (671, 755), 4)
    # add_light(22, [11, 12, 15, 25, 26, 27], (671, 808), 4)
    # add_light(23, [11, 12, 15, 25, 26, 27], (671, 860), 4)
    add_light(24, [6, 7, 10], (671, 913), 4)
    # add_light(25, [1, 2, 5, 21, 22, 23, 24, 29, 30, 31, 32, 33, 34, 35], (959, 943), 4)
    # add_light(26, [11, 12, 15, 22, 23], (1011, 943), 4)
    # add_light(27, [11, 12, 15, 22, 23], (1064, 943), 4)
    # add_light(28, [24, 34], (735, 1214), 4)  # bus line
    # add_light(29, [6, 7, 10, 21, 25, 33, 34, 35], (1092, 705), 4)
    # add_light(30, [1, 2, 5, 21, 25, 33, 34, 35], (1092, 653), 4)
    # add_light(31, [1, 2, 5, 21, 25, 33, 34, 35], (1092, 600), 4)
    # add_light(32, [16, 17, 20, 21, 25], (1092, 548), 4)
    # add_light(33, [11, 12, 15, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31], (891, 519), 4)
    # add_light(34, [6, 7, 10, 21, 22, 23, 24, 29, 25, 30, 31, 32], (750, 519), 4)
    # add_light(35, [1, 2, 5, 25, 30, 31], (694, 519), 4)
    # add_light(36, [4], (2396, 966), 4)  # bridge

    return light_dict


def loads_roads(game):
    roads = dict()
    road_conns = dict()

    def add_road(
            index: int,
            start: Tuple[int, int],
            end: Tuple[int, int],
            light_id: Optional[int],
            connection_ids: List[int],
            sensors: List[Tuple[Box, Sensor.SensorType]]
    ):
        light = game.state[light_id] if light_id is not None else None

        roads[index] = Road(game, start, end, [], light)
        road_conns[index] = connection_ids

        for area, type in sensors: road.add_sensor(area, type)


    add_road(1, (2883, 465), (2883, 1007), None, [], [])
    add_road(2, (4023, 646), (3492, 646), None, [], [])
    add_road(3, (3685, 490), (3685, 1040), None, [], [])
    add_road(4, (3744, 490), (3744, 1040), None, [], [])
    add_road(5, (3018, 1209), (3448, 1209), None, [], [])
    add_road(6, (3018, 1260), (3448, 1260), None, [], [])
    add_road(7, (3367, 1571), (3367, 1023), None, [], [])
    add_road(8, (79, 906), (675, 906), 24 , [], [])
    add_road(9, (79, 853), (675, 853), None, [], [])
    add_road(10, (79, 800), (675, 800), None, [], [])
    add_road(11, (1056, 1487), (1056, 920), None, [], [])
    add_road(12, (1005, 1487), (1005, 920), None, [], [])
    add_road(13, (950, 1487), (950, 920), None, [], [])
    add_road(14, (1110, 1487), (1214, 920), None, [], [])  # bus line
    add_road(15, (100, 688), (688, 527), None, [], [])
    add_road(16, (100, 740), (740, 527), None, [], [])
    add_road(17, (100, 792), (792, 527), None, [], [])
    add_road(18, (2826, 1062), (1552, 1062), None, [], [])
    add_road(19, (2826, 1115), (1552, 1115), None, [], [])
    add_road(20, (2826, 380), (1552, 380), None, [], [])
    add_road(21, (2826, 328), (1552, 328), None, [], [])

    # add_road(2, (3002, 651), (2062, 651),  None, [], [])

    # Set connections after all roads have been created so they can reference each other.
    for i, road in roads.items():
        conns = [roads[conn] for conn in road_conns[i]]
        roads[i].connections = conns

    return roads


def load_spawnpoints(game):
    spawnpoints = [
        # Type, Road
        ('man', 1),
        ('car', 2),
        ('bike', 3),
        ('car', 4),
        ('bike',5),
        ('man',6),
        ('car', 8),

    ]

    result = []
    for type, road_idx in spawnpoints:
        result.append(SpawnPoint(game, type, game.roads[road_idx]))

    return result


class Game:
    def __init__(self, connection):
        self.connection = connection

        self.state = load_intersection_layout(self)
        self.tick_rate = 20

        self.last_mouse_pos = None
        self.translation = [0, 0]
        self.screen_size = (1920, 1080)

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg = pygame.image.load(os.path.join('assets', 'background.png'))

        self.vehicles = []
        self.roads = loads_roads(self)
        self.spawnpoints = load_spawnpoints(self)

        pygame.display.set_caption("Glorious TrafficSim 3000XL Sponsored by Bad Dragon")

    def listen_input(self):
        mouse_pos = mouse.get_pos()

        if self.last_mouse_pos is None:
            self.last_mouse_pos = mouse_pos
            return

        if not pygame.mouse.get_pressed()[0]:
            self.last_mouse_pos = mouse_pos
            return

        sens = (1, 1)

        self.translation = add(self.translation, mul(sens, sub(mouse_pos, self.last_mouse_pos)))
        self.translation[0] = clamp(self.translation[0], -self.bg.get_size()[0] + self.screen_size[0], 0)
        self.translation[1] = clamp(self.translation[1], -self.bg.get_size()[1] + self.screen_size[1], 0)

        self.last_mouse_pos = mouse_pos

    def loop(self):
        for events in pygame.event.get(): pass  # Event fetching is required to prevent screen freeze.
        self.listen_input()

        for s in self.spawnpoints: s.tick()
        for v in self.vehicles: v.tick()
        for r in self.roads.values(): r.tick()

        # set map
        self.screen.blit(self.bg, self.translation)
        for v in self.vehicles: v.render()
        for k, t in self.state.items(): t.render()

        pygame.display.update()
        self.dt = self.clock.tick(self.tick_rate)
