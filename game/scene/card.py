import pygame

from engine.button import Button
from engine.gameobjectcontainer import GameObjectContainer


class Card(GameObjectContainer):
    def __init__(self, color, number=0, ability=None):  # 일반 숫자 카드
        super().__init__()
        self.color = color
        self.number = number
        self.ability = ability
        self.font = pygame.font.SysFont("Arial", 20)
        self.rect = pygame.Rect(0, 0, 30, 50)
        self.card_number = self.font.render(f"{number}", True, pygame.Color("black"))
        self.card_button = Button(
            "",
            pygame.Rect(0, 0, 30, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.ability(),
        )
        self.add_child(self.card_button)

    def render(self, surface: pygame.Surface):
        super().render(surface)
        pygame.draw.rect(surface, pygame.Color(self.color), self.rect)
        surface.blit(
            self.card_number, self.card_number.get_rect(center=self.rect.center)
        )

    def abil_add2(self, nowplaying):
        print("work")

    def abil_skip(self, nowplaying):
        print("work")

    def abil_reverse(self, nowplaying):
        print("work")

    def abil_change(self):
        print("work")

    def abil_add4(self):
        print("work")
