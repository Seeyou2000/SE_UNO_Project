import random

from game.scene.card import Card
from game.scene.constant import ABILITY, COLORS, NAME
from game.scene.deck import Deck
from game.scene.player import Player


class Gameplay:
    def __init__(self):
        self.cards = [
            Card(color, number) for number in (range(1, 10)) for color in COLORS
        ]
        self.cards += [
            Card(color, 0, ability) for ability in ABILITY[:3] for color in COLORS
        ]
        self.cards += [Card("black", 0, ability) for ability in ABILITY[3:]]
        random.shuffle(self.cards)
        self.gamedeck = Deck(self.cards)

    def start(self, index):
        self.players = [Player(name) for name in NAME[:index]]
        for player in self.players:
            for j in range(0, 7):
                player.drow_card(self.gamedeck)
        self.nowplaying = 0

    def nowplayer(self):
        return self.players[self.nowplaying]
