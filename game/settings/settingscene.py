import pygame

from engine.button import Button
from engine.layout import Layout, LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from engine.world import World
from game.settings.settings import POSSIBLE_SCREEN_SIZES

BUTTON_HEIGHT = 60


class SettingScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = pygame.font.SysFont("Arial", 20)
        self.layout = Layout(world.get_rect())
        self.on("resize", lambda _: self.layout.rect.update(self.world.get_rect()))

        self.place_screen_size_buttons()
        self.place_colorblind_button()
        self.place_sound_buttons()
        self.place_keyboard_options()
        self.place_bottom_buttons()

    def place_screen_size_buttons(self) -> None:
        screen_size_buttons = [
            Button(
                f"{width} * {height}",
                pygame.Rect(0, 0, 100, BUTTON_HEIGHT),
                self.font,
                lambda _, width=width, height=height: self.world.settings.set_values(
                    width, height
                ),
            )
            for width, height in POSSIBLE_SCREEN_SIZES
        ]

        for i, button in enumerate(screen_size_buttons):
            self.layout.add(
                button,
                LayoutAnchor.TOP_LEFT,
                pygame.Vector2(50 + i * (button.rect.width + 20), 50),
            )

        self.add_children(screen_size_buttons)

    def place_colorblind_button(self) -> None:
        colorblind_button = Button(
            "Colorblind mode [on/off]",
            pygame.Rect(0, 0, 200, BUTTON_HEIGHT),
            self.font,
            lambda _: self.world.settings.toggle_colorblind(),
        )

        self.layout.add(
            colorblind_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 150)
        )

        self.add_child(colorblind_button)

    def place_sound_buttons(self) -> None:
        pass

    def place_keyboard_options(self) -> None:
        for i, (description, key) in enumerate(self.world.settings.keymap.items()):
            y = 250 + i * (BUTTON_HEIGHT + 20)

            description_text = Text(
                snake_key_to_name(description),
                pygame.Vector2(0, 0),
                self.font,
                pygame.Color("black"),
            )
            self.layout.add(
                description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, y + 15)
            )
            self.add_child(description_text)

            change_key_button = Button(
                pygame.key.name(key).upper(),
                pygame.Rect(0, y, 200, BUTTON_HEIGHT),
                self.font,
            )
            self.layout.add(
                change_key_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(300, y)
            )
            self.add_child(change_key_button)

    def place_bottom_buttons(self) -> None:
        from game.menu.menuscene import MenuScene

        back_button = Button(
            "BACK",
            pygame.Rect(0, 0, 100, BUTTON_HEIGHT),
            self.font,
            on_click=lambda _: self.world.director.change_scene(MenuScene(self.world)),
        )
        self.layout.add(
            back_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-50, -50)
        )
        self.add_child(back_button)

        reset_button = Button(
            "RESET",
            pygame.Rect(0, 0, 100, BUTTON_HEIGHT),
            self.font,
            on_click=lambda _: self.world.settings.reset(),
        )
        self.layout.add(
            reset_button, LayoutAnchor.BOTTOM_RIGHT, pygame.Vector2(-170, -50)
        )
        self.add_child(reset_button)

    def update(self) -> None:
        super().update()
        self.layout.update()


def snake_key_to_name(str: str) -> None:
    return str.upper().replace("_", " ")
