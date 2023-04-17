import pygame

from engine.gameobjectcontainer import GameObjectContainer
from engine.sprite import Sprite
from game.gameplay.cardentitiy import get_card_color
from game.gameplay.gamestate import GameState
from game.settings.settings import Settings


class NowColorIndicator(GameObjectContainer):
    def __init__(self, game_state: GameState, settings: Settings) -> None:
        super().__init__()

        self.game_state = game_state
        self.settings = settings

        self.rect = pygame.Rect(0, 0, 70, 70)
        background_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            background_surface, pygame.Color("#FFF6EF"), self.rect, border_radius=20
        )
        background = Sprite(background_surface)
        self.add_child(background)

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        pygame.draw.rect(
            surface,
            get_card_color(self.game_state.now_color, self.settings.is_colorblind),
            self.absolute_rect.inflate(-8, -8),
            border_radius=16,
        )
