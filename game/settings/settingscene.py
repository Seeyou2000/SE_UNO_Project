import pygame

from engine.button import Button
from engine.event import Event, EventHandler
from engine.layout import LayoutAnchor
from engine.scene import Scene
from engine.text import Text
from engine.world import World
from game.font import FontType, get_font
from game.settings.settings import POSSIBLE_SCREEN_SIZES

BUTTON_HEIGHT = 60


class SettingScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)

        self.font = get_font(FontType.UI_BOLD, 20)
        # 0: keymap key, 1: Button
        self.changing_key = (None, None)

        self.place_screen_size_buttons()
        self.place_colorblind_button()
        self.place_sound_buttons()
        self.place_keyboard_options()
        self.place_bottom_buttons()

        self.on("keydown", self.handle_key_down)

    def place_screen_size_buttons(self) -> None:
        screen_size_buttons = [
            Button(
                f"{width} * {height}",
                pygame.Rect(0, 0, 200, BUTTON_HEIGHT),
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
            pygame.Rect(0, 0, 300, BUTTON_HEIGHT),
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
        for i, (dict_key, keyboard_key) in enumerate(
            self.world.settings.keymap.items()
        ):
            y = 250 + i * (BUTTON_HEIGHT + 20)

            description_text = Text(
                snake_key_to_name(dict_key),
                pygame.Vector2(0, 0),
                self.font,
                pygame.Color("black"),
            )
            self.layout.add(
                description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, y + 15)
            )
            self.add_child(description_text)

            change_key_button = Button(
                self.get_display_keyname(dict_key),
                pygame.Rect(0, y, 240, BUTTON_HEIGHT),
                self.font,
                self.create_key_button_click_handler(dict_key),
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

    def create_key_button_click_handler(self, dict_key: str) -> EventHandler:
        def handle_click(event: Event) -> None:
            button: Button = event.target
            button.set_text("PRESS ANY KEY")
            self.changing_key = (dict_key, button)

        return handle_click

    def handle_key_down(self, event: Event) -> None:
        settings = self.world.settings
        changing_dict_key: str = self.changing_key[0]
        changing_button: Button = self.changing_key[1]
        pressed_key = event.data["key"]

        if pressed_key == pygame.K_ESCAPE:
            changing_button.set_text(self.get_display_keyname(changing_dict_key))
            return

        if changing_dict_key is not None:
            new_keymap = settings.keymap.copy()
            new_keymap[changing_dict_key] = pressed_key
            settings.set_values(keymap=new_keymap)
            self.changing_key = (None, None)

            changing_button.set_text(self.get_display_keyname(changing_dict_key))

    def get_display_keyname(self, dict_key: str) -> str:
        return pygame.key.name(self.world.settings.keymap[dict_key]).upper()


def snake_key_to_name(str: str) -> str:
    return str.upper().replace("_", " ")
