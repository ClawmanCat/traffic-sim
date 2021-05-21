from typing import Tuple, Optional, List

import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight
from utils import *
from game_objects import Vehicle, SpawnPoint, Road, Sensor, Bridge

import layout
import layout_debug


class Game:
    def __init__(self, connection, debug = False):
        Layout = layout.Layout if not debug else layout_debug.Layout

        self.connection = connection

        self.state = Layout.load_intersection_layout(self)
        self.tick_rate = 20

        self.last_mouse_pos = None
        self.translation = [0, 0]
        self.screen_size = (1920, 1080)

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode(self.screen_size)

        bg_img = 'background.png' if not debug else 'debug_background.png'
        self.bg = pygame.image.load(os.path.join('assets', bg_img))

        self.vehicles = []
        self.roads = Layout.loads_roads(self)
        self.spawnpoints = Layout.load_spawnpoints(self)
        self.bridge = Bridge(self, Box((2522, 276), (2700, 1167)), [ self.roads[38], self.roads[39] ], self.state[39])

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

        # perform sim logic
        for s in self.spawnpoints: s.tick()
        for v in self.vehicles: v.tick()
        for r in self.roads.values(): r.tick()
        self.bridge.tick()

        # render map
        self.screen.blit(self.bg, self.translation)
        self.bridge.render()
        for r in self.roads.values(): r.render()
        for v in self.vehicles: v.render()
        for k, t in self.state.items(): t.render()

        pygame.display.update()
        self.dt = self.clock.tick(self.tick_rate)
