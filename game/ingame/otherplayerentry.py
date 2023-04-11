import pygame

from engine.event import Event
from engine.gameobjectcontainer import GameObjectContainer
from engine.text import Text
from game.font import FontType, get_font
from game.gameplay.card import Card, create_card_sprite
from game.gameplay.player import Player

CARD_SIZE_UNIT = 14
CARD_BACK_WIDTH = CARD_SIZE_UNIT * 3
CARD_BACK_HEIGHT = CARD_SIZE_UNIT * 5
CARD_BACK_BORDER_RADIUS = 5


class OtherPlayerEntry(GameObjectContainer):
    card_sprites: list[Card]

    def __init__(self, size: pygame.Vector2, player: Player) -> None:
        super().__init__()

        self.player = player
        self.player.on("card_earned", self.handle_card_earned)
        self.rect = pygame.Rect(0, 0, size.x, size.y)

        name_font = get_font(FontType.UI_BOLD, 20)

        self.add_child(
            Text(player.name, pygame.Vector2(10, 10), name_font, pygame.Color("black"))
        )

        self.card_sprites = []

        for _ in range(0, len(player.cards)):
            self.create_card_sprite()

    def update(self, dt: float) -> None:
        super().update(dt)
        self.update_cards_position()

    def create_or_remove_cards_if_needed(self) -> None:
        displaying_card_count = len(self.card_sprites)
        player_card_count = len(self.player.cards)
        if displaying_card_count < player_card_count:
            for _ in range(0, player_card_count - displaying_card_count):
                self.create_card_sprite()
        elif displaying_card_count > player_card_count:
            for _ in range(0, displaying_card_count - player_card_count):
                removed = self.card_sprites.pop()
                self.remove_child(removed)

    def update_cards_position(self) -> None:
        for i, card in enumerate(self.card_sprites):
            card.rect.x = i * (CARD_BACK_WIDTH - 10)

    def create_card_sprite(self) -> None:
        card_back_sprite = create_card_sprite("black", True)
        card_back_sprite.rect.y = 50
        self.add_child(card_back_sprite)
        self.card_sprites.append(card_back_sprite)

    def handle_card_earned(self, event: Event) -> None:
        self.create_or_remove_cards_if_needed()
