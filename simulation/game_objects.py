import copy
import os
import random
from enum import Enum

import pygame

from utils import *


class Vehicle:
    def __init__(self, image, game, speed = 50.0, acceleration = 1.2, deceleration = 0.8):
        self.image     = pygame.image.load(os.path.join('assets', f'{image}.png'))
        self.position  = [0, 0]
        self.direction = [0, 0]
        self.speed     = speed
        self.max_speed = speed
        self.size      = self.image.get_size()
        self.progress  = 0
        self.game      = game
        self.accel     = acceleration
        self.decel     = deceleration

    def accelerate(self):
        # Can't accelerate from 0 by just multiplying, so give some initial velocity.
        if self.speed == 0: self.speed = 0.01 * self.max_speed
        self.speed *= self.accel

        # Don't go faster than max_speed
        if self.speed > self.max_speed: self.speed = self.max_speed


    def decelerate(self):
        self.speed *= self.decel
        if self.speed < 0.01: self.speed = 0

    def tick(self):
        delta = mul(vec(self.speed), self.direction)
        delta = div(delta, vec(self.game.tick_rate))

        self.position = add(self.position, delta)
        self.progress += mag(delta)

    def render(self):
        self.game.screen.blit(self.image, sub(add(self.game.translation, self.position), div(self.size, vec(2))))


class SpawnPoint:
    def __init__(self, game, type, road, speed, chance = 0.005, cooldown = 20):
        self.game            = game
        self.type            = type
        self.road            = road
        self.chance          = chance
        self.speed           = speed
        self.cooldown        = 0
        self.cooldown_length = cooldown

    def tick(self):
        if self.cooldown == 0 and random.uniform(0, 1) < self.chance:
            v = Vehicle(self.type, self.game, speed = self.speed)
            self.road.add(v)
            self.game.vehicles.append(v)
            self.cooldown = self.cooldown_length

        elif self.cooldown > 0: self.cooldown -= 1


class Road:
    def __init__(self, game, start, end, connections, light = None):
        self.game          = game
        self.start         = start
        self.end           = end
        self.light         = light
        self.vector        = norm(sub(end, start))
        self.length        = mag(sub(end, start))
        self.connections   = connections
        self.vehicles      = []
        self.sensors       = []
        self.clearing_time = light.clearing_time if light is not None else 0


        if self.light is not None:
            stop_offset = 50

            # Point where vehicles stop for the light.
            self.stop_dist = Road.calculate_stop_point_distance(self.start, self.end, self.light.position, stop_offset)
            # Vehicles past this point don't stop anymore if the light is red.
            self.past_dist = self.stop_dist + stop_offset


    def can_vehicles_pass(self):
        return self.light is None or self.light.state == 'green'


    def add_sensor(self, area, type, target = None):
        self.sensors.append(Sensor(self, area, type, target_light = target if target is not None else self.light))


    def add(self, vehicle):
        self.vehicles.append(vehicle)
        vehicle.position  = self.start
        vehicle.direction = self.vector
        vehicle.progress  = 0


    def remove(self, vehicle):
        self.vehicles.remove(vehicle)


    @staticmethod
    def calculate_stop_point_distance(start, end, light, offset):
        start = list(map(float, start))
        end   = list(map(float, end))
        light = list(map(float, light))


        # Project light position onto road vector.
        AB = sub(end, start)
        AP = sub(light, start)

        stop_point = add(start, mul(vec(dot(AP, AB) / dot(AB, AB)), AB))

        # Stop distance is distance to point minus offset.
        return mag(sub(stop_point, start)) - offset


    def render(self):
        start = add(self.game.translation, self.start)
        end   = add(self.game.translation, self.end)

        pygame.draw.line(self.game.screen, (139, 0, 139), start, end, 2)

        for sensor in self.sensors: sensor.render()


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


        sorted_vehicles = list(sorted(self.vehicles, key = lambda v: v.progress))

        for i, v in enumerate(sorted_vehicles):
            # If the next vehicle is too close, decelerate
            if len(sorted_vehicles) > (i + 1):
                next = sorted_vehicles[i + 1]

                safety_distance = 1.2 * (
                    0.5 * mag(project(next.size, self.vector)) +
                    0.5 * mag(project(v.size, self.vector))
                )


                if should_brake(v.progress, v.speed, next.progress, next.speed, safety_distance):
                    v.decelerate()
                    continue

            # If there's a non-green traffic light ahead, decelerate
            if self.light is not None and not self.can_vehicles_pass():
                if v.progress < self.past_dist and should_brake(v.progress, v.speed, self.stop_dist, 0.0, 0.0):
                    v.decelerate()
                    continue

            # Otherwise, just accelerate to the max velocity if we're not at it already.
            v.accelerate()


        # There is no point in checking the sensors if they don't control any light.
        if self.light is not None:
            updates = dict()

            for sensor in self.sensors:
                sensor.tick()

                if sensor.was_changed():
                    if sensor.target not in updates: updates[sensor.target] = []
                    updates[sensor.target].append([sensor.type.name, sensor.is_pressed()])

            for key, value in updates.items():
                for sensor_type, pressed in value: setattr(key, sensor_type, pressed)


