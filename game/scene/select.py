import pygame

from engine.button import Button
from engine.scene import Scene
from engine.world import World
from game.scene.gameplay import Gameplay
from game.scene.ingame import InGameScene


class SelectScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        self.player_index = 0

        from game.scene.menu import MenuScene

        menu_button = Button(
            "Back to menu",
            pygame.Rect(600, 500, 200, 100),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.world.director.change_scene(MenuScene(self.world)),
        )
        one_player_button = Button(
            "1",
            pygame.Rect(100, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(1),
        )
        two_player_button = Button(
            "2",
            pygame.Rect(200, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(2),
        )
        three_player_button = Button(
            "3",
            pygame.Rect(300, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(3),
        )
        four_player_button = Button(
            "4",
            pygame.Rect(400, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(4),
        )
        five_player_button = Button(
            "5",
            pygame.Rect(500, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(5),
        )
        six_player_button = Button(
            "6",
            pygame.Rect(600, 150, 50, 50),
            pygame.font.SysFont("Arial", 20),
            lambda event: self.select_player_num(6),
        )

        self.add_children(
            [
                menu_button,
                one_player_button,
                two_player_button,
                three_player_button,
                four_player_button,
                five_player_button,
                six_player_button,
            ]
        )
        self.currentgame = Gameplay()
        self.currentgame.start(self.player_index)

    def update(self) -> None:
        super().update()

    def select_player_num(self, number: int) -> None:
        self.player_index = number
        self.world.director.change_scene(InGameScene(self.world, self.player_index))
