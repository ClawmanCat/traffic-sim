from typing import Tuple, Optional, List

import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight
from utils import *
from game_objects import Vehicle, SpawnPoint, Road, Sensor, Bridge


def load_intersection_layout(game):
    light_dict = {}

    def add_light(index, crossing, position, clearing_time=4.0):
        light_dict[index] = TrafficLight(index, crossing, clearing_time, "red", position, game)

    add_light(1,                                           [30, 31, 35],   (530, 520), 4)
    add_light(2,                                           [30, 31, 35],   (488, 613), 4)
    add_light(3,                                       [21, 22, 23, 24],   (512, 739), 4)
    add_light(4,                                       [21, 22, 23, 24],   (486, 923), 4)
    add_light(5,                                           [30, 31, 35],   (510, 520), 4)
    add_light(6,                                           [24, 28, 34],  (759, 1118), 4)
    add_light(7,                                           [24, 28, 34],  (940, 1097), 4)
    add_light(8,                                           [25, 26, 27], (1040, 1095), 4)
    add_light(9,                                           [25, 26, 27], (1075, 1124), 4)
    add_light(10,                                          [24, 28, 34],  (680, 1095), 4)
    add_light(11,                                      [22, 23, 27, 33],  (1225, 925), 10)
    add_light(12,                                      [22, 23, 27, 33],  (1275, 850), 3)
    add_light(13,                                      [29, 30, 31, 32],  (1249, 723), 4)
    add_light(14,                                      [29, 30, 31, 32],  (1276, 536), 4)
    add_light(15,                                      [22, 23, 27, 33],  (1250, 925), 10)
    add_light(16,                                          [21, 25, 32],  (1081, 391), 4)
    add_light(17,                                          [21, 25, 32],  (1003, 338), 4)
    add_light(18,                                          [33, 34, 35],   (819, 363), 4)
    add_light(19,                                          [33, 34, 35],   (688, 336), 4)
    add_light(20,                                          [21, 25, 32],  (1081, 365), 4)
    add_light(21,                          [16, 17, 20, 29, 30, 31, 32],   (671, 755), 4)
    add_light(22,                              [11, 12, 15, 25, 26, 27],   (671, 808), 4)
    add_light(23,                              [11, 12, 15, 25, 26, 27],   (671, 860), 4)
    add_light(24,                                            [6, 7, 10],   (671, 913), 4)
    add_light(25, [1, 2, 5, 21, 22, 23, 24, 29, 30, 31, 32, 33, 34, 35],   (959, 943), 4)
    add_light(26,                                  [11, 12, 15, 22, 23],  (1011, 943), 4)
    add_light(27,                                  [11, 12, 15, 22, 23],  (1064, 943), 4)
    add_light(28,                                              [24, 34], (1084, 1224), 4)  # bus line
    add_light(29,                        [6, 7, 10, 21, 25, 33, 34, 35],  (1092, 705), 4)
    add_light(30,                         [1, 2, 5, 21, 25, 33, 34, 35],  (1092, 653), 4)
    add_light(31,                         [1, 2, 5, 21, 25, 33, 34, 35],  (1092, 600), 4)
    add_light(32,                                  [16, 17, 20, 21, 25],  (1092, 548), 4)
    add_light(33,  [11, 12, 15, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31],   (791, 519), 4)
    add_light(34,        [6, 7, 10, 21, 22, 23, 24, 29, 25, 30, 31, 32],   (750, 519), 4)
    add_light(35,                                 [1, 2, 5, 25, 30, 31],   (694, 519), 4)
    add_light(36,                                                   [4],  (2396, 966), 4)  # bridge
    add_light(37,                                                    [], (2650, 1179), 10)

    return light_dict


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

    add_road(1, (2883, 465), (2883, 1007), None, [], [])
    add_road(2, (4023, 646), (3492, 646), None, [], [])
    add_road(3, (3685, 490), (3685, 1040), None, [], [])
    add_road(4, (3744, 490), (3744, 1040), None, [], [])
    add_road(5, (3018, 1209), (3448, 1209), None, [], [])
    add_road(6, (3018, 1260), (3448, 1260), None, [], [])
    add_road(7, (3367, 1571), (3367, 1023), None, [], [])
    add_road(8, (79, 906), (690, 906), 24, [35, 36], [
        (Box((285, 895), (313, 920)), VC),
        (Box((395, 895), (423, 920)), VW)
    ])
    add_road(9, (79, 856), (1005, 856), 23, [40], [
        (Box((285, 840), (313, 867)), VC),
        (Box((395, 840), (423, 867)), VW)
    ])
    add_road(10, (79, 800), (1005, 800), 22, [41], [
        (Box((285, 788), (313, 815)), VC),
        (Box((395, 788), (423, 815)), VW)
    ])
    add_road(11, (1056, 1487), (1056, 856), 27, [52], [])
    add_road(12, (1005, 1487), (1005, 856), 26, [], [])
    add_road(13, (950, 1487), (950, 920), 25, [], [])
    add_road(14, (1110, 1487), (1110,  1245), 28, [], [])  # bus line
    add_road(15, (688, 100), (688, 540), 35, [43, 49], [
        (Box((673, 180), (700, 207)), VC),
        (Box((673, 266), (700, 293)), VW)
    ])
    add_road(16, (740, 100), (740, 850), 34, [44, 46], [
        (Box((726, 180), (754, 207)), VC),
        (Box((726, 266), (745, 293)), VW)
    ])
    add_road(17, (792, 100), (792, 856), 33, [48, 47], [])
    add_road(18, (2826, 1062), (1552, 1062), None, [], [])
    add_road(19, (2826, 1115), (1552, 1115), None, [], [])
    add_road(20, (2826, 380), (1552, 380), None, [], [])
    add_road(21, (2826, 328), (1552, 328), None, [], [])
    add_road(22, (1268, 461), (1268, 985), None, [], [])
    add_road(23, (1211, 461), (1211, 985), None, [], [])
    add_road(24, (1134, 328), (610, 328), None, [], [])
    add_road(25, (1134, 380), (610, 380), None, [], [])
    add_road(26, (478, 461), (478, 985), None, [], [])
    add_road(27, (531, 461), (531, 985), None, [], [])
    add_road(28, (610, 1062), (1134, 1062), None, [], [])
    add_road(29, (610, 1115), (1134, 1115), None, [], [])
    add_road(30, (79, 749), (648, 749), 21, [31], [
        (Box((285, 735), (313, 763)), VC),
        (Box((395, 735), (423, 763)), VW)
    ])
    add_road(31, (648, 749), (1002, 749), None, [32, 34], [])
    add_road(32, (1002, 749), (1056, 749), None, [33], [])
    add_road(33, (1056, 749), (1056, 100), None, [], [])
    add_road(34, (1002, 749), (1002, 100), None, [], [])
    add_road(35, (690, 906), (690, 1342), None, [], [])
    add_road(36, (690, 906), (747, 906), None, [37], [])
    add_road(37, (747, 906), (747, 1342), None, [], [])
    add_road(38, (2670, 1366), (2670, 107), 37, [], [], bridge=True)
    # add_road(39, (2550, 107 ), (2550 , 1366), None, [], [], bridge=True)
    add_road(40, (1005, 856), (1090, 906), None, [42], [])
    add_road(41, (1005, 800), (1090, 856), None, [], [])
    add_road(42, (1090, 906), (3040, 906), 36, [], [
        (Box((1779, 894), (1808, 921)), VC),
        (Box((1816, 894), (1844, 921)), VW)
    ])  # super long road
    add_road(43, (688, 540), (79, 540), None, [], [])
    add_road(44, (740, 850), (690, 850), None, [45], [])
    add_road(45, (690, 850), (690, 1342), None, [], [])
    add_road(46, (740, 850), (740, 1342), None, [], [])
    add_road(47, (792, 856), (1090, 856), None, [], [])
    add_road(48, (792, 853), (792, 906), None, [49], [])
    add_road(49, (792, 906), (1090, 906), None, [42], [])
    add_road(50, (688, 540), (688, 591), None, [51], [])
    add_road(51, (688, 591), (79, 591), None, [], [])
    add_road(52, (1056, 906), (1090, 906), None, [42], [])
    add_road(53, (1056, 856), (1090, 856), None, [], [])
    # add_road(54, (688, 906), (79000, 591), None, [], [])

    for i, connections_for_road in road_conns.items():
        roads[i].connections = [roads[j] for j in connections_for_road]

    return roads


def load_spawnpoints(game):
    spawnpoints = [
        ('bike', 1),
        ('car', 2),
        ('bike', 3),
        ('man', 4),
        ('bike', 5),
        ('man', 6),
        ('car', 8),
        ('car', 9),
        ('car', 10),
        ('car', 11),
        ('car', 12),
        ('car', 13),
        ('car', 14),  # bus
        ('car', 15),
        ('car', 16),
        ('car', 17),
        ('bike', 18),
        ('man', 19),
        ('bike', 20),
        ('man', 21),
        ('man', 22),
        ('bike', 23),
        ('man', 24),
        ('bike', 25),
        ('man', 26),
        ('bike', 27),
        ('bike', 28),
        ('man', 29),
        ('car', 30),
        ('boat', 38)
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
        for r in self.roads.values(): r.render()
        for v in self.vehicles: v.render()
        for k, t in self.state.items(): t.render()

        pygame.display.update()
        self.dt = self.clock.tick(self.tick_rate)
