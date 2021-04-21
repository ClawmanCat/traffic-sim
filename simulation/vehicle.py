import copy
import os
import random

import pygame

from utils import *


class Vehicle:
    def __init__(self, image, game):
        self.image     = pygame.image.load(os.path.join('assets', f'{image}.png'))
        self.position  = [0, 0]
        self.direction = [0, 0]
        self.speed     = [1, 1]
        self.progress  = 0
        self.game      = game

    def tick(self):
        delta = mul(self.speed, self.direction)
        self.position = add(self.position, delta)
        self.progress += mag(delta)

    def render(self):
        self.game.screen.blit(self.image, sub(add(self.game.translation, self.position), div(self.image.get_size(), (2, 2))))


class SpawnPoint:
    def __init__(self, game, type, road, chance = 0.05):
        self.game     = game
        self.type     = type
        self.road     = road
        self.chance   = chance

    def tick(self):
        if random.uniform(0, 1) < self.chance:
            v = Vehicle(self.type, self.game)
            self.road.add(v)
            self.game.vehicles.append(v)


class Road:
    def __init__(self, game, start, end, connections):
        self.game        = game
        self.start       = start
        self.end         = end
        self.vector      = norm(sub(end, start))
        self.length      = mag(sub(end, start))
        self.connections = connections
        self.vehicles    = []


    def add(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.position  = self.start
        vehicle.direction = self.vector
        vehicle.progress  = 0


    def remove(self, vehicle):
        self.vehicles.remove(vehicle)


    def tick(self):
        for v in self.vehicles:
            if v.progress >= self.length:
                if len(self.connections) > 0:
                    # Move to different road
                    next_road = random.choice(self.connections)

                    self.remove(v)
                    next_road.add(v)
                else:
                    # Destroy!!!
                    self.remove(v)
                    self.game.vehicles.remove(v)