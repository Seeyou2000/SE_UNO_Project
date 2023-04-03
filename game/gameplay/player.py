from game.gameplay.card import Card
from game.gameplay.deck import Deck


class Player:
    cards: list[Card]

    def __init__(self, name: str) -> None:
        self.name = name
        self.cards = []

    def draw_card(self, deck: Deck) -> None:
        self.cards.append(deck.draw())

    def play_card(self, index: int) -> Card:
        return self.cards.pop(index)
