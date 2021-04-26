import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight
from utils import *
from vehicle import Vehicle, SpawnPoint, Road


def load_intersection_layout(game):
    return {
        # TODO: Real traffic lights

        1: TrafficLight([4], 4, "red", (530, 520), game),  # 1
        2: TrafficLight([4], 4, "red", (488, 613), game),  # 2
        3: TrafficLight([4], 4, "red", (512, 739), game),  # 3
        4: TrafficLight([4], 4, "red", (486, 923), game),  # 4
        5: TrafficLight([4], 4, "red", (510, 520), game),  # 5
        6: TrafficLight([4], 4, "red", (759, 1118), game),  # 6
        7: TrafficLight([4], 4, "red", (940, 1097), game),  # 7
        8: TrafficLight([4], 4, "red", (1040, 1095), game),  # 8
        9: TrafficLight([4], 4, "red", (1075, 1124), game),  # 9
        10: TrafficLight([4], 4, "red", (680, 1095), game),  # 10
        11: TrafficLight([1, 3], 10, "red", (1225, 925), game),  # 11
        12: TrafficLight([5], 3, "red", (1275, 850), game),  # 12
        13: TrafficLight([4], 4, "red", (1249, 723), game),  # 13
        14: TrafficLight([4], 4, "red", (1276, 536), game),  # 14
        15: TrafficLight([1, 2], 10, "red", (1250, 925), game),  # 15
        16: TrafficLight([4], 4, "red", (1081, 391), game),  # 16
        17: TrafficLight([4], 4, "red", (1003, 338), game),  # 17
        18: TrafficLight([4], 4, "red", (819, 363), game),  # 18
        19: TrafficLight([4], 4, "red", (688, 336), game),  # 19
        20: TrafficLight([4], 4, "red", (1081, 365), game),  # 20
        21: TrafficLight([4], 4, "red", (671, 755), game),  # 21 heeft meerdere stoplichten ?
        22: TrafficLight([4], 4, "red", (671, 808), game),  # 22
        23: TrafficLight([4], 4, "red", (671, 860), game),  # 23
        24: TrafficLight([4], 4, "red", (671, 913), game),  # 24 heeft meerdere stoplichten
        25: TrafficLight([4], 4, "red", (959, 943), game),  # 25 heeft meerdere stoplichten
        26: TrafficLight([4], 4, "red", (1011, 943), game),  # 26
        27: TrafficLight([4], 4, "red", (1064, 943), game),  # 27
        28: TrafficLight([4], 4, "red", (735, 1214), game),  # 28
        29: TrafficLight([4], 4, "red", (1092, 705), game),  # 29 heeft meerdere stoplichten
        30: TrafficLight([4], 4, "red", (1092, 653), game),  # 30
        31: TrafficLight([4], 4, "red", (1092, 600), game),  # 31
        32: TrafficLight([4], 4, "red", (1092, 548), game),  # 32
        33: TrafficLight([4], 4, "red", (891, 519), game),  # 33 meerdere stoplichten
        34: TrafficLight([4], 4, "red", (750, 519), game),  # 34
        35: TrafficLight([4], 4, "red", (694, 519), game),  # 35
        36: TrafficLight([4], 4, "red", (2396, 966 ), game),  # 36 meerdere stoplichten
        37: TrafficLight([4], 4, "red", (2567, 1202), game),  # 37 meerdere stoplichten

    }


def load_traffic_routes(game):
    roads = [
        ((2883, 465), (2883, 1007), []),
        ((3002, 651), (2062, 651), [])
    ]

    for start, end, conns in roads: game.roads.append(Road(game, start, end, conns))

    spawnpoints = [
        ('man', 0),
        ('car', 1)
    ]

    for type, road_idx in spawnpoints: game.spawnpoints.append(SpawnPoint(game, type, game.roads[road_idx]))


class Game:
    def __init__(self):
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
        self.spawnpoints = []
        self.roads = []

        load_traffic_routes(self)

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
        for r in self.roads: r.tick()

        # set map
        self.screen.blit(self.bg, self.translation)
        for v in self.vehicles: v.render()
        for k, t in self.state.items(): t.render()

        pygame.display.update()
        self.dt = self.clock.tick(self.tick_rate)
