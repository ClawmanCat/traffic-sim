import copy
import os
import random
from enum import Enum

import pygame

from utils import *


class Vehicle:
    def __init__(self, image, game):
        self.image     = pygame.image.load(os.path.join('assets', f'{image}.png'))
        self.position  = [0, 0]
        self.direction = [0, 0]
        self.speed     = [1, 1]
        self.max_speed = copy.deepcopy(self.speed)
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
    def __init__(self, game, start, end, connections, light = None):
        self.game        = game
        self.start       = start
        self.end         = end
        self.light       = light
        self.vector      = norm(sub(end, start))
        self.length      = mag(sub(end, start))
        self.connections = connections
        self.vehicles    = []
        self.sensors     = []

        if self.light is not None:
            stop_distance = 20

            # Point where vehicles stop for the light.
            self.stop_point = Road.calculate_stop_point_distance(self.start, self.vector, self.light.position, stop_distance)
            # Vehicles past this point don't stop anymore if the light is red.
            self.past_point = self.stop_point + stop_distance

            self.light.position = add(self.start, mul(self.vector, (self.stop_point, self.stop_point)))


    def add_sensor(self, area, type):
        self.sensors.append(Sensor(self, area, type))


    def add(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.position  = self.start
        vehicle.direction = self.vector
        vehicle.progress  = 0


    def remove(self, vehicle):
        self.vehicles.remove(vehicle)


    @staticmethod
    def calculate_stop_point_distance(start, direction, light_position, offset):
        # Project light position onto road vector.
        c = dot(start, light_position) / dot(direction, direction)
        p = mul((c, c), direction)

        # Get stopping point as distance to projection - some constant
        return mag(p) - offset


    def tick(self):
        # Move vehicles and transfer to next road if they reach the end.
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


        # Stop vehicles if they are before a light.
        if self.light is not None:
            if self.light.state == 'green':
                for v in self.vehicles:
                    v.speed = copy.deepcopy(v.max_speed)
            else:
                for v in self.vehicles:
                    if self.stop_point <= v.progress < self.past_point:
                        v.speed = [0, 0]


        # There is no point in checking the sensors if they don't control any light.
        if self.light is not None:
            updates = dict()

            for sensor in self.sensors:
                sensor.update()

                if sensor.was_changed() and sensor.is_pressed():
                    updates[sensor.type.name] = True

            for key, value in updates.items():
                light = self.game.state[self.light]
                setattr(light, key, value)

            # if len(updates) > 0: self.game.connection.mark_dirty()


class Sensor:
    # TODO: Implement other sensor types.
    class SensorType(Enum):
        VEHICLES_WAITING = "vehicles_waiting"
        VEHICLES_COMING  = "vehicles_coming"


    def __init__(self, road, area, type):
        self.road = road
        self.area = area
        self.type = type
        self.pressed = False
        self.changed = False

    def update(self):
        previously_pressed = self.pressed

        for vehicle in self.road.vehicles:
            if is_in_box(vehicle.position, self.area):
                self.pressed = True
                break

        self.pressed = False
        self.changed = (self.pressed != previously_pressed)

    def is_pressed(self):
        return self.pressed

    def was_changed(self):
        return self.changed