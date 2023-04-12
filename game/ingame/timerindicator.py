import math

import pygame
from pygame import gfxdraw

from engine.gameobject import GameObject
from game.gameplay.timer import Timer


class TimerIndicator(GameObject):
    timer: Timer | None

    def __init__(self, rect: pygame.Rect) -> None:
        super().__init__()
        self.rect = rect

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        start_angle = 0
        stop_angle = 270
        angle_step = 1
        arc_radius = 16
        circle_radius = 2

        for i in range(start_angle, stop_angle, angle_step):
            rad = math.radians(i)
            x = self.absolute_rect.centerx + arc_radius * math.cos(rad)
            y = self.absolute_rect.centery + arc_radius * math.sin(rad)
            gfxdraw.aacircle(
                surface, int(x), int(y), circle_radius, pygame.Color("#FF9549")
            )

    def update(self, dt: float) -> None:
        super().update(dt)

    def set_timer(self, timer: Timer) -> None:
        self.timer = timer
