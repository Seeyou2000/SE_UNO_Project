from game.scene.card import Card


class Player:
    cards: list[Card]

    def __init__(self, name):
        self.name = name
        self.cards = []

    def drow_card(self, deck):
        self.cards.append(deck.drow())

    def play_card(self, index):
        return self.cards.pop(index)
