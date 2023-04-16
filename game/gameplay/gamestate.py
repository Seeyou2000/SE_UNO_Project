import random
from enum import Enum

from engine.event import Event, EventEmitter
from game.constant import COLORS, ColorableAbilityType, NonColorableAbilityType
from game.gameplay.card import Card
from game.gameplay.deck import Deck
from game.gameplay.player import Player
from game.gameplay.timer import Timer
from game.gameplay.turn import Turn


class GameStateEventType(Enum):
    PLAYER_EARNED_CARD = "player_earned_card"
    TURN_DIRECTION_REVERSE = "turn_direction_reverse"
    TURN_NEXT = "next_turn"


class GameState(EventEmitter):
    """
    게임 진행과 관련된 데이터를 모두 담아놓는 클래스.
    함수는 데이터 조작과 관련된 것만 있어야 합니다.
    게임의 실제 로직 관련된 부분은 game.gameplay.state 모듈에 작성해 주세요.
    """

    game_deck: Deck
    players: list[Player]
    turn: Turn
    turn_timer: Timer

    _turn_to_add: int
    _cards_to_attack: int

    def __init__(self) -> None:
        super().__init__()
        self.now_color = "red"
        self.turn_timer = Timer(10)

    def create_full_deck_cards(self) -> list[Card]:
        cards = [Card(color, number) for number in (range(1, 10)) for color in COLORS]
        cards += [
            Card(color, None, ability)
            for ability in ColorableAbilityType
            for color in COLORS
        ]
        cards += [Card("black", None, ability) for ability in NonColorableAbilityType]
        random.shuffle(cards)
        return cards

    def reset(self, players: list[Player]) -> None:
        self.game_deck = Deck(self.create_full_deck_cards())
        self.discard_pile = Deck([])
        self.players = players
        self.turn = Turn(len(players))
        self._turn_to_add = 0
        self._cards_to_attack = 0
        self.turn_timer.reset()

    def get_current_player(self) -> Player:
        return self.players[self.turn.current]

    def draw_card(self, player: Player) -> None:
        drawn_card = self.game_deck.draw()
        player.cards.append(drawn_card)
        self.emit(
            GameStateEventType.PLAYER_EARNED_CARD,
            Event({"player": player, "card": drawn_card}),
        )

    def discard(self, card: Card) -> None:
        self.discard_pile.cards.append(card)
        self.now_color = card.color
        self.get_current_player().cards.remove(card)

    def attack_cards(self, n: int) -> None:
        self._cards_to_attack += n

    def is_attacked(self) -> bool:
        return self._cards_to_attack > 0

    def flush_attack_cards(self, player: Player) -> None:
        for _ in range(0, self._cards_to_attack):
            self.draw_card(player)
        self._cards_to_attack = 0

    def reserve_skip(self, n: int) -> None:
        self._turn_to_add += n

    def flush_skip(self) -> None:
        self.turn.skip(self._turn_to_add)
        self._turn_to_add = 0

    def go_next_turn(self) -> None:
        self.flush_skip()
        self.turn.next()
        self.emit(GameStateEventType.TURN_NEXT, Event(None))

    def reverse_turn_direction(self) -> None:
        self.turn.reverse()
        self.emit(GameStateEventType.TURN_DIRECTION_REVERSE, Event(None))

    def is_player_next_turn(self, player: Player) -> bool:
        is_clockwise = self.turn.is_clockwise
        target_turn_diff = -1 if is_clockwise else 1

        player_index = self.players.index(player)
        current_index = self.turn.current
        diff = current_index - player_index
        reverse_diff = (
            diff - len(self.players) if is_clockwise else diff + len(self.players)
        )
        return (diff == target_turn_diff) or (reverse_diff == target_turn_diff)
