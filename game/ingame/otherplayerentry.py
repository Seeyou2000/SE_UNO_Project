import pygame

from engine.event import Event
from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer
from engine.layout import (
    Layout,
    LayoutAnchor,
    update_horizontal_linear_overlapping_layout,
)
from engine.text import Text
from game.font import FontType, get_font
from game.gameplay.cardentitiy import CardEntity, create_card_sprite
from game.gameplay.flow.gameflowmachine import GameFlowMachine
from game.gameplay.gamestate import GameState
from game.gameplay.player import Player
from game.gameplay.timer import Timer
from game.ingame.timerindicator import TimerIndicator

CARD_SIZE_UNIT = 14
CARD_BACK_WIDTH = CARD_SIZE_UNIT * 3
CARD_BACK_HEIGHT = CARD_SIZE_UNIT * 5
CARD_BACK_BORDER_RADIUS = 5


class OtherPlayerEntry(GameObjectContainer):
    card_sprites: list[CardEntity]
    delay_timers: list[Timer]

    def __init__(
        self,
        size: pygame.Vector2,
        player: Player,
        anchor: pygame.Vector2,
        timer: Timer,
        flow: GameFlowMachine,
        deck_button: GameObject,
    ) -> None:
        super().__init__()

        self.earned_card_idx_in_this_frame = 0
        self.player = player
        self.rect = pygame.Rect(0, 0, size.x, size.y)
        self.anchor = anchor
        self.flow = flow
        self.layout = Layout(self.rect.copy())
        self.deck_button = deck_button

        name_font = get_font(FontType.UI_BOLD, 20)
        name_text = Text(
            player.name, pygame.Vector2(0, 0), name_font, pygame.Color("black")
        )
        self.add_child(name_text)

        self.next_text = Text(
            "NEXT", pygame.Vector2(100, 10), name_font, pygame.Color("#FF9549")
        )

        self.uno_text = Text(
            "UNO", pygame.Vector2(50, 10), name_font, pygame.Color("gray")
        )
        self.add_child(self.uno_text)

        self.timer_display = TimerIndicator(pygame.Rect(0, 0, 20, 20), timer)
        self.add_child(self.timer_display)

        if anchor.x < 0.5:
            name_text.rect.topleft = (10, 10)
            self.next_text.rect.topright = (size.x - 10, 10)
            self.timer_display.rect.topright = (size.x - 10, 10)
            self.uno_text.rect.topright = (self.next_text.rect.left - 20, 10)
        elif anchor.x > 0.5:
            name_text.rect.topright = (size.x - 10, 10)
            self.next_text.rect.topleft = (10, 10)
            self.timer_display.rect.topright = (10, 10)
            self.uno_text.rect.topright = (self.next_text.rect.right + 20, 10)
        else:
            name_text.rect.top = 10
            name_text.rect.centerx = (size / 2).x
            self.next_text.rect.topleft = (name_text.rect.right + 20, 10)
            self.timer_display.rect.topleft = (name_text.rect.right + 20, 10)
            self.uno_text.rect.topright = (name_text.rect.left - 20, 10)

        self.card_sprites = []
        self.delay_timers = []

        for _ in range(0, len(player.cards)):
            self.create_card_sprite()

    def render(self, surface: pygame.Surface) -> None:
        # pygame.draw.rect(surface, pygame.Color("gray"), self.absolute_rect)
        super().render(surface)

    def update(self, dt: float) -> None:
        super().update(dt)

        self.earned_card_idx_in_this_frame = 0

        for timer in self.delay_timers:
            timer.update(dt)
            if not timer.enabled:
                self.delay_timers.remove(timer)

        update_horizontal_linear_overlapping_layout(
            objects=self.card_sprites,
            layout=self.layout,
            dt=dt,
            max_width=self.rect.width,
            gap=20,
            offset_retriever=lambda obj, total_width: pygame.Vector2(
                -(self.rect.width - total_width) / 2
                if self.anchor.x < 0.5
                else (self.rect.width - total_width) / 2
                if self.anchor.x > 0.5
                else 0,
                0,
            ),
        )
        self.layout.update(dt)

    def create_or_remove_cards_if_needed(self) -> None:
        displaying_card_count = len(self.card_sprites) + len(self.delay_timers)
        player_card_count = len(self.player.cards)
        if displaying_card_count < player_card_count:
            for _ in range(0, player_card_count - displaying_card_count):
                self.earned_card_idx_in_this_frame += 1
                delay_timer = Timer(0.1 * self.earned_card_idx_in_this_frame)
                delay_timer.on("tick", lambda _: self.create_card_sprite())
                self.delay_timers.append(delay_timer)
        elif displaying_card_count > player_card_count:
            for _ in range(0, displaying_card_count - player_card_count):
                removed = self.card_sprites.pop()
                self.remove_child(removed)
                self.layout.remove(removed)

    def create_card_sprite(self) -> None:
        card_back_sprite = create_card_sprite("black", True, False)
        card_back_sprite.rect.y = 50
        self.add_child(card_back_sprite)
        self.card_sprites.append(card_back_sprite)
        self.layout.add(
            card_back_sprite,
            LayoutAnchor.BOTTOM_CENTER,
            pygame.Vector2(self.deck_button.absolute_rect.center)
            - pygame.Vector2(self.absolute_rect.center),
        )

    def show_or_hide_indicators(self, game_state: GameState) -> None:
        if self.has_child(self.next_text):
            self.remove_child(self.next_text)
        if self.has_child(self.timer_display):
            self.remove_child(self.timer_display)
        if game_state.is_player_next_turn(self.player):
            self.add_child(self.next_text)
        if game_state.get_current_player() is self.player:
            self.add_child(self.timer_display)

    def handle_uno_clicked(self, event: Event) -> None:
        self.uno_text.set_color(
            pygame.Color("blue")
            if self.player.is_unobutton_clicked
            else pygame.Color("red")
        )

    def handle_card_earned(self, event: Event) -> None:
        self.create_or_remove_cards_if_needed()

    def handle_card_played(self, event: Event) -> None:
        self.create_or_remove_cards_if_needed()

    def handle_turn_direction_reverse(self, event: Event) -> None:
        self.show_or_hide_indicators(event.target)

    def handle_next_turn(self, event: Event) -> None:
        self.show_or_hide_indicators(event.target)
