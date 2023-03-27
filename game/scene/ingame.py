import pygame

from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from game.scene.gameplay import Gameplay


class InGameScene(Scene):
    def __init__(self, world: World, player_index):
        super().__init__(world)

        from game.scene.menu import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(600, 500, 200, 100),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.world.director.change_scene(MenuScene(self.world)),
        )
        deck_button = Button(
            "",
            pygame.Rect(300, 200, 30, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.currentgame.nowplayer().drow_card(
                self.currentgame.gamedeck
            ),
        )
        self.hand = pygame.Rect(0, 500, 600, 100)
        self.add_children([menu_button, deck_button])
        self.currentgame = Gameplay()
        self.currentgame.start(player_index)

    def update(self):
        super().update()

    def render(self, surface: pygame.Surface):
        super().render(surface)
        pygame.draw.rect(surface, (80, 188, 223, 0), self.hand)
        for i, card in enumerate(self.currentgame.nowplayer().cards):
            card.rect.center = (50 + 50 * i, 550)
            card.card_button.rect.center = (50 + 60 * i, 550)
            card.render(surface)