class Sensor:
    class SensorType(Enum):
        VEHICLES_WAITING = "vehicles_waiting"
        VEHICLES_COMING  = "vehicles_coming"
        PUBLIC_TRANSPORT = "public_vehicle"
        BLOCKING         = "vehicles_blocking"


    def __init__(self, road, area, type, target_light = None):
        self.road   = road
        self.area   = area
        self.type   = type
        self.target = target_light if target_light is not None else self.road.light
        self.pressed = False
        self.changed = False

        mmb = minmaxbox(self.area)
        end_a  = project(sub(mmb.min, self.road.start), self.road.vector)
        end_b  = project(sub(mmb.max, self.road.start), self.road.vector)
        dist_a = mag(end_a)
        dist_b = mag(end_b)

        self.min_progress = min(dist_a, dist_b)
        self.max_progress = max(dist_a, dist_b)


    def tick(self):
        previously_pressed = self.pressed

        for vehicle in self.road.vehicles:
            if self.min_progress <= vehicle.progress <= self.max_progress:
                self.pressed = True
                break
        else:
            self.pressed = False

        self.changed = (self.pressed != previously_pressed)

        if self.changed:
            self.road.light.dirty = True
            setattr(self.road.light, self.type.value, self.pressed)


    def render(self):
        box = minmaxbox(self.area)

        tl = add(self.road.game.translation, box.min)
        wh = sub(box.max, box.min)

        inactive_color = (127, 127, 127)
        active_color   = (60,  105, 43)
        blink_color    = (255, 0,   0)

        pygame.draw.rect(
            self.road.game.screen,
            blink_color if self.changed else
            active_color if self.pressed else
            inactive_color,
            pygame.Rect(tl, wh)
        )

    def is_pressed(self):
        return self.pressed

    def was_changed(self):
        return self.changed


class Bridge:
    class State(Enum):
        CLOSED  = 0
        OPENING = 1
        OPEN    = 2
        CLOSING = 3


    def __init__(self, game, area, roads, light):
        self.game              = game
        self.area              = area
        self.roads             = roads
        self.light             = light
        self.state             = Bridge.State.CLOSED
        self.open_time         = 100
        self.open_percentage   = 0
        self.state_duration    = 0

        assert all(road.light is not None and not road.light.sync for road in self.roads)


        self.boat_clearing_time  = self.roads[0].light.clearing_time
        self.clearing_time       = 2 * self.boat_clearing_time + self.open_time
        self.light.clearing_time = self.clearing_time


    def tick(self):
        # There are three lights: one is synced with the controller, and controls whether the bridge is open or closed,
        # the other two are not synced, and use the first light to control which side of the bridge will have a green light.
        # TODO: Implement this in a less stupid way.
        if self.light.state == "red":
            self.progress_close()
        else:
            self.progress_open()


        if self.state == Bridge.State.OPEN:
            if self.light.state == "green":
                self.roads[0].light.state = "green"
                self.roads[1].light.state = "red"
            else:
                self.roads[1].light.state = "green"
                self.roads[0].light.state = "red"
        else:
            self.roads[0].light.state = "red"
            self.roads[1].light.state = "red"


    def progress_open(self):
        if self.state != Bridge.State.OPEN:
            self.state = Bridge.State.OPENING
            self.open_percentage = min(self.open_percentage + 1, 100)

        if self.open_percentage >= 100:
            self.state = Bridge.State.OPEN


    def progress_close(self):
        if self.state != Bridge.State.CLOSED:
            self.state = Bridge.State.CLOSING
            self.open_percentage = max(self.open_percentage - 1, 0)

        if self.open_percentage <= 0:
            self.state = Bridge.State.CLOSED


    def can_vehicles_pass(self):
        return self.state == Bridge.State.CLOSED


    def render(self):
        tl = add(self.game.translation, self.area.min)
        br = add(self.game.translation, self.area.max)

        bridge_rect = pygame.Rect(
            tl,
            mul(sub(br, tl), (self.open_percentage / self.open_time, 1.0))
        )

        pygame.draw.rect(
            self.game.screen,
            (0, 41, 58), # Sea Blue
            bridge_rect
        )