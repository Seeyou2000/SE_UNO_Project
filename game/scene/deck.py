class Deck:
    def __init__(self, cards):
        self.cards = cards

    def drow(self):
        return self.cards.pop()
