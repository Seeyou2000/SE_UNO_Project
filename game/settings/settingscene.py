import pygame

from engine.button import Button
from engine.event import Event, EventHandler
from engine.focus import FocusMoveDirection
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
        self.connect_focus_siblings()

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
            self.focus_controller.add(button)

        self.add_children(screen_size_buttons)
        self.screen_size_buttons = screen_size_buttons

    def place_colorblind_button(self) -> None:
        def handle_colorblind_change(event: Event) -> None:
            self.world.settings.toggle_colorblind()
            button: Button = event.target
            button.set_text(
                f"Colorblind Mode: {'ON' if self.world.settings.is_colorblind else 'OFF'}"  # noqa: E501
            )

        colorblind_button = Button(
            f"Colorblind Mode: {'ON' if self.world.settings.is_colorblind else 'OFF'}",
            pygame.Rect(0, 0, 300, BUTTON_HEIGHT),
            self.font,
            handle_colorblind_change,
        )

        self.layout.add(
            colorblind_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 150)
        )
        self.focus_controller.add(colorblind_button)

        self.add_child(colorblind_button)

    def place_sound_buttons(self) -> None:
        button_width = 80
        button_rect = pygame.Rect(
            0,
            0,
            button_width,
            BUTTON_HEIGHT,
        )
        gap = 10

        description_text = Text(
            "Master Volume",
            pygame.Vector2(0, 0),
            self.font,
            pygame.Color("black"),
        )
        self.add_child(description_text)
        self.layout.add(
            description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 250 + 15)
        )
        for i, volume_value in enumerate(range(0, 100 + 1, 25)):
            master_volume_button = Button(
                f"{volume_value}%",
                button_rect.copy(),
                self.font,
                lambda _, volume_value=volume_value: self.world.settings.set_values(
                    effect_volume=volume_value, bgm_volume=volume_value
                ),
            )
            self.add_child(master_volume_button)
            self.layout.add(
                master_volume_button,
                LayoutAnchor.TOP_LEFT,
                pygame.Vector2((button_width + gap) * i + 250, 250),
            )
            self.focus_controller.add(master_volume_button)

        description_text = Text(
            "BGM Volume",
            pygame.Vector2(0, 0),
            self.font,
            pygame.Color("black"),
        )
        self.add_child(description_text)
        self.layout.add(
            description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 320 + 15)
        )
        for i, volume_value in enumerate(range(0, 100 + 1, 25)):
            bgm_volume_button = Button(
                f"{volume_value}%",
                button_rect.copy(),
                self.font,
                lambda _, volume_value=volume_value: self.world.settings.set_values(
                    bgm_volume=volume_value
                ),
            )
            self.add_child(bgm_volume_button)
            self.layout.add(
                bgm_volume_button,
                LayoutAnchor.TOP_LEFT,
                pygame.Vector2((button_width + gap) * i + 250, 320),
            )
            self.focus_controller.add(bgm_volume_button)

        description_text = Text(
            "Effect Volume",
            pygame.Vector2(0, 0),
            self.font,
            pygame.Color("black"),
        )
        self.add_child(description_text)
        self.layout.add(
            description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, 390 + 15)
        )
        for i, volume_value in enumerate(range(0, 100 + 1, 25)):
            effect_volume_button = Button(
                f"{volume_value}%",
                button_rect.copy(),
                self.font,
                lambda _, volume_value=volume_value: self.world.settings.set_values(
                    effect_volume=volume_value
                ),
            )
            self.add_child(effect_volume_button)
            self.layout.add(
                effect_volume_button,
                LayoutAnchor.TOP_LEFT,
                pygame.Vector2((button_width + gap) * i + 250, 390),
            )
            self.focus_controller.add(effect_volume_button)

    def place_keyboard_options(self) -> None:
        for i, (dict_key, keyboard_key) in enumerate(
            self.world.settings.keymap.items()
        ):
            y = 430 + i * (BUTTON_HEIGHT + 20)

            description_text = Text(
                snake_key_to_name(dict_key),
                pygame.Vector2(0, 0),
                self.font,
                pygame.Color("black"),
            )
            self.layout.add(
                description_text, LayoutAnchor.TOP_LEFT, pygame.Vector2(50, y + 85)
            )
            self.add_child(description_text)

            change_key_button = Button(
                self.get_display_keyname(dict_key),
                pygame.Rect(0, y, 240, BUTTON_HEIGHT),
                self.font,
                self.create_key_button_click_handler(dict_key),
            )
            self.layout.add(
                change_key_button, LayoutAnchor.TOP_LEFT, pygame.Vector2(250, y + 70)
            )
            self.focus_controller.add(change_key_button)
            self.last_key_button = change_key_button
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
        self.focus_controller.add(back_button)
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
        self.focus_controller.add(reset_button)
        self.add_child(reset_button)
        self.reset_button = reset_button

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

        if changing_dict_key is not None:
            if pressed_key == pygame.K_ESCAPE:
                changing_button.set_text(self.get_display_keyname(changing_dict_key))
                return
            new_keymap = settings.keymap.copy()
            new_keymap[changing_dict_key] = pressed_key
            settings.set_values(keymap=new_keymap)
            self.changing_key = (None, None)

            changing_button.set_text(self.get_display_keyname(changing_dict_key))

    def connect_focus_siblings(self) -> None:
        self.focus_controller.set_siblings(
            self.screen_size_buttons[1],
            {FocusMoveDirection.LEFT: self.screen_size_buttons[0]},
        )
        self.focus_controller.set_siblings(
            self.reset_button, {FocusMoveDirection.LEFT: self.last_key_button}
        )
        self.focus_controller.set_siblings(
            self.last_key_button, {FocusMoveDirection.RIGHT: self.reset_button}
        )

    def get_display_keyname(self, dict_key: str) -> str:
        return pygame.key.name(self.world.settings.keymap[dict_key]).upper()


def snake_key_to_name(str: str) -> str:
    return str.upper().replace("_", " ")
