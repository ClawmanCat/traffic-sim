import os

import pygame

from utils import *


class TrafficLight:
    red_light = pygame.image.load(os.path.join('assets', 'red.png'))
    orange_light = pygame.image.load(os.path.join('assets', 'orange.png'))
    green_light = pygame.image.load(os.path.join('assets', 'green.png'))


    def __init__(self, id, crossings, clearing_time, state, position, game, sync = True):
        self.id = id
        self.crossing = crossings  # cant go on green
        self.clearing_time = clearing_time
        self.vehicles_waiting = False
        self.vehicles_coming = False
        self.emergency_vehicle = False
        self.state = state
        self.true_state = None
        self.position = position
        self.game = game
        self.image = TrafficLight.red_light
        self.dirty = False
        self.sync = sync

    def tick(self):
        # Make green if clicked.
        if (
            pygame.mouse.get_pressed()[0] and
            dist(add(self.position, self.game.translation), pygame.mouse.get_pos()) < self.image.get_width()
        ):
            if self.true_state is None:
                self.true_state = self.state
                self.state = "green"
        else:
            if self.true_state is not None:
                self.state = self.true_state
                self.true_state = None


    def render(self):
        if self.state == "red": self.image = TrafficLight.red_light
        if self.state == "orange": self.image = TrafficLight.orange_light
        if self.state == "green": self.image = TrafficLight.green_light

        self.game.screen.blit(self.image, sub(add(self.game.translation, self.position), div(self.image.get_size(), (2, 2))))
