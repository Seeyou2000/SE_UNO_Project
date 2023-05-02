from game.gameplay.card import Card


class Deck:
    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def draw(self) -> Card:
        return self.cards.pop()

    def get_last(self) -> Card:
        return self.cards[-1]

    def get_card_amount(self) -> int:
        return len(self.cards)
