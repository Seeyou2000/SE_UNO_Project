from game.gameplay.card import Card


class Player:
    cards: list[Card]

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.cards = []
