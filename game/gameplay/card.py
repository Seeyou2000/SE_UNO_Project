import pygame

from engine.button import Button
from engine.gameobjectcontainer import GameObjectContainer
from game.constant import UI_FONT_BOLD_PATH, AbilityType


class Card(GameObjectContainer):
    def __init__(
        self, color: str, number: int = None, ability: AbilityType = None
    ) -> None:  # 일반 숫자 카드
        super().__init__()
        self.color = color
        self.number = number
        self.ability = ability
        self.font = pygame.font.Font(UI_FONT_BOLD_PATH, 20)
        self.rect = pygame.Rect(0, 0, 30, 50)
        self.card_number = self.font.render(f"{number}", True, pygame.Color("black"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        pygame.draw.rect(surface, pygame.Color(self.color), self.rect)
        surface.blit(
            self.card_number, self.card_number.get_rect(center=self.rect.center)
        )
