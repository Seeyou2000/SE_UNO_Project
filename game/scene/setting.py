import pygame

from engine.button import Button
from engine.scene import Scene
from engine.world import World


class SettingScene(Scene):
    def __init__(self, world: World):
        super().__init__(world)

        self.font = pygame.font.SysFont("Arial", 20)

        from game.scene.menu import MenuScene

        self.add_children(
            [
                Button(
                    "Small",
                    pygame.Rect(0, 0, 100, 100),
                    self.font,
                    on_click=lambda event: self.world.set_size((800, 600)),
                ),
                Button(
                    "Medium",
                    pygame.Rect(150, 0, 100, 100),
                    self.font,
                    on_click=lambda event: self.world.set_size((1280, 720)),
                ),
                Button(
                    "Large",
                    pygame.Rect(300, 0, 100, 100),
                    self.font,
                    on_click=lambda event: self.world.set_size((1920, 1080)),
                ),
                Button(
                    "Back",
                    pygame.Rect(450, 0, 100, 100),
                    self.font,
                    on_click=lambda event: self.world.director.change_scene(
                        MenuScene(self.world)
                    ),
                ),
                Button(
                    "Reset",
                    pygame.Rect(600, 700, 100, 100),
                    self.font,
                    on_click=lambda event: self.world.reset(),
                ),
                Button(
                    "Colorblind mode[on/off]",
                    pygame.Rect(0, 200, 300, 100),
                    self.font,
                    on_click=lambda event: self.world.toggle_set_colorblind(
                        not self.world.is_colorblind
                    ),
                ),
                Button(
                    "Save settings",
                    pygame.Rect(550, 500, 150, 100),
                    self.font,
                    on_click=lambda event: self.world.save_settings(),
                ),
            ]
        )
        options = {"Draw the card": "D", "Play the card": "P"}
        # create the dictionary named "options", and defined the key 'D' and 'P'
        for i, (description, key) in enumerate(options.items()):
            y = (
                400 + i * 100
            )  # use for loop to iterate the value of i and the value of y will change when i increase.
            self.add_child(Button(key, pygame.Rect(0, y, 200, 60), self.font))
            self.add_child(Button(key, pygame.Rect(0, y, 200, 60), self.font))
            # create the two buttons for the corresponding description.            # create the two buttons for the corresponding description.
