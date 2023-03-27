class Deck:
    def __init__(self, cards: list) -> None:
        self.cards = cards

    def drow(self) -> None:
        return self.cards.pop()
