import random

from engine.event import EventEmitter
from game.gameplay.turn import Turn
from game.scene.card import Card
from game.scene.constant import ABILITY, COLORS
from game.scene.deck import Deck
from game.scene.player import Player


class GameState(EventEmitter):
    """
    게임 진행과 관련된 데이터를 모두 담아놓는 클래스.
    함수는 데이터 조작과 관련된 것만 있어야 합니다.
    게임의 실제 로직 관련된 부분은 game.gameplay.state 모듈에 작성해 주세요.
    """

    players: list[Player]
    turn: Turn

    def __init__(self) -> None:
        super().__init__()
        self.game_deck = Deck(self.create_full_deck_cards())
        self.drawn_deck = Deck([])
        self.attack_cards = Card([])

    def create_full_deck_cards(self) -> list[Card]:
        cards = [Card(color, number) for number in (range(1, 10)) for color in COLORS]
        cards += [
            Card(color, None, ability) for ability in ABILITY[:3] for color in COLORS
        ]
        cards += [Card("black", None, ability) for ability in ABILITY[3:]]
        random.shuffle(cards)
        return cards

    def reset(self, players: list[Player]) -> None:
        self.players = players
        self.turn = Turn(len(players))

    def get_current_player(self) -> Player:
        return self.players[self.turn.current]
