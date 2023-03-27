from game.scene.card import Card
from game.scene.deck import Deck


class Player:
    cards: list[Card]

    def __init__(self, name: str) -> None:
        self.name = name
        self.cards = []

    def drow_card(self, deck: Deck) -> None:
        self.cards.append(deck.drow())

    def play_card(self, index: int) -> None:
        return self.cards.pop(index)
