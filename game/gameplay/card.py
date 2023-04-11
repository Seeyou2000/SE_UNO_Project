import pygame

from engine.gameobjectcontainer import GameObjectContainer


class Card(GameObjectContainer):
    WIDTH = 60
    HEIGHT = 100

    def __init__(
        self, color: str, number: int = None, ability: AbilityType = None
    ) -> None:  # 일반 숫자 카드
        super().__init__()
        self.color = color
        self.number = number
        self.ability = ability
        self.rect = pygame.Rect(0, 0, Card.WIDTH, Card.HEIGHT)
        self.card_number = self.font.render(f"{number}", True, pygame.Color("black"))

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)
        pygame.draw.rect(surface, pygame.Color(self.color), self.absolute_rect)
        surface.blit(
            self.card_number,
            self.card_number.get_rect(center=self.absolute_rect.center),
        )

    def update(self, dt: float) -> None:
        super().update(dt)
