import json
from typing import Any

import pygame

from engine.event import Event, EventEmitter

SETTINGS_FILE_PATH = "settings.json"
POSSIBLE_SCREEN_SIZES: list[tuple[int, int]] = [(800, 600), (1280, 720), (1920, 1080)]
KEYS = [
    "draw_card",
    "play_card",
]

KeyMap = dict[str, int]

DEFAULT_KEYMAP: KeyMap = {}
DEFAULT_KEYMAP[KEYS[0]] = pygame.K_s
DEFAULT_KEYMAP[KEYS[1]] = pygame.K_RETURN

DEFAULT_SETTINGS = {
    "width": 1280,
    "height": 720,
    "is_colorblind": False,
    "keymap": DEFAULT_KEYMAP,
}


class Settings(EventEmitter):
    _width: int
    _height: int
    _is_colorblind: bool
    _keymap: KeyMap

    def __init__(self) -> None:
        super().__init__()
        self.load_dict(DEFAULT_SETTINGS)
        pass

    def save(self) -> None:
        with open(SETTINGS_FILE_PATH, "w") as f:
            json.dump(
                {
                    "width": self.width,
                    "height": self.height,
                    "is_colorblind": self.is_colorblind,
                    "keymap": self.keymap,
                },
                f,
            )

    def load(self) -> None:
        try:
            with open(SETTINGS_FILE_PATH) as f:
                self.load_dict(json.load(f))
        except FileNotFoundError:
            self.reset()

    def load_dict(self, value: dict[str, Any]) -> None:
        try:
            self.set_values(
                width=value["width"],
                height=value["height"],
                is_colorblind=value["is_colorblind"],
                keymap=value["keymap"],
            )

        except AttributeError:
            if value is DEFAULT_SETTINGS:
                print("기본 설정값을 불러오는 데 문제가 있습니다. 키값을 점검하세요.")
            else:
                print("저장된 설정을 불러오는 데 문제가 있어 기본 설정값으로 대체합니다.")
                self.reset()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def is_colorblind(self) -> bool:
        return self._is_colorblind

    @property
    def keymap(self) -> KeyMap:
        return self._keymap

    # property helper
    @property
    def window_size(self) -> tuple[int, int]:
        return (self._width, self._height)

    def set_values(
        self,
        width: int | None = None,
        height: int | None = None,
        is_colorblind: bool | None = None,
        keymap: KeyMap | None = None,
    ) -> None:
        self._width = width if width is not None else self._width
        self._height = height if height is not None else self._height
        self._is_colorblind = (
            is_colorblind if is_colorblind is not None else self._is_colorblind
        )
        self._keymap = keymap if keymap is not None else self._keymap

        self.save()
        self.emit("change", Event(None))

    def toggle_colorblind(self) -> None:
        self.set_values(is_colorblind=not self.is_colorblind)

    def reset(self) -> None:
        self.load_dict(DEFAULT_SETTINGS)