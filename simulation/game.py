import pygame
import pygame.mouse as mouse
import os

from traffic_light import TrafficLight


def load_intersection_layout():
    return {
        # TODO: Real traffic lights
        1: TrafficLight([2, 3], 10, "green", (0, 0)),
        2: TrafficLight([1, 3], 10, "red", (0, 0)),
        3: TrafficLight([1, 2], 10, "red", (0, 0)),
        4: TrafficLight([5], 3, "green", (0, 0)),
        5: TrafficLight([4], 4, "green", (0, 0)),
    }


def clamp(x, min_value, max_value):
    if x < min_value: x = min_value
    if x > max_value: x = max_value
    return x


class Game:
    def __init__(self):
        self.state = load_intersection_layout()
        self.tick_rate = 20

        self.last_mouse_pos = None
        self.translation = [0, 0]
        self.screen_size = (1920, 1080)

        self.clock = pygame.time.Clock()
        self.dt = 0
        self.screen = pygame.display.set_mode(self.screen_size)
        self.bg = pygame.image.load(os.path.join('assets', 'background.png'))
        pygame.display.set_caption("Glorious TrafficSim 3000XL Sponsored by Bad Dragon")


    def listen_input(self):
        mouse_pos = mouse.get_pos()

        if self.last_mouse_pos is None:
            self.last_mouse_pos = mouse_pos
            return

        if not pygame.mouse.get_pressed()[0]:
            self.last_mouse_pos = mouse_pos
            return

        sens = 1
        self.translation = [
            self.translation[0] + (sens * (mouse_pos[0] - self.last_mouse_pos[0])),
            self.translation[1] + (sens * (mouse_pos[1] - self.last_mouse_pos[1]))
        ]

        self.translation[0] = clamp(self.translation[0], -self.bg.get_size()[0] + self.screen_size[0], 0)
        self.translation[1] = clamp(self.translation[1], -self.bg.get_size()[1] + self.screen_size[1], 0)

        self.last_mouse_pos = mouse_pos


    def loop(self):
        for events in pygame.event.get(): pass
        self.listen_input()

        # set map
        self.screen.blit(self.bg, self.translation)

        pygame.display.update()
        self.dt = self.clock.tick(self.tick_rate)
