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
        self.test_crossing_list_validity()

        self.tick_rate = 20

        self.last_mouse_pos = None
        self.translation = [0, 0]
        self.screen_size = (1920, 1080)

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode(self.screen_size, display = 0)

        bg_img = 'background.png' if not debug else 'debug_background.png'
        self.bg = pygame.image.load(os.path.join('assets', bg_img))

        self.vehicles = []

        self.roads = Layout.loads_roads(self)
        self.test_light_usage()
        self.test_sensor_presence()

        self.spawnpoints = Layout.load_spawnpoints(self)
        self.test_reachability()

        self.bridge = Bridge(self, Box((2522, 276), (2700, 1167)), [ self.roads[38], self.roads[39] ], self.state[39])

        pygame.display.set_caption("Glorious TrafficSim 3000XL Sponsored by Bad Dragon")


        sound = pygame.mixer.Sound(os.path.join('assets', 'sus.mp3'))
        sound.play(loops = 0)


    def test_crossing_list_validity(self):
        illegal_crossings = []

        for id, light in self.state.items():
            for crossing_id in light.crossing:
                crossing = self.state[crossing_id]
                if id not in crossing.crossing: illegal_crossings.append((id, crossing_id))


        error_string = f'Illegal configuration:\n'
        for a, b in illegal_crossings: error_string += f'Light {a} crosses light {b} but not vice versa.\n'

        assert len(illegal_crossings) == 0, error_string


    def test_light_usage(self):
        bridge_control_light = 39

        unused_lights = set()
        for id in self.state: unused_lights.add(id)
        unused_lights.remove(bridge_control_light)

        for road in self.roads.values():
            if road.light is not None and road.light.id in unused_lights:
                unused_lights.remove(road.light.id)


        error_string = 'Illegal configuration:\n'
        for id in unused_lights: error_string += f'Light {id} has no associated road(s).\n'

        assert len(unused_lights) == 0, error_string


    def test_reachability(self):
        unreachable_roads = set()
        for id in self.roads: unreachable_roads.add(id)

        roads = set([spawn.road for spawn in self.spawnpoints])

        while len(roads) > 0:
            removed = []

            for road in roads:
                unreachable_roads.remove(road.id)
                removed.append(road)

            for road in removed:
                roads.remove(road)

                for conn in road.connections:
                    if conn.id in unreachable_roads: roads.add(conn)


        error_string = 'Illegal configuration:\n'
        for id in unreachable_roads: error_string += f'Road {id} cannot be reached from any spawnpoint.\n'

        assert len(unreachable_roads) == 0, error_string


    def test_sensor_presence(self):
        bridge_control_light = 39


        uncontrolled_lights = set()
        for id, light in self.state.items():
            if light.sync: uncontrolled_lights.add(id)

        uncontrolled_lights.remove(bridge_control_light)


        for road in self.roads.values():
            if road.light is not None and len([s for s in road.sensors if s.type == Sensor.SensorType.VEHICLES_WAITING]) > 0:
                if road.light.id in uncontrolled_lights: uncontrolled_lights.remove(road.light.id)


        error_string = 'Illegal configuration:\n'
        for id in uncontrolled_lights: error_string += f'Light {id} does not have a VehiclesWaiting sensor.\n'

        assert len(uncontrolled_lights) == 0, error_string


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
        for l in self.state.values(): l.tick()
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
