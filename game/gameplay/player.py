from engine.event import Event, EventEmitter
from game.gameplay.card import Card
from game.gameplay.deck import Deck


class Player(EventEmitter):
    cards: list[Card]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.cards = []

    def draw_card(self, deck: Deck) -> None:
        card = deck.draw()
        self.cards.append(card)
        self.emit("card_earned", Event({"card": card}))

    def play_card(self, index: int) -> Card:
        return self.cards.pop(index)
