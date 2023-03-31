from game.scene.card import Card


class Deck:
    def __init__(self, cards: list) -> None:
        self.cards = cards

    def draw(self) -> Card:
        return self.cards.pop()

    def get_last(self) -> Card:
        return self.cards[-1]
