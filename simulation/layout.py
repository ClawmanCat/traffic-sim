from typing import List, Tuple, Optional

from game_objects import *
from traffic_light import *
from utils import *


class Layout:
    @staticmethod
    def load_intersection_layout(game):
        light_dict = {}

        def add_light(index, crossing, position, clearing_time=4.0):
            light_dict[index] = TrafficLight(index, crossing, clearing_time, "green", position, game)

        add_light(1, [30, 31, 35], (530, 520), 4)
        add_light(2, [30, 31, 35], (488, 613), 4)
        add_light(3, [21, 22, 23, 24], (512, 739), 4)
        add_light(4, [21, 22, 23, 24], (486, 923), 4)
        add_light(5, [30, 31, 35], (510, 520), 4)
        add_light(6, [24, 28, 34], (759, 1118), 4)
        add_light(7, [24, 28, 34], (940, 1097), 4)
        add_light(8, [25, 26, 27], (1040, 1095), 4)
        add_light(9, [25, 26, 27], (1075, 1124), 4)
        add_light(10, [24, 28, 34], (680, 1095), 4)
        add_light(11, [22, 23, 27, 33], (1225, 925), 10)
        add_light(12, [22, 23, 27, 33], (1275, 850), 3)
        add_light(13, [29, 30, 31, 32], (1249, 723), 4)
        add_light(14, [29, 30, 31, 32], (1276, 536), 4)
        add_light(15, [22, 23, 27, 33], (1250, 925), 10)
        add_light(16, [21, 25, 32], (1081, 391), 4)
        add_light(17, [21, 25, 32], (1003, 338), 4)
        add_light(18, [33, 34, 35], (819, 363), 4)
        add_light(19, [33, 34, 35], (688, 336), 4)
        add_light(20, [21, 25, 32], (1081, 365), 4)
        add_light(21, [16, 17, 20, 29, 30, 31, 32], (671, 755), 4)
        add_light(22, [11, 12, 15, 25, 26, 27], (671, 808), 4)
        add_light(23, [11, 12, 15, 25, 26, 27], (671, 860), 4)
        add_light(24, [6, 7, 10], (671, 913), 4)
        add_light(25, [1, 2, 5, 21, 22, 23, 24, 29, 30, 31, 32, 33, 34, 35], (959, 943), 4)
        add_light(26, [11, 12, 15, 22, 23], (1011, 943), 4)
        add_light(27, [11, 12, 15, 22, 23], (1064, 943), 4)
        add_light(28, [24, 34], (1084, 1224), 4)  # bus line
        add_light(29, [6, 7, 10, 21, 25, 33, 34, 35], (1092, 705), 4)
        add_light(30, [1, 2, 5, 21, 25, 33, 34, 35], (1092, 653), 4)
        add_light(31, [1, 2, 5, 21, 25, 33, 34, 35], (1092, 600), 4)
        add_light(32, [16, 17, 20, 21, 25], (1092, 548), 4)
        add_light(33, [11, 12, 15, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31], (791, 519), 4)
        add_light(34, [6, 7, 10, 21, 22, 23, 24, 29, 25, 30, 31, 32], (750, 519), 4)
        add_light(35, [1, 2, 5, 25, 30, 31], (694, 519), 4)
        add_light(36, [4], (2396, 966), 4)  # bridge
        add_light(37, [], (2650, 1179), 10)

        return light_dict


    @staticmethod
    def loads_roads(game):
        VC  = Sensor.SensorType.VEHICLES_COMING
        VW  = Sensor.SensorType.VEHICLES_WAITING
        VB  = Sensor.SensorType.BLOCKING
        BUS = Sensor.SensorType.PUBLIC_TRANSPORT

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
        add_road(2, (4023, 646), (3478, 646), None, [55], [])
        add_road(3, (3685, 490), (3685, 1040), None, [], [])
        add_road(4, (3744, 490), (3744, 1040), None, [], [])
        add_road(5, (3018, 1209), (3448, 1209), None, [], [])
        add_road(6, (3018, 1260), (3448, 1260), None, [], [])
        add_road(7, (3367, 1571), (3367, 1010), None, [], [])
        add_road(8, (79, 906), (690, 906), 24, [35, 36], [
            (Box((286, 895), (316, 925)), VC),
            (Box((618, 895), (648 , 925)), VW)
        ])
        add_road(9, (79, 856), (1005, 856), 23, [40], [
            (Box((286, 840), (316, 870)), VC),
            (Box((618, 840), (648, 870)), VW)
        ])
        add_road(10, (79, 800), (1005, 800), 22, [41], [
            (Box((286, 788), (316, 818)), VC),
            (Box((618, 788), (648, 818)), VW)
        ])
        add_road(11, (1056, 1487), (1056, 906), 27, [52], [
            (Box((1043, 958), (1073, 988)), VW),
            (Box((1043, 1421), (1073, 1451)), VC)
        ])
        add_road(12, (1005, 1487), (1005, 856), 26, [53], [
            (Box((991, 958), (1021, 988)), VW),
            (Box((991, 1421), (1021, 1451)), VC)
        ])
        add_road(13, (950, 1485), (950, 540), 25, [54], [
            (Box((940, 958), (970, 988)), VW),
            (Box((936, 1421), (966, 1451)), VC)
        ])
        add_road(14, (1110, 1487), (1110, 1200), 28, [79], [
            (Box((1095, 1250), (1125, 1280)), VC),
            (Box((1095, 1421), (1125, 1451)), VW)
        ])  # bus line
        add_road(15, (688, 100), (688, 540), 35, [43, 50], [
            (Box((670, 180), (700, 210)), VC),
            (Box((670, 468), (700, 498)), VW)
        ])
        add_road(16, (740, 100), (740, 856), 34, [44, 46], [
            (Box((726, 180), (756, 210)), VC),
            (Box((726, 468), (756, 498)), VW)
        ])
        add_road(17, (792, 100), (792, 856), 33, [48, 47], [
            (Box((778, 180), (808, 210)), VC),
            (Box((778, 468), (808, 498)), VW)
        ])
        add_road(18, (2826, 1062), (1552, 1062), None, [], [])
        add_road(19, (2826, 1115), (1552, 1115), None, [], [])
        add_road(20, (2826, 380), (1552, 380), None, [], [])
        add_road(21, (2826, 328), (1552, 328), None, [], [])
        add_road(22, (1268, 461), (1268, 525), 14, [77], [])
        add_road(23, (1211, 461), (1211, 985), None, [], [])
        add_road(24, (1134, 328), (610, 328), None, [], [])
        add_road(25, (1134, 380), (610, 380), None, [], [])
        add_road(26, (478, 461), (478, 985), None, [], [])
        add_road(27, (531, 461), (531, 985), None, [], [])
        add_road(28, (610, 1062), (1134, 1062), None, [], [])
        add_road(29, (610, 1115), (1134, 1115), None, [], [])
        add_road(30, (79, 749), (648, 749), 21, [31], [
            (Box((286, 735), (316, 765)), VC),
            (Box((618, 735), (648, 765)), VW)
        ])
        add_road(31, (648, 749), (1002, 749), None, [32, 34], [])
        add_road(32, (1002, 749), (1056, 749), None, [33], [])
        add_road(33, (1056, 749), (1056, 100), None, [], [])
        add_road(34, (1002, 749), (1002, 100), None, [], [])
        add_road(35, (690, 906), (690, 1342), None, [], [])
        add_road(36, (690, 906), (740, 906), None, [37], [])
        add_road(37, (740, 906), (740, 1342), None, [], [])
        add_road(38, (2670, 1366), (2670, 107), 37, [], [], bridge=True)
        # add_road(39, (2550, 107 ), (2550 , 1366), None, [], [], bridge=True)
        add_road(40, (1005, 856), (1090, 906), None, [42], [])
        add_road(41, (1005, 800), (1090, 856), None, [], [])
        add_road(42, (1090, 906), (3022, 906), 36, [59], [
            (Box((1780, 894), (1810, 924)), VC),
            (Box((2360, 894), (2390, 924)), VW)
        ])  # super long road
        add_road(43, (688, 540), (79, 540), None, [], [])
        add_road(44, (740, 856), (690, 856), None, [45], [])
        add_road(45, (690, 856), (690, 1342), None, [], [])
        add_road(46, (740, 856), (740, 1342), None, [], [])
        add_road(47, (792, 856), (1090, 856), None, [], [])
        add_road(48, (792, 853), (792, 906), None, [49], [])
        add_road(49, (792, 906), (1090, 906), None, [42], [])
        add_road(50, (688, 540), (688, 591), None, [51], [])
        add_road(51, (688, 591), (79, 591), None, [], [])
        add_road(52, (1056, 906), (1090, 906), None, [42], [])
        add_road(53, (1005, 856), (1090, 856), None, [], [])
        # add_road(54, (688, 906), (79000, 591), None, [], [])
        add_road(54, (950, 540), (688, 540), None, [43], [])
        # roundabout
        add_road(55, (3478, 646), (3364, 554), None, [56], [])
        add_road(56, (3364, 554), (3115, 554), None, [57], [])
        add_road(57, (3115, 554), (3022, 648), None, [58, 65], [])
        add_road(58, (3022, 648), (3022, 906), None, [59], [])
        add_road(59, (3022, 906), (3115, 1010), None, [60, 63], [])
        add_road(60, (3115, 1010), (3367, 1010), None, [61], [])
        add_road(61, (3367, 1010), (3478, 906), None, [62, 64], [])
        add_road(62, (3478, 906), (3478, 646), None, [55], [])
        add_road(63, (3115, 1010), (3115, 1570), None, [], [])
        add_road(64, (3478, 906), (4018, 906), None, [], [])
        # purple road
        add_road(65, (3022, 648), (2060, 648), None, [66, 67, 73], [])
        add_road(66, (2060, 648), (2060, 588), None, [68, 71], [])
        add_road(67, (2060, 648), (2060, 700), None, [75], [])
        add_road(68, (2060, 588), (2060, 537), None, [69], [])
        add_road(69, (2060, 537), (1056, 537), 32, [70], [
            (Box((1400, 526), (1430,  556)), VC),
            (Box((1100, 526), (1130, 556)), VW)
        ])
        add_road(70, (1056, 537), (1056, 70), None, [], [])
        add_road(71, (2060, 588), (720, 588), 31, [72], [
            (Box((1400, 578), (1430, 608)), VC),
            (Box((1100, 578), (1130, 608)), VW)
        ])
        add_road(72, (720, 588), (688, 540), None, [43], [])
        add_road(73, (2060, 648), (720, 648), 30, [74], [
            (Box((1400, 630), (1430, 660)), VC),
            (Box((1100, 630), (1130, 660)), VW)
        ])
        add_road(74, (720, 648), (688, 591), 29, [51], [
            (Box((1400, 680), (1430, 710)), VC),
            (Box((1100, 680), (1130, 710)), VW)
        ])
        add_road(75, (2060, 700), (690, 700), None, [76], [])
        add_road(76, (690, 700), (690, 906), None, [35], [])
        add_road(77, (1268, 525), (1268, 840), None, [78], [])
        add_road(78, (1268, 840), (1268, 985), None, [], [])
        add_road(79, (1110, 1200), (740, 1200), None, [80], [])
        add_road(80, (740, 1200 ), (740, 1345), None, [], [])

        for i, connections_for_road in road_conns.items():
            roads[i].connections = [roads[j] for j in connections_for_road]

        return roads


    @staticmethod
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
            ('bus', 14),  # bus
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
                speed    = 15
                cooldown = 20
            elif type in ['car', 'boat']:
                speed    = 65
                cooldown = 20
            elif type in ['bus']:
                speed    = 40
                cooldown = 200
            else:
                raise NotImplementedError()

            result.append(SpawnPoint(game, type, game.roads[road_idx], speed = speed, cooldown = cooldown))

        return result