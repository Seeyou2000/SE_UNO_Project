import pygame

from engine.event import Event
from engine.gameobjectcontainer import GameObjectContainer
from engine.text import Text
from game.font import FontType, get_font
from game.gameplay.card import Card, create_card_sprite
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player
from game.gameplay.timer import Timer
from game.ingame.timerindicator import TimerIndicator

CARD_SIZE_UNIT = 14
CARD_BACK_WIDTH = CARD_SIZE_UNIT * 3
CARD_BACK_HEIGHT = CARD_SIZE_UNIT * 5
CARD_BACK_BORDER_RADIUS = 5


class OtherPlayerEntry(GameObjectContainer):
    card_sprites: list[Card]

    def __init__(
        self, size: pygame.Vector2, player: Player, anchor: pygame.Vector2, timer: Timer
    ) -> None:
        super().__init__()

        self.player = player
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self.anchor = anchor

        name_font = get_font(FontType.UI_BOLD, 20)
        name_text = Text(
            player.name, pygame.Vector2(0, 0), name_font, pygame.Color("black")
        )
        self.add_child(name_text)

        self.next_text = Text(
            "NEXT", pygame.Vector2(100, 10), name_font, pygame.Color("#FF9549")
        )

        self.timer_display = TimerIndicator(pygame.Rect(0, 0, 20, 20), timer)
        self.add_child(self.timer_display)

        if anchor.x < 0.5:
            name_text.rect.topleft = (10, 10)
            self.next_text.rect.topright = (size.x - 10, 10)
            self.timer_display.rect.topright = (size.x - 10, 10)
        elif anchor.x > 0.5:
            name_text.rect.topright = (size.x - 10, 10)
            self.next_text.rect.topleft = (10, 10)
            self.timer_display.rect.topright = (10, 10)
        else:
            name_text.rect.top = 10
            name_text.rect.centerx = (size / 2).x
            self.next_text.rect.topleft = (name_text.rect.right + 20, 10)
            self.timer_display.rect.topleft = (name_text.rect.right + 20, 10)

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
        gap = 20
        delta = CARD_BACK_WIDTH - gap
        for i, card in enumerate(self.card_sprites):
            if self.anchor.x < 0.5:
                card.rect.left = i * delta
            elif self.anchor.x > 0.5:
                card.rect.right = self.rect.width - i * delta
            else:
                card.rect.left = (
                    i * delta
                    + ((self.rect.width - len(self.card_sprites) * delta) / 2.0)
                    - gap
                )

    def create_card_sprite(self) -> None:
        card_back_sprite = create_card_sprite("black", True, False)
        card_back_sprite.rect.y = 50
        self.add_child(card_back_sprite)
        self.card_sprites.append(card_back_sprite)

    def show_or_hide_indicators(self, game_state: GameState) -> None:
        if self.has_child(self.next_text):
            self.remove_child(self.next_text)
        if self.has_child(self.timer_display):
            self.remove_child(self.timer_display)
        if game_state.is_player_next_turn(self.player):
            self.add_child(self.next_text)
        if game_state.get_current_player() is self.player:
            self.add_child(self.timer_display)

    def handle_card_earned(self, event: Event) -> None:
        self.create_or_remove_cards_if_needed()

    def handle_turn_direction_reverse(self, event: Event) -> None:
        self.show_or_hide_indicators(event.target)

    def handle_next_turn(self, event: Event) -> None:
        self.show_or_hide_indicators(event.target)
