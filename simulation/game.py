import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight
from utils import *
from vehicle import Vehicle, SpawnPoint, Road


def load_intersection_layout(game):
    return {
        # TODO: Real traffic lights
        1: TrafficLight([2, 3], 10, "green", (2914, 606), game),
        # 2: TrafficLight([1, 3], 10, "red", (0, 0), game),
        # 3: TrafficLight([1, 2], 10, "red", (0, 0), game),
        # 4: TrafficLight([5], 3, "green", (0, 0), game),
        # 5: TrafficLight([4], 4, "green", (0, 0), game),
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
