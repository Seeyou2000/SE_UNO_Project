import pygame

from engine.sprite import Sprite


class TurnDirectionIndicator(Sprite):
    def __init__(self) -> None:
        self.original = pygame.image.load("resources/images/turn-indicator.png")
        self.flipped = pygame.transform.flip(self.original, True, False)
        super().__init__(self.original)

    def set_direction(self, is_clockwise: bool) -> None:
        if is_clockwise:
            self.image = self.original
        else:
            self.image = self.flipped
